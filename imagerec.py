import base64
import requests
import cv2
import numpy as np
from say import say

# OpenAI API Key
api_key = "sk-proj-jBrtG6TRqETlklbXFoLST3BlbkFJwUhu1DuoYJjEabQ20yNy"

# Function to capture image from camera and encode it
def capture_and_encode_image():
    cap = cv2.VideoCapture(0)  # 0 is the default camera device
    ret, frame = cap.read()
    cap.release()
    
    # Convert image to JPEG format
    _, buffer = cv2.imencode('.jpg', frame)
    
    # Encode image to base64 string
    base64_image = base64.b64encode(buffer).decode('utf-8')
    
    return base64_image

# Function to send request to OpenAI API
def send_request_to_openai(base64_image,prompt="what are you looking at"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()

# Main function to execute
def main():
    base64_image = capture_and_encode_image()
    
    # Send request to OpenAI API
    response = send_request_to_openai(base64_image)
    
    # Extract content from response
    content = response['choices'][0]['message']['content']
    
    return content