import requests

# API endpoint and parameters
API_ENDPOINT = "https://opentdb.com/api.php"
parameters = {
    "amount": 10,
    "type": "boolean"
}

# Get response from Open Trivia Database
response = requests.get(url=API_ENDPOINT, params=parameters)
response.raise_for_status()

# Store response questions in a list
question_data = response.json()["results"]
