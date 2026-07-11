#!/usr/bin/env python3
"""
Course Doubt Assistant - Inference Script

Usage:
    python src/inference.py --question "What is machine learning?"
    python src/inference.py --model "path/to/model" --question "Your question here"
"""

import argparse
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import os


class CourseDoubtAssistant:
    """Course-specific doubt assistant using fine-tuned model."""

    def __init__(
        self,
        model_path="./models/dpo_aligned_adapter",
        base_model="unsloth/tinyllama-bnb-4bit",
        device="cuda" if torch.cuda.is_available() else "cpu",
    ):
        """
        Initialize the assistant.

        Args:
            model_path: Path to fine-tuned model/adapter
            base_model: Base model name
            device: Device to use (cuda/cpu)
        """
        self.device = device
        print(f"Loading model from {model_path}...")

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.tokenizer.pad_token = self.tokenizer.eos_token

        # Load base model
        self.model = AutoModelForCausalLM.from_pretrained(
            base_model, device_map="auto", torch_dtype=torch.float16
        )

        # Load adapter if it exists
        if os.path.isdir(model_path) and os.path.exists(
            os.path.join(model_path, "adapter_config.json")
        ):
            self.model = PeftModel.from_pretrained(self.model, model_path)
            print(f"LoRA adapter loaded from {model_path}")

        self.model.eval()
        print(f"Model loaded on {device}")

    def answer_question(
        self, question, max_length=200, temperature=0.7, top_p=0.9, do_sample=True
    ):
        """
        Generate answer to a course doubt question.

        Args:
            question: User's question
            max_length: Maximum response length
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            do_sample: Whether to use sampling

        Returns:
            Generated answer
        """
        # Format prompt
        prompt = f"""### Instruction:
{question}
### Response:
"""

        # Tokenize
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                inputs.input_ids,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=do_sample,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        # Decode
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract only the response part
        if "### Response:" in response:
            response = response.split("### Response:")[1].strip()

        return response

    def interactive_mode(self):
        """
        Run in interactive mode for multiple questions.
        """
        print(
            "\n" + "=" * 60
        )
        print("Course Doubt Assistant - Interactive Mode")
        print("Type 'exit' to quit")
        print("=" * 60 + "\n")

        while True:
            question = input("You: ").strip()

            if question.lower() == "exit":
                print("Thank you for using Course Doubt Assistant!")
                break

            if not question:
                print("Please enter a question.\n")
                continue

            print("\nAssistant: ", end="", flush=True)
            answer = self.answer_question(question)
            print(answer)
            print("\n" + "-" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Course Doubt Assistant")
    parser.add_argument(
        "--question", type=str, help="Question to ask the assistant"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="./models/dpo_aligned_adapter",
        help="Path to fine-tuned model",
    )
    parser.add_argument(
        "--base-model",
        type=str,
        default="unsloth/tinyllama-bnb-4bit",
        help="Base model name",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode",
    )
    parser.add_argument(
        "--max-length", type=int, default=200, help="Maximum response length"
    )
    parser.add_argument(
        "--temperature", type=float, default=0.7, help="Sampling temperature"
    )

    args = parser.parse_args()

    # Initialize assistant
    assistant = CourseDoubtAssistant(
        model_path=args.model, base_model=args.base_model
    )

    if args.interactive:
        # Interactive mode
        assistant.interactive_mode()
    elif args.question:
        # Single question mode
        print(f"Question: {args.question}\n")
        answer = assistant.answer_question(
            args.question, max_length=args.max_length, temperature=args.temperature
        )
        print(f"Answer:\n{answer}\n")
    else:
        # Default interactive mode
        assistant.interactive_mode()


if __name__ == "__main__":
    main()
