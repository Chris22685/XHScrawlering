from def_basic import *
from def_run import *
from urllib.parse import quote

"""抓取搜索结果数据"""
if __name__ == '__main__':

    # 搜索关键词
    keyword = "三江侗寨"
    
    # 设置向下翻页爬取次数
    times = 2

    # 第1次运行需要登录，后面不用登录，可以注释掉
    # sign_in()

    # 关键词转为 url 编码
    keyword_temp_code = quote(keyword.encode('utf-8'))
    keyword_encode = quote(keyword_temp_code.encode('gb2312'))

    # 根据关键词搜索小红书文章
    search(keyword_encode)

    # 根据设置的次数，开始爬取数据
    contents = craw(times)
    # 爬到的数据保存到本地excel文件
    save_to_excel(contents)