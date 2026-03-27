import requests

def get_quote():
    url = "https://zenquotes.io/api/random"
    response = requests.get(url, timeout=5)
    data = response.json()[0]
    return data["q"], data["a"]