
import json
from pathlib import Path

from search_faq import search_faq

TEST_CASES = [
    {
        "question": "How can I become a member?",
        "keywords": ["member", "membership"],
    },
    {
        "question": "Is there a membership fee?",
        "keywords": ["membership", "fee", "price", "cost"],
    },
    {
        "question": "What seasonal produce is available?",
        "keywords": ["seasonal", "produce", "harvest", "vegetable", "fruit"],
    },
    {
        "question": "How does the co-op support sustainability?",
        "keywords": ["soil", "water", "sustainable", "farm", "conservation"],
    },
    {
        "question": "How can I contact GreenField Farmers?",
        "keywords": ["contact", "email", "phone", "reach"],
    },
]


def main():
    total_relevant = 0
    total_retrieved = 0
    report_lines = [
        "# GreenField Farmers FAQ Assistant — Evaluation",
        "",
        "## Method",
        "",
        "Precision@3 is calculated as the number of relevant retrieved FAQs "
        "divided by the number of retrieved FAQs, up to three per question. "
        "Relevance is judged using the keywords below as a simple heuristic; "
        "it is not a human-validated relevance assessment.",
        "",
        "## Results",
        "",
    ]

    for case in TEST_CASES:
        results = search_faq(case["question"])[:3]
        relevant = 0

        report_lines.extend(
            [
                f"### Question: {case['question']}",
                "",
            ]
        )

        for item in results:
            text = f"{item['question']} {item['answer']}".lower()
            is_relevant = any(
                keyword in text for keyword in case["keywords"]
            )

            if is_relevant:
                relevant += 1

            report_lines.append(
                f"- {'Relevant' if is_relevant else 'Not marked relevant'}: "
                f"{item['question']} "
                f"(similarity: {item.get('similarity_score', 0):.3f})"
            )

        total_relevant += relevant
        total_retrieved += len(results)

        report_lines.extend(
            [
                "",
                f"- Relevant results: {relevant}/{len(results)}",
                "",
            ]
        )

    precision_at_3 = (
        total_relevant / total_retrieved if total_retrieved else 0.0
    )

    report_lines.extend(
        [
            "## Summary",
            "",
            f"- Test questions: {len(TEST_CASES)}",
            f"- FAQs retrieved: {total_retrieved}",
            f"- Results marked relevant by keyword heuristic: {total_relevant}",
            f"- **Micro-averaged Precision@3: {precision_at_3:.2%}**",
            "",
            "## Limitations",
            "",
            "This small evaluation uses keyword matching as a relevance "
            "proxy. It can misclassify relevant results and should not be "
            "treated as a human-reviewed benchmark.",
            "",
        ]
    )

    output_path = Path(__file__).resolve().parent / "evaluation.md"
    output_path.write_text("\n".join(report_lines), encoding="utf-8")

    print(f"Evaluation report written to: {output_path}")
    print(f"Micro-averaged Precision@3: {precision_at_3:.2%}")


if __name__ == "__main__":
    main()
