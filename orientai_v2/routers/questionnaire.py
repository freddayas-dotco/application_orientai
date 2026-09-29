"""API questionnaire : fournit les 48 questions selon le mode (élève / adulte)."""

from typing import Literal

from fastapi import APIRouter

from questionnaire import QUESTIONS_ADULTE, QUESTIONS_ELEVE, SS_SECTION_NAMES

router = APIRouter(prefix="/api", tags=["questionnaire"])

Mode = Literal["eleve", "adulte"]


def get_questions(mode: str) -> list[dict]:
    return QUESTIONS_ADULTE if mode == "adulte" else QUESTIONS_ELEVE


@router.get("/questions")
def questions(mode: Mode = "eleve"):
    return {
        "mode": mode,
        "questions": [
            {"n": q["n"], "section": SS_SECTION_NAMES[q["ss"]], "q": q["q"], "opts": q["opts"]}
            for q in get_questions(mode)
        ],
    }
