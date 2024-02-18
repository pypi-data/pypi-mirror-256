from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name="SimorghOCR",
    version="0.1.0",
    author="Kido Ishikawa",
    author_email="kido.ishikawa6@gmail.com",
    description="A simple OCR application using CustomTkinter, Tesseract, and EasyOCR.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KidoIshi/SimorghOCR",
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "pytesseract",
        "python-docx",
        "pdf2image",
        "easyocr",
        "numpy",
        "customtkinter"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
