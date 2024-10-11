from def_basic import *
from def_run import *
from urllib.parse import quote

"""抓取作者笔记数据"""
if __name__ == '__main__':
    # 作者链接
    author_link = "https://www.xiaohongshu.com/user/profile/62063c900000000021021710"
    # 设置向下翻页爬取次数
    times = 20

    """读取作者页面"""
    note_page = ChromiumPage()
    note_page.get(author_link)
    contents = []
    for i in tqdm(range(1, times + 1)):
        # get_info(note_page, contents)
        # 定位包含笔记信息的sections
        container = note_page.ele('.feeds-container')
        sections = container.eles('.note-item')
        for section in sections:
            # 定位文章链接
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
            # 定位点赞
            like = footer.ele('.like-wrapper like-active').text
            # 将获取到的信息添加到 contents 列表
            contents.append([title,  note_link, like])
        page_scroll_down(note_page)

    name = ['标题',  '笔记链接', '点赞数']
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