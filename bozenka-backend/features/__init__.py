import os
import importlib.util

from api.models import Category, Feature


def get_list_of_features() -> dict[str: list]:
    """
    Generates list of features
    available right now in the function's own directory
    :return: List of features
    """
    list_of_features = {}

    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get list of directories in the current directory
    directories = [
        smth
        for smth in os.listdir(current_dir) # Use current_dir here
        if os.path.isdir(os.path.join(current_dir, smth)) # Use current_dir here to form full path
    ]

    # Import classes from each directory
    for directory in directories:
        print(directory)
        # Get list of modules in the directory
        modules = [m for m in os.listdir(os.path.join(current_dir, directory)) if m.endswith('.py')] # Use current_dir here to form full path

        for module in modules:
            # Import the module
            module_path = os.path.join(current_dir, directory, module) # Use current_dir here to form full path
            spec = importlib.util.spec_from_file_location(module[:-3], module_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            # Get list of classes in the module
            classes = [getattr(mod, name) for name in dir(mod) if isinstance(getattr(mod, name), type)]

            for cls in classes:
                # Don't add Basic Feature to list of features
                if cls.__name__ == 'BasicFeature':
                    continue

                # Creating list of features
                if not list_of_features.get(directory):
                    list_of_features[directory] = [cls]
                else:
                    list_of_features[directory].append(cls)
    return list_of_features

def register_features(naming_utils: dict) -> None:
    """
    Registers features from all directories in the features package
    for django
    :return: Nothing
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))

    categories = [
        d for d in os.listdir(current_dir)
        if os.path.isdir(os.path.join(current_dir, d))
        and not d.startswith('__')
    ]

    for category_name in categories:
        category, _ = Category.objects.get_or_create(
            name=category_name,
            defaults={
                'description': naming_utils[category_name]['description']
                if category_name in naming_utils and naming_utils[category_name]['description']
                    else f'Features related to {category_name}',
                'icon': naming_utils[category_name]['icon'] if category_name in naming_utils and naming_utils[category_name]['icon'] else 'error'
            }
        )

        category_path = os.path.join(current_dir, category_name)
        for file in os.listdir(category_path):
            if file.endswith('.py') and not file.startswith('__'):
                module_path = os.path.join(category_path, file)
                module_name = f'features.{category_name}.{file[:-3]}'

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and
                        hasattr(attr, '__base__') and
                        attr.__base__.__name__ == 'BasicFeature'):

                        Feature.objects.update_or_create(
                            name=attr.__name__,
                            category=category,
                            defaults={
                                'description': attr.__doc__ or '',
                                'feature_class': f'{module_name}.{attr.__name__}',

                            }
                        )

