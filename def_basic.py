import openpyxl
from DrissionPage.errors import ElementNotFoundError
import random
import time


'''读取文章信息函数'''
def get_info(page, contents):
    # 定位包含笔记信息的sections
    container = page.ele('.feeds-page')
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

'''下滑页面函数'''
def page_scroll_down(page):
    print("********下滑页面********")
    # 生成一个随机时间
    random_time = random.uniform(0.5, 1.5)
    # 暂停
    time.sleep(random_time)
    # time.sleep(1)
    # page.scroll.down(5000)
    page.scroll.to_bottom()

'''整理Excel表格函数'''
def auto_resize_column(excel_path):
    """自适应列宽度"""
    wb = openpyxl.load_workbook(excel_path)
    worksheet = wb.active
    # 循环遍历工作表中的1-2列
    for col in worksheet.iter_cols(min_col=1, max_col=2):
        max_length = 0
        # 列名称
        column = col[0].column_letter
        # 循环遍历列中的所有单元格
        for cell in col:
            try:
                # 如果当前单元格的值长度大于max_length，则更新 max_length 的值
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        # 计算调整后的列宽度
        adjusted_width = (max_length + 2) * 2
        # 使用 worksheet.column_dimensions 属性设置列宽度
        worksheet.column_dimensions[column].width = adjusted_width

        # 循环遍历工作表中的3-5列
        for col in worksheet.iter_cols(min_col=3, max_col=5):
            max_length = 0
            column = col[0].column_letter  # Get the column name

            # 使用 worksheet.column_dimensions 属性设置列宽度
            worksheet.column_dimensions[column].width = 15

    wb.save(excel_path)

"""将'1.6万'格式的点赞量转换为整数"""
def convert_like_to_int(like_str):
    if '万' in like_str:
        # 去掉 '万'，将字符串转换为浮点数并乘以 10000
        like_str = like_str.replace('万','')
        return int(float(like_str) * 10000)
    try:
        # 尝试将字符串直接转换为整数
        return int(like_str)
    except ValueError:
        # 如果转换失败，返回 0 作为默认值
        return 0