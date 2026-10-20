# GreenField Farmers FAQ Assistant — Evaluation

## Method

Precision@3 is calculated as the number of relevant retrieved FAQs divided by the number of retrieved FAQs, up to three per question. Relevance is judged using the keywords below as a simple heuristic; it is not a human-validated relevance assessment.

## Results

### Question: How can I become a member?

- Relevant: Do I need to be a farmer to become a member? (similarity: 0.547)
- Relevant: How can I become a member of GreenField Farmers? (similarity: 0.520)
- Relevant: Is there a membership fee? (similarity: 0.481)

- Relevant results: 3/3

### Question: Is there a membership fee?

- Relevant: Is there a membership fee? (similarity: 1.000)
- Relevant: Are prices different for members and non-members? (similarity: 0.502)
- Relevant: How do I update my membership details? (similarity: 0.348)

- Relevant results: 3/3

### Question: What seasonal produce is available?

- Relevant: What fruits and vegetables are in season now? (similarity: 0.772)
- Relevant: Can I request a specific seasonal crop? (similarity: 0.691)
- Relevant: What produce does GreenField Farmers sell? (similarity: 0.584)

- Relevant results: 3/3

### Question: How does the co-op support sustainability?

- Relevant: Does the co-op support soil health? (similarity: 0.648)
- Relevant: Does the co-op use water-saving methods? (similarity: 0.568)
- Relevant: What sustainable farming practices do member farms use? (similarity: 0.433)

- Relevant results: 3/3

### Question: How can I contact GreenField Farmers?

- Relevant: How can I contact GreenField Farmers with another question? (similarity: 0.959)
- Relevant: Who can join GreenField Farmers? (similarity: 0.835)
- Relevant: How can I become a member of GreenField Farmers? (similarity: 0.829)

- Relevant results: 3/3

## Summary

- Test questions: 5
- FAQs retrieved: 15
- Results marked relevant by keyword heuristic: 15
- **Micro-averaged Precision@3: 100.00%**

## Limitations

This small evaluation uses keyword matching as a relevance proxy. It can misclassify relevant results and should not be treated as a human-reviewed benchmark.
