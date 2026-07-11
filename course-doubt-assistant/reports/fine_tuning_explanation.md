# Fine-Tuning Techniques Explanation
## Course Doubt Assistant - Fine-Tuning Project

---

## 1. Why Full Fine-Tuning is Expensive

Full fine-tuning updates ALL model parameters during training.

### Memory Requirements
- Large Language Models like GPT or Llama have billions of parameters
- Each parameter needs to store: weight, gradient, and optimizer state
- Example: 7B model requires ~84GB memory for full fine-tuning (7B parameters × 3 × 4 bytes)

### Computational Cost
- Training time: hours to days depending on data size and GPU
- Requires high-end GPUs (A100, H100)
- Expensive cloud infrastructure or specialized hardware
- Cost: often $1000+ per model fine-tuning run

### Practical Challenges
- Only accessible to organizations with significant resources
- Prohibitive for researchers and small teams
- Overkill for domain adaptation (small target data)

---

## 2. What is LoRA (Low-Rank Adaptation)?

LoRA adds learnable low-rank matrices to pre-trained weights without modifying them.

### How It Works
```
Original weight: W (d_out × d_in)
LoRA adds: W_A (d_out × r) × W_B (r × d_in)
Total parameters: W_A + W_B = (d_out + d_in) × r
```

### Mathematical Detail
- Instead of updating W, we compute: W' = W + α/r × W_A × W_B
- W_A: initialized randomly, learns during training
- W_B: initialized to zero (no change initially)
- Rank r: typically 8-16 (much smaller than d_in, d_out)

### Benefits
1. **Memory Efficient**: 99% parameter reduction
   - Original: 7B parameters
   - LoRA: ~0.07B parameters (1% overhead)
2. **Speed**: 10x faster training
   - Smaller gradient computation
   - Fewer matrix multiplications
3. **Multiple Adapters**: Can train many LoRA adapters for different tasks, reuse base model
4. **Quality**: Comparable performance to full fine-tuning

### Limitation
- Cannot adapt to drastically different domains
- Works best for incremental learning

---

## 3. What is QLoRA (Quantized LoRA)?

QLoRA combines quantization with LoRA for extreme efficiency.

### How It Works
1. **Quantize Base Model**: Reduce weights from 32-bit to 4-bit
   - 7B model: 28GB → 7GB (4x compression)
2. **Apply LoRA**: Add trainable low-rank adapters
3. **Back to 32-bit During Backprop**: Dequantize before gradients (for accuracy)

### Quantization Types
- **4-bit Quantization**: 4 values per byte
  - NF4 (normalized float 4-bit): optimal for weights
  - FP4 (floating point 4-bit): simpler but less optimal
- **Dequantization**: Scales back to higher precision for computation

### Benefits
1. **Extreme Memory Savings**: 4x reduction
   - 7B model + LoRA: ~16GB memory (fits on consumer GPU)
2. **Still Accurate**: Minimal performance degradation
3. **Consumer-Friendly**: Run on 8GB-16GB GPUs
4. **Cost-Effective**: No expensive hardware needed

### Trade-offs
- Slightly slower inference (dequantization overhead)
- Minor accuracy loss compared to LoRA
- Still faster overall than full fine-tuning

---

## 4. Why QLoRA is Useful on Limited GPU

### Hardware Constraints
```
Memory Comparison:
- Full Fine-Tuning: 84GB (impractical)
- LoRA: 14GB (still demanding)
- QLoRA: 3.5GB (consumer GPU friendly)
```

### Use Cases
- **Academic Researchers**: Limited GPU budget
- **Individual Practitioners**: Personal laptops with 8GB GPU
- **Startups**: Cost-sensitive fine-tuning
- **Educational Settings**: Learning on accessible hardware

### Performance Trade-off
- Speed: QLoRA ~20% slower than LoRA
- Accuracy: QLoRA ~2% lower than LoRA (acceptable for most tasks)
- Memory: QLoRA 4x better than LoRA

