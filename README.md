Decision Engine (Next Step Selector)

📌 Overview

This module is the core intelligence controller of the interview/evaluation system. Once a candidate's response has been scored and evaluated, this engine is responsible for deciding what happens next — whether the system should ask another question, ask a follow-up, or end the interview altogether.

In short: this is the "brain" that takes evaluation results and turns them into a concrete next action.

- Module / Phase: Phase 3
- Difficulty: High
- Estimated Duration: 4–6 days

🎯 Objective

- Decide the system's next action immediately after an evaluation step is completed.
- Act as the core decision-making / intelligence layer of the system — everything downstream depends on this module making the right call.

🛠️ What to Build

# Input
The engine receives:
- Score — the evaluation result of the candidate's last response.
- Context — surrounding information about the interview state (e.g. previous questions, history, performance trend, etc.).

# Output
The engine returns a single decision in the following JSON format:

{
  "action": "next_question | follow_up | end_interview"
}

The action field will always be exactly one of these three values:
next_question - Move on and ask a new, unrelated question 
follow_up - Ask a deeper/related question on the same topic 
end_interview - Conclude the interview 

👩‍💻 What I Did

For this task, I implemented the complete Decision Engine module end-to-end:


1.Designed the decision logic — I defined a set of fixed thresholds (high score, low score, borderline range, max follow-ups per topic, max total questions) and wrote the rule-based function decide_next_action() in src/decision_engine.py that takes a score and context as input and returns one of next_question, follow_up, or end_interview.

2.Handled the required edge cases:

-Borderline scores (4.0–7.0) — handled with a dedicated rule that defaults to a confirming follow_up unless the follow-up limit on that topic is already reached.

-Inconsistent evaluation signals — I added a check that looks at the spread between the last few scores; if the spread is 5 or more points, the signals are treated as inconsistent and the engine plays it safe with a follow_up instead of guessing.

-No random decisions — the entire function is deterministic (no random() anywhere); the same score + context will always produce the same action.

3.Built the API endpoint — I wrapped the decision logic in a Flask app (api/endpoint.py) with a POST /decide route that accepts JSON input (score + context) and returns the decided action as JSON, plus a basic health-check route.

4.Wrote the decision rules document — docs/decision-rules.md explains every threshold, every rule, and how each edge case is handled, along with a text-based flow diagram.

5.Wrote and ran the test suite:

-tests/test_transitions.py — unit tests covering every individual transition (high score, low score, borderline, inconsistent signals, missing context fields, determinism check).
-tests/test_simulations.py — simulation tests that run full multi-question interview flows (strong candidate, weak candidate, borderline candidate, mixed realistic flow, long interview, inconsistent scores) to confirm the engine behaves correctly across an entire conversation, not just one call.

6.Tested the API manually — ran the Flask server locally and verified the /decide endpoint with sample requests to confirm the response format matched the required {"action": "..."} structure.

⚙️ Constraints & Edge Cases

The decision logic must be robust enough to handle real-world messiness, including:

- Borderline scores — scores that sit right at the edge between two decisions (e.g. neither clearly "good" nor "bad") must still be handled gracefully and consistently.
- Inconsistent evaluation signals — sometimes different evaluation signals may contradict each other; the engine should resolve this sensibly rather than breaking.
- No random decisions — the same input (score + context) should reliably lead to the same decision. The logic must be deterministic and rule-based, not arbitrary or random.

## 📂 Project Structure

decision-engine/
├── README.md
├── requirements.txt
├── docs/
│   └── decision-rules.md        # Full decision rules explained
├── src/
│   └── decision_engine.py       # Core decision logic
├── api/
│   └── endpoint.py              # Flask API endpoint
└── tests/
    ├── test_transitions.py      # Unit tests for all transitions
    └── test_simulations.py      # Simulation tests for multiple flows


✅ Deliverables

By the end of this task, the following must be completed:

1. Decision Rules (Document)
   A clearly written document explaining the rules/logic used to decide between `next_question`, `follow_up`, and `end_interview` — including how borderline cases and conflicting signals are handled.

2. API Endpoint
   A working API endpoint that accepts `score` + `context` as input and returns the `action` decision in the specified JSON format.

3. Simulation Tests (Multiple Flows)
   Test cases simulating multiple possible interview flows to verify the engine behaves correctly and consistently across different scenarios (good scores, bad scores, borderline scores, conflicting signals, etc.).
