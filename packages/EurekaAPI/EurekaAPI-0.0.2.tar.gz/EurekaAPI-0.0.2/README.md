# Eureka-Py

Library for interaction with the Eureka API.

## Installation

``` bash
pip install EurekaPy
```

## Usage

``` python

from EurekaPy import *


# Replace YOUR_API_KEY with your actual API key

Agent = Eureka_Agent("YOUR_API_KEY")

# Send a message to the API

response = Agent.say("Hello, world!")

# Print the response text

print(response)

```