---

## 5. Non-Instruction Fine-Tuning

Training on raw domain text without specific questions/answers.

### Purpose
1. **Domain Adaptation**: Teach model domain vocabulary and terminology
2. **Language Pattern Learning**: Understand writing style of domain
3. **Knowledge Transfer**: Absorb domain-specific knowledge
4. **Foundation Building**: Prepare model before instruction tuning

### Data
- 50+ paragraphs of raw course text
- Textbooks, lecture notes, documentation
- No question-answer structure needed

### Technique
- Causal Language Modeling: predict next token given previous tokens
- Loss: cross-entropy between predicted and actual next token
- Standard transformer training objective

### Expected Outcomes
- Model learns domain terminology
- Improves vocabulary knowledge
- Better language understanding within domain
- Foundation for instruction fine-tuning

### When to Skip
- If domain is very similar to pre-training data
- If only small amount of data available
- Time is critical

---

## 6. Instruction Fine-Tuning (SFT)

Training on question-answer pairs to teach the model to respond to queries.

### Purpose
1. **Response Formatting**: Teach model to format answers properly
2. **Question Understanding**: Understand what questions are asking
3. **Answer Quality**: Improve response quality for specific tasks
4. **Instruction Following**: Respond to instructions correctly

### Data Structure
```json
{
  "instruction": "What is machine learning?",
  "response": "Machine learning is..."
}
```

### Training Process
1. Concatenate instruction and response: `[instruction] → [response]`
2. Compute loss only on response tokens
3. Update weights to predict correct responses

### Dataset Size
- Minimum 100 Q&A pairs recommended
- Quality > Quantity (50 high-quality pairs > 1000 low-quality)
- Diverse questions covering domain breadth

### Expected Outcomes
- Model learns to answer questions
- Responses become more helpful and specific
- Better understanding of domain queries
- Foundation for preference alignment

### Hyperparameters Used
- Epochs: 3
- Learning Rate: 1e-4 (lower than pre-training)
- Batch Size: 8
- Max Sequence Length: 512

---

## 7. What is DPO (Direct Preference Optimization)?

DPO aligns model with human preferences without needing a reward model.

### Traditional RLHF (Reinforcement Learning from Human Feedback)
1. Train reward model on preference data
2. Use reward model to generate scores
3. Use RL to optimize policy based on scores
4. Complex, requires multiple models

### DPO Approach
1. **Direct Preference Learning**: Learn preferences directly without reward model
2. **Simpler**: Only needs language model and preferences
3. **More Stable**: No RL instability
4. **Faster**: Single training phase

### Mathematical Intuition
```
Objective: Maximize log P(chosen | prompt) - log P(rejected | prompt)
This directly optimizes model to prefer chosen over rejected responses
```

### Training Process
1. Compute likelihood of chosen response: log P(y_c | x)
2. Compute likelihood of rejected response: log P(y_r | x)
3. Loss encourages chosen to be more likely than rejected
4. Update model weights

### Data Format
```json
{
  "prompt": "What is ML?",
  "chosen": "Machine learning enables systems to learn from data...",
  "rejected": "ML is complex and not worth learning."
}
```

### Benefits
1. **No Reward Model**: Simpler than RLHF
2. **More Stable**: No RL training instability
3. **Better Alignment**: Direct preference optimization
4. **Fewer Parameters**: Only train language model

---

## 8. Difference Between SFT and DPO

| Aspect | SFT | DPO |
|--------|-----|-----|
| **Goal** | Predict correct answers | Align with preferences |
| **Data** | Q&A pairs | Preference pairs (chosen/rejected) |
| **Training** | Likelihood maximization | Preference optimization |
| **Metric** | Accuracy on answers | Preference alignment |
| **Stage** | Stage 2 | Stage 3 (after SFT) |
| **Use Case** | Learn to answer questions | Improve answer quality |

### Conceptual Difference
- **SFT**: "Learn what correct answers look like"
- **DPO**: "Learn which answers are better than others"

