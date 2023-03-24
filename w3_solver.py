import sys
import time
import re
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

# link = https://www.w3schools.com/html/exercise.asp?filename=exercise_html_attributes2
WAIT_TIME = 0.25
MANUAL_TIME = 10000
assert len(sys.argv) == 2, "musi być podana 1 zmienna - url"
startUrl = sys.argv[1]
driver = webdriver.Chrome()

def click(button):
    try:
        WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable(button))
        button.click()
    except Exception as e:
        pass
    
def clickAll(buttons):
    for b in buttons:
        click(b)
    
def getAnswers():
    assigment = driver.find_element(By.ID, "assignmentcode").get_attribute("innerText")
    correct = driver.find_element(By.ID, "correctcode").get_attribute("innerText")
    answers = []

    while (len(assigment) > 0 and len(correct) > 0):
        common_len = len(os.path.commonprefix([assigment, correct]))
        assigment = assigment[common_len:]
        correct = correct[common_len:]
        
        # a_split = assigment.split('"', 1)
        # c_split = correct.split('"', 1)
        # if (len(a_split) == 2 and len(c_split) == 2):
        #     print("...")
        #     answers.append(c_split[0])
        #     assigment = a_split[1]
        #     correct = c_split[1]

        a_split = assigment.split(')', 1)
        if (len(a_split) == 2):
            next_c = a_split[1][0]
            c_split = correct.split(next_c, 1)
            answers.append(c_split[0])
            assigment = a_split[1][1:]
            correct = c_split[1]

        # c_split = correct.split('"', 1)
        # if (len(a_split) == 2 and len(c_split) == 2):
        #     print("...")
        #     answers.append(c_split[0])
        #     assigment = a_split[1]
        #     correct = c_split[1]

    return answers


def manualFill(submit):
    WebDriverWait(driver, MANUAL_TIME).until(EC.staleness_of(driver.find_element(By.TAG_NAME, "html")))

def fillPage():
    inputAns = []

    inputFields = driver.find_elements(By.CLASS_NAME, "editablesection")
    showAns = driver.find_elements(By.CLASS_NAME, "showanswerbutton")
    hideAns = driver.find_elements(By.CLASS_NAME, "hideanswerbutton")
    submit = driver.find_element(By.ID, "answerbutton")

    clickAll(showAns)
    inputAns = getAnswers()

    clickAll(hideAns)
    for i in range(len(inputFields)):
        inputFields[i].clear()
        inputFields[i].send_keys(inputAns[i])

    print(inputAns)

    WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable(submit))
    click(submit)
    if (submit.get_attribute("innerText") == "Try Again"):
        manualFill(submit)
    else:
        click(submit)

def repeat():
    string = driver.find_element(By.ID, "completedExercisesNo").get_attribute("innerText")
    print("SSS ", string)
    pattern = r"Completed (\d+) of (\d+) Exercises:"
    match = re.match(pattern, string)
    completed = int(match.group(1))
    exercisesNo = int(match.group(2))

    return completed < exercisesNo

def completeCourse(url):
    driver.get(url)
    while(repeat()):
        fillPage()
    time.sleep(999)

# main
completeCourse(startUrl)
