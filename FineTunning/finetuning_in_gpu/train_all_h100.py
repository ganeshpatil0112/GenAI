#!/usr/bin/env python3
"""
H100 Complete Training Script
Train all 5 models on H100 GPU with BF16 optimization
"""

import os
import sys
import subprocess
import time

def set_h100_environment():
    """Set H100 optimized environment variables"""
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    os.environ['PYTORCH_ALLOC_CONF'] = 'max_split_size_mb:512'
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    os.environ['NCCL_P2P_DISABLE'] = '1'
    os.environ['NCCL_IB_DISABLE'] = '1'
    print("✅ H100 environment variables set")

def check_h100_setup():
    """Check H100 setup"""
    try:
        import torch
        if not torch.cuda.is_available():
            print("❌ CUDA not available!")
            return False
        
        gpu_name = torch.cuda.get_device_name(0)
        if "H100" in gpu_name:
            print(f"✅ H100 GPU detected: {gpu_name}")
        else:
            print(f"⚠️  GPU detected: {gpu_name} (not H100)")
        
        memory_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"✅ GPU Memory: {memory_gb:.1f}GB")
        return True
        
    except Exception as e:
        print(f"❌ GPU check failed: {e}")
        return False

def train_model(script_name, model_name, description):
    """Train a single model"""
    print(f"\n🚀 {description}")
    print("=" * 60)
    
    try:
        # Import and run H100 optimized training
        if script_name == "full_finetuning_h100":
            from finetuning.full_finetuning_h100 import train_h100_full_finetuning
            output_path = train_h100_full_finetuning(
                dataset_path=f'datasets/{model_name}_dataset.json',
                model_name='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
                output_dir=f'models/{model_name}_finetuned',
                epochs=3,
                batch_size=2,
                learning_rate=5e-5
            )
        elif script_name == "lora_finetuning_h100":
            from finetuning.lora_finetuning_h100 import train_h100_lora_finetuning
            output_path = train_h100_lora_finetuning(
                dataset_path=f'datasets/{model_name}_dataset.json',
                model_name='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
                output_dir=f'models/{model_name}_finetuned',
                epochs=3,
                batch_size=4,
                learning_rate=2e-4
            )
        elif script_name == "peft_finetuning_h100":
            from finetuning.peft_finetuning_h100 import train_h100_peft_finetuning
            output_path = train_h100_peft_finetuning(
                dataset_path=f'datasets/{model_name}_dataset.json',
                model_name='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
                output_dir=f'models/{model_name}_finetuned',
                epochs=3,
                batch_size=4,
                learning_rate=2e-4
            )
        elif script_name == "qlora_finetuning_h100":
            from finetuning.qlora_finetuning_h100 import train_h100_qlora_finetuning
            output_path = train_h100_qlora_finetuning(
                dataset_path=f'datasets/{model_name}_dataset.json',
                model_name='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
                output_dir=f'models/{model_name}_finetuned',
                epochs=3,
                batch_size=2,
                learning_rate=2e-4
            )
        elif script_name == "dpo_finetuning_h100":
            from finetuning.dpo_finetuning_h100 import train_h100_dpo_finetuning
            output_path = train_h100_dpo_finetuning(
                dataset_path=f'datasets/{model_name}_dpo_dataset.json',
                model_name='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
                output_dir=f'models/{model_name}_finetuned',
                epochs=2,
                batch_size=2,
                learning_rate=1e-5
            )
        else:
            # Fallback to subprocess
            result = subprocess.run([
                sys.executable, 
                f"finetuning/{script_name}.py"
            ], check=True, capture_output=True, text=True)
            
            output_path = f"models/{model_name}_finetuned"
        
        print(f"✅ {description} completed successfully!")
        print(f"📁 Model saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    """Main training function"""
    print("🎯 H100 Complete Training Pipeline")
    print("=" * 50)
    
    # Set environment
    set_h100_environment()
    
    # Check setup
    if not check_h100_setup():
        print("❌ H100 setup check failed!")
        return False
    
    # Training sequence - H100 optimized versions
    models = [
        ("full_finetuning_h100", "hr", "HR Model (Full Fine-tuning)"),
        ("lora_finetuning_h100", "healthcare", "Healthcare Model (LoRA)"),
        ("peft_finetuning_h100", "sales", "Sales Model (PEFT)"),
        ("qlora_finetuning_h100", "marketing", "Marketing Model (QLoRA)"),
        ("dpo_finetuning_h100", "finance", "Finance Model (DPO)")
    ]
    
    successful = 0
    failed = 0
    start_time = time.time()
    
    for script, model, description in models:
        success = train_model(script, model, description)
        if success:
            successful += 1
        else:
            failed += 1
        
        # Brief pause between models
        time.sleep(2)
    
    # Calculate total time
    total_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("📊 H100 Training Summary")
    print("=" * 60)
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"⏱️  Total time: {total_time/60:.1f} minutes")
    
    if successful == len(models):
        print("\n🎉 All models trained successfully on H100!")
        print("📁 Models saved in: models/")
        print("🚀 Next step: Deploy API with ./deploy_h100_api.sh")
    else:
        print(f"\n⚠️  {failed} model(s) failed. Check the errors above.")
    
    return successful == len(models)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
