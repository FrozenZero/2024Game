"""
@Author  ：Author  ：dlfrozen
@Date    ：2024/1/6 16:19
Gradio 动态添加Button
"""

import multiprocessing
import os
from multiprocessing import Pool
from multiprocessing import Process, Queue, Manager

import gradio as gr

from baidu_translate import translate
from gen_pdf import gen_pdf_by_reportlab
from get_article_list import gen_top10_articles
from get_article_paragraph import get_article_paragraphs
from zip_files import zip_files


def translate_consumer(queue,shared_result_list):
    while True:
        # 从队列中获取数据
        data = queue.get()
        if data is None:
            break  # 结束消费
        for i in data:
            tmp =[]
            for d in i[1]:
                tmp.append([d[0],d[1],translate(d[0])])
            shared_result_list.append([i[0],tmp])


def worker():
    try:
        # 共享状态变量
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
        with Pool(processes=4) as pool1:
            async_results1 = gen_pdf_by_reportlab(translate_result, pool1)
            # 等待所有进程执行完毕
            pool1.close()
            pool1.join()
            results = async_results1.get()
        # 打包
        print(4)
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # 构建文件的绝对路径
        print(5)
        zip_files(script_dir, zip_file_path= os.path.join(script_dir, "files/article.zip"), suffix='.pdf')
        return True
    except Exception as e:
        print(e.args)
        return False



def greet(result):
    if result:
        download_btn = [gr.Button(value="Download", visible=True,
                              link="/file=D:\\ml\\source\\duan\\game2024\\spider\\utils\\parallel_process\\files\\article.zip")]
    else:
        download_btn = [gr.Button(value="文件生成失败", visible=True)]
    unvisible_btn = [gr.Button(visible=False, value="")for _ in range(1)]
    return download_btn + unvisible_btn



def main():
    try:
        result= worker()
        download_btn = [gr.Button(value="文件生成失败", visible=True)]
        if result:
            download_btn = [gr.Button(value="Download", visible=True,
                                      link="/file=D:\\ml\\source\\duan\\game2024\\spider\\utils\\parallel_process\\files\\article.zip")]
        unvisible_btn = [gr.Button(visible=False, value="") for _ in range(1)]
        return download_btn + unvisible_btn
    except Exception as e:
        print(e)
        return [gr.Button(visible=True, value="文件生成失败") for _ in range(2)]


if __name__ == "__main__":
    btn_list = []

    with gr.Blocks() as demo:
        with gr.Row():
            for i in range(2): 
                btn = gr.Button(visible=False)
                btn_list.append(btn)
        b = gr.Button("后台生成文件")
        b.click(main, None, btn_list)

    demo.launch(share=True,allowed_paths=["D:\\ml\\source\\duan\\game2024\\spider\\utils\\parallel_process\\files\\article.zip"])
