# pycvtools

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)   

## Functionality of the pyevaltool

- Automated testing of the bot response deployed gpt


```
pip install pyevaltool
```
#### To run
```
from pyevaltool import *
```
#### For GPT test -
```
url = '' # Add the frontend url 
token = '' # add your token or key - Apim-Subscription-Key or Bearer token
# change the chat completion format if required. 
# This code will work only if the question asked is at chat_completion_format['messages'][0]["content"]
chat_completion_format = {'chatId': '', 'siteInfo': {'domain': ''}, 'messages': [{'role': 'user', 'content': ''}], 'model': '', 'stream': False} 
answer_loc = "['choices'][0]['messages'][0]['content']" #in string format
input_file = " " # Here you add your input file link
gpt_test(url,token,chat_completion_format,answer_loc,input_file,output_file = "output.csv" )
```


