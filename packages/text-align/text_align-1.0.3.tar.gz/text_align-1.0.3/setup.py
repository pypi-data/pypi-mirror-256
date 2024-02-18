from setuptools import setup


def readme():
    with open('README.md') as file:
        return file.read()


setup(
    name='text_align',
    version='1.0.3',
    author='Ejyou',
    author_email='ejyou.user@gmail.com',
    description='This module allows you to align text relative to the center, right, left and both sides',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Danil-114195722/TextAlign',
    packages=['text_align'],
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='text_align python',
    project_urls={},
    python_requires='>=3.7'
)
