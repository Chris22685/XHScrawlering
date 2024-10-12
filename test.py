import logging
from DrissionPage import ChromiumPage
import re
import pandas as pd
from def_basic import *
from def_run import *
import time
import random
import emoji
import pickle
import os

note_link = 'https://www.xiaohongshu.com/explore/64a6cd11000000001201024b'

note_page = ChromiumPage()
note_page.get(note_link)

no_comments_element = note_page.ele('.no-comments')
if no_comments_element:
    logging.info("该页面没有评论")
    print("无评论")

comment_elements = note_page.eles('.comment-item')
if not comment_elements:
    logging.info("未找到评论元素，可能是页面结构变化")
    print("未找到评论元素")

for comment in comment_elements[:10]:  # 限制为10条评论
    comment_text = comment.ele('.note-text').text
    print(comment_text)
