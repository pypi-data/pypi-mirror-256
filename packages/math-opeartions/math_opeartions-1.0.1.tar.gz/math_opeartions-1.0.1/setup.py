from setuptools import setup, find_packages


# Setting up
setup(
    name="math_opeartions",
    version='1.0.1',
    author="Deana Kola",
    author_email="<mail@gmail.com>",
    description='A package for math operations',
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=[ 'math_opetations', 'addition', 'multiplication', 'substraction', 'division'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)