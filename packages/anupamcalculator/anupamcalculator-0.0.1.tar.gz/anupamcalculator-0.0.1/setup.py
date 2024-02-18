from setuptools import setup, find_packages
classifiers = [
    "Development Status :: 5 — Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]
setup(
    name="anupamcalculator",
    version="0.0.1",
    description="a calculator with some advanced functions",
    long_description=open("README.txt").read() + "\n\n" + open("CHANGELOG.txt").read(),
    long_description_content_type='text/plain',
    url="",
    author="anupamkumar",
    author_email="anupamkumar.nith@gmail.com",
    license="MIT",
   classifiers=[
        'Development Status :: 5 - Production/Stable',
    ],
    keywords="calculator, math, arithmetic, advanced, functions",
    packages=find_packages(),
)








