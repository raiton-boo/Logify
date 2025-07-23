from log import LogManager
import asyncio


async def main():
    # LogManagerの使い方サンプル
    # フォルダ構造:
    # logs/
    # ├── json/     <- JSON形式のログファイル
    # └── csv/      <- CSV形式のログファイル

    # デフォルトの保存先（constants.pyのLOG_DIR）を使う場合
    # JSON形式がデフォルト
    log = LogManager()

    # デフォルト設定では、warning, error, criticalのみファイル保存されます
    # debug, infoはファイル保存されません（必要な場合はsave_file=Trueを指定）
    await log.debug("This is a debug message")  # ファイル保存されない
    await log.info("This is an info message")  # ファイル保存されない
    await log.warning(
        "This is a warning message"
    )  # logs/json/warning.json に保存される
    await log.error("This is an error message")  # logs/json/error.json に保存される
    await log.critical(
        "This is a critical message"
    )  # logs/json/critical.json に保存される

    # debug, infoもファイルに保存したい場合は、save_file=Trueを指定
    await log.debug(
        "ファイルに保存したいdebug", save_file=True
    )  # logs/json/debug.json に保存される
    await log.info(
        "ファイルに保存したいinfo", save_file=True
    )  # logs/json/info.json に保存される

    # CSV形式で保存したい場合
    await log.warning(
        "CSV形式で保存", save_file=True, file_format="csv"
    )  # logs/csv/warning.csv に保存される
    await log.error(
        "CSV形式のエラーログ", file_format="csv"
    )  # logs/csv/error.csv に保存される

    # 保存先を指定したい場合
    custom_dir = "data/tmp/logs"
    log3 = LogManager(log_dir=custom_dir)
    await log3.info("カスタムディレクトリに保存されるinfoログ")  # ファイル保存されない
    await log3.info(
        "JSONに保存したいinfo（カスタムディレクトリ）", save_file=True
    )  # data/tmp/logs/json/info.json に保存される

    # CSV形式をデフォルトにしたい場合
    csv_log = LogManager(default_format="csv")
    await csv_log.error(
        "CSV形式がデフォルトのエラーログ"
    )  # logs/csv/error.csv に保存される
    await csv_log.error(
        "JSON形式で保存したいエラーログ", file_format="json"
    )  # logs/json/error.json に保存される


# --- 同期ログは非同期関数外でも使えます ---
log2 = LogManager()
log2.info_sync("同期infoログ")  # ファイル保存されない
log2.info_sync(
    "同期infoログをファイル保存", save_file=True
)  # logs/json/info.json に保存される
log2.error_sync(
    "同期errorログをCSV保存", file_format="csv"
)  # logs/csv/error.csv に保存される


if __name__ == "__main__":
    asyncio.run(main())
