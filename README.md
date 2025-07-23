# Logify - Advanced Python Logging System

Logify は、Python での高度なログ管理を簡単にする軽量ユーティリティです。  
JSON・CSV 両対応、フォルダ分離、非同期・同期処理をサポートした現代的なログシステムです。

---

## 目次

- [特徴](#特徴)
- [フォルダ構成](#フォルダ構成)
- [インストール](#インストール)
- [使用方法](#使用方法)
  - [基本的な使い方](#基本的な使い方)
  - [ファイル形式の指定](#ファイル形式の指定)
  - [カスタムディレクトリ](#カスタムディレクトリ)
  - [同期ログの使い方](#同期ログの使い方)
- [ファイル保存の仕組み](#ファイル保存の仕組み)
- [サンプルコード](#サンプルコード)
- [メソッドリファレンス](#メソッドリファレンス)
- [よくある質問](#よくある質問)
- [ライセンス](#ライセンス)

---

## 特徴

### 🚀 **高度な機能**

- **JSON・CSV 両対応**: 構造化データ（JSON）と Excel 対応（CSV）を選択可能
- **フォルダ分離**: `json/`と`csv/`で自動的にファイルを分類
- **非同期・同期対応**: `async/await`とブロッキング処理の両方をサポート
- **メタデータ**: タイムスタンプ、プロセス ID、ロガー名を自動記録

### 🎨 **美しいコンソール出力**

- **カラー表示**: ログレベルごとに色分けされた見やすい出力
- **Rich 対応**: Rich library による高品質なコンソール表示
- **整列表示**: ログレベルを固定幅で揃えた美しいフォーマット

### ⚡ **パフォーマンス**

- **非同期 I/O**: ファイル書き込みをノンブロッキングで実行
- **JSONL 形式**: 1 行 1JSON で高速解析が可能
- **効率的な処理**: 必要な時だけファイル書き込みを実行

---

## フォルダ構成

```
logify/
├── log.py              # LogManagerクラスの実装
├── constants.py        # 設定定数
├── requirements.txt    # 依存関係
├── README.md          # このファイル
├── example/
│   └── sample.py      # サンプルコード
└── data/              # ログデータが保存されるディレクトリ
    └── logs/
        ├── json/      # JSON形式のログファイル
        │   ├── debug.json
        │   ├── info.json
        │   ├── warning.json
        │   ├── error.json
        │   └── critical.json
        └── csv/       # CSV形式のログファイル
            ├── debug.csv
            ├── info.csv
            ├── warning.csv
            ├── error.csv
            └── critical.csv
```

---

## インストール

必要なライブラリをインストールしてください。

```zsh
pip install rich
```

---

## 使用方法

### 基本的な使い方

```python
from log import LogManager
import asyncio

async def main():
    # JSON形式がデフォルト
    log = LogManager()

    # コンソール出力とファイル保存（設定による）
    await log.debug("デバッグメッセージ")        # コンソールのみ
    await log.info("情報メッセージ")            # コンソールのみ
    await log.warning("警告メッセージ")         # コンソール + JSON保存
    await log.error("エラーメッセージ")         # コンソール + JSON保存
    await log.critical("重大エラー")           # コンソール + JSON保存

if __name__ == "__main__":
    asyncio.run(main())
```

### ファイル形式の指定

```python
# JSON形式（デフォルト）
await log.error("JSON形式で保存")

# CSV形式で保存
await log.error("CSV形式で保存", file_format="csv")

# 強制的にファイル保存（通常は保存されないレベルでも）
await log.debug("強制保存", save_file=True)
await log.info("CSV形式で強制保存", save_file=True, file_format="csv")
```

### カスタムディレクトリ

```python
# カスタムディレクトリを指定
custom_log = LogManager(log_dir="my_app/logs")
await custom_log.error("カスタムディレクトリに保存")

# CSV形式をデフォルトに設定
csv_log = LogManager(default_format="csv")
await csv_log.error("CSV形式がデフォルト")
```

### 同期ログの使い方

非同期関数外や、同期処理でログを出したい場合は `*_sync` メソッドを使います。

```python
log = LogManager()
log.info_sync("同期処理でのログ")
log.error_sync("CSV形式で同期保存", file_format="csv")
log.debug_sync("強制保存", save_file=True)
```

---

## ファイル保存の仕組み

### デフォルト保存レベル

- `debug`, `info`: コンソール出力のみ
- `warning`, `error`, `critical`: コンソール出力 + ファイル保存

### ファイル形式

- **JSON 形式（推奨）**: 構造化データで詳細情報を保存
  ```json
  {
    "timestamp": "2025-07-23T20:30:09.908454",
    "level": "ERROR",
    "message": "エラーメッセージ",
    "logger_name": "log",
    "process_id": 8729
  }
  ```
- **CSV 形式**: Excel 等で開きやすい表形式
  ```csv
  timestamp,level,message
  2025-07-23 20:30:09,ERROR,エラーメッセージ
  ```

### フォルダ構成

- `logs/json/`: JSON 形式のログファイル
- `logs/csv/`: CSV 形式のログファイル
- 各形式内でレベル別にファイル分離

---

## サンプルコード

詳細な使用例は `example/sample.py` を参照してください。

```python
from log import LogManager
import asyncio

async def main():
    # 基本的な使用方法
    log = LogManager()

    # 各ログレベルのテスト
    await log.debug("デバッグ情報")                    # コンソールのみ
    await log.info("アプリ開始")                      # コンソールのみ
    await log.warning("設定ファイルが見つかりません")    # logs/json/warning.json に保存
    await log.error("データベース接続エラー")           # logs/json/error.json に保存
    await log.critical("システム停止")                # logs/json/critical.json に保存

    # 形式を指定した保存
    await log.error("CSV形式で保存したいエラー", file_format="csv")  # logs/csv/error.csv に保存
    await log.info("JSONで強制保存", save_file=True)              # logs/json/info.json に保存

    # カスタムディレクトリの使用
    app_log = LogManager(log_dir="app_logs")
    await app_log.info("アプリケーション専用ログ", save_file=True)

    # CSV形式をデフォルトに
    csv_logger = LogManager(default_format="csv")
    await csv_logger.warning("CSVがデフォルトの警告")  # logs/csv/warning.csv に保存

# 同期処理での使用
def sync_function():
    log = LogManager()
    log.info_sync("同期処理からのログ")
    log.error_sync("同期エラーログ", file_format="csv")

if __name__ == "__main__":
    asyncio.run(main())
    sync_function()
```

---

## メソッドリファレンス

### LogManager クラス

#### コンストラクタ

```python
LogManager(log_dir=None, default_format="json")
```

- `log_dir`: ログ保存ディレクトリ（デフォルト: `constants.LOG_DIR`）
- `default_format`: デフォルトファイル形式（`"json"` または `"csv"`）

#### 非同期メソッド

```python
await log.debug(message, save_file=False, file_format=None)
await log.info(message, save_file=False, file_format=None)
await log.warning(message, save_file=False, file_format=None)
await log.error(message, save_file=False, file_format=None)
await log.critical(message, save_file=False, file_format=None)
```

#### 同期メソッド

```python
log.debug_sync(message, save_file=False, file_format=None)
log.info_sync(message, save_file=False, file_format=None)
log.warning_sync(message, save_file=False, file_format=None)
log.error_sync(message, save_file=False, file_format=None)
log.critical_sync(message, save_file=False, file_format=None)
```

#### パラメータ

- `message`: ログメッセージ（文字列）
- `save_file`: 強制的にファイル保存するか（ブール値）
- `file_format`: ファイル形式（`"json"` または `"csv"`、None の場合はデフォルト形式）

---

## よくある質問

### Q. JSON 形式と CSV 形式、どちらを使うべき？

**A.** 用途に応じて選択してください：

- **JSON 形式（推奨）**: ログ解析ツール、API 連携、構造化データが必要な場合
- **CSV 形式**: Excel 等で直接開きたい、単純な表形式で十分な場合

### Q. 非同期・同期はどう使い分ける？

**A.** 実行環境に応じて選択：

- **非同期**: `async/await`関数内で使用 → `await log.info(...)`
- **同期**: 通常の関数や直接実行 → `log.info_sync(...)`

### Q. ファイル保存されるログレベルは？

**A.** デフォルト設定：

- **自動保存**: `warning`, `error`, `critical`
- **手動保存**: `debug`, `info` は `save_file=True` で保存可能

### Q. ログファイルはどこに保存される？

**A.** フォルダ構造：

```
data/logs/
├── json/     # JSON形式のログ
└── csv/      # CSV形式のログ
```

カスタムディレクトリを指定した場合も同じ構造で作成されます。

### Q. ログファイルの形式は？

**A.**

- **JSON**: JSONL 形式（1 行 1JSON）で高速解析対応
- **CSV**: ヘッダー付き CSV 形式で Excel 対応

### Q. 複数の LogManager インスタンスを使える？

**A.** はい、異なる設定で複数作成可能：

```python
main_log = LogManager()                      # JSON形式、デフォルトディレクトリ
csv_log = LogManager(default_format="csv")   # CSV形式、デフォルトディレクトリ
app_log = LogManager(log_dir="app_logs")     # JSON形式、カスタムディレクトリ
```

### Q. パフォーマンスへの影響は？

**A.** 最小限に設計されています：

- 非同期 I/O による非ブロッキング書き込み
- 必要な時だけファイル操作を実行
- 効率的な JSONL 形式を使用

---

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。

---

## 更新履歴

### v2.0.0 (2025-07-23)

- JSON 形式サポート追加
- フォルダ分離機能（json/、csv/）
- メタデータ強化（プロセス ID、ISO 形式タイムスタンプ）
- API 改善（save_file、file_format パラメータ）

### v1.0.0

- 初回リリース
- CSV 形式サポート
- 非同期・同期ログ機能
