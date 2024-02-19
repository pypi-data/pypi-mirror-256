from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_desc = f.read()

setup(
    name='decisiontree_lite',
    version='0.0.2',
    author='Harisiva R G',
    author_email='harisivarg@gmail.com',
    description='A custom implementation of decision tree classifier.',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url='https://github.com/Harisiva-rg/decisiontree_lite',
    packages=find_packages(),
    install_requires=["numpy", "scikit-learn", "pandas"], 
    license="MIT",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",

)
