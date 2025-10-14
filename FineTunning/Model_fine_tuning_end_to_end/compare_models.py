"""
Compare Multiple Models - See responses from different models side-by-side
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import os

def load_model(model_path, is_peft=False):
    """Load a model"""
    if not os.path.exists(model_path):
        return None, None
    
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    if is_peft:
        base = AutoModelForCausalLM.from_pretrained(
            'TinyLlama/TinyLlama-1.1B-Chat-v1.0',
            low_cpu_mem_usage=True
        )
        model = PeftModel.from_pretrained(base, model_path)
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            low_cpu_mem_usage=True
        )
    
    model.eval()
    return model, tokenizer

def generate_response(model, tokenizer, query, max_tokens=150):
    """Generate response from model"""
    prompt = f"### Instruction: {query}\n### Response:"
    inputs = tokenizer(prompt, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = response.split("### Response:")[-1].strip()
    return response

def compare_models(query, models_to_compare):
    """
    Compare responses from multiple models
    
    Args:
        query: Question to ask
        models_to_compare: List of tuples (name, path, is_peft)
    """
    print("\n" + "="*80)
    print(f"Query: {query}")
    print("="*80)
    
    for name, path, is_peft in models_to_compare:
        print(f"\n{'─'*80}")
        print(f"Model: {name}")
        print(f"{'─'*80}")
        
        model, tokenizer = load_model(path, is_peft)
        
        if model is None:
            print("❌ Model not found")
            continue
        
        print("Generating...")
        response = generate_response(model, tokenizer, query)
        print(f"\n{response}\n")
        
        # Clean up to free memory
        del model, tokenizer
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

if __name__ == "__main__":
    print("\n" + "="*80)
    print(" "*25 + "MODEL COMPARISON")
    print("="*80)
    
    # Define models to compare (only available ones)
    models = [
        ("HR - Full Fine-tuning", "models/hr_full_finetuned", False),
        ("Sales - PEFT", "models/sales_peft_finetuned", True),
        ("Healthcare - LoRA", "models/healthcare_lora_finetuned", True),
        ("Marketing - QLoRA", "models/marketing_qlora_finetuned", True),
    ]
    
    # Test queries for different domains
    queries = [
        "How do I apply for leave in the company?",  # HR
        "What are symptoms of fever?",  # Healthcare
        "How to handle customer complaints?",  # Sales
    ]
    
    for query in queries:
        compare_models(query, models)
        print("\n" + "="*80 + "\n")
    
    print("✓ Comparison complete!\n")

