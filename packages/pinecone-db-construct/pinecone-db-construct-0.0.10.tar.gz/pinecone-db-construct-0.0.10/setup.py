import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "pinecone-db-construct",
    "version": "0.0.10",
    "description": "A CDK construct for Pinecone Indexes",
    "license": "MIT",
    "url": "https://github.com/petterle-endeavors/pinecone-db-construct",
    "long_description_content_type": "text/markdown",
    "author": "Jacob Petterle<jacobpetterle@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/petterle-endeavors/pinecone-db-construct"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "pinecone_db_construct",
        "pinecone_db_construct._jsii"
    ],
    "package_data": {
        "pinecone_db_construct._jsii": [
            "pinecone-db-construct@0.0.10.jsii.tgz"
        ],
        "pinecone_db_construct": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.118.0, <3.0.0",
        "aws-cdk.aws-lambda-python-alpha>=2.100.0.a0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.94.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
