import pytest
from pydantic import ValidationError

from career_copilot.vault.schemas import Skill


def test_skill_with_valid_data():
    skill = Skill(name="Python", level=4, years=3.5)

    assert skill.name == "Python"
    assert skill.level == 4
    assert skill.years == 3.5


def test_skill_level_above_5_is_rejected():
    with pytest.raises(ValidationError):
        Skill(name="Python", level=6)


def test_skill_level_below_1_is_rejected():
    with pytest.raises(ValidationError):
        Skill(name="Python", level=0)


def test_skill_negative_years_is_rejected():
    with pytest.raises(ValidationError):
        Skill(name="Python", level=3, years=-1)
