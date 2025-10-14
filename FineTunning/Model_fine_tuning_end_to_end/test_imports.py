"""
Quick test to verify all imports and basic functionality
"""

print("Testing imports...")

try:
    import torch
    print("✓ PyTorch imported")
    print(f"  Version: {torch.__version__}")
    print(f"  CUDA available: {torch.cuda.is_available()}")
    
    from transformers import AutoTokenizer, AutoModelForCausalLM
    print("✓ Transformers imported")
    
    from peft import LoraConfig, get_peft_model, TaskType
    print("✓ PEFT imported")
    
    from trl import DPOTrainer
    print("✓ TRL imported")
    
    import json
    from datasets import Dataset
    print("✓ Datasets imported")
    
    print("\n" + "="*50)
    print("All imports successful! ✓")
    print("="*50)
    
    # Test dataset loading
    print("\nTesting dataset loading...")
    with open('datasets/hr_dataset.json', 'r', encoding='utf-8') as f:
        hr_data = json.load(f)
    print(f"✓ HR Dataset: {len(hr_data)} samples")
    
    with open('datasets/finance_dpo_dataset.json', 'r', encoding='utf-8') as f:
        finance_data = json.load(f)
    print(f"✓ Finance DPO Dataset: {len(finance_data)} samples")
    
    with open('datasets/sales_dataset.json', 'r', encoding='utf-8') as f:
        sales_data = json.load(f)
    print(f"✓ Sales Dataset: {len(sales_data)} samples")
    
    with open('datasets/healthcare_dataset.json', 'r', encoding='utf-8') as f:
        health_data = json.load(f)
    print(f"✓ Healthcare Dataset: {len(health_data)} samples")
    
    with open('datasets/marketing_dataset.json', 'r', encoding='utf-8') as f:
        marketing_data = json.load(f)
    print(f"✓ Marketing Dataset: {len(marketing_data)} samples")
    
    print("\n" + "="*50)
    print("All datasets loaded successfully! ✓")
    print("="*50)
    
    print("\n✨ System is ready for training!")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

