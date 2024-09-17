This is the beyond API validator.

When developing your API to be compatible with Beyond you may use this validator to validate your endpoints are successful and returning the data in the expected format.

How to run?
$ cd beyond_validator
$ pip3 install -r requirements.txt

In the validator file:
Add your variables: 
BASE_URL = the base url for all your endpoints
API_KEY = The api key 

$ python3 validator.py

This will return the result of your API. If you have any errors they will be outputted.
