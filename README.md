# LogManager - Python Logging Utility

LogManagerは、Pythonでのログ管理を簡単にする軽量ユーティリティです。  
コンソール出力とCSVファイル保存をサポートし、ログレベルごとに整ったフォーマットで出力します。

---

## 目次

- [特徴](#特徴)
- [フォルダ構成](#フォルダ構成)
- [インストール](#インストール)
- [使用方法](#使用方法)
  - [基本的な使い方（非同期）](#基本的な使い方非同期)
  - [同期ログの使い方](#同期ログの使い方)
  - [CSV保存の挙動](#csv保存の挙動)
- [サンプルコード](#サンプルコード)
- [よくある質問](#よくある質問)
- [ライセンス](#ライセンス)

---

## 特徴

- **コンソール出力**: ログレベルごとに色分けされたフォーマットで出力
- **CSVファイル保存**: ログレベルごとに個別のCSVファイルに保存
- **時間フォーマット**: `[MM/DD/YY HH:MM:SS]` の形式で時間を表示
- **レベルの整列**: ログレベルを固定幅で揃え、美しい出力を実現

---

## フォルダ構成

```
logs/
├── log.py       # LogManagerクラスの実装
├── example/
│   └── sample.py # サンプルコード
├── test.py      # 動作確認用のテストコード
└── data/        # ログデータ（CSVファイル）が保存されるディレクトリ
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

### 基本的な使い方（非同期）

```python
from log import LogManager
import asyncio

async def main():
    logger = LogManager(log_dir="data")  # 保存先ディレクトリを指定（省略可）
    await logger.info("Bot is starting...")
    await logger.warning("This is a warning...", save_csv=True)  # CSVにも保存

if __name__ == "__main__":
    asyncio.run(main())
```

### 同期ログの使い方

非同期関数外や、同期処理でログを出したい場合は `*_sync` メソッドを使います。

```python
logger = LogManager()
logger.info_sync("同期infoログ")              # CSV保存されない
logger.info_sync("同期infoログをCSV保存", save_csv=True)  # CSV保存される
```

### CSV保存の挙動

- デフォルトでは `warning`, `error`, `critical` のみCSV保存されます。
- `debug`, `info` もCSV保存したい場合は `save_csv=True` を指定してください。

---

## サンプルコード

example/sample.py より抜粋：

```python
from log import LogManager
import asyncio

async def main():
    log = LogManager()
    await log.debug("This is a debug message")      # CSV保存されない
    await log.info("This is an info message")       # CSV保存されない
    await log.warning("This is a warning message")  # CSV保存される
    await log.error("This is an error message")     # CSV保存される
    await log.critical("This is a critical message")# CSV保存される

    # debug, infoもCSVに保存したい場合
    await log.debug("CSVに保存したいdebug", save_csv=True)
    await log.info("CSVに保存したいinfo", save_csv=True)

    # 保存先を指定したい場合
    log2 = LogManager(log_dir="data/tmp/logs")
    await log2.info("カスタムディレクトリに保存されるinfoログ")
    await log2.info("CSVに保存したいinfo（カスタムディレクトリ）", save_csv=True)

# 同期ログ
log3 = LogManager()
log3.info_sync("同期infoログ")
log3.info_sync("同期infoログをCSV保存", save_csv=True)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## よくある質問

- **Q. 非同期・同期はどう使い分ける？**  
  A. 非同期関数内では `await logger.info(...)` のように、同期関数やスクリプトでは `logger.info_sync(...)` を使ってください。

- **Q. CSV保存の有無はどう決まる？**  
  A. デフォルトでは `warning`, `error`, `critical` のみ保存。`save_csv=True` を指定すれば他レベルも保存されます。

- **Q. 保存先ディレクトリがなければ？**  
  A. 自動で作成されます。

---

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

---