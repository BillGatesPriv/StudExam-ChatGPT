#!/usr/bin/env python3

import argparse
import openai
import os
import queue
from queue import Empty
import sys
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException, TimeoutException

# CONSTANTS
URL_LOGIN = "https://www.studon-exam.fau.de/winter22/login.php?lang=de"
QUESTION_OUTER_CLASS = 'ilc_question_Standard'

# Variables
input_queue = queue.Queue()


def add_input(input_queue):
    while True:
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



def build_chatgpt_question(question_standard):
    child_elements = question_standard.find_elements(By.XPATH, './/*')

    question_type = child_elements[0].get_dom_attribute("class")
    question_text = ''
    try:
        question_text = '%s\n' % question_standard.find_element(By.CLASS_NAME, 'ilc_qtitle_Title').text
    except NoSuchElementException:
        pass

    match question_type:
        case 'ilc_question_MultipleChoice':
            for answer in question_standard.find_elements(By.CLASS_NAME, 'answertext'):
                question_text += '* %s\n' % answer.text
        case 'ilc_question_KprimChoice':
            question_text += '%s\n' % question_standard.find_element(By.CLASS_NAME, 'ilAssKprimInstruction').text
            for answer in question_standard.find_elements(By.CLASS_NAME, 'ilc_qanswer_Answer')[1 :]:
                question_text += '* %s\n' % answer.text
        case 'ilc_question_OrderingQuestion':
            for item in question_standard.find_elements(By.CLASS_NAME, 'ilc_qordli_OrderListItem'):
                question_text += '* %s\n' % item.text
        case 'ilc_question_ClozeTest':
            question_text = question_standard.text
            question_text += '\n%s' % 'Fill the blanks!'
        case 'ilc_question_MatchingQuestion':
            question_text += "%s\n" % question_standard.find_element(By.ID, 'targetArea').text
            question_text += "%s\n" % question_standard.find_element(By.ID, 'sourceArea').text
        case 'ilc_question_FormulaQuestion':
            question_text += "%s\n" % question_standard.find_element(By.CLASS_NAME, 'ilc_question_FormulaQuestion').text
        case 'ilc_question_TextQuestion':
            pass
        case _:
            print(">>> Warning: Question type not recognized", file=sys.stderr)
            question_text = question_standard.text
    return question_text


class QuestionThread(threading.Thread):

    def __init__(self, question_element, *args, **kwargs):
        super(QuestionThread, self).__init__(*args, *kwargs, daemon=True)
        self.question_element = question_element
        self.stop_event = threading.Event()

    def ask_chatgpt(self, question, context=''):
        print("=========\n%s\n=========\n" % "Question: ", flush=True)
        print(question, flush=True)
        model_engine = "text-davinci-003"

        prompt = "context:" + context + "\n\n" + "prompt:" + question
        prompt = prompt.strip()

        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=2048,
            n=1,
            temperature=1,
            stream=True)
        # Model Response
        print("=========\n%s\n=========\n" % "ChatGPT: ", flush=True)

        response = ''
        for resp in completion:
            streamed = resp.choices[0].text
            print(streamed, end="", flush=True)
            response += streamed
            # Abort if stop_event is set
            if self.stop_event.is_set():
                return ('', '')

        if len(response) == 0:
            print("\n\n Tell ChatGPT what to do:", end=' ', flush=True)
        else:
            print("\n\n Ask ChatGPT:", end=' ', flush=True)

        context += "\n".join([context, question, response])
        return (context, response)

    def stop(self):
        self.stop_event.set()

    def run(self):
        os.system('clear')
        question = build_chatgpt_question(self.question_element)
        context, _ = self.ask_chatgpt(question)
        while not self.stop_event.is_set():
            try:
                # Poll the input queue in interval
                question = input_queue.get(timeout=1)
                context, _ = self.ask_chatgpt(question, context)
            except Empty:
                pass
        input_queue.queue.clear()



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


    # Main Loop
    wait_stale = WebDriverWait(driver, timeout=100, poll_frequency=1)
    wait_question = WebDriverWait(driver, timeout=100, poll_frequency=1
                                    , ignored_exceptions=[ElementNotVisibleException])

    questionThread = None
    while True:
        try:
            if questionThread is not None:
                # Wait until Element is stale
                wait_stale.until(EC.staleness_of(questionThread.question_element))
                # Wait until Thread returned
                questionThread.stop()
                questionThread.join()
                questionThread = None
            else:
                wait_question.until(EC.presence_of_element_located((By.CLASS_NAME, QUESTION_OUTER_CLASS)))
                question_element = driver.find_element(By.CLASS_NAME, QUESTION_OUTER_CLASS)
                questionThread = QuestionThread(question_element)
                questionThread.start()

        except TimeoutException:
            pass


