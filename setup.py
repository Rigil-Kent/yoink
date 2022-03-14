from importlib.metadata import entry_points
import setuptools



with open('README.md', 'r') as readme:
    long_description = readme.read()



setuptools.setup(
    name='yoink',
    version='0.2.0',
    author='Bryan Bailey',
    author_email='brizzledev@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/Rigil-Kent/yoink',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'yoink = yoink.cli:yoink'
        ]
    },
    install_requires=['click', 'bs4', 'requests']
)