import requests

url = "https://www.llama2.ai/api"
headers = {
    "Content-Type": "application/json",
    "Referer": "https://www.llama2.ai/"
}


data = {
    "prompt": "When was nato founded?",
    "model": "meta/llama-2-70b-chat",
    "systemPrompt": "You are a helpful assistant.",
    "temperature": 0.6,
    "topP": 0.1,
    "topK": 40,
    "maxTokens": 1800,
    "image": None,
    "audio": None
}


def llama2_simple(prompt):
    dt = data
    dt["prompt"] = prompt
    r = requests.post(url, headers=headers, json=data)
    return r.text
