import time
import requests
import base64
from io import BytesIO


# Function to generate an image based on a text prompt
def generateRequest(api_key, prompt, negative_prompt, output_format, aspect_ratio, seed):
    """
    Sends a request to the Stability AI API to generate an image based on the provided parameters.

    Args:
        api_key (str): API key for authorization.
        prompt (str): Text prompt for generating the image.
        negative_prompt (str): Optional negative prompt to exclude certain features.
        output_format (str): Desired output format (e.g., 'png').
        aspect_ratio (str): Aspect ratio for the generated image.
        seed (int): Seed for deterministic output.

    Returns:
        str: Base64-encoded string of the generated image or error message.
    """
    data = {
        'prompt': prompt,
        'output_format': output_format,
        'aspect_ratio': aspect_ratio,
        'seed': seed
    }
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
        # Return Base64-encoded image content if successful
        return base64.b64encode(response.content).decode('utf-8')
    elif response.status_code == 403:
        # Handle content moderation errors
        return "Content moderation triggered"
    else:
        # Raise an exception for other errors
        raise Exception(str(response.json()))


# Function to apply a sketch control to an image
def sketchRequest(api_key, prompt, negative_prompt, output_format, b64String, control_strength, seed):
    """
    Applies a sketch control to an image based on the provided parameters.

    Args:
        api_key (str): API key for authorization.
        prompt (str): Text prompt for the sketch transformation.
        negative_prompt (str): Optional negative prompt.
        output_format (str): Desired output format (e.g., 'png').
        b64String (str): Base64-encoded original image.
        control_strength (float): Strength of the sketch control.
        seed (int): Seed for deterministic output.

    Returns:
        str: Base64-encoded string of the modified image or error message.
    """
    data = {
        'prompt': prompt,
        'output_format': output_format,
        'control_strength': control_strength,
        'seed': seed
    }
    if negative_prompt:
        data['negative_prompt'] = negative_prompt

    # Decode the Base64 image and send it as part of the request
    imageBinary = base64.b64decode(b64String)
    image = BytesIO(imageBinary)
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/control/sketch",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={"image": ("sketch.png", image, "image/png")},
        data=data,
    )

    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    elif response.status_code == 403:
        return "Content moderation triggered"
    else:
        raise Exception(str(response.json()))


# Function to style an image based on a prompt
def styleRequest(api_key, prompt, negative_prompt, output_format, b64String, fidelity, seed):
    """
    Applies a style transformation to an image based on the provided parameters.

    Args:
        api_key (str): API key for authorization.
        prompt (str): Text prompt for the style transformation.
        negative_prompt (str): Optional negative prompt.
        output_format (str): Desired output format (e.g., 'png').
        b64String (str): Base64-encoded original image.
        fidelity (float): Fidelity level for the transformation.
        seed (int): Seed for deterministic output.

    Returns:
        str: Base64-encoded string of the styled image or error message.
    """
    data = {
        'prompt': prompt,
        'output_format': output_format,
        'fidelity': fidelity,
        'seed': seed
    }
    if negative_prompt:
        data['negative_prompt'] = negative_prompt

    # Decode the Base64 image and send it as part of the request
    imageBinary = base64.b64decode(b64String)
    image = BytesIO(imageBinary)
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/control/style",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={"image": ("style.png", image, "image/png")},
        data=data,
    )

    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    elif response.status_code == 403:
        return "Content moderation triggered"
    else:
        raise Exception(str(response.json()))


# Function for outpainting an image
def outpaintRequest(api_key, prompt, left, right, up, down, b64String, output_format, creativity, seed):
    """
    Performs outpainting on an image to expand its boundaries based on the provided parameters.

    Args:
        api_key (str): API key for authorization.
        prompt (str): Text prompt for the outpainting.
        left, right, up, down (int): Pixels to expand in each direction.
        b64String (str): Base64-encoded original image.
        output_format (str): Desired output format (e.g., 'png').
        creativity (float): Creativity level for the transformation.
        seed (int): Seed for deterministic output.

    Returns:
        str: Base64-encoded string of the outpainted image or error message.
    """
    data = {
        'prompt': prompt,
        'output_format': output_format,
        'creativity': creativity,
        'seed': seed,
        'left': left,
        'right': right,
        'up': up,
        'down': down
    }

    # Decode the Base64 image and send it as part of the request
    imageBinary = base64.b64decode(b64String)
    image = BytesIO(imageBinary)
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/edit/outpaint",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={"image": ("outpaint.png", image, "image/png")},
        data=data,
    )

    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    elif response.status_code == 403:
        return "Content moderation triggered"
    else:
        raise Exception(str(response.json()))


