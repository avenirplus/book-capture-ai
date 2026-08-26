from __future__ import annotations

import json
import os
import sys
import tempfile
import traceback
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QHBoxLayout, QMessageBox, QPushButton

from app import APP_NAME
from app_v5 import GlobalHotkeyFilter
from app_v6 import MainWindow as V6MainWindow, run_self_test as run_v6_self_test


VERSION = "0.6.0"
MANUAL_URL = "https://branzfamily01.github.io/book-capture-ai/manual.html"


def bundled_manual_path() -> Path:
    """Return manual.html beside the packaged EXE, or beside source while developing."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / "manual.html"
    return Path(__file__).resolve().parent / "manual.html"


class MainWindow(V6MainWindow):
    """Completion release: v0.5.8 capture engine + one-tap HTML manual."""

    def build_ui(self):
        super().build_ui()
        self.setWindowTitle(f"{APP_NAME} v{VERSION}")

        self.manual_btn = QPushButton("？ 使い方")
        self.manual_btn.setToolTip("Book Capture AI の詳しい使い方を開きます")
        self.manual_btn.setMinimumHeight(34)
        self.manual_btn.clicked.connect(self.open_manual)

        main = self.centralWidget().layout()
        controls_index = None
        for i in range(main.count()):
            item = main.itemAt(i)
            layout = item.layout()
            if layout is not None and layout.indexOf(self.start_btn) >= 0:
                controls_index = i
                break

        help_row = QHBoxLayout()
        help_row.addStretch(1)
        help_row.addWidget(self.manual_btn)
        if controls_index is None:
            main.addLayout(help_row)
        else:
            main.insertLayout(controls_index, help_row)

    def open_manual(self):
        local = bundled_manual_path()
        target = QUrl.fromLocalFile(str(local)) if local.exists() else QUrl(MANUAL_URL)
        if not QDesktopServices.openUrl(target):
            QMessageBox.warning(
                self,
                APP_NAME,
                "使い方ページを開けませんでした。\n\n"
                f"ブラウザで次を開いてください。\n{MANUAL_URL}",
            )


def run_self_test(output_path: str) -> int:
    """Run the proven v0.5.8 checks and completion-release manual checks."""
    report = {"ok": False, "checks": {}, "python": sys.version, "version": VERSION}
    try:
        with tempfile.TemporaryDirectory(prefix="bookcapture-v060-selftest-") as td:
            base_report_path = Path(td) / "v058.json"
            base_rc = run_v6_self_test(str(base_report_path))
            base_report = json.loads(base_report_path.read_text(encoding="utf-8"))
            report["checks"]["v058_regression_suite"] = base_rc == 0 and bool(base_report.get("ok"))

        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        app = QApplication.instance() or QApplication([])
        win = MainWindow()
        win.resize(900, 600)
        win.show()
        app.processEvents()

        report["checks"]["mainwindow_constructed"] = bool(win.windowTitle())
        report["checks"]["version_in_title"] = VERSION in win.windowTitle()
        report["checks"]["manual_button_exists"] = win.manual_btn.text() == "？ 使い方"
        report["checks"]["start_button_visible_short_screen"] = win.start_btn.isVisible()
        report["checks"]["manual_source_exists"] = bundled_manual_path().exists()
        report["checks"]["post_process_thread_available"] = hasattr(win, "on_post_process_progress")

        win.close()
        app.processEvents()

        report["ok"] = all(report["checks"].values())
    except Exception:
        report["error"] = traceback.format_exc()

    Path(output_path).write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return 0 if report["ok"] else 1


def main():
    if "--self-test" in sys.argv:
        idx = sys.argv.index("--self-test")
        output_path = (
            sys.argv[idx + 1]
            if idx + 1 < len(sys.argv) and not sys.argv[idx + 1].startswith("--")
            else str(Path.cwd() / "bookcapture-v060-selftest.json")
        )
        raise SystemExit(run_self_test(output_path))

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    hotkey_filter = GlobalHotkeyFilter(win)
    app.installNativeEventFilter(hotkey_filter)
    win._hotkey_filter = hotkey_filter
    win.register_global_hotkeys()
    app.aboutToQuit.connect(win.unregister_global_hotkeys)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
