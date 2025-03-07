import requests

def fetch_data(api_endpoint):
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data")
        return None

data = fetch_data('https://api.example.com/data')
print(data)