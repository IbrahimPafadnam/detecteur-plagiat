import requests

def search_web(query, api_key, cse_id):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
    }
    response = requests.get(url, params=params)
    return response.json()