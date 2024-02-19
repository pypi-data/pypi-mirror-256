from setuptools import setup
import setuptools

with open("README1.md", "r") as fh:
    long_description = fh.read()

setup(
    name='LiveCandles',
    version='0.0.2',
    description='API for getting live OHLC candle-stick data of Indian Stocks for free',
    author= 'Ronit Magar',
    url = 'https://github.com/ronitmagar/tradinBot/blob/main/liveOHLCFeed.py',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['OHLC feed', 'stock', 'candle stick', 'stock market'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.6',
    py_modules=['LiveCandles'],
    package_dir={'':'src'},
    install_requires = [
        'beautifulsoup4',
        'requests',
    ]
)
