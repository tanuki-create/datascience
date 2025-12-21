#!/usr/bin/env python3
"""
PDFからテキストを抽出するスクリプト（RAG用）

rag/papers/フォルダ内の全PDFファイルをPyMuPDFで処理し、
LLM用のテキストファイルとして保存します。

使用方法:
    python extract_pdfs.py

依存ライブラリ:
    pip install pymupdf
"""

import os
from pathlib import Path
import sys

def extract_pdf_with_pymupdf(pdf_path):
    """PyMuPDF (fitz)を使用してテキストを抽出"""
    try:
        import fitz  # PyMuPDF
        
        print(f"処理中: {pdf_path.name}")
        text_content = []
        
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        for page_num in range(total_pages):
            page = doc[page_num]
            text = page.get_text()
            if text:
                text_content.append(f"\n{'='*80}\nページ {page_num + 1}\n{'='*80}\n{text}\n")
        
        doc.close()
        
        return '\n'.join(text_content)
    
    except ImportError:
        print("エラー: PyMuPDFがインストールされていません。")
        print("インストール: pip install pymupdf")
        return None
    except Exception as e:
        print(f"エラー: {pdf_path.name}の処理中にエラーが発生しました: {e}")
        return None

def main():
    # スクリプトのディレクトリを取得
    script_dir = Path(__file__).parent
    papers_dir = script_dir / "papers"
    output_dir = script_dir / "extracted"
    
    # 出力ディレクトリを作成
    output_dir.mkdir(exist_ok=True)
    
    # PDFファイルを取得
    pdf_files = list(papers_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"エラー: {papers_dir}にPDFファイルが見つかりません。")
        sys.exit(1)
    
    print(f"見つかったPDFファイル数: {len(pdf_files)}")
    print(f"出力先: {output_dir}\n")
    
    success_count = 0
    error_count = 0
    
    # 各PDFファイルを処理
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}] ", end="")
        
        text = extract_pdf_with_pymupdf(pdf_path)
        
        if text:
            # 出力ファイル名を決定（拡張子を.txtに変更）
            output_filename = pdf_path.stem + ".txt"
            output_path = output_dir / output_filename
            
            # テキストを保存
            output_path.write_text(text, encoding='utf-8')
            print(f"✓ 保存完了: {output_filename} ({len(text)} 文字)")
            success_count += 1
        else:
            print(f"✗ 抽出失敗: {pdf_path.name}")
            error_count += 1
    
    print(f"\n処理完了:")
    print(f"  成功: {success_count} ファイル")
    print(f"  失敗: {error_count} ファイル")
    print(f"  出力先: {output_dir}")

if __name__ == '__main__':
    main()

