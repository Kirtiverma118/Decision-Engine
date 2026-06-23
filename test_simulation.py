import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from decision_engine import decide_next_action


def simulate_interview(score_sequence):
    history = []
    follow_up_count_on_topic = 0
    actions_taken = []

    for score in score_sequence:
        context = {
            "history": history,
            "total_questions_asked": len(history),
            "follow_up_count_on_topic": follow_up_count_on_topic,
        }

        result = decide_next_action(score, context)
        action = result["action"]
        actions_taken.append(action)

        history.append({"score": score})
        if action == "follow_up":
            follow_up_count_on_topic += 1
        else:
            follow_up_count_on_topic = 0 

        if action == "end_interview":
            break

    return actions_taken


def test_simulation_strong_candidate():
    scores = [8, 9, 7.5, 8.2, 9.1]
    actions = simulate_interview(scores)
    assert "next_question" in actions
    assert all(a != "follow_up" for a in actions)  

def test_simulation_weak_candidate():
    scores = [2, 3, 1.5, 2.8]
    actions = simulate_interview(scores)
    assert "follow_up" in actions


def test_simulation_borderline_candidate():
    scores = [5.5, 5.0, 6.0, 5.5]
    actions = simulate_interview(scores)
    assert "follow_up" in actions
    assert "next_question" in actions


def test_simulation_mixed_realistic_flow():
    scores = [8, 3, 5.5, 9, 2, 6]
    actions = simulate_interview(scores)
    valid_actions = {"next_question", "follow_up", "end_interview"}
    assert all(a in valid_actions for a in actions)


def test_simulation_long_interview_ends_eventually():
    scores = [7, 8, 7, 8, 7, 8, 7, 8, 7, 8, 7, 8]
    actions = simulate_interview(scores)
    assert "end_interview" in actions


def test_simulation_inconsistent_scores_handled_safely():
    scores = [9, 2, 8, 1, 9]
    actions = simulate_interview(scores)
    assert len(actions) == len(scores)
