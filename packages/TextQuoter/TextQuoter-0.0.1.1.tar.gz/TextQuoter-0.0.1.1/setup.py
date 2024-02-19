from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    version="0.0.1.1",
    name="TextQuoter",
    description="TextQuoter is a versatile Python script designed to simplify the processing of quotation marks in a given string.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gr1336/TextQuoter/",
    author="gr1336",
    license="MIT License",
    classifiers=[
        "Topic :: Text Editors",
        "Topic :: Text Editors :: Text Processing",
        "Topic :: Text Editors :: Word Processors",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
