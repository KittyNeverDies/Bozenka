import base64
import json
import os
import time

import pathlib

import requests


class Kadinsky:
    """
    Kadinsky class from their documentation.
    """
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        """
        Generates image by kadinsky api
        :param prompt:
        :param model:
        :param images:
        :param width:
        :param height:
        :return:
        """
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        """
        Checks status of image generation by kadinsky
        :param request_id:
        :param attempts:
        :param delay:
        """
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                print("Fine!")
                return data['images']

            attempts -= 1
            time.sleep(delay)

    @staticmethod
    def save_image(data_of_image, file_name):
        """
        Saves image and returns its path
        :param data_of_image:
        :param file_name:
        """
        path = str(pathlib.Path().absolute()) + "\\image\\" + file_name + ".jpg"
        with open(path, "wb") as file:
            file.write(base64.b64decode(data_of_image))
            file.close()
        return path


kadinsky_gen = Kadinsky('https://api-key.fusionbrain.ai/', os.getenv("kadinsky_api"), os.getenv("kadinsky_secret"))
