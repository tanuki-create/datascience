"""pytest共通フィクスチャ。

samples/ 配下のスクリプトはファイル名が `04_classify_usage.py` のように
数字で始まり、Pythonの `import` 文で直接読み込めない(数字始まりの識別子は
不正なため)。importlib でファイルパスから直接モジュールをロードする
ヘルパーをここに置き、各テストファイルからフィクスチャとして使う。

第13章 13.7 も参照。
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SAMPLES_PYTHON_DIR = REPO_ROOT / "samples" / "python"


def load_sample_module(filename: str) -> ModuleType:
    """samples/python/<filename> を、一意なモジュール名でロードして返す。

    同名のスクリプトを複数回ロードしても、モジュールキャッシュ
    (sys.modules)により同じインスタンスが返る。
    """
    path = SAMPLES_PYTHON_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(f"sample script not found: {path}")

    module_name = f"sample_{path.stem}"
    if module_name in sys.modules:
        return sys.modules[module_name]

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load module spec: {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def load_sample():
    """テスト関数から `load_sample("04_classify_usage.py")` の形で使うフィクスチャ。"""
    return load_sample_module
