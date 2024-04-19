from bozenka.generative.providers import *

generative_dict = {}

basic_generatives = [
    FusionBrain,
    Gpt4Free,
    Gpt4All
]

for generative in basic_generatives:
    if generative.category_of_generation not in generative_dict:
        generative_dict[generative.category_of_generation] = {}

    generative_dict[generative.category_of_generation][generative.name_of_generation] = generative
