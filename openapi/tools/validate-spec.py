#!/usr/bin/env python3
"""
OpenAPI仕様書検証ツール

OpenAPI 3.x 仕様書の妥当性をチェックし、エラーがあれば報告します。
"""

import json
import yaml
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple

try:
    import jsonschema
    from jsonschema import validate, ValidationError
except ImportError:
    print("Error: jsonschema is required. Install with: pip install jsonschema")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Error: requests is required. Install with: pip install requests")
    sys.exit(1)


class OpenAPIValidator:
    """OpenAPI仕様書の検証クラス"""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_file(self, file_path: str) -> bool:
        """
        OpenAPI仕様書ファイルを検証
        
        Args:
            file_path: 検証するファイルのパス
            
        Returns:
            bool: 検証が成功した場合True
        """
        try:
            # ファイルの読み込み
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                    spec = yaml.safe_load(f)
                elif file_path.endswith('.json'):
                    spec = json.load(f)
                else:
                    self.errors.append(f"Unsupported file format: {file_path}")
                    return False
            
            # 基本検証
            if not self._validate_basic_structure(spec):
                return False
            
            # 詳細検証
            self._validate_paths(spec)
            self._validate_components(spec)
            self._validate_security(spec)
            
            return len(self.errors) == 0
            
        except FileNotFoundError:
            self.errors.append(f"File not found: {file_path}")
            return False
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parsing error: {e}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON parsing error: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Unexpected error: {e}")
            return False
    
    def _validate_basic_structure(self, spec: Dict[str, Any]) -> bool:
        """基本構造の検証"""
        required_fields = ['openapi', 'info', 'paths']
        
        for field in required_fields:
            if field not in spec:
                self.errors.append(f"Missing required field: {field}")
                return False
        
        # OpenAPIバージョンの検証
        openapi_version = spec.get('openapi', '')
        if not openapi_version.startswith('3.'):
            self.errors.append(f"Unsupported OpenAPI version: {openapi_version}")
            return False
        
        # info フィールドの検証
        info = spec.get('info', {})
        if 'title' not in info:
            self.errors.append("Missing required field: info.title")
        if 'version' not in info:
            self.errors.append("Missing required field: info.version")
        
        return True
    
    def _validate_paths(self, spec: Dict[str, Any]):
        """paths セクションの検証"""
        paths = spec.get('paths', {})
        
        if not paths:
            self.warnings.append("No paths defined")
            return
        
        for path, path_item in paths.items():
            if not path.startswith('/'):
                self.errors.append(f"Path must start with '/': {path}")
            
            # HTTPメソッドの検証
            http_methods = ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']
            for method in http_methods:
                if method in path_item:
                    operation = path_item[method]
                    self._validate_operation(operation, path, method)
    
    def _validate_operation(self, operation: Dict[str, Any], path: str, method: str):
        """個別のオペレーションの検証"""
        # 必須フィールドの検証
        if 'responses' not in operation:
            self.errors.append(f"Missing responses in {method.upper()} {path}")
        
        # レスポンスの検証
        responses = operation.get('responses', {})
        if '200' not in responses and '201' not in responses:
            self.warnings.append(f"No success response defined for {method.upper()} {path}")
        
        # リクエストボディの検証
        if 'requestBody' in operation:
            request_body = operation['requestBody']
            if 'content' not in request_body:
                self.errors.append(f"Missing content in requestBody for {method.upper()} {path}")
    
    def _validate_components(self, spec: Dict[str, Any]):
        """components セクションの検証"""
        components = spec.get('components', {})
        
        # schemas の検証
        schemas = components.get('schemas', {})
        for schema_name, schema in schemas.items():
            self._validate_schema(schema, schema_name)
        
        # securitySchemes の検証
        security_schemes = components.get('securitySchemes', {})
        for scheme_name, scheme in security_schemes.items():
            self._validate_security_scheme(scheme, scheme_name)
    
    def _validate_schema(self, schema: Dict[str, Any], schema_name: str):
        """スキーマの検証"""
        if 'type' not in schema:
            self.warnings.append(f"Schema '{schema_name}' missing type field")
        
        # 参照の検証
        if '$ref' in schema:
            ref = schema['$ref']
            if not ref.startswith('#/'):
                self.errors.append(f"Invalid reference format in schema '{schema_name}': {ref}")
    
    def _validate_security_scheme(self, scheme: Dict[str, Any], scheme_name: str):
        """セキュリティスキームの検証"""
        if 'type' not in scheme:
            self.errors.append(f"Security scheme '{scheme_name}' missing type field")
        
        scheme_type = scheme.get('type', '')
        if scheme_type == 'http':
            if 'scheme' not in scheme:
                self.errors.append(f"HTTP security scheme '{scheme_name}' missing scheme field")
        elif scheme_type == 'oauth2':
            if 'flows' not in scheme:
                self.errors.append(f"OAuth2 security scheme '{scheme_name}' missing flows field")
    
    def _validate_security(self, spec: Dict[str, Any]):
        """セキュリティ設定の検証"""
        security = spec.get('security', [])
        security_schemes = spec.get('components', {}).get('securitySchemes', {})
        
        for security_item in security:
            for scheme_name in security_item.keys():
                if scheme_name not in security_schemes:
                    self.errors.append(f"Security scheme '{scheme_name}' not defined in components.securitySchemes")
    
    def print_results(self):
        """検証結果の表示"""
        if self.errors:
            print("❌ Errors found:")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print("⚠️  Warnings:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors and not self.warnings:
            print("✅ No issues found!")
        elif not self.errors:
            print("✅ Validation passed with warnings")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='Validate OpenAPI specification files')
    parser.add_argument('files', nargs='+', help='OpenAPI specification files to validate')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    validator = OpenAPIValidator()
    all_valid = True
    
    for file_path in args.files:
        print(f"\n🔍 Validating: {file_path}")
        print("-" * 50)
        
        if not Path(file_path).exists():
            print(f"❌ File not found: {file_path}")
            all_valid = False
            continue
        
        if validator.validate_file(file_path):
            print("✅ Validation passed")
        else:
            print("❌ Validation failed")
            all_valid = False
        
        validator.print_results()
    
    if all_valid:
        print("\n🎉 All files validated successfully!")
        sys.exit(0)
    else:
        print("\n💥 Some files failed validation!")
        sys.exit(1)


if __name__ == '__main__':
    main()
