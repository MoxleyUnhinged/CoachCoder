"""PySide6 desktop interface for Code Coach."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from .lessons import LANGUAGES, Lesson, lessons_for
from .progress import ProgressStore


class CodeCoachWindow(QMainWindow):
    def __init__(self, progress: ProgressStore):
        super().__init__()
        self.progress = progress
        self._lessons: list[Lesson] = []
        self.setWindowTitle("Code Coach")
        self.resize(1000, 720)

        root = QWidget()
        layout = QVBoxLayout(root)
        self.setCentralWidget(root)

        heading = QLabel("Your coding journey")
        heading.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(heading)

        stats = QHBoxLayout()
        self.xp_label = QLabel()
        self.completed_label = QLabel()
        self.streak_label = QLabel()
        for label in (self.xp_label, self.completed_label, self.streak_label):
            label.setStyleSheet("font-size: 15px; padding: 8px;")
            stats.addWidget(label)
        layout.addLayout(stats)

        self.language_picker = QComboBox()
        for key, name in LANGUAGES.items():
            self.language_picker.addItem(name, key)
        layout.addWidget(self.language_picker)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.lesson_list = QListWidget()
        splitter.addWidget(self.lesson_list)

        lesson_panel = QWidget()
        lesson_layout = QVBoxLayout(lesson_panel)
        self.lesson_text = QTextBrowser()
        lesson_layout.addWidget(self.lesson_text, 3)

        practice_heading = QLabel("Try it yourself")
        practice_heading.setStyleSheet("font-size: 16px; font-weight: bold;")
        lesson_layout.addWidget(practice_heading)
        self.practice_editor = QPlainTextEdit()
        self.practice_editor.setPlaceholderText(
            "Write your solution or notes here. Save a non-empty attempt to count today's practice."
        )
        self.practice_editor.setTabStopDistance(32)
        lesson_layout.addWidget(self.practice_editor, 2)

        buttons = QHBoxLayout()
        self.save_button = QPushButton("Save practice")
        self.complete_button = QPushButton("Mark complete (+10 XP)")
        buttons.addWidget(self.save_button)
        buttons.addWidget(self.complete_button)
        lesson_layout.addLayout(buttons)
        splitter.addWidget(lesson_panel)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter, 1)

        self.language_picker.currentIndexChanged.connect(self._load_language)
        self.lesson_list.currentRowChanged.connect(self._show_lesson)
        self.save_button.clicked.connect(self._save_practice)
        self.complete_button.clicked.connect(self._complete_lesson)
        self._load_language()
        self._refresh_stats()

    def _load_language(self, _index: int = 0) -> None:
        language = self.language_picker.currentData()
        self._lessons = lessons_for(language)
        self.lesson_list.clear()
        for lesson in self._lessons:
            prefix = "✓ " if lesson.id in self.progress.completed else ""
            self.lesson_list.addItem(prefix + lesson.title)
        self.lesson_list.setCurrentRow(0)

    def _show_lesson(self, row: int) -> None:
        if row < 0 or row >= len(self._lessons):
            self.lesson_text.clear()
            self.practice_editor.clear()
            self.complete_button.setEnabled(False)
            self.save_button.setEnabled(False)
            return

        lesson = self._lessons[row]
        language = LANGUAGES[self.language_picker.currentData()]
        self.lesson_text.setMarkdown(
            f"# {lesson.title}\n\n"
            f"{lesson.explanation}\n\n"
            f"## Example ({language})\n\n"
            f"```{language.lower()}\n{lesson.example}\n```\n\n"
            f"## Your challenge\n\n{lesson.challenge}\n"
        )
        self.practice_editor.setPlainText(self.progress.draft_for(lesson.id))
        completed = lesson.id in self.progress.completed
        self.complete_button.setText(
            "Completed — review again" if completed else "Mark complete (+10 XP)"
        )
        self.complete_button.setEnabled(True)
        self.save_button.setEnabled(True)

    def _selected_lesson(self) -> Lesson | None:
        row = self.lesson_list.currentRow()
        return self._lessons[row] if 0 <= row < len(self._lessons) else None

    def _save_practice(self) -> None:
        lesson = self._selected_lesson()
        if lesson is None:
            return
        try:
            self.progress.save_draft(lesson.id, self.practice_editor.toPlainText())
        except OSError as error:
            QMessageBox.critical(self, "Could not save practice", str(error))
            return
        self._refresh_stats()
        self.statusBar().showMessage("Practice saved on this computer.", 3000)

    def _complete_lesson(self) -> None:
        lesson = self._selected_lesson()
        if lesson is None:
            return
        attempt = self.practice_editor.toPlainText()
        if not attempt.strip():
            QMessageBox.information(
                self,
                "Try the challenge first",
                "Write a code attempt or a few notes before marking this lesson complete.",
            )
            return
        try:
            self.progress.save_draft(lesson.id, attempt)
            newly_completed = self.progress.complete_lesson(lesson.id)
        except OSError as error:
            QMessageBox.critical(self, "Could not save progress", str(error))
            return
        self._refresh_stats()
        self.lesson_list.currentItem().setText("✓ " + lesson.title)
        self.complete_button.setText("Completed — review again")
        self.statusBar().showMessage(
            "Lesson completed! You earned 10 XP." if newly_completed
            else "Practice saved. This lesson's XP was already earned.",
            4000,
        )

    def _refresh_stats(self) -> None:
        self.xp_label.setText(f"⭐ {self.progress.xp} XP")
        self.completed_label.setText(
            f"📘 {len(self.progress.completed)} lessons completed"
        )
        self.streak_label.setText(
            f"🔥 {self.progress.current_streak()} day study streak"
        )
