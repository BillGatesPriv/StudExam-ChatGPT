# StudExam and ChatGPT

```sh
usage: studon_chatgpt.py [-h] [-u USERNAME] [-p PASSWORD] [-key OPENAI_KEY]

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Enter StudOn-Exam "Username"
  -p PASSWORD, --password PASSWORD
                        Enter StudOn-Exam "Password"
  -key OPENAI_KEY, --openai_key OPENAI_KEY
                        Openai API Key
```

## Introduction

This is a small script that when started will open a firefox instance.  
From there it will log you in StudOn-Exam automatically and scans your current tab for occurences of a StudOn-Exam Question.  
If it finds one it will ask the question to ChatGPT. You can then communicate with the Model or simply jump to the next question.


## Usage

Open the script on a seperate monitor and only use it if you don't know the question.  
The model does not know our slides and will likely answer garbage for most questions.  
However that may be better than nothing.  
  
Enjoy!

## Setup & Costs

How to run:

```
./studon_chatgpt.py -u $studname -p $studpassword -key $openapikey
```

The API Key can be generated on the [OpenAPI](https://platform.openai.com/account/usage) WebSite.
> To get an OpenAPI Key you need to have an OpenAPI Account.  

**18$ of requests a month are free! This is enough for any exam!**
