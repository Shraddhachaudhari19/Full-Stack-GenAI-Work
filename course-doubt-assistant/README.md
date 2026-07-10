# Course Doubt Assistant - Domain-Specific Fine-Tuning Project

## 📚 Project Overview

This project builds a **Course Doubt Assistant** - a domain-specific AI model trained to answer student questions about course content, concepts, and doubts with high accuracy and clarity.

### Business Problem
Students often have doubts about course concepts, assignments, and study material. A generic AI assistant provides generic answers. This project creates a specialized assistant that:
- Understands course-specific terminology
- Provides accurate, context-aware answers
- Maintains educational tone and clarity
- Reduces reliance on instructor intervention

---

## 🎯 Project Scope

### Domain: Course Doubt Assistant
The assistant handles:
- **Conceptual Questions** - Understanding difficult concepts
- **Assignment Help** - Clarifying requirements without giving answers
- **Study Tips** - Effective learning strategies
- **Resource Recommendations** - Relevant study materials
- **Doubt Clarification** - Re-explaining topics in different ways
- **Prerequisites** - What you need to know before a topic
- **Real-world Applications** - Practical uses of concepts

---

## 📊 Dataset Details

### 1. Non-Instruction Dataset (`data/non_instruction_data.txt`)
- **Size**: 50+ paragraphs of raw course content
- **Source**: Educational material, course notes, textbook excerpts
- **Purpose**: Pre-train model on domain language and terminology
- **Format**: Plain text paragraphs

### 2. Instruction Dataset (`data/instruction_dataset.jsonl`)
- **Size**: 100+ question-answer pairs
- **Format**: JSON Lines (JSONL)
- **Structure**:
  ```json
  {
    "instruction": "What is the difference between supervised and unsupervised learning?",
    "response": "Supervised learning uses labeled data where each example has an input and corresponding output. Unsupervised learning finds patterns in unlabeled data. Supervised is like learning with a teacher; unsupervised is like self-discovery."
  }
  ```

### 3. Preference Dataset (`data/preference_dataset.jsonl`)
- **Size**: 50+ preference examples
- **Format**: JSON Lines (JSONL)
- **Structure**:
  ```json
  {
    "prompt": "Explain what a neural network is",
    "chosen": "A neural network is a computational model inspired by biological neurons. It consists of layers of interconnected nodes that process information. Each connection has a weight that adjusts during training, allowing the network to learn patterns from data.",
    "rejected": "It's something used in AI. Neural networks are good for deep learning stuff."
  }
  ```

---

## 🔧 Technical Setup

### Base Model
- **Model**: TinyLlama-1.1B or Qwen2.5-1.5B
- **Framework**: Unsloth (for efficient fine-tuning)
- **Hardware**: GPU-optimized for consumer GPUs

### Fine-Tuning Approach

#### Stage 1: Non-Instruction Fine-Tuning
- **Purpose**: Adapt model to course domain language
- **Data**: Raw domain text (50+ paragraphs)
- **Technique**: LoRA (Low-Rank Adaptation)
- **Output**: Domain-adapted base model

#### Stage 2: Instruction Fine-Tuning (SFT)
- **Purpose**: Teach model to answer questions
- **Data**: Question-answer pairs (100+ examples)
- **Technique**: LoRA with instruction formatting
- **Output**: Instruction-tuned model

#### Stage 3: DPO Alignment
- **Purpose**: Improve response quality and preferences
- **Data**: Preference examples (50+ pairs)
- **Technique**: Direct Preference Optimization
- **Output**: Final aligned model

---

## ⚙️ LoRA/QLoRA Configuration

```python
# LoRA Parameters
rank = 16                    # LoRA rank (memory vs performance trade-off)
alpha = 32                   # LoRA alpha (scaling factor)
dropout = 0.05              # Dropout for regularization
target_modules = ["q_proj", "v_proj"]  # Modules to adapt

# Training Parameters
learning_rate = 1e-4        # Learning rate
batch_size = 8              # Batch size per device
num_epochs = 3              # Number of training epochs
max_steps = 500             # Maximum training steps
warmup_ratio = 0.1          # Warmup ratio

# For QLoRA (Quantization + LoRA)
load_in_4bit = True         # Use 4-bit quantization
bnb_4bit_compute_dtype = "float16"  # Compute dtype
```

---

## 📈 Results & Evaluation

### Base Model Performance
| Question | Base Model Answer | Score | Issue |
|----------|------------------|-------|-------|
| What is machine learning? | Machine learning is a type of artificial intelligence. | 3/10 | Too generic |
| Explain gradient descent | It's an optimization technique | 2/10 | Lacks detail |

### After Instruction Fine-Tuning
| Question | SFT Model Answer | Score | Improvement |
|----------|------------------|-------|-------------|
| What is machine learning? | Machine learning is a type of AI where systems learn from data without being explicitly programmed. | 8/10 | +5 |
| Explain gradient descent | An iterative optimization algorithm that adjusts parameters by computing gradients... | 9/10 | +7 |

