#!/usr/bin/env python3

import argparse
import sys
import time
import openai
import os
import threading
import queue

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException

# CONSTANTS
URL_LOGIN = "https://www.studon-exam.fau.de/winter22/login.php?lang=de"

# Variables
input_queue = queue.Queue()

def add_input(input_queue):
    while True:
        # input_queue.put(sys.stdin.read(1))
        input_queue.put(input())

def parse_credentials():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', dest='username', type=str, action='store', help='Enter StudOn-Exam "Username"')
    parser.add_argument('-p', '--password', dest='password', type=str, action='store', help='Enter StudOn-Exam "Password"')
    parser.add_argument('-key', '--openai_key', dest='openai_key'
                        , type=str, action='store', help='Openai API Key')
    # parser.add_argument('-org', '--openai_org', dest='openai_org'
    args = parser.parse_args()
    return (args.username, args.password, args.openai_key)


def ask_chatgpt(question, context=''):
    print("=========")
    print("Question: ", flush=True)
    print("=========")
    print(question)
    model_engine = "text-davinci-003"

    completion = openai.Completion.create(
        engine=model_engine,
        prompt="context:" + context + "\n\n" + "prompt:" + question,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7)
    # Model Response
    response = completion.choices[0].text
    print("=========")
    print("ChatGPT: ", flush=True)
    print("=========")
    print(response)
    print("\n Ask another Question?", end=' ', flush=True)
    context += "\n".join([context, question, response])
    return (context, response)



if __name__ == '__main__':
    username, password, openai_api_key = parse_credentials()

    assert username != None and password != None, "See '%s --help' for help!" % sys.argv[0]
    openai.api_key = openai_api_key

    # Start Input Queue
    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    # Login
    driver = webdriver.Firefox()
    driver.get(URL_LOGIN)

    field_username = driver.find_element(By.NAME, "username")
    field_password = driver.find_element(By.NAME, "password")
    field_username.send_keys(username)
    field_password.send_keys(password)

    driver.find_element(By.NAME, "cmd[doStandardAuthentication]").click()


    title_class = 'ilc_qtitle_Title'

    current_page = driver.current_url
    question_answered = False

    question_element = None
    context = ''

    while True:
        if question_element is not None:
            wait_stale = WebDriverWait(driver, timeout=0)
            try:
                wait_stale.until(EC.staleness_of(question_element))
                # Question has become stale
                question_element = None
                context = ''
                input_queue.queue.clear()
                os.system('clear')
            except TimeoutException:
                if not input_queue.empty():
                    input = input_queue.get()
                    ask_chatgpt(input, context)
                else:
                    time.sleep(1)
        else:
            wait_question = WebDriverWait(driver, timeout=100, poll_frequency=1
                                          , ignored_exceptions=[ElementNotVisibleException])
            try:
                wait_question.until(EC.presence_of_element_located((By.CLASS_NAME, title_class)))
                question_element = driver.find_element(By.CLASS_NAME, title_class)
                question = question_element.text
                # Ask chatgpt
                context, _ = ask_chatgpt(question)
            except:
                pass
            finally:
                time.sleep(3)




