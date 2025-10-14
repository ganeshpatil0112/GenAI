"""
Quick Start Script - Train small sample for testing
Fast training with reduced parameters for quick validation
"""

import torch
from finetuning.lora_finetuning import train_lora_finetuning

def quick_test_training():
    """Quick training test with minimal parameters"""
    print("\n" + "="*60)
    print("QUICK START - Training Healthcare model with LoRA")
    print("(Fast training for testing - 1 epoch, small batch)")
    print("="*60 + "\n")
    
    print("This will take approximately 5-10 minutes on GPU, 15-30 minutes on CPU\n")
    
    try:
        # Train with minimal parameters for quick testing
        output = train_lora_finetuning(
            dataset_path='datasets/healthcare_dataset.json',
            model_name='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
            output_dir='models/healthcare_lora_quick_test',
            epochs=1,  # Just 1 epoch for quick test
            batch_size=2,
            learning_rate=2e-4
        )
        
        print("\n" + "="*60)
        print("✓ QUICK TRAINING COMPLETED!")
        print("="*60)
        print(f"\nModel saved at: {output}")
        print("\nNow you can:")
        print("  1. Test this model: Modify test_models.py to use this path")
        print("  2. Train all models: python main.py --train all")
        print("  3. Train specific: python main.py --train <model_name>")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error during training: {str(e)}")
        print("\nTroubleshooting:")
        print("  - Ensure you have installed all requirements: pip install -r requirements.txt")
        print("  - Check if you have enough disk space (at least 5GB)")
        print("  - If GPU error, training will fall back to CPU (slower)")

if __name__ == "__main__":
    quick_test_training()

