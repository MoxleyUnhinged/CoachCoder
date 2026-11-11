"""Local progress and practice-draft storage for Code Coach."""

import json
from datetime import date, timedelta
from pathlib import Path


DEFAULT_PROGRESS_PATH = Path.home() / ".code_coach" / "progress.json"


class ProgressStore:
    def __init__(self, path: str | Path = DEFAULT_PROGRESS_PATH):
        self.path = Path(path)
        self.completed: set[str] = set()
        self.drafts: dict[str, str] = {}
        self.study_days: set[date] = set()
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            completed = data["completed"]
            drafts = data["drafts"]
            study_days = data["study_days"]
            if (
                not isinstance(completed, list)
                or not all(isinstance(item, str) for item in completed)
                or not isinstance(drafts, dict)
                or not all(
                    isinstance(key, str) and isinstance(value, str)
                    for key, value in drafts.items()
                )
                or not isinstance(study_days, list)
            ):
                raise ValueError("Progress file has an invalid format.")
            self.completed = set(completed)
            self.drafts = drafts
            self.study_days = {date.fromisoformat(day) for day in study_days}
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            raise ValueError(f"Could not read progress file {self.path}: {error}") from error

    def _save(
        self,
        completed: set[str],
        drafts: dict[str, str],
        study_days: set[date],
    ) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(self.path.suffix + ".tmp")
        payload = {
            "completed": sorted(completed),
            "drafts": drafts,
            "study_days": sorted(day.isoformat() for day in study_days),
        }
        temporary_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        temporary_path.replace(self.path)

    def draft_for(self, lesson_id: str) -> str:
        return self.drafts.get(lesson_id, "")

    def save_draft(self, lesson_id: str, text: str, today: date | None = None) -> None:
        completed = self.completed.copy()
        drafts = self.drafts | {lesson_id: text}
        study_days = self.study_days.copy()
        if text.strip():
            study_days.add(today or date.today())
        self._save(completed, drafts, study_days)
        self.drafts = drafts
        self.study_days = study_days

    def complete_lesson(self, lesson_id: str, today: date | None = None) -> bool:
        completed = self.completed | {lesson_id}
        study_days = self.study_days | {today or date.today()}
        newly_completed = lesson_id not in self.completed
        self._save(completed, self.drafts.copy(), study_days)
        self.completed = completed
        self.study_days = study_days
        return newly_completed

    def current_streak(self, today: date | None = None) -> int:
        current_day = today or date.today()
        if current_day not in self.study_days:
            current_day -= timedelta(days=1)
            if current_day not in self.study_days:
                return 0
        streak = 0
        while current_day in self.study_days:
            streak += 1
            current_day -= timedelta(days=1)
        return streak

    @property
    def xp(self) -> int:
        return len(self.completed) * 10
