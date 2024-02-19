import requests
import json

class APIInterface:
    def __init__(self, API):
        self.API_Key = API
    
    def send_request(self, message):
        response = requests.post("http://82.165.235.137/", headers={
            "API-Key": f"{self.API_Key}"
            }, data=json.dumps({
            "query": f"{message}"
            }))

        return response
