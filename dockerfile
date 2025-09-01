FROM ubuntu:22.04
#FROM python:3.10

#设置时区
RUN echo "Asia/Shanghai" > /etc/timezone

# 使用国内镜像源
# change the system source for installing libs
RUN sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list
RUN sed -i s/security.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list
RUN echo "Use aliyun source for installing libs"

# 安装 Python 3.10 和相关依赖
RUN apt-get update && apt-get install -y python3.10 python3.10-dev python3-pip
# 安装wget
RUN apt-get install -y wget

# 设置环境变量
ENV PYTHONPATH=/usr/lib/python3.10

# 安装jdk安装包
RUN apt-get install -y openjdk-11-jdk

# 安装git
RUN apt-get install -y git

# 克隆代码
RUN git clone https://gitlink.org.cn/floraachy/uiautotest_playwright.git


# 设置工作目录
WORKDIR /uiautotest_playwright

# 修改测试账号密码  关键字：****autotest-test****
RUN sed -i "s/\*\*\*\*autotest-test\*\*\*\*/你的测试账号的密码/g" config/settings.py

# 安装pipenv
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pipenv

# 安装依赖
RUN pipenv install --python 3.10 --skip-lock

# 安装浏览器驱动
RUN pipenv run playwright install
RUN pipenv run playwright install-deps


# 运行自动化测试
CMD ["pipenv", "run", "python", "run.py"]
