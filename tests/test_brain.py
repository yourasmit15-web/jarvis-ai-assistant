from backend.ai.brain import AIBrain


def test_brain_classifies_search_intent():
    brain = AIBrain()
    intent = brain.classify_intent("Please search the latest AI news")
    assert intent.intent == "web_search"
    assert intent.confidence > 0.8


def test_brain_decomposes_multi_task_message():
    brain = AIBrain()
    subtasks = brain.decompose_task("open dashboard and search project roadmap")
    assert subtasks == ["open dashboard", "search project roadmap"]
