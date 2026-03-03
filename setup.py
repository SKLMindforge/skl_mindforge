from setuptools import setup, find_packages

setup(
    name="skl_mindforge",
    version="0.1.2",  # Bumping to 0.1.2 to force the refresh
    packages=find_packages(),
    install_requires=[
        "tokenizers>=0.13.0",
    ],
    include_package_data=True,
    package_data={
        "skl_mindforge": ["*.json"],
    },
    author="Your Name",
    description="Zenith Tokenizer with built-in artifact cleaning",
    url="https://github.com/SKLMindforge/skl_mindforge",
)
