import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from decision_engine import decide_next_action


def test_high_score_gives_next_question():
    context = {"history": [], "total_questions_asked": 2}
    result = decide_next_action(score=8.5, context=context)
    assert result["action"] == "next_question"


def test_low_score_gives_follow_up():
    context = {"history": [], "total_questions_asked": 2, "follow_up_count_on_topic": 0}
    result = decide_next_action(score=2.0, context=context)
    assert result["action"] == "follow_up"


def test_low_score_after_max_follow_ups_moves_on():
    context = {"history": [], "total_questions_asked": 4, "follow_up_count_on_topic": 2}
    result = decide_next_action(score=2.0, context=context)
    assert result["action"] == "next_question"


def test_borderline_score_gives_follow_up_by_default():
    context = {"history": [], "total_questions_asked": 2, "follow_up_count_on_topic": 0}
    result = decide_next_action(score=5.5, context=context)
    assert result["action"] == "follow_up"


def test_borderline_score_with_max_follow_ups_moves_on():
    context = {"history": [], "total_questions_asked": 4, "follow_up_count_on_topic": 2}
    result = decide_next_action(score=5.0, context=context)
    assert result["action"] == "next_question"


def test_inconsistent_signals_lead_to_follow_up():
    context = {
        "history": [{"score": 9}, {"score": 2}],
        "total_questions_asked": 3,
        "follow_up_count_on_topic": 0,
    }
    result = decide_next_action(score=5.5, context=context)
    assert result["action"] == "follow_up"


def test_max_questions_limit_ends_interview():
    context = {"history": [], "total_questions_asked": 10}
    result = decide_next_action(score=9.0, context=context)
    assert result["action"] == "end_interview"


def test_missing_context_keys_does_not_crash():
    context = {}
    result = decide_next_action(score=6.0, context=context)
    assert result["action"] in ["next_question", "follow_up", "end_interview"]


def test_decision_is_deterministic():
    context = {"history": [], "total_questions_asked": 2, "follow_up_count_on_topic": 0}
    result1 = decide_next_action(score=5.0, context=context)
    result2 = decide_next_action(score=5.0, context=context)
    assert result1 == result2
