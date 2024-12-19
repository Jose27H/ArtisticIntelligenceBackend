import requests
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