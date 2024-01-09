"""
@Author  ：dlfrozen
@Date    ：2024/1/6 13:35
生成pdf文件
"""
import os

# from fpdf import FPDF
import re
# from docx import Document
# from docx2pdf import convert
import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from multiprocessing import Pool

# 定义样式
styles = getSampleStyleSheet()
# 在样式中使用刚刚加载的中文字体
# 请替换成你实际的中文 TrueType 字体文件路径
chinese_font_path = 'C:\Windows\Fonts\simsun.ttc'
pdfmetrics.registerFont(TTFont('Chinese', chinese_font_path))
styles.add(ParagraphStyle(name='ChineseTitle', parent=styles['Heading1'], fontName='Chinese'))
styles.add(ParagraphStyle(name='ChineseBodyText', parent=styles['BodyText'], fontName='Chinese'))
styles.add(ParagraphStyle(name='ChineseTitle2', parent=styles['Heading2'], fontName='Chinese'))



# class PDFWithHeader(FPDF):
#     def header(self):
#         self.set_font('Arial', 'B', 16)
#         # self.cell(0, 10, 'My PDF Document', 0, 1, 'C')
#
#     def footer(self):
#         self.set_y(-15)
#         self.set_font('Arial', 'I', 8)
#         self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')
#
#
# def generate_pdf(file_path, title, content):
#     pdf = PDFWithHeader()
#     pdf.add_page()
#
#     # 设置标题字体和大小
#     pdf.set_font("Arial", 'B', 16)
#     pdf.cell(0, 10, title, 0, 1, 'C')
#
#     # 设置正文字体和大小
#     pdf.set_font("Arial", size=12)
#     pdf.cell(0, 10, txt=content, ln=True, align='L')
#
#     # 保存PDF文件
#     pdf.output(file_path)


def clean_filename(filename):
    # 使用正则表达式只保留字母、数字、下划线和连字符
    cleaned_filename = re.sub(r'[^\w\-\.]', '_', filename)

    return cleaned_filename


# data格式[[title,[text, type,zh]]]--> 格式 {title:[[text, type,zh],...]}
def mergedata(data):
    result_dict = {}

    for title, paragraph in data:
        title =title
        # 检查字典中是否已经有该类型的键
        if title in result_dict:
            # result_dict[title].append([paragraph[0], paragraph[1], paragraph[2]])
            result_dict[title].append(paragraph)
        else:
            # 如果没有该类型的键，则创建一个新的键并初始化为包含当前text的列表
            result_dict[title] = paragraph #[[paragraph[0], paragraph[1], paragraph[2]]]

    return result_dict


# 格式[[title,[text, type],zh]]
# def gen_pdf_by_fpdf(datas):
#     family ='Times'  #"Arial"
#     pdf = PDFWithHeader()
#     pdf.add_page()
#     pdf_contents = mergedata(datas)
#     for key, content in pdf_contents.items():
#         # 使用正则表达式只保留字母、数字、下划线和连字符
#         file_name = re.sub(r'[^\w\-\.]', '_', key) + ".pdf"
#         # 设置标题字体和大小
#         pdf.set_font(family, 'B', 16)
#         pdf.cell(0, 10, key, 0, 1, 'C')
#         for text, type, zh in content:
#             if type == "H3":
#                 pdf.set_font(family, 'B', 16)
#                 pdf.cell(0, 10, text, 0, 1, 'L')
#                 pdf.cell(0, 10, zh, 0, 1, 'L')
#             elif type == "H4":
#                 pdf.set_font(family, 'B', 14)
#                 pdf.cell(0, 10, text, 0, 1, 'L')
#                 pdf.cell(0, 10, zh, 0, 1, 'L')
#             elif type == "P":
#                 pdf.set_font(family, size=12)
#                 pdf.cell(0, 10, text, 0, 1, 'L')
#                 pdf.cell(0, 10, zh, 0, 1, 'L')
#
#     pdf.output("files" + os.sep + file_name)




