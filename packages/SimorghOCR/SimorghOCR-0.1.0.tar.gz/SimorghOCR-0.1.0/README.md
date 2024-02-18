# SimorghOCR

SimorghOCR is an optical character recognition (OCR) application specialized in Persian language.<br>

SimorghOCRは、ペルシア語に特化した光学文字認識（OCR）アプリケーションです。

## Features
- Tesseract OCR and EasyOCR<br>
- Capable of processing both image files (JPEG, PNG, BMP, TIFF, etc.) and PDF documents<br>
- User-friendly GUI built with CustomTkinter<br>
- Language support focused on Persian (Farsi)<br>
- Direct conversion of extracted text to Microsoft Word (DOCX) format for easy editing and formatting<br>
<br>
- Tesseract OCRおよびEasyOCR<br>
- 画像ファイル（JPEG、PNG、BMP、TIFFなど）とPDFドキュメントの両方を処理可能<br>
- CustomTkinterで構築されたユーザーフレンドリーなGUI<br>
- ペルシア語（ファルシ）に焦点を当てた言語サポート<br>
- 抽出されたテキストを簡単な編集とフォーマットのためにMicrosoft Word（DOCX）形式に直接変換<br>

## Inastall
Before installing SimorghOCR, it is necessary to have Tesseract OCR pre-installed, which is one of the main OCR engines used in the application. Please download and install Tesseract OCR from [here](https://github.com/tesseract-ocr/tesseract).<br>
<br>
Once Tesseract OCR is installed, follow these steps to install SimorghOCR:<br>
<br>
SimorghOCRをインストールする前に、アプリケーションで使用される主要なOCRエンジンの1つであるTesseract OCRの事前インストールされているが必要です。[こちら](https://github.com/tesseract-ocr/tesseract)からTesseract OCRをダウンロードしてインストールしてください。<br>
<br>
Tesseract OCRがインストールされたら、以下の手順でSimorghOCRをインストールしてください：


```bash
# Clone the repository
# リポジトリをクローン
git clone https://github.com/KidoIshi/SimorghOCR.git

# Go to clone directory
# クローンしたディレクトリに移動
cd SimorghOCR

# Install necessary Python packages
# 必要なPythonパッケージをインストール
pip install -r requirements.txt
# SimorghOCR
```
Select the OCR engine<br>
Upload an image or PDF file<br>
Upon completion of OCR processing, the extracted text will be displayed in the application window and can be downloaded as a Word document<br>
<br>
OCRエンジンを選びます<br>
画像またはPDFファイルをアップロードします<br>
OCR処理が完了すると、抽出されたテキストがアプリケーションウィンドウに表示され、Wordドキュメントとしてダウンロードできます
## Licence
GNU GPL version 3
