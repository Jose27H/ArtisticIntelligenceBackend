import requests
import base64
from io import BytesIO
def generateRequest(api_key, prompt, negative_prompt, output_address, output_format, aspect_ratio, seed):
    data = {}
    data['prompt'] = prompt
    data['output_format'] = output_format
    data['aspect_ratio'] = aspect_ratio
    data['seed'] = seed
    if negative_prompt:
        data['negative_prompt'] = negative_prompt
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/ultra",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={"none": ''},
        data=data,
    )

    if response.status_code == 200:
        with open(f"{output_address}.{output_format}", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))

def sketchRequest(api_key, prompt, negative_prompt, output_address, output_format, b64String, control_strength, seed):
    data = {}
    data['prompt'] = prompt
    data['output_format'] = output_format
    data['control_strength'] = control_strength
    data['seed'] = seed
    if negative_prompt:
        data['negative_prompt'] = negative_prompt
    b64Image = b64String
    imageBinary = base64.b64decode(b64Image)
    image = BytesIO(imageBinary)
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/control/sketch",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={
            "image": ("sketch.png", image, "image/png")
        },
        data=data,
    )
    if response.status_code == 200:
        with open(f"{output_address}.{output_format}", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))


# from test import image_to_base64
# b64String = image_to_base64("./sketch.png")
# sketchRequest("sk-7pxhh6aU3wEzQW9VCTqbiDASmMMXgQhUmw7PbedAimUyOjVl", "a creepy wooden cathedral in the forest", None, "output/sketch", "png", b64String, 0.7, 0)