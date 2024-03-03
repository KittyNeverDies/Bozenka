from dataclasses import dataclass


@dataclass
class QueueMember:
    """
    Queue Member for waiting to get generated
    content by AI
    """
    content_type: str   # Example "text2text"
    data: dict          # Example


# List of text generative categories, what we support
text2text_generative_libraries = [
    "Gpt4Free",
    "Gpt4All",
]

# List of image generative categories, what we support
image_generative_categories = [
    "Kadinsky",
    "StableDiffusion XL"
]

image_generative_size = [
    "1024x1024",
    "1024x576",
    "576x1024",
    "1024x680",
    "680x1024"
]