### Why Both?
- SFT teaches facts and structure
- DPO teaches preference (quality, tone, safety)
- Combined: accurate AND high-quality responses

---

## 9. Hyperparameter Values Used

### Non-Instruction Fine-Tuning
```python
# LoRA Configuration
rank = 16                      # Low-rank matrices rank
alpha = 32                     # Scaling factor (alpha/rank)
dropout = 0.05                 # Regularization
target_modules = ["q_proj", "v_proj"]  # Layers to adapt

# Training Configuration
learning_rate = 2e-4           # Step size
batch_size = 16                # Samples per batch
num_epochs = 1                 # Single epoch for pre-training
max_steps = 500                # Maximum training steps
warmup_ratio = 0.1             # Learning rate warmup
gradient_accumulation = 4      # Accumulate before update
```

### Instruction Fine-Tuning
```python
# LoRA Configuration (same as above)
rank = 16
alpha = 32
dropout = 0.05
target_modules = ["q_proj", "v_proj"]

# Training Configuration
learning_rate = 1e-4           # Lower for fine-tuning
batch_size = 8                 # Smaller batch
num_epochs = 3                 # Multiple epochs
max_steps = 1000               # More steps for Q&A
warmup_ratio = 0.1
gradient_accumulation = 4
```

### DPO Alignment
```python
# LoRA Configuration
rank = 16
alpha = 32
dropout = 0.05
target_modules = ["q_proj", "v_proj"]

# DPO-Specific
learning_rate = 5e-5           # Very small for fine preference
beta = 0.1                     # DPO temperature
batch_size = 8
num_epochs = 2                 # Fewer epochs
max_steps = 500                # Fewer steps
```

### Rationale for Values

**Rank = 16**
- Balances expressiveness and efficiency
- Smaller ranks (8) may limit adaptation
- Larger ranks (32+) increase memory
- 16 is sweet spot for domain adaptation

**Alpha = 32**
- Follows LoRA paper recommendation: alpha = 2 × rank
- 32 = 2 × 16
- Controls LoRA contribution magnitude

**Learning Rate Progression**
- Pre-training: 2e-4 (higher, raw text learning)
- SFT: 1e-4 (moderate, Q&A tuning)
- DPO: 5e-5 (low, fine preference tuning)
- General: lower for finer adjustments

**Batch Size Considerations**
- Pre-training: 16 (more stable gradients)
- SFT: 8 (limited data)
- Smaller batches enable gradient accumulation
- Trade-off: larger = faster, smaller = better generalization

**Epochs Strategy**
- Pre-training: 1 epoch (large raw text data)
- SFT: 3 epochs (medium Q&A data, needs repetition)
- DPO: 2 epochs (preference data, quick learning)
- Prevent overfitting with early stopping

**Dropout = 0.05**
- Mild regularization (5% neuron dropout)
- Prevents co-adaptation
- Conservative value for domain adaptation
- Higher (0.1+) may hurt performance on small data

---

## Summary Table

| Technique | Parameters | Memory | Speed | Quality | Use Case |
|-----------|-----------|--------|-------|---------|----------|
| Full FT | 100% | High | Slow | Best | Large target data |
| LoRA | 1% | Medium | 10x faster | Good | Standard choice |
| QLoRA | 1% | Low | 20% slower | Good | Limited GPU |
| Non-Inst FT | 1% | Low | Fast | Better vocab | Pre-training |
| SFT | 1% | Low | Fast | Better answers | Q&A training |
| DPO | 1% | Low | Fast | Best answers | Preference learning |

---

## Conclusion

Modern fine-tuning uses LoRA/QLoRA with staged training:
1. **Non-instruction**: Build domain foundation
2. **Instruction**: Learn Q&A format
3. **DPO**: Align with preferences

This approach achieves near-full-training quality with 1% parameters and 10x speed improvement, making AI model fine-tuning accessible to everyone.
