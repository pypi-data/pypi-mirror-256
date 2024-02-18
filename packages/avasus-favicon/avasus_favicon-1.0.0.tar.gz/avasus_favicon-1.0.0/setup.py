import sys
from setuptools import setup, find_packages

version = "1.0.0"
if len(sys.argv) >= 3 and sys.argv[1] == "validate_tag":
    if sys.argv[2] != version:
        raise Exception(
            f"A versão TAG [{sys.argv[2]}] é diferente da versão no arquivo setup.py [{version}]."
        )
    exit()

setup(
    **dict(
        version=version,
        name="avasus_favicon",
        description="Favicon do AVASUS",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        license="Apache-2.0",
        author="Kelson da Costa Medeiros",
        author_email="kelson.medeiros@lais.huol.ufrn.br",
        download_url=f"https://github.com/lais-huol/avasus_favicon/releases/tag/{version}",
        url="https://github.com/lais-huol/avasus_favicon",
        keywords=["favicon", "AVASUS"],
        python_requires=">=3.0",
        packages=find_packages(),
        include_package_data=True,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.0",
            "Programming Language :: Python :: 3.1",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    )
)
