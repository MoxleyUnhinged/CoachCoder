"""Tests for Code Coach lessons and local progress storage."""

from datetime import date, timedelta

import pytest

from code_coach.lessons import LANGUAGES, lessons_for
from code_coach.progress import ProgressStore


def test_each_language_has_the_same_complete_learning_path():
    paths = {language: lessons_for(language) for language in LANGUAGES}
    assert len({len(path) for path in paths.values()}) == 1
    assert all(len(path) >= 5 for path in paths.values())
    for language, path in paths.items():
        assert all(lesson.id.startswith(f"{language}:") for lesson in path)
        assert all(lesson.example.strip() and lesson.challenge.strip() for lesson in path)
    for lesson in paths["python"]:
        compile(lesson.example, f"<{lesson.id}>", "exec")


def test_unknown_language_is_rejected():
    with pytest.raises(ValueError, match="Unknown language"):
        lessons_for("javascript")


def test_completing_a_lesson_awards_xp_once_and_persists(tmp_path):
    store = ProgressStore(tmp_path / "progress.json")
    today = date(2026, 11, 12)

    assert store.complete_lesson("python:first-output", today) is True
    assert store.complete_lesson("python:first-output", today) is False
    assert store.xp == 10
    assert store.current_streak(today) == 1

    reopened = ProgressStore(store.path)
    assert reopened.completed == {"python:first-output"}
    assert reopened.xp == 10
    assert reopened.current_streak(today) == 1


def test_practice_saves_drafts_and_tracks_consecutive_study_days(tmp_path):
    store = ProgressStore(tmp_path / "progress.json")
    today = date(2026, 11, 12)
    store.save_draft("cpp:loops", "for (int i = 0; i < 10; ++i) {}", today)
    store.save_draft("python:loops", "for i in range(10): pass", today - timedelta(days=1))
    store.save_draft("csharp:loops", "for (int i = 0; i < 10; i++) {}", today - timedelta(days=2))

    reopened = ProgressStore(store.path)
    assert reopened.draft_for("cpp:loops") == "for (int i = 0; i < 10; ++i) {}"
    assert reopened.current_streak(today) == 3
    assert reopened.xp == 0


def test_streak_ends_after_a_missed_day(tmp_path):
    store = ProgressStore(tmp_path / "progress.json")
    today = date(2026, 11, 12)
    store.save_draft("python:loops", "practice", today)
    store.save_draft("python:loops", "practice", today - timedelta(days=2))
    assert store.current_streak(today) == 1


def test_invalid_progress_file_has_a_clear_error(tmp_path):
    path = tmp_path / "progress.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="Could not read progress file"):
        ProgressStore(path)
