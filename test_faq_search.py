
import pytest

from search_faq import search_faq


@pytest.mark.parametrize(
    "question, expected_keywords",
    [
        ("How can I become a member?", ["member"]),
        ("Is there a membership fee?", ["membership"]),
        ("What seasonal produce is available?", ["produce"]),
        (
            "How does the co-op support sustainability?",
            ["soil", "water", "sustainable", "farm"],
        ),
        ("How can I contact GreenField Farmers?", ["contact"]),
    ],
)
def test_search_returns_relevant_faq(question, expected_keywords):
    results = search_faq(question)

    assert isinstance(results, list)
    assert len(results) > 0

    result_text = " ".join(
        f"{item['question']} {item['answer']}" for item in results[:3]
    ).lower()

    assert any(keyword in result_text for keyword in expected_keywords), (
        f"No expected keywords {expected_keywords} found in top 3 results: "
        f"{result_text}"
    )


def test_search_returns_at_most_three_results():
    results = search_faq("membership at GreenField Farmers")

    assert isinstance(results, list)
    assert len(results) <= 3


def test_search_results_include_similarity_score():
    results = search_faq("How can I become a member?")

    assert results
    assert "similarity_score" in results[0]
    assert isinstance(results[0]["similarity_score"], (int, float))
