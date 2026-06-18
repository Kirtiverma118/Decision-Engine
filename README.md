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

⚙️ Constraints & Edge Cases

The decision logic must be robust enough to handle real-world messiness, including:

- Borderline scores — scores that sit right at the edge between two decisions (e.g. neither clearly "good" nor "bad") must still be handled gracefully and consistently.
- Inconsistent evaluation signals — sometimes different evaluation signals may contradict each other; the engine should resolve this sensibly rather than breaking.
- No random decisions — the same input (score + context) should reliably lead to the same decision. The logic must be deterministic and rule-based, not arbitrary or random.

✅ Deliverables

By the end of this task, the following must be completed:

1. Decision Rules (Document)
   A clearly written document explaining the rules/logic used to decide between `next_question`, `follow_up`, and `end_interview` — including how borderline cases and conflicting signals are handled.

2. API Endpoint
   A working API endpoint that accepts `score` + `context` as input and returns the `action` decision in the specified JSON format.

3. Simulation Tests (Multiple Flows)
   Test cases simulating multiple possible interview flows to verify the engine behaves correctly and consistently across different scenarios (good scores, bad scores, borderline scores, conflicting signals, etc.).

🧪 Related Requirement (from previous section)

- Unit tests must be written for **all transitions** between decision states/actions, ensuring every possible path through the decision logic is verified.
