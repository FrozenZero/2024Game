"""
@Author  ：段龙
@Date    ：2024/1/6 15:21
界面
"""
import streamlit as st


def generate_and_download():
    # 生成文件并保存在服务器路径

    # 在这里添加生成数据的代码
    from logic_core import logic_solution
    result = logic_solution()
    if result:
        server_file_path = "D:\ml\source\duan\cio_task\spider\\utils\\files\article.zip"
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


def main():
    st.title("Streamlit Generate and Download Example")

    # 添加生成按钮
    if st.button("生成"):
        generate_and_download()


if __name__ == "__main__":
    main()
