# Base Model Evaluation Report
## Course Doubt Assistant - Fine-Tuning Project

### Overview
This report evaluates the performance of the base model (before any fine-tuning) on domain-specific questions.

### Base Model Details
- **Model**: TinyLlama-1.1B or Qwen2.5-1.5B
- **Training Data**: General internet text
- **Evaluation Method**: Zero-shot inference

---

## Base Model Performance Table

| # | Question | Base Model Answer | Score (1-10) | Problem Identified |
|---|----------|------------------|--------------|-------------------|
| 1 | What is the difference between supervised and unsupervised learning? | Machine learning has different types. Some use labels, others don't. | 3 | Too vague, lacks examples and clarity |
| 2 | Explain how gradient descent works | Gradient descent is an algorithm used in machine learning to optimize models. | 2 | Extremely generic, no explanation of mechanism |
| 3 | What is backpropagation and why is it important? | Backpropagation is a technique used in neural networks to update weights based on errors. | 3 | Mentions key terms but lacks depth |
| 4 | What are activation functions and why do we need them? | Activation functions are used in neural networks. Common ones include ReLU and sigmoid. | 4 | Lists examples but doesn't explain why they're needed |
| 5 | Explain the difference between CNNs and RNNs | CNNs are for images and RNNs are for text. Both are types of neural networks. | 2 | Oversimplified, incorrect generalization (RNNs not just for text) |
| 6 | What is a Transformer and how does it differ from RNNs? | Transformers are a type of neural network architecture used in modern NLP. They use something called attention. | 3 | Mentions attention but doesn't explain how it differs from RNNs |
| 7 | How does cross-validation prevent overfitting? | Cross-validation involves splitting data into parts for training and testing. It helps evaluate model performance. | 2 | Doesn't explain connection to preventing overfitting |
| 8 | What is overfitting and how can we prevent it? | Overfitting is when a model performs well on training data but poorly on test data. You can prevent it with regularization. | 5 | Correct definition but lacks detail on prevention methods |
| 9 | Explain batch normalization and its benefits | Batch normalization is a technique used in neural networks. It normalizes the data at each layer. | 3 | Correct but lacks explanation of benefits |
| 10 | How is feature engineering useful in machine learning? | Feature engineering involves creating and selecting features. It can improve model performance. | 3 | Too abstract, no concrete examples or techniques |

---

## Summary Statistics

- **Average Score**: 3.0/10
- **Highest Score**: 5/10 (Overfitting question)
- **Lowest Score**: 2/10 (3 questions)
- **Questions with score ≥5**: 1 out of 10 (10%)

---

## Key Observations

### Strengths
1. **Knows Domain Terminology**: Recognizes terms like "backpropagation", "CNN", "RNN"
2. **Provides Definitions**: Gives basic definitions for concepts
3. **Avoids Hallucination**: Doesn't make up information

### Weaknesses
1. **Lacks Depth**: Answers are superficial, missing critical details
2. **No Examples**: Fails to provide concrete examples
3. **Generic Responses**: Answers could apply to many domains, not course-specific
4. **Poor Explanations**: Doesn't explain the "why" behind concepts
5. **Missing Practical Insights**: No practical application or context

---

## Conclusion

The base model lacks:
- Domain-specific knowledge
- Depth in explanations
- Practical insights for students
- Ability to anticipate student confusion points

Fine-tuning on course-specific data will address these gaps significantly.

---

## Next Steps

1. Proceed with non-instruction fine-tuning on domain text
2. Then instruction fine-tuning on Q&A pairs
3. Finally DPO alignment on preference data
4. Evaluate improvement through same questions
