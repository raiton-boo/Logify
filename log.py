import logging
import os
import csv
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
        async def wrapper(self, message, save_csv=False):
            await self._log_to_console(level_name, message)
            await self._write_to_csv(level_name, message, save_csv)
            if func is not None:
                return await func(self, message, save_csv)

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
        def wrapper(self, message, save_csv=False):
            self._log_to_console_sync(level_name, message)
            self._write_to_csv_sync(level_name, message, save_csv)
            if func is not None:
                return func(self, message, save_csv)

        return wrapper

    return decorator


class LogManager:
    """
    ログ管理クラス
    - 非同期・同期のログ出力
    - CSV保存
    - コンソール出力
    """

    def __init__(self, log_dir=None):
        """
        LogManagerの初期化処理。

        Args:
            log_dir (str, optional): ログ保存ディレクトリのパス。指定がなければデフォルトを使用。

        Returns:
            None
        """
        self.console = Console()
        self.log_dir = (
            log_dir if log_dir is not None else LOG_DIR
        )  # ログ保存ディレクトリ

        # フォルダがなければ作成し、作成時のみログ出力
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir, exist_ok=True)
            self._log_to_console_sync("info", f"LOG_DIRを作成しました: {self.log_dir}")

        # CSVに書き出すログレベル
        self.csv_write_levels = {
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

    async def _write_to_csv(self, level, message, save_csv):
        """
        非同期でCSVにログを書き込む

        Args:
            level (str): ログレベル
            message (str): ログメッセージ
            save_csv (bool): 一時的にCSV保存するか

        Returns:
            None
        """
        if not (self.csv_write_levels.get(level, False) or save_csv):
            return
        log_file = os.path.join(self.log_dir, f"{level}.csv")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        is_new = not os.path.exists(log_file)
        await asyncio.to_thread(
            self._append_to_csv, log_file, timestamp, level, message, is_new
        )

    def _write_to_csv_sync(self, level, message, save_csv):
        """
        同期でCSVにログを書き込む

        Args:
            level (str): ログレベル
            message (str): ログメッセージ
            save_csv (bool): 一時的にCSV保存するか

        Returns:
            None
        """
        if not (self.csv_write_levels.get(level, False) or save_csv):
            return
        log_file = os.path.join(self.log_dir, f"{level}.csv")
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
    async def debug(self, message, save_csv=False):
        """
        非同期debugログ

        Args:
            message (str): ログメッセージ
            save_csv (bool): 一時的にCSV保存するか

        Returns:
            None
        """
        pass

    @async_log_method("info")
    async def info(self, message, save_csv=False):
        """
        非同期infoログ

        Args:
            message (str): ログメッセージ
            save_csv (bool): 一時的にCSV保存するか

        Returns:
            None
        """
        pass

    @async_log_method("warning")
    async def warning(self, message, save_csv=False):
        """
        非同期warningログ

        Args:
            message (str): ログメッセージ
            save_csv (bool): 一時的にCSV保存するか

        Returns:
            None
        """
        pass

    @async_log_method("error")
    async def error(self, message, save_csv=False):
        """
        非同期errorログ

        Args:
            message (str): ログメッセージ
            save_csv (bool): 一時的にCSV保存するか

        Returns:
            None
        """
        pass

    @async_log_method("critical")
    async def critical(self, message, save_csv=False):
        """
        非同期criticalログ

        Args:
            message (str): ログメッセージ
            save_csv (bool): 一時的にCSV保存するか

        Returns:
            None
        """
        pass

    # --- 同期ログレベルメソッド ---
    @sync_log_method("debug")
    def debug_sync(self, message, save_csv=False):
        """
        同期debugログ

        Args:
            message (str): ログメッセージ
            save_csv (bool): 一時的にCSV保存するか

        Returns:
            None
        """
        pass

    @sync_log_method("info")
    def info_sync(self, message, save_csv=False):
        """
        同期infoログ

        Args:
            message (str): ログメッセージ
            save_csv (bool): 一時的にCSV保存するか

        Returns:
            None
        """
        pass

    @sync_log_method("warning")
    def warning_sync(self, message, save_csv=False):
        """
        同期warningログ

        Args:
            message (str): ログメッセージ
            save_csv (bool): 一時的にCSV保存するか

        Returns:
            None
        """
        pass

    @sync_log_method("error")
    def error_sync(self, message, save_csv=False):
        """
        同期errorログ

        Args:
            message (str): ログメッセージ
            save_csv (bool): 一時的にCSV保存するか

        Returns:
            None
        """
        pass

    @sync_log_method("critical")
    def critical_sync(self, message, save_csv=False):
        """
        同期criticalログ

        Args:
            message (str): ログメッセージ
            save_csv (bool): 一時的にCSV保存するか

        Returns:
            None
        """
        pass
