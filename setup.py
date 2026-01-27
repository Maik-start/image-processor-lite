"""Setup configuration for imgprocessor package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="imgprocessor",
    version="1.0.0",
    author="ImageProcessor Team",
    description="Package modulaire de traitement et d'analyse d'images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/imgprocessor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
    ],
    extras_require={
        "text_detection": [
            "easyocr>=1.6.0",
        ],
        "text_detection_tesseract": [
            "pytesseract>=0.3.10",
        ],
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/username/imgprocessor/issues",
        "Source": "https://github.com/username/imgprocessor",
    },
)
