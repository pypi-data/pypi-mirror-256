from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='textPlay',
    version='0.1.0',
    description='A package for text manipulation and more',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/rakeshkanna-rk/textPlay',
    author='Rakesh Kanna',
    author_email='rakeshkanna0108@gmail.com',
    packages=find_packages(),
    install_requires=[
        "requests==2.26.0",
        "gTTS==2.3.2",
        "googletrans==4.0.0rc1",
        "beautifulsoup4==4.10.0",
        "qrcode==7.4.2",
        "textblob==0.17.1",
        "newspaper3k==0.2.8",
        "pyspellchecker==0.7.2",
        "spacy==3.6.1"
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'textplay = textPlay.main:main'
        ]
    }
)
