#!/usr/bin/env python3
"""
OpenAPI クライアント生成ツール

OpenAPI仕様書から各種言語のクライアントコードを自動生成します。
"""

import json
import yaml
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional


class OpenAPIClientGenerator:
    """OpenAPIクライアント生成クラス"""
    
    def __init__(self):
        self.supported_languages = {
            'python': {
                'generator': 'python',
                'package_name': 'openapi_client',
                'description': 'Python client using httpx and pydantic'
            },
            'typescript': {
                'generator': 'typescript-axios',
                'package_name': 'openapi-client',
                'description': 'TypeScript client using axios'
            },
            'javascript': {
                'generator': 'javascript',
                'package_name': 'openapi-client',
                'description': 'JavaScript client using fetch'
            },
            'java': {
                'generator': 'java',
                'package_name': 'com.example.openapi',
                'description': 'Java client using OkHttp'
            },
            'go': {
                'generator': 'go',
                'package_name': 'openapi',
                'description': 'Go client using net/http'
            },
            'csharp': {
                'generator': 'csharp',
                'package_name': 'OpenAPI.Client',
                'description': 'C# client using HttpClient'
            }
        }
    
    def generate_client(self, spec_file: str, language: str, output_dir: str, 
                       package_name: Optional[str] = None) -> bool:
        """
        クライアントコードを生成
        
        Args:
            spec_file: OpenAPI仕様書ファイル
            language: 生成する言語
            output_dir: 出力ディレクトリ
            package_name: パッケージ名（オプション）
            
        Returns:
            bool: 生成が成功した場合True
        """
        if language not in self.supported_languages:
            print(f"❌ Unsupported language: {language}")
            print(f"Supported languages: {', '.join(self.supported_languages.keys())}")
            return False
        
        # OpenAPI Generatorの確認
        if not self._check_openapi_generator():
            return False
        
        # 出力ディレクトリの作成
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 言語設定の取得
        lang_config = self.supported_languages[language]
        generator = lang_config['generator']
        
        if package_name is None:
            package_name = lang_config['package_name']
        
        # 生成コマンドの構築
        cmd = [
            'npx', '@openapitools/openapi-generator-cli', 'generate',
            '-i', spec_file,
            '-g', generator,
            '-o', str(output_path),
            '--package-name', package_name,
            '--skip-validate-spec'
        ]
        
        # 言語固有のオプション
        if language == 'python':
            cmd.extend([
                '--additional-properties', 'packageVersion=1.0.0,projectName=openapi-client'
            ])
        elif language == 'typescript':
            cmd.extend([
                '--additional-properties', 'npmName=openapi-client,npmVersion=1.0.0'
            ])
        
        print(f"🚀 Generating {language} client...")
        print(f"📁 Output directory: {output_dir}")
        print(f"📦 Package name: {package_name}")
        print(f"🔧 Generator: {generator}")
        
        try:
            # コマンド実行
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            print("✅ Client generated successfully!")
            print(f"📋 Generated files:")
            
            # 生成されたファイルの表示
            self._list_generated_files(output_path)
            
            # 次のステップの表示
            self._print_next_steps(language, output_dir)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Generation failed:")
            print(f"Error: {e.stderr}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def _check_openapi_generator(self) -> bool:
        """OpenAPI Generatorの確認"""
        try:
            result = subprocess.run(
                ['npx', '@openapitools/openapi-generator-cli', 'version'],
                capture_output=True, text=True, check=True
            )
            print(f"✅ OpenAPI Generator found: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ OpenAPI Generator not found!")
            print("Please install it with: npm install -g @openapitools/openapi-generator-cli")
            return False
    
    def _list_generated_files(self, output_path: Path):
        """生成されたファイルの一覧表示"""
        if not output_path.exists():
            return
        
        # 主要なファイルを表示
        important_files = [
            'README.md', 'package.json', 'requirements.txt', 'setup.py',
            'pom.xml', 'go.mod', '*.csproj'
        ]
        
        for pattern in important_files:
            for file_path in output_path.rglob(pattern):
                print(f"  📄 {file_path.relative_to(output_path)}")
    
    def _print_next_steps(self, language: str, output_dir: str):
        """次のステップの表示"""
        print(f"\n📚 Next steps for {language}:")
        
        if language == 'python':
            print(f"  1. cd {output_dir}")
            print("  2. pip install -r requirements.txt")
            print("  3. python -c \"import openapi_client; print('Client imported successfully!')\"")
        elif language == 'typescript':
            print(f"  1. cd {output_dir}")
            print("  2. npm install")
            print("  3. npm run build")
        elif language == 'javascript':
            print(f"  1. cd {output_dir}")
            print("  2. npm install")
            print("  3. node -e \"console.log('Client ready!')\"")
        elif language == 'java':
            print(f"  1. cd {output_dir}")
            print("  2. mvn clean install")
            print("  3. mvn exec:java -Dexec.mainClass=\"com.example.openapi.ApiClient\"")
        elif language == 'go':
            print(f"  1. cd {output_dir}")
            print("  2. go mod tidy")
            print("  3. go run main.go")
        elif language == 'csharp':
            print(f"  1. cd {output_dir}")
            print("  2. dotnet restore")
            print("  3. dotnet build")
    
    def list_languages(self):
        """サポートされている言語の一覧表示"""
        print("🌍 Supported languages:")
        for lang, config in self.supported_languages.items():
            print(f"  {lang}: {config['description']}")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='Generate OpenAPI client code')
    parser.add_argument('--spec', '-s', required=True, help='OpenAPI specification file')
    parser.add_argument('--lang', '-l', required=True, help='Target language')
    parser.add_argument('--output', '-o', required=True, help='Output directory')
    parser.add_argument('--package', '-p', help='Package name (optional)')
    parser.add_argument('--list-languages', action='store_true', help='List supported languages')
    
    args = parser.parse_args()
    
    generator = OpenAPIClientGenerator()
    
    if args.list_languages:
        generator.list_languages()
        return
    
    # 仕様書ファイルの確認
    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"❌ Specification file not found: {args.spec}")
        sys.exit(1)
    
    # クライアント生成
    success = generator.generate_client(
        spec_file=args.spec,
        language=args.lang,
        output_dir=args.output,
        package_name=args.package
    )
    
    if success:
        print("\n🎉 Client generation completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Client generation failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()
