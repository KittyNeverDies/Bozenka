from bozenka.generative.gpt4all import Gpt4All
from bozenka.generative.kadinsky import KadinskyApiGenetartion
from bozenka.generative.gpt4free import Gpt4Free

basic_generatives = [
    KadinskyApiGenetartion,
    Gpt4Free,
    Gpt4All
]

# The dictionary to be created, categorized by `category_of_generation`
generative_dict = {}

for generative in basic_generatives:
    # Check if the category already exists in the dictionary
    if generative.category_of_generation not in generative_dict:
        # If not, create a new empty dictionary for this category
        generative_dict[generative.category_of_generation] = {}

    # Add the BasicGenerative instance under its `name_of_generation`
    generative_dict[generative.category_of_generation][generative.name_of_generation] = generative
