"""
@Author  ：段龙
@Date    ：2024/1/9 20:25 
"""
from tts.duan_tts_service import get_model,generate_and_save_tts
import re,sys
# sys.path.append("D:\ml\source\duan\game2024\spider\\utils\parallel_process\\tts\\")


# data格式[[title,[text, type,zh]]]--> 格式 {[title:[zh]]}
def mergedata(data):
    result_dict = {}

    for title, paragraph in data:
        title =title
        # 检查字典中是否已经有该类型的键,这里只收集中文
        if title in result_dict:
            tmp = []
            for p in paragraph:
                tmp.append(p[2])
            result_dict[title].append(tmp)
        else:
            # 如果没有该类型的键，则创建一个新的键并初始化为包含当前text的列表
            tmp =[]
            for p in paragraph:
                tmp.append(p[2])
            result_dict[title] = tmp

    return result_dict


# def gen_tts(datas,pool,path):# 扛不住,roducer process has been terminated before all shared CUDA tensors released. See Note [Sharing CUDA tensors]
#     try:
#         tts_contents = mergedata(datas)
#         print(len(tts_contents))
#         model = get_model()
#         arg_list = []
#         for key, content in tts_contents.items():
#             file_name = re.sub(r'[^\w\-\.]', '_', key) + ".wav"
#             # 构建文件的绝对路径
#             file_name = path.join(file_name)
#             arg_list.append(( content,file_name,model))
#         async_results = pool.starmap_async(generate_and_save_tts, arg_list)
#         return async_results
#     except Exception as e:
#         print(e)
#         return None

def gen_tts(datas,fpath):
    try:
        tts_contents = mergedata(datas)
        print(len(tts_contents))
        model = get_model()
        for key, content in tts_contents.items():
            file_name = re.sub(r'[^\w\-\.]', '_', key) + ".wav"
            # 构建文件的绝对路径
            file_name = fpath+file_name
            generate_and_save_tts("".join(content),file_name,model)
        return True
    except Exception as e:
        print(e)
        return False
