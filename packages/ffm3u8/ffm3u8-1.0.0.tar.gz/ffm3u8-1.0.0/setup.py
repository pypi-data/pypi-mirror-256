import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ffm3u8',
    version='1.0.0',
    author='Nongyi',
    author_email='13360350080@163.com',
    description='一个简单的下载m3u8ts文件的模块',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Nong-Yi/ny.git',
    packages=setuptools.find_packages(),
    classifiers=[
        "programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT LICENSE",
        "Operating System :: win Independent",
    ],
    python_requires='>=3.6',
)

