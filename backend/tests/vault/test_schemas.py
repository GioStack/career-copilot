from career_copilot.vault.schemas import Skill


def test_skill_with_valid_data():
    skill = Skill(name="Python", level=4, years=3.5)

    assert skill.name == "Python"
    assert skill.level == 4
    assert skill.years == 3.5
