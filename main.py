#Distinguish between login fail and no upcoming tests or quizes
#If test name is not specific enough, ask for context. Give the user the option to provde context for each test in the dashboard.
#Give the user the ability to go from a practice to the dashboard or another practice
#Switch to headless mode
from flask import Flask, render_template, request, redirect, session
import requests, json
from selenium import webdriver
driver = webdriver.Firefox()
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from flask import jsonify
import os
import openai

# Set your OpenAI API key
openai.api_key = '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'

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/404')
def page_404():
    return render_template('404.html')

@app.route('/dashboard')
def dashboard():
    # Data = request.args.get('tasks')
    # return Data
    return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(f'Username: {username}, Password: {password}')

    # Define the URL for the login page
    url = 'https://schoology.harker.org'  # Replace with actual URL

    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, 'i0116'))).send_keys(username)
    except:
        return redirect("/404")
    WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, 'idSIButton9'))).click()
    try:
        WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, 'i0118'))).send_keys(password)
    except:
        return redirect("/404")
    WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, 'idSIButton9'))).click()
    sleep(1)
    try:
        WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, 'idSIButton9'))).click()
    except:
        return redirect("/404")
    sleep(2)
    to_do_list = []
    to_do_items = driver.find_elements(By.CSS_SELECTOR, 'div:not(.hidden-important) > h4 span.event-title a')
    for t in to_do_items:
        if 'quiz' in t.text.lower() or 'test' in t.text.lower() or 'tst' in t.text.lower() or 'qz' in t.text.lower():
            if 'study guide' not in t.text.lower():
                to_do_list.append({'title': t.text, 'url': t.get_attribute('href')})
    print(to_do_list)

    name = driver.find_element(By.CSS_SELECTOR, 'div[data-sgy-sitenav="header-my-account-menu"] button img').get_attribute('alt').split(' ')[0]

    if to_do_list:
        return redirect(f"/dashboard?tasks={json.dumps(to_do_list)}&name={name}")
    else:
        return 'Login failed.'

@app.route('/test/<test_name>')
def test(test_name):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate 10 relevant and helpful practice questions to help me prepare for my upcoming {test_name} test. Finally, do not provide additional messages that are not questions such as 'Here are the practice questions'."}
        ]
    )

    practice_questions = response.choices[0].message['content'].strip()

    return render_template('practice_questions.html', questions=practice_questions, test_name=test_name)

if __name__ == '__main__':
    app.run(debug=True)