# UnicodeEncodeError: 'latin-1' codec can't encode character '\u2019' in position 100: ordinal not in range(256)
# 用这个，上述问题没时间解决
# 格式[[title,[text, type],zh]]
# def gen_pdf_by_docx2pdf(datas):
#     family ='Times'  #"Arial"
#     # 创建Word文档
#     try:
#         pdf_contents = mergedata(datas)
#         for key, content in pdf_contents.items():
#             doc = Document()
#             # 使用正则表达式只保留字母、数字、下划线和连字符
#             file_name = re.sub(r'[^\w\-\.]', '_', key) + ".pdf"
#             docx_name = re.sub(r'[^\w\-\.]', '_', key) + ".docx"
#             # 设置标题字体和大小
#             doc.add_heading(key, level=1)
#             for text, type, zh in content:
#                 if type == "H3":
#                     doc.add_heading(text, level=2)
#                     doc.add_heading(zh, level=2)
#                 elif type == "H4":
#                     doc.add_heading(text, level=3)
#                     doc.add_heading(zh, level=3)
#                 elif type == "P":
#                     doc.add_paragraph(text)
#                     doc.add_paragraph(zh)
#             doc.save(docx_name)
#             convert(docx_name, file_name)
#             if os.path.exists(docx_name):
#                 os.remove(docx_name)
#             time.sleep(1)
#     except Exception as  e:
#         print(e)

def gen_pdf_by_reportlab(datas,pool):
    try:
        pdf_contents = mergedata(datas)
        arg_list = []
        for key, content in pdf_contents.items():
            arg_list.append((key, content))
        async_results = pool.starmap_async(gen_pdf_worker, arg_list)
        return async_results
    except Exception as e:
        print(e)
        return None

def gen_pdf_worker(key, content):
    contents = []
    # 使用正则表达式只保留字母、数字、下划线和连字符
    file_name = re.sub(r'[^\w\-\.]', '_', key) + ".pdf"
    # 创建 PDF 文档
    doc = SimpleDocTemplate(file_name, pagesize=letter)

    # 设置标题字体和大小
    # contents.append(Paragraph(key, title_style))
    # 添加空行
    contents.append(Spacer(1, 12))
    for text, type, zh in content:
        if type == "H3":
            contents.append(Paragraph(text, styles['Heading1']))
            contents.append(Paragraph(zh, styles['ChineseTitle']))
            contents.append(Spacer(1, 12))
        elif type == "H4":
            contents.append(Paragraph(text, styles['Heading2']))
            contents.append(Paragraph(zh, styles['ChineseTitle2']))
            contents.append(Spacer(1, 12))
        elif type == "P":
            contents.append(Paragraph(text, styles['BodyText']))
            contents.append(Paragraph(zh, styles['ChineseBodyText']))
    doc.build(contents)
    contents.clear()

# data_a = [['a', [
#     'I’ve used these features of Git for years across teams and projects. I’m still developing opinions around some workflows (like to squash or not) but the core tooling is powerful and flexible (and scriptable!).',
#     'H3'], '日本人呀'],
#           ['b', ['中华人名 Git logs are gross to go through out of the box.', 'H4'], '日本人呀'],
#           ['a', [
#               'Using git log gives you some information. But it’s extremely high-resolution and not usually what you’re looking for.',
#               'P'], '1'],
#           ['a', [
#               'Let’s be real. These logs aren’t impressing anyone. They are boring. And they’re full of information that you don’t really need right now. You’re trying to get a high-level understanding of what has been going on in your project.',
#               'H3'], '2'],
#           ['b', ['Wow! These are some good-looking logs! There’s even a semblance of a branched tree beside it.', 'P'],
#            '1'],
#           ['a', [
#               'These logs show you who has been working on what, when changes were made, and where your changes fit into the bigger picture.',
#               'P'], '2']]
# gen_pdf_by_reportlab(data_a)
