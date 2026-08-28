from backend.ai.brain import AIBrain


def test_brain_intent_and_greeting():
    brain = AIBrain(assistant_name="RAGHUVIR")
    assert brain.classify_intent("search web for docs") == "search"
    assert "RAGHUVIR" in brain.generate_response("hello")
