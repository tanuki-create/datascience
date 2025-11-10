#!/usr/bin/env python3
"""
PDFからテキストを抽出するスクリプト（2025年11月最新版）

使用方法:
    python extract_pdf_text.py <pdf_file_path> [output_file]

依存ライブラリ:
    pip install pdfplumber pymupdf
"""

import sys
import os
from pathlib import Path

def extract_with_pdfplumber(pdf_path):
    """pdfplumberを使用してテキストを抽出"""
    try:
        import pdfplumber
        
        print(f"pdfplumberを使用して抽出中: {pdf_path}")
        text_content = []
        
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"総ページ数: {total_pages}")
            
            for i, page in enumerate(pdf.pages, 1):
                print(f"ページ {i}/{total_pages} を処理中...", end='\r')
                text = page.extract_text()
                if text:
                    text_content.append(f"\n{'='*80}\nページ {i}\n{'='*80}\n{text}\n")
            
            print(f"\n完了: {total_pages}ページを処理しました")
        
        return '\n'.join(text_content)
    
    except ImportError:
        print("pdfplumberがインストールされていません。")
        print("インストール: pip install pdfplumber")
        return None
    except Exception as e:
        print(f"pdfplumberでの抽出中にエラーが発生しました: {e}")
        return None

def extract_with_pymupdf(pdf_path):
    """PyMuPDF (fitz)を使用してテキストを抽出"""
    try:
        import fitz  # PyMuPDF
        
        print(f"PyMuPDFを使用して抽出中: {pdf_path}")
        text_content = []
        
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        print(f"総ページ数: {total_pages}")
        
        for page_num in range(total_pages):
            print(f"ページ {page_num + 1}/{total_pages} を処理中...", end='\r')
            page = doc[page_num]
            text = page.get_text()
            if text:
                text_content.append(f"\n{'='*80}\nページ {page_num + 1}\n{'='*80}\n{text}\n")
        
        doc.close()
        print(f"\n完了: {total_pages}ページを処理しました")
        
        return '\n'.join(text_content)
    
    except ImportError:
        print("PyMuPDFがインストールされていません。")
        print("インストール: pip install pymupdf")
        return None
    except Exception as e:
        print(f"PyMuPDFでの抽出中にエラーが発生しました: {e}")
        return None

def extract_with_pypdf2(pdf_path):
    """PyPDF2を使用してテキストを抽出（フォールバック）"""
    try:
        import PyPDF2
        
        print(f"PyPDF2を使用して抽出中: {pdf_path}")
        text_content = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            print(f"総ページ数: {total_pages}")
            
            for i, page in enumerate(pdf_reader.pages, 1):
                print(f"ページ {i}/{total_pages} を処理中...", end='\r')
                text = page.extract_text()
                if text:
                    text_content.append(f"\n{'='*80}\nページ {i}\n{'='*80}\n{text}\n")
            
            print(f"\n完了: {total_pages}ページを処理しました")
        
        return '\n'.join(text_content)
    
    except ImportError:
        print("PyPDF2がインストールされていません。")
        return None
    except Exception as e:
        print(f"PyPDF2での抽出中にエラーが発生しました: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("使用方法: python extract_pdf_text.py <pdf_file_path> [output_file]")
        sys.exit(1)
    
    pdf_path = Path(sys.argv[1])
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not pdf_path.exists():
        print(f"エラー: ファイルが見つかりません: {pdf_path}")
        sys.exit(1)
    
    if not pdf_path.suffix.lower() == '.pdf':
        print(f"警告: PDFファイルではない可能性があります: {pdf_path}")
    
    # 優先順位: pdfplumber > PyMuPDF > PyPDF2
    text = None
    
    # 1. pdfplumberを試す
    text = extract_with_pdfplumber(pdf_path)
    
    # 2. PyMuPDFを試す
    if not text:
        text = extract_with_pymupdf(pdf_path)
    
    # 3. PyPDF2を試す（フォールバック）
    if not text:
        text = extract_with_pypdf2(pdf_path)
    
    if not text:
        print("エラー: テキストの抽出に失敗しました。")
        print("以下のいずれかをインストールしてください:")
        print("  pip install pdfplumber")
        print("  pip install pymupdf")
        print("  pip install PyPDF2")
        sys.exit(1)
    
    # 出力
    if output_file:
        output_path = Path(output_file)
        output_path.write_text(text, encoding='utf-8')
        print(f"\nテキストを保存しました: {output_path}")
        print(f"ファイルサイズ: {len(text)} 文字")
    else:
        # 標準出力に出力
        print("\n" + "="*80)
        print("抽出されたテキスト:")
        print("="*80)
        print(text)
    
    return text

if __name__ == '__main__':
    main()

