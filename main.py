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
from http import cookies
import pickle
from socket import timeout

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
from facebook_scraper import get_posts

# import nest_asyncio
app = FastAPI()  # gọi constructor và gán vào biến app


def connect_and_login_public(group_id: str):
    PROXY = "113.20.99.18"
    FILE_NAME_PROFILE = "C:\\Users\\tranhuytu242000\\AppData\\Local\\Google\\Chrome\\User Data"
    options = Options()
    # options.add_argument('--proxy-server=%s' % PROXY)
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    # options.add_argument('--user-data-dir='+FILE_NAME_PROFILE)
    # options.add_argument('profile-directory=Default')
    chrome = webdriver.Chrome(chrome_options=options)
    chrome.get("https://www.facebook.com/")
    time.sleep(2)
    email = chrome.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input")
    password = chrome.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input")
    email.send_keys("tu.th184216@sis.hust.edu.vn")
    password.send_keys("Huytu@1111")
    password.submit()
    time.sleep(2)
    chrome.get("https://www.facebook.com/groups/"+group_id)
    return chrome


def connect_and_login_private(group_id: str):
    PROXY = "113.20.99.18"
    # FILE_NAME_PROFILE="C:\\Users\\tranhuytu242000\\AppData\\Local\\Google\\Chrome\\User Data"
    options = Options()
    # options.add_argument('--proxy-server=%s' % PROXY)
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    # options.add_argument('--user-data-dir='+FILE_NAME_PROFILE)
    # options.add_argument('profile-directory=Default')
    chrome = webdriver.Chrome(chrome_options=options)
    chrome.get("https://www.facebook.com/")
    time.sleep(2)
    email = chrome.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input")
    password = chrome.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input")
    email.send_keys("tu.th184216@sis.hust.edu.vn")
    password.send_keys("Huytu@1111")
    password.submit()
    time.sleep(2)
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
        time.sleep(2)
        chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        tree = html.fromstring(chrome.page_source)
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        # click See more
        i = i+1
    match = soup.find_all('div', class_='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0')
    time.sleep(6)
    for ele in match:
        author = ele.find(
            'h2', class_='gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl aahdfvyu hzawbc8m').strong.span.text
        content = ele.find('div', {'class': regex})
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


@app.get("/public/{group_id}")  # giống flask, khai báo phương thức get và url
# RUN:python -m uvicorn main:app --reload
# do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
async def root(group_id: str, q: Optional[str] = None):
    if group_id == None:
        return {"message": "Group id cannot be null"}
    # chrome = connect_and_login_public(group_id)
    # posts = get_all_post(chrome, num=5)
    # chrome.quit()
    posts = get_posts(group=group_id, pages=1, timeout=30,
                      options={"posts_per_page": 10})
    datas = []
    for post in posts:
        phone_number = re.findall("0[0-9]{9}", post['post_text'])
        datas.append({'author': post['username'],
                     'content': post['text'], 'phone_number': phone_number})

    return datas


@app.get("/private/{group_id}")  # giống flask, khai báo phương thức get và url
# RUN:python -m uvicorn main:app --reload
# do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
async def root(group_id: str, q: Optional[str] = None):
    if group_id == None:
        return {"message": "Group id cannot be null"}
    # chrome = connect_and_login_public(group_id)
    # posts = get_all_post(chrome, num=5)
    # chrome.quit()
    posts = get_posts(group=group_id, pages=1, timeout=30,cookies="fb_cookies.txt",
                      options={"posts_per_page": 10})
    datas = []
    for post in posts:
        phone_number = re.findall("0[0-9]{9}", post['post_text'])
        datas.append({'author': post['username'],
                     'content': post['text'], 'phone_number': phone_number})

    return datas

# Allows the server to be run in this interactive environment
# nest_asyncio.apply()

# # Host depends on the setup you selected (docker or virtual env)
# host = "0.0.0.0" if os.getenv("DOCKER-SETUP") else "127.0.0.1"

# # Spin up the server!
# uvicorn.run("main:app", host="0.0.0.0")
