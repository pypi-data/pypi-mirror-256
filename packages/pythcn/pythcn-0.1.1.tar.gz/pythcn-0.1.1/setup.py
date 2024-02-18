import setuptools

with open("README.md","r",encoding="utf-8") as f:
    README=f.read()

setuptools.setup(
    name='pythcn',
    version='0.1.1',
    author='Jianrui Li',
    author_email='lijianrui7560@qq.com',
    description='Python中文式编程——Pythcn，简称pycn',
    long_description_content_type="text/markdown",
    long_description=README,
    url='https://github.com/',
    packages=setuptools.find_packages(),
    classifiers= [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent" ,
    ],
)
