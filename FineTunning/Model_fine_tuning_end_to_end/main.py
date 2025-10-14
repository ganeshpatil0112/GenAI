"""
Main Execution Script for LLM Fine-tuning Project
Orchestrates all fine-tuning processes
"""

import argparse
import sys
import os

# Import all fine-tuning functions
sys.path.append('finetuning')
from finetuning.full_finetuning import train_full_finetuning
from finetuning.dpo_finetuning import train_dpo_finetuning
from finetuning.peft_finetuning import train_peft_finetuning
from finetuning.lora_finetuning import train_lora_finetuning
from finetuning.qlora_finetuning import train_qlora_finetuning

def print_banner():
    """Print project banner"""
    print("\n" + "="*70)
    print(" "*15 + "LLM FINE-TUNING PROJECT")
    print(" "*10 + "5 Techniques × 5 Indian Domain Datasets")
    print("="*70)
    print("\nTechniques:")
    print("  1. Full Fine-tuning  → HR Dataset (Employee policies)")
    print("  2. DPO              → Finance Dataset (Banking, Tax)")
    print("  3. PEFT             → Sales Dataset (E-commerce)")
    print("  4. LoRA             → Healthcare Dataset (Medical, Ayurveda)")
    print("  5. QLoRA            → Marketing Dataset (Campaigns)")
    print("\nBase Model: TinyLlama-1.1B-Chat-v1.0")
    print("="*70 + "\n")

def train_all_models():
    """Train all models sequentially"""
    print_banner()
    
    models_trained = []
    
    print("\n🚀 Starting comprehensive fine-tuning pipeline...\n")
    
    # 1. Full Fine-tuning - HR
    try:
        print("\n[1/5] Training Full Fine-tuning model...")
        train_full_finetuning(
            dataset_path='datasets/hr_dataset.json',
            output_dir='models/hr_full_finetuned',
            epochs=3,
            batch_size=2
        )
        models_trained.append("✓ HR - Full Fine-tuning")
    except Exception as e:
        print(f"❌ Error in Full Fine-tuning: {str(e)}")
        models_trained.append("❌ HR - Full Fine-tuning (Failed)")
    
    # 2. DPO - Finance
    try:
        print("\n[2/5] Training DPO model...")
        train_dpo_finetuning(
            dataset_path='datasets/finance_dpo_dataset.json',
            output_dir='models/finance_dpo_finetuned',
            epochs=3,
            batch_size=1
        )
        models_trained.append("✓ Finance - DPO")
    except Exception as e:
        print(f"❌ Error in DPO: {str(e)}")
        models_trained.append("❌ Finance - DPO (Failed)")
    
    # 3. PEFT - Sales
    try:
        print("\n[3/5] Training PEFT model...")
        train_peft_finetuning(
            dataset_path='datasets/sales_dataset.json',
            output_dir='models/sales_peft_finetuned',
            epochs=5,
            batch_size=2
        )
        models_trained.append("✓ Sales - PEFT")
    except Exception as e:
        print(f"❌ Error in PEFT: {str(e)}")
        models_trained.append("❌ Sales - PEFT (Failed)")
    
    # 4. LoRA - Healthcare
    try:
        print("\n[4/5] Training LoRA model...")
        train_lora_finetuning(
            dataset_path='datasets/healthcare_dataset.json',
            output_dir='models/healthcare_lora_finetuned',
            epochs=5,
            batch_size=2
        )
        models_trained.append("✓ Healthcare - LoRA")
    except Exception as e:
        print(f"❌ Error in LoRA: {str(e)}")
        models_trained.append("❌ Healthcare - LoRA (Failed)")
    
    # 5. QLoRA - Marketing
    try:
        print("\n[5/5] Training QLoRA model...")
        train_qlora_finetuning(
            dataset_path='datasets/marketing_dataset.json',
            output_dir='models/marketing_qlora_finetuned',
            epochs=5,
            batch_size=2
        )
        models_trained.append("✓ Marketing - QLoRA")
    except Exception as e:
        print(f"❌ Error in QLoRA: {str(e)}")
        models_trained.append("❌ Marketing - QLoRA (Failed)")
    
    # Summary
    print("\n" + "="*70)
    print("TRAINING SUMMARY")
    print("="*70)
    for model in models_trained:
        print(f"  {model}")
    print("="*70)
    print("\n✨ All training completed! Run 'python test_models.py' to test.\n")

def train_specific_model(model_type):
    """Train a specific model"""
    print_banner()
    
    if model_type == 'hr':
        print("Training HR model with Full Fine-tuning...")
        train_full_finetuning()
    elif model_type == 'dpo':
        print("Training Finance model with DPO...")
        train_dpo_finetuning()
    elif model_type == 'peft':
        print("Training Sales model with PEFT...")
        train_peft_finetuning()
    elif model_type == 'lora':
        print("Training Healthcare model with LoRA...")
        train_lora_finetuning()
    elif model_type == 'qlora':
        print("Training Marketing model with QLoRA...")
        train_qlora_finetuning()
    else:
        print(f"❌ Unknown model type: {model_type}")
        print("Valid options: hr, dpo, peft, lora, qlora")
        sys.exit(1)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='LLM Fine-tuning Project - Train models with different techniques'
    )
    parser.add_argument(
        '--train',
        type=str,
        choices=['all', 'hr', 'dpo', 'peft', 'lora', 'qlora'],
        help='Train specific model or all models'
    )
    
    args = parser.parse_args()
    
    if args.train:
        if args.train == 'all':
            train_all_models()
        else:
            train_specific_model(args.train)
    else:
        print_banner()
        print("Usage:")
        print("  Train all models:      python main.py --train all")
        print("  Train specific model:  python main.py --train <hr|dpo|peft|lora|qlora>")
        print("\nExample:")
        print("  python main.py --train hr")
        print("  python main.py --train all")
        print("\nAfter training, test models:")
        print("  python test_models.py\n")

if __name__ == "__main__":
    main()

