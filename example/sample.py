from log import LogManager
import asyncio

async def main():
    # LogManagerの使い方サンプル

    # デフォルトの保存先（constants.pyのLOG_DIR）を使う場合
    log = LogManager()

    # デフォルト設定では、warning, error, criticalのみCSV保存されます
    # debug, infoはCSV保存されません（必要な場合はsave_csv=Trueを指定）
    await log.debug("This is a debug message")      # CSV保存されない
    await log.info("This is an info message")       # CSV保存されない
    await log.warning("This is a warning message")  # CSV保存される
    await log.error("This is an error message")     # CSV保存される
    await log.critical("This is a critical message")# CSV保存される

    # debug, infoもCSVに保存したい場合は、save_csv=Trueを指定
    await log.debug("CSVに保存したいdebug", save_csv=True)   # CSV保存される
    await log.info("CSVに保存したいinfo", save_csv=True)     # CSV保存される

    # 保存先を指定したい場合
    custom_dir = "data/tmp/logs"
    log3 = LogManager(log_dir=custom_dir)
    await log3.info("カスタムディレクトリに保存されるinfoログ")  # CSV保存されない
    await log3.info("CSVに保存したいinfo（カスタムディレクトリ）", save_csv=True)  # CSV保存される

# --- 同期ログは非同期関数外でも使えます ---
log2 = LogManager()
log2.info_sync("同期infoログ（カスタムディレクトリ）")    # CSV保存されない
log2.info_sync("同期infoログをCSV保存", save_csv=True)     # CSV保存される


if __name__ == "__main__":
    asyncio.run(main())