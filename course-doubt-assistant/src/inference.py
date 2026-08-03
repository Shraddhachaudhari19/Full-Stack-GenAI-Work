#!/usr/bin/env python3
"""
Course Doubt Assistant - Inference Script
Usage: python src/inference.py --question "Your question here"
"""

import argparse
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import os

class CourseDoubtAssistant:
    def __init__(self, model_path="./models/dpo_aligned_adapter", base_model="unsloth/tinyllama-bnb-4bit"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading model from {model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(base_model, device_map="auto", torch_dtype=torch.float16)
        if os.path.isdir(model_path) and os.path.exists(os.path.join(model_path, "adapter_config.json")):
            self.model = PeftModel.from_pretrained(self.model, model_path)
        self.model.eval()
        print(f"Model loaded on {self.device}")

    def answer_question(self, question, max_length=200, temperature=0.7):
        prompt = f"### Instruction:\n{question}\n### Response:\n"
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(inputs.input_ids, max_length=max_length, temperature=temperature, top_p=0.9, do_sample=True, pad_token_id=self.tokenizer.eos_token_id)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        if "### Response:" in response:
            response = response.split("### Response:")[1].strip()
        return response

    def interactive_mode(self):
        print("\n" + "="*60)
        print("Course Doubt Assistant - Interactive Mode")
        print("Type 'exit' to quit")
        print("="*60 + "\n")
        while True:
            question = input("You: ").strip()
            if question.lower() == "exit":
                print("Thank you for using Course Doubt Assistant!")
                break
            if not question:
                continue
            print("\nAssistant: ", end="", flush=True)
            answer = self.answer_question(question)
            print(answer)
            print("\n" + "-"*60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Course Doubt Assistant")
    parser.add_argument("--question", type=str, help="Question to ask")
    parser.add_argument("--model", type=str, default="./models/dpo_aligned_adapter", help="Path to model")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    args = parser.parse_args()
    assistant = CourseDoubtAssistant(model_path=args.model)
    if args.interactive:
        assistant.interactive_mode()
    elif args.question:
        print(f"Question: {args.question}\n")
        answer = assistant.answer_question(args.question)
        print(f"Answer:\n{answer}\n")
    else:
        assistant.interactive_mode()

if __name__ == "__main__":
    main()
