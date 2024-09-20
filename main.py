from tqdm import tqdm
from DrissionPage import ChromiumPage
from DrissionPage.errors import ElementNotFoundError
import time
import random
import pandas as pd
from urllib.parse import quote

# 登录函数
def sign_in():
    sign_in_page = ChromiumPage()
    sign_in_page.get('https://www.xiaohongshu.com')
    print("请扫码登录")
    # 第一次运行需要扫码登录
    time.sleep(20)

#122222

# 搜索函数
def search(keyword):
    global page
    page = ChromiumPage()
    page.get(f'https://www.xiaohongshu.com/search_result?keyword={keyword}&source=web_search_result_notes')

# 获取笔记信息函数
def get_info():
    # 定位包含笔记信息的sections
    container = page.ele('.feeds-page')
    sections = container.eles('.note-item')
    for section in sections:
        try:
            note_link = section.ele('tag:a', timeout=0).link
        except ElementNotFoundError:
            print("文章链接元素未找到。跳过当前循环...")
            continue

        # 定位标题
        footer = section.ele('.footer', timeout=0.2)
        title = "空标题"
        try:
            title = footer.ele('.title', timeout=0.2).text
            if not title:  # 如果标题为空，跳过当前循环
                title = "空标题"
        except ElementNotFoundError:
            print("Title element not found. Skipping...")
            title = "空标题"
        # 定位作者
        author_wrapper = footer.ele('.author-wrapper')
        author = author_wrapper.ele('.author').text
 # 定位作者主页地址
        author_link = author_wrapper.ele('tag:a', timeout=0).link
        # 定位作者头像
        author_img = author_wrapper.ele('tag:img', timeout=0).link
        # 定位点赞
        like = footer.ele('.like-wrapper like-active').text
        # 将获取到的信息添加到 contents 列表
        contents.append([title, author, note_link, author_link, author_img, like])

# 下滑页面函数
def page_scroll_down():
    print("********下滑页面********")
    # 生成一个随机时间
    random_time = random.uniform(0.5, 1.5)
    # 暂停
    time.sleep(random_time)
    # time.sleep(1)
    # page.scroll.down(5000)
    page.scroll.to_bottom()

# 爬取函数
def craw(times):
    for i in tqdm(range(1, times + 1)):
        get_info()
        page_scroll_down()

# 保存数据到excel文件
def save_to_excel(contents):
    # 创建一个 DataFrame 来存储数据
    name = ['title', 'author', 'note_link', 'author_link', 'author_img', 'like']
    df =pd.DataFrame(columns=name, data=contents)

    # 数据类型转换，将点赞量字符串类型转为 int 类型
    df['like'] = df['like'].astype(int)
    # 删除重复行
    df = df.drop_duplicates()
    # 按点赞量降序排序
    df = df.sort_values(by='like', ascending=False)

    # 保存为 文件
    df.to_excel('/Users/cris/Documents/Project/Find_Coder/actual/XHScrawler/result.xlsx', index=False)


if __name__ == '__main__':
    # contents列表用来存放所有爬取到的信息
    contents = []

    # 搜索关键词
    keyword = "广西三江"
    # 设置向下翻页爬取次数
    times = 1

    # 第1次运行需要登录，后面不用登录，可以注释掉
    # sign_in()

    # 关键词转为 url 编码
    keyword_temp_code = quote(keyword.encode('utf-8'))
    keyword_encode = quote(keyword_temp_code.encode('gb2312'))

    # 根据关键词搜索小红书文章
    search(keyword_encode)

    # 根据设置的次数，开始爬取数据
    craw(times)

    # 爬到的数据保存到本地excel文件
    save_to_excel(contents)