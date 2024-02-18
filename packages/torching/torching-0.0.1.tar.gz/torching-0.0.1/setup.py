import setuptools

import site
site.ENABLE_USER_SITE = True

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="torching",
    version="0.0.1",
    author="Khue Le",
    author_email="khue.fr@gmail.com",
    description="PyTorch Extensions and Utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/netw0rkf10w/torching.git",
    project_urls={
        "Bug Tracker": "https://github.com/netw0rkf10w/torching/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)