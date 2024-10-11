from DrissionPage import ChromiumPage
import re
import pandas as pd
from def_basic import *
from def_run import *
import time
import random
import emoji


# 收藏数 评论数	发布时间 正文 标签 评论1 评论2 评论3 评论4 评论5

"""获取访问笔记页面链接"""
excel_path = '/Users/cris/Documents/Project/Find_Coder/actual/XHScrawler/result.xlsx'

# 读取 Excel 文件
df = pd.read_excel(excel_path)

# 提取 '笔记链接' 字段的每个值
note_links = df['笔记链接'].tolist()

note_main = []
# 遍历每个链接并赋值给 note_link 进行操作
for note_link in note_links:

    """读取笔记页面"""
    note_page = ChromiumPage()
    note_page.get(note_link)

    """正文、标签、收藏、评论、发布时间"""
    # 正文：note_text
    note_wrapper = note_page.ele('.desc')
    full_text = note_wrapper.text
    tags = [tag.text for tag in note_wrapper.eles('.tag')]
    note_text = full_text
    for tag1 in tags:
        note_text = note_text.replace(f"#{tag1}", "").replace(tag1, "")
    clean_text = emoji.replace_emoji(note_text, replace="")
    clean_text = clean_text.replace(" ", "")

    # 标签：tag
    tag = ' '.join(tag.text for tag in note_wrapper.eles('.tag'))

    # 发布时间/IP：note_time/ip
    note_time_raw = note_page.ele('.date').text
    note_time, ip = parse_time_and_location(note_time_raw)

    # 收藏数：collect_count
    collect_wrapper = note_page.ele('.collect-wrapper').text
    collect_count = re.search(r'(\d+\.?\d*万?|\d+)|(收藏)', collect_wrapper).group()
    if collect_count == '收藏':
        collect_count = '0'
    print(collect_count)

    # 评论数：chat_count
    chat_wrapper = note_page.ele('.chat-wrapper').text
    chat_count = re.search(r'(\d+\.?\d*万?|\d+)|(评论)', chat_wrapper).group()
    if chat_count == '评论':
        chat_count = '0'  # 如果是'收藏'，则设置收藏数为0

    note_main.append([collect_count, chat_count,clean_text,tag,note_time,ip])
    sleep_time = random.uniform(3, 5)
    print(f"暂停 {sleep_time:.2f} 秒...")
    time.sleep(sleep_time)

    """评论"""

"""插入表格"""
df = pd.read_excel(excel_path)
new_names = ['收藏数','评论数','正文','标签','发布时间','IP']
new_data_df = pd.DataFrame(note_main, columns=new_names)
result_df = pd.concat([df, new_data_df], axis=1)
result_df['收藏数'] = result_df['收藏数'].astype(str).apply(convert_count_to_int)
result_df['评论数'] = result_df['评论数'].astype(str).apply(convert_count_to_int)
result_df.to_excel(excel_path, index=False)
auto_resize_column(excel_path)