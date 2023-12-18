import os


def check(model_filename: str) -> bool:
    """
    Checking & downloading our gpt4all models
    Returns True if it's already downloaded
    Returns False if it's not downloaded
    :param model_filename:
    :return:
    """
    return os.path.exists("models\\" + model_filename)
