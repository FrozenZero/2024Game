"""
@Author  ：段龙
@Date    ：2024/1/6 15:21
界面
"""
import streamlit as st
from multiprocessing import Pool
from get_article_list import gen_top10_articles
from get_article_paragraph import get_article_paragraph,get_article_paragraphs
from baidu_translate import translate
from zip_files import zip_files
from gen_pdf import gen_pdf_by_reportlab
import multiprocessing
from multiprocessing import Process, Queue ,Manager
import threading
import os
def translate_consumer(queue,article_paragraph_arg):
    while True:
        # 从队列中获取数据
        data = queue.get()
        if data is None:
            break  # 结束消费
        for i in data:
            tmp =[]
            for d in i[1]:
                tmp.append([d[0],d[1],translate(d[0])])
            article_paragraph_arg.append([i[0],tmp])


def worker():
    try:
        top10_articles_info=[]
        with Pool(processes=4) as pool:
            # 获取top10 文章信息  格式[[clapCount,mediumUrl,title]]
            top10_articles_info = gen_top10_articles(pool)
        result_queue = Queue()
        # 创建一个Manager用于共享数据
        with Manager() as manager:
            # 创建一个共享的list，用于存放消费者处理的结果
            shared_result_list = manager.list()
            # 创建一个进程池，可以指定进程数量
            with multiprocessing.Pool(processes=4) as pool:
                article_paragraph_arg = []
                for article in top10_articles_info:
                    article_paragraph_arg.append((article[2], article[1]))
                # [364, 'https://medium.com/@techsuneel99/design-patterns-in-node-js-31211904903e', 'Design Patterns in Node.js']
                # 获取文章的段落信息，使用map_async函数并行调用函数get_article_paragraph，并将结果放入队列,队列格式[article,[[text, type]]]
                async_results = get_article_paragraphs(pool, article_paragraph_arg, result_queue)
                num_consumers = 2
                consumers = [Process(target=translate_consumer, args=(result_queue,shared_result_list)) for _ in
                             range(num_consumers)]
                # 启动消费者进程
                for consumer in consumers:
                    consumer.start()

                # 等待所有进程执行完毕
                pool.close()
                pool.join()

                # 等待队列中的结果全部被消费
                for _ in range(num_consumers):
                    result_queue.put(None)  # 发送终止信号
                for consumer in consumers:
                    consumer.join()

                # 等get_article_paragraph执行完
                tmp = async_results.get()
                translate_result = list(shared_result_list)
                # 生成pdf
                gen_pdf_by_reportlab(translate_result)
                # 打包
                script_dir = os.path.dirname(os.path.realpath(__file__))
                # 构建文件的绝对路径
                zip_files(script_dir, zip_file_path= os.path.join(script_dir, "files/article.zip"), suffix='.pdf')
                # zip_files("./", zip_file_path="files/article.zip", suffix='.pdf')
                thread1.return_value = True
    except Exception as e:
        print(e.args)
        thread1.return_value = False

def generate_and_download(thread1,result_event):
    # 生成文件并保存在服务器路径
    try:
        # 启动线程
        thread1.start()
        # 等待工作完成
        result_event.wait()
        result = thread1.return_value if hasattr(thread1, 'return_value') else None
        if result:
            server_file_path = "D:\ml\source\duan\cio_task\spider\\utils\\files\\article.zip"
            # 提供下载链接
            with open(server_file_path, "r") as file:
                st.download_button(
                    label="Download Generated File",
                    key="download_button",
                    file_name="generated_file.txt",
                    data=file.read(),
                    mime="text/plain",
                )
        else:
            st.text("failed process~~")
    except Exception as e:
        print(e)


def main(thread1,result_event):
    st.title("生成medium的文章压缩包，点击生成后稍等片刻，即可出现下载文件。")

    # 添加生成按钮
    if st.button("生成"):
        generate_and_download(thread1,result_event)


if __name__ == "__main__":
    # 创建一个Event对象，用于通知主线程工作完成
    result_event = threading.Event()
    thread1 = threading.Thread(target=worker, args=())
    main(thread1,result_event)
