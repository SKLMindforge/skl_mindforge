from setuptools import setup, find_packages

setup(
    name="skl_mindforge",
    version="0.1.4", 
    packages=find_packages(),
    install_requires=[
        "tokenizers>=0.13.0",
    ],
    include_package_data=True,
    package_data={
        "skl_mindforge": ["*.json"],
    },
    author="SKLMindforge",
    description="Zenith Tokenizer with Glue-Logic Decoder",
    url="https://github.com/SKLMindforge/skl_mindforge",
)
