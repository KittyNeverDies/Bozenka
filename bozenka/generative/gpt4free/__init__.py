import g4f
from g4f.Provider import RetryProvider
from varname import nameof


def generate_gpt4free_providers():
    """
    Generates list of g4f providers
    :return:
    """
    provider = {}
    for prov in g4f.Provider.__all__:
        if prov != "BaseProvider" and prov != "AsyncProvider" and prov != "RetryProvider":
            exec(f"provider['{prov}']=g4f.Provider.{prov}")
    result = {}
    for check in provider:
        if provider[check].working:
            result[check] = provider[check]
    return result


def generate_gpt4free_models():
    """
    Generates list of g4f models
    :return:
    """
    models = {}
    for model, model_name in g4f.models.ModelUtils.convert.items(), g4f.models.ModelUtils.convert.keys():
        if type(model.best_provider) is RetryProvider:
            for pr in model.best_provider.providers:
                if pr in models:
                    models[nameof(pr)].append(model_name)
                else:
                    models[nameof(pr)] = [model_name]
        else:
            if nameof(model.best_provider) in models:
                models[nameof(model.best_provider)].append(model_name)
            else:
                models[nameof(model.best_provider)] = [model_name]
    return models
