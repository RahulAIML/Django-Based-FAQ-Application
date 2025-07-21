import requests

try:
    response = requests.get('http://localhost:8000/api/questions/')
    print(f"Status Code: {response.status_code}")
    print("Response:", response.text)
except Exception as e:
    print(f"Error: {e}")
