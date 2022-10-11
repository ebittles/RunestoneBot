from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import creds

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://runestone.academy/ns/books/published/MBA-CSP-2022-23-Easley/index.html')
    page.fill('input#auth_user_username', creds.username)
    page.fill('input#auth_user_password', creds.password)
    page.click('button[type=submit]')
    html = page.inner_html('div.toctree-wrapper.compound')
    soup = BeautifulSoup(html, 'html.parser')
    to_complete = soup.findAll('a', href=True)

links = []
vid_ids = []
q_ids = []
vocab_ids = []
    
for unit in to_complete:
    link = 'https://runestone.academy/ns/books/published/MBA-CSP-2022-23-Easley/' + unit['href']
    links.append(link)



for url in links:
    payload = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:105.0) Gecko/20100101 Firefox/105.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://runestone.academy/ns/books/published/MBA-CSP-2022-23-Easley/index.html",
        "DNT": "1",
        "Connection": "keep-alive",
        "Cookie": "access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJiaXR0bGVzX2UiLCJleHAiOjE2Njc5MTk5ODV9.uzKqiA2vRx5vrrUzQkl9JWaL0DwMIh72a5jab9gyLuo; session_id_runestone=45694090:71cb3efc-fb7c-41ec-b4e5-812c22d5ceeb; RS_info={\"tz_offset\": 0}",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin"
    }

    r = requests.request("GET", url, data=payload, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    divs = soup.find_all('div', class_='runestone')

    for div in divs:
        id = div.findChild()['id']
        if id[0:4] == "mcsp" or id[0:4] == "mscp":
            q_ids.append(id)
        elif id[0:5] == "vocab":
            vocab_ids.append(id)
        else:
            vid_ids.append(id)

def complete_youtube_vid(vid_id):
    log_url = "https://runestone.academy/ns/logger/bookevent"

    payload = {
        "event": "video",
        "div_id": v_id,
        "act": "ready",
        "course_name": "MBA-CSP-2022-23-Easley",
        "clientLoginStatus": True,
        "timezoneoffset": 0
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:105.0) Gecko/20100101 Firefox/105.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://runestone.academy/ns/books/published/MBA-CSP-2022-23-Easley/Unit4-Animation-Simulation-Modeling/LightsOff-Projects.html",
        "content-type": "application/json; charset=utf-8",
        "Origin": "https://runestone.academy",
        "DNT": "1",
        "Connection": "keep-alive",
        "Cookie": "session_id_runestone=45693372:3f759db7-972f-4d0a-9bea-857dd9c113ab; RS_info={\"tz_offset\": 0}; access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJiaXR0bGVzX2UiLCJleHAiOjE2Njc5MTQyMTV9.B0rWfTUE9jHzwn-XireDOSj_GKQCW9pHEPQRH9_1_Bo",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    response = requests.request("POST", log_url, json=payload, headers=headers)

    print(response.text)


def complete_questions(q_id):
    url = "https://runestone.academy/ns/logger/bookevent"

    payload = {
        "event": "mChoice",
        "act": "answer::no",
        "answer": "",
        "correct": "T",
        "div_id": q_id,
        "course_name": "MBA-CSP-2022-23-Easley",
        "clientLoginStatus": True,
        "timezoneoffset": 0
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:105.0) Gecko/20100101 Firefox/105.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://runestone.academy/ns/books/published/MBA-CSP-2022-23-Easley/Unit4-Animation-Simulation-Modeling/Coin-Flip-Simulation-Tutorial.html",
        "content-type": "application/json; charset=utf-8",
        "Origin": "https://runestone.academy",
        "DNT": "1",
        "Connection": "keep-alive",
        "Cookie": "session_id_runestone=45693372:3f759db7-972f-4d0a-9bea-857dd9c113ab; RS_info={\"tz_offset\": 0}; access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJiaXR0bGVzX2UiLCJleHAiOjE2Njc5MTQyMTV9.B0rWfTUE9jHzwn-XireDOSj_GKQCW9pHEPQRH9_1_Bo",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)

def do_vocab(vocab_id):
    url = "https://runestone.academy/ns/logger/bookevent"

    payload = {
        "event": "shortanswer",
        "act": "",
        "answer": "",
        "div_id": vocab_id,
        "course_name": "MBA-CSP-2022-23-Easley",
        "clientLoginStatus": True,
        "timezoneoffset": 0
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:105.0) Gecko/20100101 Firefox/105.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://runestone.academy/ns/books/published/MBA-CSP-2022-23-Easley/Unit4-Animation-Simulation-Modeling/Unit-Overview.html",
        "content-type": "application/json; charset=utf-8",
        "Origin": "https://runestone.academy",
        "DNT": "1",
        "Connection": "keep-alive",
        "Cookie": "access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJiaXR0bGVzX2UiLCJleHAiOjE2Njc5MTk5ODV9.uzKqiA2vRx5vrrUzQkl9JWaL0DwMIh72a5jab9gyLuo; session_id_runestone=45724838:8e8398cd-b14a-4aa5-bc11-2667c0407a76; RS_info={\"tz_offset\": 0}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)


"""
for video in vid_ids:
    complete_youtube_vid(video)

for question in q_ids:
    complete_questions(question)

for vocab in vocab_ids:
    do_vocab(vocab)
"""
print(vid_ids)
print("-------------------")
print(q_ids)
print("-------------------")
print(vocab_ids)