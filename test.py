from DrissionPage import ChromiumPage



search_page = ChromiumPage()
search_page.get(f'https://www.xiaohongshu.com/search_result?keyword=%25E8%2582%2587%25E5%2585%25B4%25E4%25BE%2597%25E5%25AF%25A8&source=web_explore_feed')
container = search_page.ele('.feeds-page')
sections = container.eles('.note-item')
# note_link = sections[0].ele('tag:a', timeout=0).link

# note_link2 = sections[0].ele('a.cover.ld.mask', timeout=0).attr('href')
# note_link2 = sections[0].ele('a.cover.mask', timeout=5).attr('href')
note_link = sections[0].ele('css:.cover.ld.mask').attr('href')
print(note_link)
