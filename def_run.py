from def_basic import *
from DrissionPage import ChromiumPage
import time
import pandas as pd
from tqdm import tqdm

'''登录函数'''
def sign_in():
    sign_in_page = ChromiumPage()
    sign_in_page.get('https://www.xiaohongshu.com')
    print("请扫码登录")
    # 第一次运行需要扫码登录
    time.sleep(20)


'''搜索函数'''
def search(keyword):
    global search_page
    search_page = ChromiumPage()
    search_page.get(f'https://www.xiaohongshu.com/search_result?keyword={keyword}&source=web_search_result_notes')


'''爬取搜索列表函数'''
def craw(times):
    contents = []
    for i in tqdm(range(1, times + 1)):
        get_info(search_page, contents)
        page_scroll_down(search_page)
    return contents


'''保存到excel函数'''
def save_to_excel(contents):
    # 创建一个 DataFrame 来存储数据
    name = ['标题', '作者', '笔记链接', '作者链接', '作者头像', '点赞数']
    df =pd.DataFrame(columns=name, data=contents)

    # 使用 convert_like_to_int 函数处理 'like' 列
    df['点赞数'] = df['点赞数'].apply(convert_count_to_int)
    # 删除重复行
    df = df.drop_duplicates()
    # 按点赞量降序排序
    df = df.sort_values(by='点赞数', ascending=False)

    # 保存为 文件
    df.to_excel('/Users/cris/Documents/Project/Find_Coder/actual/XHScrawler/result.xlsx', index=False)

    excel_path = '/Users/cris/Documents/Project/Find_Coder/actual/XHScrawler/result.xlsx'
    auto_resize_column(excel_path)