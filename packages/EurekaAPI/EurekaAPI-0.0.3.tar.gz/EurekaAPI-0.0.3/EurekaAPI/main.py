from EurekaAPI.API_request import *

class Eureka_Agent:
    def __init__(self, API_Key):
        self.API_Key = API_Key
        self.Agent = APIInterface(self.API_Key)
    
    def say(self, message):
        response = self.Agent.send_request(message)
        return response

if __name__ == "__main__":
    Agent = Eureka_Agent()
    ResponseOutput = Agent.say("Hello!")
    print(ResponseOutput)