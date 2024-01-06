"""
@Author  ：段龙
@Date    ：2024/1/6 12:56
控制中心
"""
from get_article_list import gen_top10_articles
from get_article_paragraph import get_article_paragraph
from baidu_translate import translate
from zip_files import zip_files
from gen_pdf import gen_pdf_by_reportlab


def logic_solution():
    try:
        # 存放文章-段落信息，格式[[title,[text, type]]],
        need_translate_p = []
        # 获取top10 文章信息  格式[[clapCount,mediumUrl,title]]
        top10_articles_into = gen_top10_articles("https://medium.com/?tag=software-engineering")
        print(1)
        # 分别获取这10文章的段落信息,格式[[text, type]],
        # 考虑多进程搞
        for article in top10_articles_into:
            # need_translate_p.extend([article[2], get_article_paragraph(article[1])])
            need_translate_p.append([article[2], get_article_paragraph(article[1])])
        # 翻译
        # 存放文章-段落信息，格式[[title,[text, type],zh]],
        translate_result = []
        for p in need_translate_p:
            for i in p[1]:
                translate_result.append([p[0], i, translate(i[0])])  # p格式[[title,[text, type],zh]],
        print(2)
        # 生成pdf
        gen_pdf_by_reportlab(translate_result)
        print(3)
        # 打包
        zip_files("./", zip_file_path="files/article.zip", suffix='.pdf')
        print(4)
    except Exception as e:
        print(e.args)
        return False
    return True

# logic_solution()