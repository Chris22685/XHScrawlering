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

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_state(counter, note_main):
    try:
        with open('crawler_state.pkl', 'wb') as f:
            pickle.dump((counter, note_main), f)
        logging.info(f"保存状态：已爬取 {counter} 条数据")
    except Exception as e:
        logging.error(f"保存状态时出错: {str(e)}")

def load_state():
    try:
        if os.path.exists('crawler_state.pkl'):
            with open('crawler_state.pkl', 'rb') as f:
                counter, note_main = pickle.load(f)
            logging.info(f"加载状态：上次已爬取 {counter} 条数据")
            return counter, note_main
        else:
            logging.info("未找到保存的状态，从头开始爬取")
            return 0, []
    except Exception as e:
        logging.error(f"加载状态时出错: {str(e)}")
        return 0, []

excel_path = '/Users/cris/Documents/Project/Find_Coder/actual/XHScrawler/result.xlsx'

# 读取 Excel 文件
try:
    df = pd.read_excel(excel_path)
    note_links = df['笔记链接'].tolist()
    logging.info(f"成功读取Excel文件，共有 {len(note_links)} 条笔记链接")
except Exception as e:
    logging.error(f"读取Excel文件时出错: {str(e)}")
    note_links = []

counter, note_main = load_state()

logging.info(f"开始爬取，总链接数：{len(note_links)}，从第 {counter + 1} 条开始")

# 遍历每个链接并赋值给 note_link 进行操作
for note_link in note_links[counter:]:
    try:
        logging.info(f"正在爬取第 {counter + 1} 条数据: {note_link}")

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

        # 评论数：chat_count
        chat_wrapper = note_page.ele('.chat-wrapper').text
        chat_count = re.search(r'(\d+\.?\d*万?|\d+)|(评论)', chat_wrapper).group()
        if chat_count == '评论':
            chat_count = '0'  # 如果是'收藏'，则设置收藏数为0
        
        # 爬取评论
        note_comments = scrape_comments(note_page)

        note_main.append([collect_count, chat_count, clean_text, tag, note_time, ip, note_comments])
        logging.info(f"成功爬取第 {counter + 1} 条数据")
        
        sleep_time = random.uniform(4, 8)
        logging.info(f"暂停 {sleep_time:.2f} 秒...")
        time.sleep(sleep_time)
        counter += 1
        
        # 每爬取60次暂停5分钟
        if counter % 100 == 0:
            logging.info(f"已爬取50次，暂停10分钟...")
            time.sleep(300)
        
        # 每次成功爬取后保存状态
        save_state(counter, note_main)

    except Exception as e:
        logging.error(f"爬取第 {counter + 1} 条数据时遇到错误: {str(e)}")
        logging.info("可能需要人工处理滑块验证。请手动处理后按Enter键继续...")
        input()
        # 出错后重试当前链接
        logging.info(f"重试第 {counter + 1} 条数据")
        continue

logging.info("爬取完成，开始保存数据到Excel")

try:
    """插入表格"""
    df = pd.read_excel(excel_path)
    new_names = ['收藏数','评论数','正文','标签','发布时间','IP','评论']
    new_data_df = pd.DataFrame(note_main, columns=new_names)
    logging.info(f"新爬取的数据数量: {len(new_data_df)}")
    result_df = pd.concat([df, new_data_df], axis=1)
    result_df['收藏数'] = result_df['收藏数'].astype(str).apply(convert_count_to_int)
    result_df['评论数'] = result_df['评论数'].astype(str).apply(convert_count_to_int)
    result_df.to_excel(excel_path, index=False)
    auto_resize_column(excel_path)
    logging.info(f"数据已成功保存到Excel文件，总行数: {len(result_df)}")
except Exception as e:
    logging.error(f"保存数据到Excel时出错: {str(e)}")

# 删除状态文件
try:
    os.remove('crawler_state.pkl')
    logging.info("爬取完成，已删除状态文件")
except Exception as e:
    logging.error(f"删除状态文件时出错: {str(e)}")