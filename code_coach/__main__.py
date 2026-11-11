"""Launch Code Coach with ``python -m code_coach``."""

import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from .progress import DEFAULT_PROGRESS_PATH, ProgressStore
from .window import CodeCoachWindow


def main() -> int:
    app = QApplication(sys.argv)
    try:
        progress = ProgressStore()
    except (OSError, ValueError) as error:
        QMessageBox.critical(
            None,
            "Could not load learning progress",
            f"Check {DEFAULT_PROGRESS_PATH} and try again.\n\n{error}",
        )
        return 1
    window = CodeCoachWindow(progress)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
