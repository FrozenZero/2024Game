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
import multiprocessing
from multiprocessing import Process, Queue ,Manager

def translate_consumer(queue,result_list):
    while True:
        # 从队列中获取数据
        data = queue.get()
        if data is None:
            break  # 结束消费
        for i in data[1]:
            result_list.append([data[0], i, translate(i[0])])  # 格式[[title,[text, type],zh]]


def logic_solution():
    try:
        # 存放文章-段落信息，格式[[title,[text, type]]],
        need_translate_p = []
        # 获取top10 文章信息  格式[[clapCount,mediumUrl,title]]
        top10_articles_into = gen_top10_articles("https://medium.com/?tag=software-engineering")
        translate_result = []  # 格式[[title,[text, type],zh]]
        result_queue = Queue()
        # 创建一个Manager用于共享数据
        with Manager() as manager:
            # 创建一个共享的list，用于存放消费者处理的结果
            shared_result_list = manager.list()
            # 创建一个进程池，可以指定进程数量
            with multiprocessing.Pool(processes=4) as pool:
                article_paragraph_arg=[]
                for article in top10_articles_into:
                    article_paragraph_arg.append((article[2],article[1]))
                # 获取文章的段落信息，使用map_async函数并行调用函数get_article_paragraph，并将结果放入队列,队列格式[article,[[text, type]]]
                async_results = pool.map_async(get_article_paragraph, article_paragraph_arg, callback=result_queue.put)
                num_consumers = 2
                consumers = [Process(target=translate_consumer, args=(result_queue,shared_result_list)) for _ in range(num_consumers)]
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
                results_A = async_results.get()
                translate_result = shared_result_list

                # 生成pdf
                gen_pdf_by_reportlab(translate_result)
                # 打包
                zip_files("./", zip_file_path="files/article.zip", suffix='.pdf')
    except Exception as e:
        print(e.args)
        return False
    return True

