# Studon Exam :heart: ChatGPT

Small python script that shadows your activity on *Studon Exam* (at FAU) and parses the question to [ChatGPT](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiSraKqvab9AhWG_bsIHVZOAjUQFnoECA4QAQ&url=https%3A%2F%2Fchat.openai.com%2Fauth%2Flogin&usg=AOvVaw2tooVVFlzOmUjyM15PSIEe).  

*From Wikipedia:*

> ChatGPT (Chat Generative Pre-trained Transformer[2]) is a chatbot developed by OpenAI and launched in November 2022. 
> It is built on top of OpenAI's GPT-3 family of large language models and has been fine-tuned (an approach to transfer learning)
> using both supervised and reinforcement learning techniques. 

The response from ChatGPT is then printed, so you can decide what to do with it.  
Read the [Limitations](#limitations) sections for more info.


## Limitations

**1. Parsing the Questions:**

> Questions are sent as plain text to ChatGPT.  
> Therefore the formating of the questions can be off. 
> While ChatGPT is surprisingly resilient to formatting errors, its results will suffer.
> Formulas are a big NO, and will ***most likely*** not work very well.  
> **Images aren't sent at all, any question requiring images will not work**.

**2. ChatGPT Limitations:**

ChatGPT has limited knowledge of events that occurred after 2021:

> This makes it unfit to answer on questions requiring later knowledge.

ChatGPT will answer confidently even if the results are incorrect:

> Does that mean it is useless? Definetly no.  
> You need common sense to judge if the question is asked in such a way that ChatGPT will answer it correctly.
> The best thing to do is to familiarize yourself with ChatGPT before the exam. 
> You can experiment with the free ChatGPT version available online.


## Installation

### Requirements

To run the script, you need

* StudOn Exam `Username` & `Password`
* OpenAI API Key

The API Key can be generated on the [OpenAPI](https://platform.openai.com/account/usage) WebSite.
> To get an OpenAPI Key you need to have an OpenAPI Account.  

The amount of interaction with the ChatBot is limited. However  
**18$ of requests a month are free! This is more than enough for all your exams!**

Next you need to install the software..

### When you hear *python*, you think of snakes or comedy

//Todo

### You know what python is

To run this script you need to install  

* `python3` with `pip`

To install the required packages:

```sh
pip install selenium openai
```

##### Usage

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

Place the terminal on a seperate monitor and let it shadow your exam.  
So if you struggle with a question, ChatGPT is up to date and ready to chat with you.  

Run the script:

```
./studon_chatgpt.py -u $studname -p $studpassword -key $openapikey
```


## Keywords

Studon Exam ChatGPT FAU Online Test 
