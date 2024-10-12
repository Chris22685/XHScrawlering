import logging
from tqdm import tqdm
import pandas as pd
from def_basic import *
from def_run import *
from urllib.parse import quote

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_note_info(section):
    """从section中提取笔记信息"""
    try:
        note_link = section.ele('tag:a', timeout=0).link
        footer = section.ele('.footer', timeout=0.2)
        title = footer.ele('.title', timeout=0.2).text or "空标题"
        like = footer.ele('.like-wrapper like-active').text
        return [title, note_link, like]
    except ElementNotFoundError as e:
        logger.warning(f"提取笔记信息时出错: {str(e)}")
        return None

def scrape_author_notes(author_link, times):
    """抓取作者笔记数据"""
    logger.info(f"开始抓取作者笔记，链接：{author_link}")
    note_page = ChromiumPage()
    note_page.get(author_link)
    contents = []

    for i in tqdm(range(1, times + 1), desc="抓取进度"):
        container = note_page.ele('.feeds-container')
        sections = container.eles('.note-item')
        
        for section in sections:
            note_info = get_note_info(section)
            if note_info:
                contents.append(note_info)
        
        page_scroll_down(note_page)
        logger.info(f"完成第 {i} 次翻页，当前获取 {len(contents)} 条笔记")

    return contents

def process_data(contents):
    """处理和保存数据"""
    name = ['标题', '笔记链接', '点赞数']
    df = pd.DataFrame(columns=name, data=contents)
    
    df['点赞数'] = df['点赞数'].apply(convert_count_to_int)
    df = df.drop_duplicates()
    df = df.sort_values(by='点赞数', ascending=False)
    
    return df

def save_to_excel(df, file_path):
    """保存数据到Excel"""
    df.to_excel(file_path, index=False)
    auto_resize_column(file_path)
    logger.info(f"数据已保存到 {file_path}")

if __name__ == '__main__':
    author_link = "https://www.xiaohongshu.com/user/profile/62063c900000000021021710"
    times = 2
    excel_path = '/Users/cris/Documents/Project/Find_Coder/actual/XHScrawler/result.xlsx'

    try:
        contents = scrape_author_notes(author_link, times)
        df = process_data(contents)
        save_to_excel(df, excel_path)
        logger.info("爬取任务完成")
    except Exception as e:
        logger.error(f"爬取过程中出现错误: {str(e)}")