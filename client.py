import requests
import json

url = 'http://127.0.0.1:5000/api/candidates'
headers = {'Accept': 'application/vnd.api+json'}

def get(expertise, location):
    response = requests.get(url, headers=headers)
    filters = [{"or":[{"name":"expertise","op":"eq","val":expertise},{"name":"location","op":"eq","val":location}]}]
    params = {'filter[objects]': json.dumps(filters)}
    response = requests.get(url, params=params, headers=headers)
    assert response.status_code == 200
    print(response.json())

get("technical", "NYC")
get("business", "SF")
get("product", "SF")
