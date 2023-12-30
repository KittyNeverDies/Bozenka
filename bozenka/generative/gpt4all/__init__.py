import os


def check(model_filename: str) -> bool:
    """
    Checking & downloading our gpt4all models
    Returns True if it's already downloaded
    Returns False if it's not downloaded
    :param model_filename: File name of gpt4all model
    :return:
    """
    return os.path.exists("models\\" + model_filename)


def get_model_path(model_filename: str) -> str:
    """
    Just returning path of our gpt4all models.
    :param model_filename: File name of gpt4all model
    :return:
    """
    return os.curdir + "models\\" + model_filename
