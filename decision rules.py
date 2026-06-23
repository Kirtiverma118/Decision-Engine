Input:  score (0-10), context
Output: { "action": "next_question" }

from collections import deque

# CONFIG / THRESHOLDS
HIGH_SCORE_THRESHOLD = 7.0     
LOW_SCORE_THRESHOLD = 4.0      
BORDERLINE_RANGE = (4.0, 7.0)  

MAX_FOLLOW_UPS_PER_TOPIC = 2   
MAX_QUESTIONS_TOTAL = 10       
MIN_QUESTIONS_BEFORE_END = 3   


def _get_recent_scores(context, n=3):
    history = context.get("history", [])
    recent = [item.get("score") for item in history[-n:] if "score" in item]
    return recent


def _is_inconsistent(recent_scores):
    if len(recent_scores) < 2:
        return False
    spread = max(recent_scores) - min(recent_scores)
    return spread >= 5  


def decide_next_action(score: float, context: dict) -> dict:
       Parameters
    ----------
    score : float
    context : dict
        Expected keys:
            - "history": list of {"question": str, "score": float, "topic": str}
            - "current_topic": str (optional)
            - "follow_up_count_on_topic": int (optional, default 0)
            - "total_questions_asked": int (optional, default 0)

    Returns
    -------
    dict
        {"action": "next_question" | "follow_up" | "end_interview"}

    # -----Safety defaults-----
    history = context.get("history", [])
    total_questions_asked = context.get("total_questions_asked", len(history))
    follow_up_count_on_topic = context.get("follow_up_count_on_topic", 0)

    recent_scores = _get_recent_scores(context, n=3)
    inconsistent = _is_inconsistent(recent_scores)

    #RULE 1
    if total_questions_asked >= MAX_QUESTIONS_TOTAL:
        return {"action": "end_interview"}

    #RULE 2
    if score >= HIGH_SCORE_THRESHOLD:
        if total_questions_asked < MIN_QUESTIONS_BEFORE_END:
            return {"action": "next_question"}
        return {"action": "next_question"}

    #RULE 3: 
    if score < LOW_SCORE_THRESHOLD:
        if follow_up_count_on_topic < MAX_FOLLOW_UPS_PER_TOPIC:
            return {"action": "follow_up"}
        return {"action": "next_question"}

    #RULE 4: 
    if BORDERLINE_RANGE[0] <= score < BORDERLINE_RANGE[1]:
        if inconsistent:
            return {"action": "follow_up"}

        if follow_up_count_on_topic >= MAX_FOLLOW_UPS_PER_TOPIC:
            return {"action": "next_question"}

        return {"action": "follow_up"}

    return {"action": "next_question"}
