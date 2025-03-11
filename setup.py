from setuptools import setup

with open("README.md") as f:
    doc = f.read()

setup(
    name="btcorerpc",
    description="Simple Bitcoin Core RPC wrapper",
    long_description=doc,
    long_description_content_type="text/markdown",
    author="Joel Torres",
    author_email="jt@joeltorres.org",
    url="https://github.com/joetor5/btcorerpc",
    license="MIT",
    platforms="any",
    install_requires=[
        "requests==2.32.3"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
    ]
)
