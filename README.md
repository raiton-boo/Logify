# LogManager - Python Logging Utility

LogManagerは、Pythonでのログ管理を簡単にする軽量なユーティリティです。  
コンソール出力とCSVファイル保存をサポートし、ログレベルごとに整ったフォーマットで出力します。

---

## 特徴

- **コンソール出力**: ログレベルごとに色分けされたフォーマットで出力。
- **CSVファイル保存**: ログレベルごとに個別のCSVファイルに保存。
- **時間フォーマット**: `[MM/DD/YY HH:MM:SS]` の形式で時間を表示。
- **レベルの整列**: ログレベルを固定幅で揃え、美しい出力を実現。

---

## フォルダ構成

```
logs/
├── log.py       # LogManagerクラスの実装
├── test.py      # 動作確認用のテストコード
└── data/        # ログデータ（CSVファイル）が保存されるディレクトリ
    ├── debug.csv
    ├── info.csv
    ├── warning.csv
    ├── error.csv
    └── critical.csv
```

---

## 使用方法

### 1. LogManagerクラスのインポート
`log.py`をインポートして使用します。

```python
from log import LogManager
```

### 2. LogManagerのインスタンス化
ログデータを保存するディレクトリを指定してインスタンス化します（デフォルトはdata/）。

```python
logger = LogManager(log_dir="data")
```

### 3. ログの記録
以下のメソッドを使用してログを記録します。

```python
logger.debug(message: str)
logger.info(message: str)
logger.warning(message: str)
logger.error(message: str)
logger.critical(message: str)
```

出力例
コンソール出力

```zsh
[04/25/25 04:35:11] | INFO     | Bot is starting...
[04/25/25 04:35:11] | DEBUG    | Debugging information...
[04/25/25 04:35:12] | WARNING  | This is a warning...
[04/25/25 04:35:13] | ERROR    | An error occurred...
[04/25/25 04:35:14] | CRITICAL | Critical issue!
```

CSVファイル出力
例: data/info.csv

```csv
timestamp,level,message
2025-04-25 04:35:11,INFO,Bot is starting...
```

### 必要なライブラリ
このプロジェクトでは、以下のライブラリを使用しています。

- rich: コンソール出力の装飾
- os: ファイル・ディレクトリ操作
- csv: CSVファイル操作
- datetime: 時間の取得とフォーマット

インストールコマンド:

```zsh
pip install rich
```

### ライセンス
このプロジェクトはMITライセンスの下で公開されています。

---