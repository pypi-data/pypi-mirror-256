import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="huehush",
    version="0.0.1",
    author="Aravind.M.S",
    author_email="aravind19112003@gmail.com",
    packages=["huehush"],
    description="huehush is a Python module that provides functionality to segment images into distinct clusters using the K-means clustering algorithm. This module is useful for tasks such as image segmentation, color quantization, and image compression.",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/avd1729/hue-hush",
    license='Apache License 2.0',
    python_requires='>=3.8',
    install_requires=[
            'numpy',
            'matplotlib',
            'scikit-learn',
            'Pillow'
    ]
)
