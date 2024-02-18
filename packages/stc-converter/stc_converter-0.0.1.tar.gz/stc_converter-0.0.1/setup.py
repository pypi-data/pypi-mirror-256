from setuptools import setup, find_packages
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))
readme = os.path.join(here, 'README.rst')
with codecs.open(readme, 'r', 'utf-8') as file:
    long_description = "\n" + file.read()

setup(
    name='stc_converter',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "certifi",
       "charset-normalizer",
        "click",
        "colorama",
        "idna",
        "joblib",
        "nltk",
        "PyAudio",
        "regex",
        "requests",
        "SpeechRecognition",
        "tqdm",
        "typing_extensions",
        "urllib3",
    ],
    url='https://github.com/SamuelSGSouza/STC-converter.git',
    license='MIT',
    author='Samuel G Souza',
    author_email='samuels.g.desouza@gmail.com',
    description='A simple speech to command converter',
    long_description=long_description
)
