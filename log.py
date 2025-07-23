import logging
import os
import csv
import json
import asyncio
from datetime import datetime
from functools import wraps
from rich.console import Console
from rich.logging import RichHandler


from constants import LOG_DIR


def async_log_method(level_name):
    """
    非同期ログ用デコレーター

    Args:
        level_name (str): ログレベル名（例: "info"）

    Returns:
        callable: デコレートされた非同期メソッド
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(self, message, save_file=False, file_format=None):
            await self._log_to_console(level_name, message)
            await self._write_to_file(level_name, message, save_file, file_format)
            if func is not None:
                return await func(self, message, save_file, file_format)

        return wrapper

    return decorator


def sync_log_method(level_name):
    """
    同期ログ用デコレーター

    Args:
        level_name (str): ログレベル名（例: "info"）

    Returns:
        callable: デコレートされた同期メソッド
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, message, save_file=False, file_format=None):
            self._log_to_console_sync(level_name, message)
            self._write_to_file_sync(level_name, message, save_file, file_format)
            if func is not None:
                return func(self, message, save_file, file_format)

        return wrapper

    return decorator


class LogManager:
    """
    ログ管理クラス
    - 非同期・同期のログ出力
    - JSON/CSV保存
    - コンソール出力
    """

    def __init__(self, log_dir=None, default_format="json"):
        """
        LogManagerの初期化処理。

        Args:
            log_dir (str, optional): ログ保存ディレクトリのパス。指定がなければデフォルトを使用。
            default_format (str): デフォルトのファイル形式 ("json" または "csv")

        Returns:
            None
        """
        self.console = Console()
        self.log_dir = (
            log_dir if log_dir is not None else LOG_DIR
        )  # ログ保存ディレクトリ
        self.default_format = default_format

        # フォルダがなければ作成し、作成時のみログ出力
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir, exist_ok=True)
            self._log_to_console_sync("info", f"LOG_DIRを作成しました: {self.log_dir}")

        # ファイルに書き出すログレベル
        self.file_write_levels = {
            "debug": False,
            "info": False,
            "warning": True,
            "error": True,
            "critical": True,
        }

        # RichHandlerで見やすいログ出力
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(message)s",
                handlers=[
                    RichHandler(
                        console=self.console,
                        show_time=False,
                        show_level=False,
                        show_path=False,
                    )
                ],
            )
        self.logger = logging.getLogger(__name__)

    async def _write_to_file(self, level, message, save_file, file_format=None):
        """
        非同期でファイルにログを書き込む

        Args:
            level (str): ログレベル
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか
            file_format (str): ファイル形式 ("json" または "csv")

        Returns:
            None
        """
        if not (self.file_write_levels.get(level, False) or save_file):
            return

        format_to_use = file_format or self.default_format

        if format_to_use.lower() == "csv":
            await self._write_to_csv(level, message, save_file)
        else:  # default to json
            await self._write_to_json(level, message, save_file)

    def _write_to_file_sync(self, level, message, save_file, file_format=None):
        """
        同期でファイルにログを書き込む

        Args:
            level (str): ログレベル
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか
            file_format (str): ファイル形式 ("json" または "csv")

        Returns:
            None
        """
        if not (self.file_write_levels.get(level, False) or save_file):
            return

        format_to_use = file_format or self.default_format

        if format_to_use.lower() == "csv":
            self._write_to_csv_sync(level, message, save_file)
        else:  # default to json
            self._write_to_json_sync(level, message, save_file)

    async def _write_to_json(self, level, message, save_file):
        """
        非同期でJSONファイルにログを書き込む

        Args:
            level (str): ログレベル
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか

        Returns:
            None
        """
        json_dir = os.path.join(self.log_dir, "json")
        os.makedirs(json_dir, exist_ok=True)
        log_file = os.path.join(json_dir, f"{level}.json")
        log_entry = self._create_log_entry(level, message)
        await asyncio.to_thread(self._append_to_json, log_file, log_entry)

    def _write_to_json_sync(self, level, message, save_file):
        """
        同期でJSONファイルにログを書き込む

        Args:
            level (str): ログレベル
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか

        Returns:
            None
        """
        json_dir = os.path.join(self.log_dir, "json")
        os.makedirs(json_dir, exist_ok=True)
        log_file = os.path.join(json_dir, f"{level}.json")
        log_entry = self._create_log_entry(level, message)
        self._append_to_json(log_file, log_entry)

    def _create_log_entry(self, level, message):
        """
        ログエントリオブジェクトを作成

        Args:
            level (str): ログレベル
            message (str): ログメッセージ

        Returns:
            dict: ログエントリ
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "level": level.upper(),
            "message": message,
            "logger_name": __name__,
            "process_id": os.getpid(),
        }

    def _append_to_json(self, log_file, log_entry):
        """
        JSONファイルに1エントリ追記（JSONL形式）

        Args:
            log_file (str): ファイルパス
            log_entry (dict): ログエントリ

        Returns:
            None
        """
        with open(log_file, mode="a", encoding="utf-8") as file:
            json.dump(log_entry, file, ensure_ascii=False)
            file.write("\n")  # JSONL形式（1行1JSON）

    async def _write_to_csv(self, level, message, save_file):
        """
        非同期でCSVにログを書き込む

        Args:
            level (str): ログレベル
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか

        Returns:
            None
        """
        csv_dir = os.path.join(self.log_dir, "csv")
        os.makedirs(csv_dir, exist_ok=True)
        log_file = os.path.join(csv_dir, f"{level}.csv")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        is_new = not os.path.exists(log_file)
        await asyncio.to_thread(
            self._append_to_csv, log_file, timestamp, level, message, is_new
        )

    def _write_to_csv_sync(self, level, message, save_file):
        """
        同期でCSVにログを書き込む

        Args:
            level (str): ログレベル
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか

        Returns:
            None
        """
        csv_dir = os.path.join(self.log_dir, "csv")
        os.makedirs(csv_dir, exist_ok=True)
        log_file = os.path.join(csv_dir, f"{level}.csv")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        is_new = not os.path.exists(log_file)
        self._append_to_csv(log_file, timestamp, level, message, is_new)

    def _append_to_csv(self, log_file, timestamp, level, message, is_new):
        """
        CSVファイルに1行追記

        Args:
            log_file (str): ファイルパス
            timestamp (str): タイムスタンプ
            level (str): ログレベル
            message (str): ログメッセージ
            is_new (bool): 新規ファイルかどうか

        Returns:
            None
        """
        with open(log_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if is_new:
                writer.writerow(["timestamp", "level", "message"])
            writer.writerow([timestamp, level.upper(), message])

    async def _log_to_console(self, level, message):
        """
        非同期でコンソールにログ出力

        Args:
            level (str): ログレベル
            message (str): ログメッセージ

        Returns:
            None
        """
        color = {
            "debug": "cyan",
            "info": "green",
            "warning": "yellow",
            "error": "red",
            "critical": "bold red",
        }.get(level, "white")
        timestamp = datetime.now().strftime("[%m/%d/%y %H:%M:%S]")
        level_padded = level.upper().ljust(8)
        await asyncio.to_thread(
            self.console.print, f"{timestamp} | [{color}]{level_padded}[/]\n{message}"
        )

    def _log_to_console_sync(self, level, message):
        """
        同期でコンソールにログ出力

        Args:
            level (str): ログレベル
            message (str): ログメッセージ

        Returns:
            None
        """
        color = {
            "debug": "cyan",
            "info": "green",
            "warning": "yellow",
            "error": "red",
            "critical": "bold red",
        }.get(level, "white")
        timestamp = datetime.now().strftime("[%m/%d/%y %H:%M:%S]")
        level_padded = level.upper().ljust(8)
        self.console.print(f"{timestamp} | [{color}]{level_padded}[/]\n{message}")

    # --- 非同期ログレベルメソッド ---
    @async_log_method("debug")
    async def debug(self, message, save_file=False, file_format=None):
        """
        非同期debugログ

        Args:
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか
            file_format (str): ファイル形式 ("json" または "csv")

        Returns:
            None
        """
        pass

    @async_log_method("info")
    async def info(self, message, save_file=False, file_format=None):
        """
        非同期infoログ

        Args:
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか
            file_format (str): ファイル形式 ("json" または "csv")

        Returns:
            None
        """
        pass

    @async_log_method("warning")
    async def warning(self, message, save_file=False, file_format=None):
        """
        非同期warningログ

        Args:
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか
            file_format (str): ファイル形式 ("json" または "csv")

        Returns:
            None
        """
        pass

    @async_log_method("error")
    async def error(self, message, save_file=False, file_format=None):
        """
        非同期errorログ

        Args:
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか
            file_format (str): ファイル形式 ("json" または "csv")

        Returns:
            None
        """
        pass

    @async_log_method("critical")
    async def critical(self, message, save_file=False, file_format=None):
        """
        非同期criticalログ

        Args:
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか
            file_format (str): ファイル形式 ("json" または "csv")

        Returns:
            None
        """
        pass

    # --- 同期ログレベルメソッド ---
    @sync_log_method("debug")
    def debug_sync(self, message, save_file=False, file_format=None):
        """
        同期debugログ

        Args:
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか
            file_format (str): ファイル形式 ("json" または "csv")

        Returns:
            None
        """
        pass

    @sync_log_method("info")
    def info_sync(self, message, save_file=False, file_format=None):
        """
        同期infoログ

        Args:
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか
            file_format (str): ファイル形式 ("json" または "csv")

        Returns:
            None
        """
        pass

    @sync_log_method("warning")
    def warning_sync(self, message, save_file=False, file_format=None):
        """
        同期warningログ

        Args:
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか
            file_format (str): ファイル形式 ("json" または "csv")

        Returns:
            None
        """
        pass

    @sync_log_method("error")
    def error_sync(self, message, save_file=False, file_format=None):
        """
        同期errorログ

        Args:
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか
            file_format (str): ファイル形式 ("json" または "csv")

        Returns:
            None
        """
        pass

    @sync_log_method("critical")
    def critical_sync(self, message, save_file=False, file_format=None):
        """
        同期criticalログ

        Args:
            message (str): ログメッセージ
            save_file (bool): 一時的にファイル保存するか
            file_format (str): ファイル形式 ("json" または "csv")

        Returns:
            None
        """
        pass
