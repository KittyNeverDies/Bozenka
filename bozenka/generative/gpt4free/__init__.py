import g4f
import g4f.Provider
from g4f.Provider import RetryProvider
from varname import nameof


def generate_gpt4free_providers():
    """
    Generates list of g4f providers
    :return:
    """
    return {prov: g4f.Provider.ProviderUtils.convert[prov] for prov in g4f.Provider.__all__
            if prov != "BaseProvider" and prov != "AsyncProvider" and prov != "RetryProvider" and
            g4f.Provider.ProviderUtils.convert[prov].working}


def generate_gpt4free_models():
    """
    Generates list of g4f models
    :return:
    """
    models = {}
    for model_name, model in g4f.models.ModelUtils.convert.items():
        if type(model.best_provider) is RetryProvider:
            for pr in model.best_provider.providers:
                if pr.__name__ in models:
                    models[pr.__name__].append(model_name)
                else:
                    models[pr.__name__] = [model_name]
        else:
            if model.best_provider.__name__ in models:
                models[model.best_provider.__name__].append(model_name)
            else:
                models[model.best_provider.__name__] = [model_name]
    print(models)
    return models
