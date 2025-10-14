"""
Interactive Model Testing - Test any model with your own queries
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import sys

def test_model_interactive(model_path, model_type='lora', base_model='TinyLlama/TinyLlama-1.1B-Chat-v1.0'):
    """
    Test a model interactively with custom queries
    
    Args:
        model_path: Path to trained model
        model_type: 'full' or 'lora'/'peft'/'qlora' for PEFT models
        base_model: Base model name (for PEFT models)
    """
    print("\n" + "="*60)
    print(f"Interactive Testing: {model_path}")
    print("="*60)
    
    # Load model
    print("\nLoading model...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    if model_type in ['lora', 'peft', 'qlora']:
        base = AutoModelForCausalLM.from_pretrained(
            base_model,
            low_cpu_mem_usage=True
        )
        model = PeftModel.from_pretrained(base, model_path)
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            low_cpu_mem_usage=True
        )
    
    model.eval()
    print("✓ Model loaded!\n")
    
    # Interactive loop
    print("Enter your queries (type 'quit' to exit):\n")
    
    while True:
        query = input("Query: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("\nExiting...")
            break
        
        if not query:
            continue
        
        # Generate response
        prompt = f"### Instruction: {query}\n### Response:"
        inputs = tokenizer(prompt, return_tensors="pt")
        
        print("\nGenerating response...\n")
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=200,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response.split("### Response:")[-1].strip()
        
        print("-" * 60)
        print("Response:")
        print("-" * 60)
        print(response)
        print("-" * 60)
        print()

if __name__ == "__main__":
    # Default: Test Healthcare LoRA model
    model_path = "models/healthcare_lora_finetuned"
    model_type = "lora"
    
    # You can change these to test different models:
    # model_path = "models/hr_full_finetuned"
    # model_type = "full"
    
    # model_path = "models/sales_peft_finetuned"
    # model_type = "peft"
    
    # model_path = "models/marketing_qlora_finetuned"
    # model_type = "qlora"
    
    print("\n" + "="*60)
    print("Interactive Model Testing")
    print("="*60)
    print(f"\nTesting: {model_path}")
    print(f"Type: {model_type}")
    print("\nYou can modify the script to test different models.")
    print("="*60)
    
    test_model_interactive(model_path, model_type)

