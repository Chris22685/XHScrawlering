import logging
from urllib.parse import quote
from def_basic import *
from def_run import *

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def encode_keyword(keyword):
    """将关键词转为URL编码"""
    try:
        keyword_temp_code = quote(keyword.encode('utf-8'))
        keyword_encode = quote(keyword_temp_code.encode('gb2312'))
        return keyword_encode
    except Exception as e:
        logger.error(f"关键词编码失败: {str(e)}")
        raise

def scrape_search_results(keyword, times):
    """抓取搜索结果数据"""
    try:
        logger.info(f"开始抓取关键词 '{keyword}' 的搜索结果")
        
        # 编码关键词
        keyword_encode = encode_keyword(keyword)
        logger.info(f"关键词编码完成: {keyword_encode}")
        
        # 搜索小红书文章
        search(keyword_encode)
        logger.info("搜索页面加载完成")
        
        # 爬取数据
        contents = craw(times)
        logger.info(f"爬取完成,共获取 {len(contents)} 条数据")
        
        return contents
    except Exception as e:
        logger.error(f"爬取过程中出现错误: {str(e)}")
        raise

if __name__ == '__main__':
    # 配置参数
    keyword = "三亚万宁"
    times = 3
    
    try:
        # 第1次运行需要登录，后面不用登录，可以取消下面这行的注释
        # sign_in()
        
        # 抓取数据
        contents = scrape_search_results(keyword, times)
        
        # 保存数据
        save_to_excel(contents)
        logger.info("数据已保存到Excel文件")
        
        logger.info("爬取任务完成")
    except Exception as e:
        logger.error(f"程序执行过程中出现错误: {str(e)}")