# Function to search and replace elements in an image based on a text prompt
def searchAndReplaceRequest(api_key, searchPrompt, replacePrompt, negativePrompt, output_format, b64String, seed):
    """
    Searches for elements in an image based on a search prompt and replaces them using a replacement prompt.

    Args:
        api_key (str): API key for authorization.
        searchPrompt (str): Text prompt for the elements to search in the image.
        replacePrompt (str): Text prompt for the elements to replace the searched elements.
        negativePrompt (str): Optional negative prompt to exclude certain features.
        output_format (str): Desired output format (e.g., 'png').
        b64String (str): Base64-encoded original image.
        seed (int): Seed for deterministic output.

    Returns:
        str: Base64-encoded string of the modified image or error message.
    """
    data = {
        'search_prompt': searchPrompt,
        'prompt': replacePrompt,
        'output_format': output_format,
        'seed': seed
    }
    if negativePrompt:
        data['negative_prompt'] = negativePrompt

    # Decode the Base64 image and send it as part of the request
    imageBinary = base64.b64decode(b64String)
    image = BytesIO(imageBinary)
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/edit/search-and-replace",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={"image": ("searchAndReplace.png", image, "image/png")},
        data=data,
    )

    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    elif response.status_code == 403:
        return "Content moderation triggered"
    else:
        raise Exception(str(response.json()))


# Function to remove the background from an image
def removeBackgroundRequest(api_key, output_format, b64String):
    """
    Removes the background from an image, leaving the subject intact.

    Args:
        api_key (str): API key for authorization.
        output_format (str): Desired output format (e.g., 'png').
        b64String (str): Base64-encoded original image.

    Returns:
        str: Base64-encoded string of the image with background removed or error message.
    """
    # Decode the Base64 image and send it as part of the request
    imageBinary = base64.b64decode(b64String)
    image = BytesIO(imageBinary)
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/edit/remove-background",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={"image": ("removeBackground.png", image, "image/png")},
        data={"output_format": output_format},
    )

    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    elif response.status_code == 403:
        return "Content moderation triggered"
    else:
        raise Exception(str(response.json()))


# Function to remove the background and relight the subject
def removeBackgroundAndRelightRequest(
        api_key,
        background_prompt,
        preserve_original_subject,
        original_background_depth,
        keep_original_background,
        light_source_strength,
        light_source_direction,
        output_format,
        b64String,
        foreground_prompt=None,
        negative_prompt=None,
        seed=None
):
    """
    Removes the background from an image and relights the subject based on the specified parameters.

    Args:
        api_key (str): API key for authorization.
        background_prompt (str): Text prompt for the new background.
        preserve_original_subject (bool): Whether to preserve the original subject.
        original_background_depth (float): Depth adjustment for the original background.
        keep_original_background (bool): Whether to retain parts of the original background.
        light_source_strength (float): Intensity of the light source.
        light_source_direction (str): Direction of the light source.
        output_format (str): Desired output format (e.g., 'png').
        b64String (str): Base64-encoded original image.
        foreground_prompt (str, optional): Text prompt for the subject.
        negative_prompt (str, optional): Optional negative prompt.
        seed (int, optional): Seed for deterministic output.

    Returns:
        str: Base64-encoded string of the modified image or error message.
    """
    # Decode the Base64 image
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

    # Send the request
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/edit/replace-background-and-relight",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        },
        data=data,
        files={"subject_image": ("subject_image.png", image, "image/png")},
    )

    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    # Polling for the result
    generation_id = response.json().get("id")
    if not generation_id:
        raise Exception("No generation ID found in response.")

    timeout = 500  # Timeout duration in seconds
    start = time.time()
    status_code = 202

    while status_code == 202:
        poll_response = requests.get(
            f"https://api.stability.ai/v2beta/results/{generation_id}",
            headers={"Authorization": f"Bearer {api_key}", "Accept": "*/*"},
        )
        status_code = poll_response.status_code

        if status_code != 202:
            break
        time.sleep(10)
        if time.time() - start > timeout:
            raise Exception(f"Timeout after {timeout} seconds")

    if status_code == 200:
        return base64.b64encode(poll_response.content).decode('utf-8')
    elif status_code == 403:
        return "Content moderation triggered"
    else:
        raise Exception(f"Error in polling response: HTTP {status_code}")
