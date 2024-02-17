from setuptools import setup, find_packages

setup(
    name='aparat_crawler',
    version='0.1',
    packages=find_packages(),
    author='Mohammad Amin Orojloo',
    author_email='ma.orojloo@gmail.com',
    description='this is an aparat crawler library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/maorojloo/aparat_crawler',
    install_requires=[
        'beautifulsoup4==4.12.3',
        'certifi==2024.2.2',
        'charset-normalizer==3.3.2',
        'idna==3.6',
        'persian==0.5.0',
        'requests==2.31.0',
        'soupsieve==2.5',
        'urllib3==2.2.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
)
