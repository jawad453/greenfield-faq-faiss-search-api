
from types import SimpleNamespace

from fastapi.testclient import TestClient

import app.main as main


client = TestClient(main.app)


def make_result(faq, score=0.8):
    return {
        "question": faq["question"],
        "answer": faq["answer"],
        "similarity_score": score,
    }


def test_empty_question_returns_fallback(monkeypatch):
    response = client.post("/answer", json={"question": "   "})

    assert response.status_code == 200
    assert response.json() == {
        "answer": "We\u2019ll get back to you shortly",
        "sources": [],
    }


def test_low_similarity_returns_fallback(monkeypatch):
    faq = main.faq_data[0]
    monkeypatch.setattr(
        main, "search_faq", lambda question: [make_result(faq, 0.2)]
    )

    response = client.post(
        "/answer", json={"question": "Tell me something unrelated"}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "We\u2019ll get back to you shortly"
    assert response.json()["sources"] == []


def test_mock_mode_returns_faq_answer(monkeypatch):
    faq = main.faq_data[0]
    monkeypatch.setattr(
        main, "search_faq", lambda question: [make_result(faq)]
    )
    monkeypatch.setattr(main, "client", None)

    response = client.post(
        "/answer", json={"question": faq["question"]}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == faq["answer"]
    assert response.json()["sources"] == [
        main.faq_ids[faq["question"]]
    ]


def test_openai_is_called_with_faq_context(monkeypatch):
    faqs = main.faq_data[:3]
    results = [make_result(faq) for faq in faqs]
    captured = {}

    def fake_create(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content="This is a mocked AI answer."
                    )
                )
            ]
        )

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(create=fake_create)
        )
    )

    monkeypatch.setattr(
        main, "search_faq", lambda question: results
    )
    monkeypatch.setattr(main, "client", fake_client)

    response = client.post(
        "/answer",
        json={"question": "Tell me about GreenField Farmers"},
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "This is a mocked AI answer."
    assert len(response.json()["sources"]) == 3

    # Verify that all three FAQ entries are included in the prompt.
    user_message = captured["messages"][1]["content"]
    for faq in faqs:
        assert faq["question"] in user_message
        assert faq["answer"] in user_message

    assert captured["temperature"] == 0


def test_missing_question_is_rejected():
    response = client.post("/answer", json={})

    assert response.status_code == 422