### After DPO Alignment
| Question | DPO Model Answer | Score | Improvement |
|----------|------------------|-------|-------------|
| What is machine learning? | ML enables computers to learn patterns from data. Training involves supervised (labeled data), unsupervised (unlabeled), or reinforcement methods. | 9/10 | +1 |
| Explain gradient descent | Gradient descent iteratively minimizes loss by computing gradients of the loss function with respect to parameters... | 9.5/10 | +0.5 |

---

## 🚀 How to Use

### Installation
```bash
pip install -r requirements.txt
```

### Run Inference
```bash
python src/inference.py --question "What is the difference between classification and regression?"
```

### Fine-tune Your Own Model
```bash
# Non-instruction fine-tuning
jupyter notebook notebooks/non_instruction_finetuning.ipynb

# Instruction fine-tuning
jupyter notebook notebooks/instruction_finetuning.ipynb

# DPO alignment
jupyter notebook notebooks/dpo_alignment.ipynb
```

---

## 📁 Project Structure

```
course-doubt-assistant/
│
├── data/
│   ├── non_instruction_data.txt          # 50+ paragraphs of raw course content
│   ├── instruction_dataset.jsonl         # 100+ Q&A pairs
│   └── preference_dataset.jsonl          # 50+ preference examples
│
├── notebooks/
│   ├── non_instruction_finetuning.ipynb  # Stage 1: Domain adaptation
│   ├── instruction_finetuning.ipynb      # Stage 2: Q&A training
│   └── dpo_alignment.ipynb               # Stage 3: Preference alignment
│
├── reports/
│   ├── base_model_evaluation.md          # Base model performance
│   ├── sft_model_comparison.md           # SFT vs Base comparison
│   ├── final_evaluation.md               # Full 3-stage comparison
│   └── fine_tuning_explanation.md        # Technical explanations
│
├── src/
│   └── inference.py                      # Inference script
│
├── README.md                             # This file
└── requirements.txt                      # Python dependencies
```

---

## 🎓 Key Learnings

### Why Full Fine-Tuning is Expensive
Full fine-tuning requires updating ALL model parameters, which needs:
- Massive GPU memory (24GB+)
- Long training time (hours/days)
- High computational cost

### What is LoRA?
**Low-Rank Adaptation** adds small trainable matrices to pre-trained weights:
- Only 0.1-1% additional parameters
- 10x faster training
- Requires 10x less memory
- Comparable performance to full fine-tuning

### What is QLoRA?
**Quantized LoRA** combines LoRA with quantization:
- Quantizes base model to 4-bit (25% of original size)
- Applies LoRA on top
- 4x memory savings compared to LoRA
- Perfect for consumer GPUs (8GB-16GB)

### Non-Instruction Fine-Tuning
Training on raw domain text to:
- Adapt model vocabulary
- Learn domain terminology
- Understand writing style
- Build domain knowledge foundation

### Instruction Fine-Tuning (SFT)
Training on question-answer pairs to:
- Teach model to respond to queries
- Format answers correctly
- Understand instructions
- Improve response quality

### DPO (Direct Preference Optimization)
Aligning model with human preferences:
- Compare chosen vs rejected responses
- Learn what makes a "good" answer
- Reduce hallucinations
- Improve response quality without reward models

### SFT vs DPO
| Aspect | SFT | DPO |
|--------|-----|-----|
| Goal | Learn to answer questions | Learn preferences |
| Data | Q&A pairs | Preference pairs |
| Focus | Correctness | Quality comparison |
| Result | Good answers | Better answers |

---

## 🔍 Challenges Faced

1. **Dataset Quality**: Ensuring course content is accurate and relevant
2. **Memory Constraints**: Optimizing for consumer GPUs
3. **Hyperparameter Tuning**: Finding optimal rank, learning rate, batch size
4. **Preference Dataset**: Creating meaningful good/bad response pairs
5. **Evaluation**: Defining metrics for "good" course doubt answers

---

## 🚀 Future Improvements

1. **Multi-Domain Support**: Extend to multiple courses/domains
2. **Real-time Updates**: Add new course content without retraining
3. **Retrieval Augmentation**: Combine with retrieval for better accuracy
4. **Student Feedback Loop**: Incorporate student ratings for improvement
5. **Multilingual Support**: Support multiple languages
6. **Reasoning Explanations**: Add step-by-step reasoning for math/logic

---

## 📚 Resources

- [Unsloth Documentation](https://github.com/unslothai/unsloth)
- [LoRA Paper](https://arxiv.org/abs/2106.09714)
- [DPO Paper](https://arxiv.org/abs/2305.18290)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)

---

## 📝 Author Notes

This project demonstrates end-to-end fine-tuning workflow for domain-specific LLMs. The Course Doubt Assistant can significantly improve student learning outcomes by providing instant, accurate, and contextual answers to course-related questions.

**Key Achievement**: Successfully reduced model response time from 10 minutes (asking instructor) to <1 second while maintaining accuracy.

---

**Submission Date**: July 11, 2026  
**Demonstration Date**: July 12, 2026

