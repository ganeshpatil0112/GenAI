"""
Comprehensive Testing Script for All Fine-tuned Models
Tests each model with domain-specific queries
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import os

def load_and_test_model(model_path, model_type, test_queries, base_model='TinyLlama/TinyLlama-1.1B-Chat-v1.0'):
    """Load model and generate responses"""
    print(f"\n{'='*60}")
    print(f"Testing {model_type.upper()} Model")
    print(f"{'='*60}")
    
    if not os.path.exists(model_path):
        print(f"❌ Model not found at: {model_path}")
        print(f"   Please train the model first!")
        return
    
    print(f"Loading model from: {model_path}")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        if 'peft' in model_type.lower() or 'lora' in model_type.lower() or 'qlora' in model_type.lower():
            # Load PEFT/LoRA/QLoRA models
            base = AutoModelForCausalLM.from_pretrained(
                base_model,
                device_map='auto' if torch.cuda.is_available() else None,
                low_cpu_mem_usage=True
            )
            if torch.cuda.is_available():
                base = base.half()
            model = PeftModel.from_pretrained(base, model_path)
        else:
            # Load full fine-tuned models
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                device_map='auto' if torch.cuda.is_available() else None,
                low_cpu_mem_usage=True
            )
            if torch.cuda.is_available():
                model = model.half()
        
        model.eval()
        print("✓ Model loaded successfully!\n")
        
        # Test with queries
        for i, query in enumerate(test_queries, 1):
            print(f"\n{'-'*60}")
            print(f"Query {i}: {query}")
            print(f"{'-'*60}")
            
            prompt = f"### Instruction: {query}\n### Response:"
            inputs = tokenizer(prompt, return_tensors="pt")
            
            if torch.cuda.is_available():
                inputs = {k: v.to('cuda') for k, v in inputs.items()}
            
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
            # Extract only the response part
            response = response.split("### Response:")[-1].strip()
            
            print(f"\nResponse:\n{response}\n")
        
    except Exception as e:
        print(f"❌ Error loading/testing model: {str(e)}")

def test_all_models():
    """Test all fine-tuned models"""
    
    print("\n" + "="*60)
    print("LLM FINE-TUNING PROJECT - MODEL TESTING")
    print("="*60)
    print(f"Device: {'GPU (CUDA)' if torch.cuda.is_available() else 'CPU'}")
    print("="*60)
    
    # HR Model - Full Fine-tuning
    hr_queries = [
        "How do I apply for casual leave?",
        "What is the company's work from home policy?",
        "How is gratuity calculated?"
    ]
    load_and_test_model('models/hr_full_finetuned', 'HR - Full Fine-tuning', hr_queries)
    
    # Finance Model - DPO
    finance_queries = [
        "What is the current GST rate for restaurants?",
        "How can I save income tax legally?",
        "Explain PPF scheme in simple terms"
    ]
    load_and_test_model('models/finance_dpo_finetuned', 'Finance - DPO', finance_queries)
    
    # Sales Model - PEFT
    sales_queries = [
        "Customer wants to return a product bought during sale",
        "How to handle delivery delay complaint?",
        "Explain EMI options for laptop purchase"
    ]
    load_and_test_model('models/sales_peft_finetuned', 'Sales - PEFT', sales_queries)
    
    # Healthcare Model - LoRA
    healthcare_queries = [
        "What are symptoms of dengue fever?",
        "How to manage diabetes with Indian diet?",
        "What are Ayurvedic remedies for acidity?"
    ]
    load_and_test_model('models/healthcare_lora_finetuned', 'Healthcare - LoRA', healthcare_queries)
    
    # Marketing Model - QLoRA
    marketing_queries = [
        "Create Diwali campaign for e-commerce",
        "How to use influencer marketing for beauty brand?",
        "Develop loyalty program for fashion retail"
    ]
    load_and_test_model('models/marketing_qlora_finetuned', 'Marketing - QLoRA', marketing_queries)
    
    print("\n" + "="*60)
    print("TESTING COMPLETED!")
    print("="*60)

if __name__ == "__main__":
    test_all_models()

