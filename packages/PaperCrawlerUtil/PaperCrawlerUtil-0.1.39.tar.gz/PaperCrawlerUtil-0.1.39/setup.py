# -*- coding: utf-8 -*-
# @Time    : 2022/7/3 21:38
# @Author  : 银尘
# @FileName: setup.py.py
# @Software: PyCharm
# @Email   ：liwudi@liwudi.fun
import re

import setuptools  # 导入setuptools打包工具

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)


PROJECT = "PaperCrawlerUtil"
setuptools.setup(
    name=PROJECT,  # 用自己的名替换其中的YOUR_USERNAME_
    version=get_property("__version__", PROJECT),  # 包版本号，便于维护版本
    author=get_property("__author__", PROJECT),  # 作者，可以写自己的姓名
    author_email=get_property("__email__", PROJECT),  # 作者联系方式，可写自己的邮箱地址
    description="a collection of utils",  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url=get_property("__github__", PROJECT),  # 自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(exclude=["PaperCrawlerUtil.logs"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['aiohttp==3.8.1', 'attr==0.3.1', 'attrs==20.3.0', 'beautifulsoup4==4.11.1', 'environs==9.5.0',
                      'fake_headers==1.0.2', 'fake-useragent==1.1.1', 'Flask==1.1.4', 'gevent==21.12.0',
                      'googletrans==4.0.0rc1', 'loguru==0.6.0', 'lxml==4.9.0', 'pdf2docx==0.5.4',
                      'pdfplumber==0.7.1', 'pyquery==1.4.3', 'requests==2.28.1', 'retrying==1.3.3',
                      'setuptools==61.2.0', 'tornado==6.1', 'redis==3.5.3', 'markupsafe==2.0.1', 'PyPDF2==2.4.2',
                      'tqdm==4.64.0', 'PyExecJS2==1.6.1', 'xlrd==2.0.1', 'xlwt==1.3.0', 'pymysql==1.0.2',
                      'sshtunnel==0.4.0'],
    python_requires='>=3.6',  # 对python的最低版本要求
    include_package_data=True,

)
