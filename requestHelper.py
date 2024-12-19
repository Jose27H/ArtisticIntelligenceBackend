import os
import time
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
        return base64.b64encode(response.content).decode('utf-8')
    elif response.status_code == 403:
        return "Content moderation triggered"
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

def styleRequest(api_key, prompt, negative_prompt, output_address, output_format, b64String, fidelity, seed):
    data = {}
    data['prompt'] = prompt
    data['output_format'] = output_format
    data['fidelity'] = fidelity
    data['seed'] = seed
    if negative_prompt:
        data['negative_prompt'] = negative_prompt
    b64Image = b64String
    imageBinary = base64.b64decode(b64Image)
    image = BytesIO(imageBinary)
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/control/style",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={
            "image": ("style.png", image, "image/png")
        },
        data=data,
    )
    if response.status_code == 200:
        with open(f"{output_address}.{output_format}", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))

def outpaintRequest(api_key, prompt, left, right, up, down, b64String, output_address, output_format, creativity, seed):
    data = {}
    data['prompt'] = prompt
    data['output_format'] = output_format
    data['creativity'] = creativity
    data['seed'] = seed
    data['left'] = left
    data['right'] = right
    data['up'] = up
    data['down'] = down
    b64Image = b64String
    imageBinary = base64.b64decode(b64Image)
    image = BytesIO(imageBinary)
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/edit/outpaint",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={
            "image": ("outpaint.png", image, "image/png")
        },
        data=data,
    )
    if response.status_code == 200:
        with open(f"{output_address}.{output_format}", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))

def searchAndReplaceRequest(api_key, searchPrompt, replacePrompt, negativePrompt, output_address, output_format, b64String, seed):
    data = {}
    data['search_prompt'] = searchPrompt
    data['prompt'] = replacePrompt
    data['output_format'] = output_format
    data['seed'] = seed
    if negativePrompt:
        data['negative_prompt'] = negativePrompt
    b64Image = b64String
    imageBinary = base64.b64decode(b64Image)
    image = BytesIO(imageBinary)
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/edit/search-and-replace",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={
            "image": ("searchAndReplace.png", image, "image/png")
        },
        data=data,
    )
    if response.status_code == 200:
        with open(f"{output_address}.{output_format}", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))

def removeBackgroundRequest(api_key, output_address, output_format, b64String):
    imageBinary = base64.b64decode(b64String)
    image = BytesIO(imageBinary)
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/edit/remove-background",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={
            "image": ("removeBackground.png", image, "image/png")
        },
        data={
            "output_format": output_format
        },
    )
    if response.status_code == 200:
        with open(f"{output_address}.{output_format}", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))

def removeBackgroundAndRelightRequest(
    api_key,
    background_prompt,
    preserve_original_subject,
    original_background_depth,
    keep_original_background,
    light_source_strength,
    light_source_direction,
    output_address,
    output_format,
    b64String,
    foreground_prompt=None,
    negative_prompt=None,
    seed=None
):
    # Decode the base64-encoded image
    image_binary = base64.b64decode(b64String)
    image = BytesIO(image_binary)

    # Prepare data payload
    data = {
        "background_prompt": background_prompt,
        "preserve_original_subject": preserve_original_subject,
        "original_background_depth": original_background_depth,
        "keep_original_background": keep_original_background,
        "light_source_strength": light_source_strength,
        "light_source_direction": light_source_direction,
        "output_format": output_format,
    }

    if foreground_prompt:
        data["foreground_prompt"] = foreground_prompt
    if negative_prompt:
        data["negative_prompt"] = negative_prompt
    if seed:
        data["seed"] = seed

    # Set up headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",  # Ensure we expect a JSON response for the initial request
    }

    # Attach the image file
    files = {
        "subject_image": ("subject_image.png", image, "image/png"),
    }

    # Send the initial POST request
    print("Sending initial request to Stability AI...")
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/edit/replace-background-and-relight",
        headers=headers,
        data=data,
        files=files,
    )

    if not response.ok:
        print("Error in initial request:")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    # Parse response
    response_dict = response.json()
    generation_id = response_dict.get("id")
    if not generation_id:
        raise Exception("No generation ID found in response.")

    # Poll for the result
    timeout = 500
    start = time.time()
    status_code = 202
    while status_code == 202:
        poll_response = requests.get(
            f"https://api.stability.ai/v2beta/results/{generation_id}",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "*/*",
            },
        )
        status_code = poll_response.status_code
        if not poll_response.ok and status_code != 202:
            print("Error in polling response:")
            print("Status Code:", poll_response.status_code)
            print("Response:", poll_response.text)
            raise Exception(f"HTTP {poll_response.status_code}: {poll_response.text}")

        if status_code == 200:
            break
        time.sleep(10)
        if time.time() - start > timeout:
            raise Exception(f"Timeout after {timeout} seconds")

    # Save the resulting image
    with open(f"{output_address}.{output_format}", "wb") as file:
        file.write(poll_response.content)