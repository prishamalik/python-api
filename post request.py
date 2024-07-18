import requests

url = 'http://127.0.0.1:5001/api/link_aadhar_status'
data = {
    "pan": "HWTPM9259P",
    "aadhaar": "987089659606"
}

try:
    response = requests.post(url, json=data)
    response.raise_for_status()  

    content_type = response.headers.get('application/json')
    print(f"Content Type: {content_type}")

    if 'application/json' in content_type:
        json_data = response.json()
        print(json_data)
    else:
        print(response.text)  

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
