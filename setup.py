from setuptools import setup, find_packages

setup(
    name="skl_mindforge",
    version="0.1.3",  # BUMP TO 0.1.3
    packages=find_packages(),
    install_requires=[
        "tokenizers>=0.13.0",
    ],
    include_package_data=True,
    package_data={
        "skl_mindforge": ["*.json"],
    },
    author="SKLMindforge",
    description="Zenith Tokenizer with Ultra-Refined Decoder",
    url="https://github.com/SKLMindforge/skl_mindforge",
)
