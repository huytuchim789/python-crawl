# from bs4 import BeautifulSoup
# import requests
# import re

# regex = re.compile('.*jsc.*')
# source=requests.get('https://m.facebook.com/groups/744721719556973/').text
# soup =BeautifulSoup(source,'lxml')
# # match=
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 01:57:06 2021
@author: wenchen
"""
import pickle

from typing import Optional
from email import message
from tokenize import group
from lxml import html
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
from fastapi import FastAPI  # import class FastAPI() từ thư viện fastapi
import re
import json
import pprint
import os
import uvicorn
# import nest_asyncio

app = FastAPI()  # gọi constructor và gán vào biến app

# class Post:
#   def __init__(self, author, content):
#     self.author = author
#     self.content = content


def connect_and_login(group_id: str):
    # connertion
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("window-size=1400,900")
    # chrome = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # chrome.get("https://facebook.com/groups/744721719556973/")
    # chrome.save_screenshot("my_screenshot.png")
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    chrome = webdriver.Chrome(executable_path=os.environ.get(
        "CHROMEDRIVER_PATH"), chrome_options=options)
    # chrome = webdriver.Chrome('./chromedriver', chrome_options=options)

    # chrome = webdriver.Chrome(chrome_options=options)
    # email = chrome.find_element_by_xpath(
    #     "/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input")
    # password = chrome.find_element_by_xpath(
    #     "/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input")
    # # read password from file
    # with open(password_filename) as f:
    #     lines = f.readlines()
    # my_password = lines
    # email.send_keys("195d140209056@hpu2.edu.vn")
    # password.send_keys("hong654321")
    # password.submit()
    # waiting login
    # time.sleep(10)
    # chrome.get("https://www.facebook.com/")
    # email = chrome.find_element_by_xpath(
    #     "/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input")
    # password = chrome.find_element_by_xpath(
    #     "/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input")
    # email.send_keys("tu.th184216@sis.hust.edu.vn")
    # password.send_keys("Huytu@1111")
    # password.submit()
    # time.sleep(10)
    # pickle.dump(chrome.get_cookies(), open("my_cookie.pkl", "wb"))
    chrome.get("https://www.facebook.com/groups/"+group_id)
    return chrome


def isclickable(e):
    try:
        WebDriverWait(chrome, 10).until(EC.element_to_be_clickable(e))
        return True
    except:
        return False


def get_all_post(chrome, num):
    posts = []
    i = 0
    regex = re.compile('.*kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql.*')
    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    while(i < num):
        # rolling page
        chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        tree = html.fromstring(chrome.page_source)
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        # click See more
        i = i+1
        # click See more
        # elements = chrome.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div/div/div/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/div/div/div/span/div[2]/div[4]/div")
        # el = tree.xpath("//*[text()='See more']")
        # for k in range(len(elements)):
        #     try:
        #         elements[k].click()
        #     except :
        #         if(el[k].getroottree().getpath(el[k])!="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div/div/div/div/span/span"):
        #             print("missed some content", el[k].getroottree().getpath(el[k]))
    match = soup.find_all('div', class_='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0')
    time.sleep(6)
    for ele in match:
        # if click !=None:
        #     click=ele.getText()
        author = ele.find(
            'h2', class_='gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl aahdfvyu hzawbc8m').strong.span.text
        content = ele.find('div', {'class': regex})
        # if content.div != None:
        #     content = content.getText()
        # elif content.span != None:
        #     content = content.getText()
        # else:
        if type(content) != str:
            try:
                content = content.getText()
            except:
                content = content
        if ele.find('div', {'data-ad-preview': 'message'}) != None:
            content = ele.find('div', {'data-ad-preview': 'message'}).getText()
        if(content != None):
            phone_number = re.findall("0[0-9]{9}", content)
        post = {'author': author, 'content': content,
                'phone_author': phone_number}
        posts.append(post)
    return posts


def get_author(post):
    try:
        author_ = post.find("strong").text
    except:
        author_ = post.find("span").text
    return author_


def get_content(post):
    content_ = ""
    try:
        contents_ = post.find_all(
            "div", class_="kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q")
        for c in contents_:
            content_ += c.text
    except:
        pass
    try:
        contents2_ = post.find_all(
            "div", class_="o9v6fnle cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q")
        for c in contents2_:
            content_ += c.text
    except:
        pass
    return content_


def get_img_content(post):
    img_content_ = ""
    try:
        img_content_ = post.find("img")["alt"]
    except:
        pass
    try:
        img_content_ += post.find("span",
                                  class_="a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ojkyduve").text
    except:
        pass
    return img_content_


def get_like(post):
    like_num = ""
    try:
        like_num = post.find("span", class_="pcp91wgn").text
    except:
        pass
    return like_num


def post_decode(posts, author, content, img_content, like):
    info_list = []

    for post in posts:

        sub_list = []
        # get uesr/group name
        if(author):
            sub_list.append(get_author(post))

        # get content
        if(content):
            sub_list.append(get_content(post))

        # get img title/alt
        if(img_content):
            sub_list.append(get_img_content(post))
        # get number of like
        if(like):
            sub_list.append(get_like(post))

        info_list.append(sub_list)

    return info_list


@app.get("/{group_id}")  # giống flask, khai báo phương thức get và url
# RUN:python -m uvicorn main:app --reload
# do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
async def root(group_id: str, q: Optional[str] = None):
    if group_id == None:
        return {"message": "Group id cannot be null"}
    chrome = connect_and_login(group_id)
    posts = get_all_post(chrome, num=15)
    chrome.quit()
    return posts
if __name__ == '__main__':
    chrome = connect_and_login('744721719556973')
    posts = get_all_post(chrome, num=10)
    # info_list = post_decode(posts, author=True, content=True, img_content=True, like=True)
    pprint.pprint(posts)
    # chrome.quit()

# Allows the server to be run in this interactive environment
# nest_asyncio.apply()

# # Host depends on the setup you selected (docker or virtual env)
# host = "0.0.0.0" if os.getenv("DOCKER-SETUP") else "127.0.0.1"

# # Spin up the server!
# uvicorn.run("main:app", host="0.0.0.0")
