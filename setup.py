from setuptools import setup, find_packages


setup(
    name="dictvalidator",
    version="0.1",
    description="Dictionary validation DSL",
    url="https://github.com/ran4/python_dict_validator",
    author_email="rasmus.ansin@gmail.com",
    packages=find_packages(),
    python_requires=">=3.6",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="validation",
)
