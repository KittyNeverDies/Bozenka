import os
import pathlib


model_path = os.getcwd() + "\\model\\"

def check(model_filename: str) -> bool:
    """
    Checking & downloading our gpt4all models
    Returns True if it's already downloaded
    Returns False if it's not downloaded
    :param model_filename: File name of gpt4all model
    :return: Does it exist
    """
    print(os.path.exists("models\\" + model_filename))
    return os.path.exists("models\\" + model_filename)
