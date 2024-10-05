import base64
import requests
import os
from dotenv import load_dotenv
import time
import json
import re

from django.http import HttpResponse


load_dotenv()

OPEN_AI_COMPLETIONS = "https://api.openai.com/v1/chat/completions"
MINI_MODEL = "gpt-4o-mini"
GPT_4_OMINI = "gpt-4o"
GPT_4_TURBO = "gpt-4-turbo"
GPT_4 = "gpt-4"
GPT_3_5_TURBO = "gpt-3.5-turbo"
DALL_E_3 = "dall-e-3"
DALL_E_2 = "dall-e-2"

MAX_TOKENS = 8,192
MAX_TURBO_TOKENS = 32,768
# OpenAI API Key
api_key = os.getenv("OPEN_AI_API_KEY")

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def use_default_prompt(item, output_type='JSON', structure=None, number=10):
    default_prompt = get_default_prompt(item, output_type, structure, number)
    return send_prompt(default_prompt)
    
               
def get_default_prompt(item, output_type='JSON', structure=None, number=10):
    print('Generating Questions for ', item)
    prompt = f"Using the Ontario MTO handbook as a guide, Generate exactly {number} questions about {item} in strict {output_type} format. Each question should have the following structure:"
    prompt += f""" {{
    "question": "The question text",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "correct_answer": "The correct option",
    "explanation": "Explanation of why the correct answer is right"
    }}""" if not structure else structure
    prompt+= "The output should only be valid {output_type}. Do not include any text or comments outside the {output_type} structure. do not prefix with the word '{output_type}'. your response should only be an array of {output_type}s."
    return prompt

def send_prompt(prompt, model=MINI_MODEL, base64_image=None, max_tokens=5000):
    content = [
        {
            "type": "text",
            "text": prompt
        }
    ]

    if base64_image:
        content.append(
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        )

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "max_tokens": max_tokens,
    }

    headers = {
        "Content-Type": 'application/json',
        "Authorization": f'Bearer {api_key}'
    }

    response = requests.post(
        'https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(payload)
    )

    if response.status_code == 200:
        print(response.text)
        output = response.json()
        data = output['choices'][0]['message']['content']
        return data
    else:
        # print('ERROR', response.text)
        raise Exception(response.text)

        
def run_prompts(item_list: list, use_timer=21, use_default_prompt=False):
    data = []
    errors = []
    for index, item in enumerate(item_list):
        try:
            if use_default_prompt:
                prompt = get_default_prompt(item)
            else:
                prompt = item

            item_data = send_prompt(prompt)
            try:
                item_data = json.loads(item_data)
            except:
                item_data = json.loads(item_data[0])
            # data.append({item: item_data})  # String
            data.append(item_data)
        except Exception as e:
            data.append({item: str(e)})

        if use_timer and index < len(item_list) - 1:
            timer(use_timer)
        
    return data, errors

def http_response(data):
    json_data = json.dumps(data)
    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="data.json"'
    return response



def timer(countdown=21):
    if not countdown:
        return
    for remaining in range(countdown, 0, -1):
        print(f"{remaining} s", end="\r")
        time.sleep(1)

def custom_prompt(prompt_type, prompt_text):
   prompt = get_prompts_by_type(prompt_type)
   prompt = prompt.format(prompt_text)
   data = send_prompt(prompt)
   return data

def get_prompts_by_type(prompt_type):
    return ''