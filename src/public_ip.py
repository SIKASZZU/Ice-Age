import requests

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=text')
        if response.status_code == 200:
            return response.text
        else:
            return "Error fetching IP: " + str(response.status_code)
    except Exception as e:
        return "Error: " + str(e)

