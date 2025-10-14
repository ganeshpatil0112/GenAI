"""
Comprehensive Setup Verification Script
Checks all components are working correctly
"""

import os
import json

print("\n" + "="*70)
print(" "*20 + "SETUP VERIFICATION")
print("="*70)

all_checks_passed = True

# Check 1: Python packages
print("\n1. Checking Python Packages...")
try:
    import torch
    import transformers
    import datasets
    import peft
    import trl
    print("   ✓ All required packages installed")
    print(f"   - PyTorch: {torch.__version__}")
    print(f"   - Transformers: {transformers.__version__}")
    print(f"   - CUDA Available: {torch.cuda.is_available()}")
    if not torch.cuda.is_available():
        print("   ⚠ Warning: No GPU detected. Training will use CPU (slower)")
except ImportError as e:
    print(f"   ❌ Missing package: {e}")
    all_checks_passed = False

# Check 2: Project structure
print("\n2. Checking Project Structure...")
required_dirs = ['datasets', 'finetuning', 'models']
for directory in required_dirs:
    if os.path.exists(directory):
        print(f"   ✓ {directory}/ exists")
    else:
        print(f"   ❌ {directory}/ missing")
        all_checks_passed = False

# Check 3: Datasets
print("\n3. Checking Datasets...")
datasets_info = {
    'datasets/hr_dataset.json': 'HR',
    'datasets/finance_dpo_dataset.json': 'Finance DPO',
    'datasets/sales_dataset.json': 'Sales',
    'datasets/healthcare_dataset.json': 'Healthcare',
    'datasets/marketing_dataset.json': 'Marketing'
}

for file_path, name in datasets_info.items():
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"   ✓ {name}: {len(data)} samples")
    else:
        print(f"   ❌ {name}: File missing")
        all_checks_passed = False

# Check 4: Training scripts
print("\n4. Checking Training Scripts...")
scripts = [
    'finetuning/full_finetuning.py',
    'finetuning/dpo_finetuning.py',
    'finetuning/peft_finetuning.py',
    'finetuning/lora_finetuning.py',
    'finetuning/qlora_finetuning.py'
]

for script in scripts:
    if os.path.exists(script):
        print(f"   ✓ {os.path.basename(script)}")
    else:
        print(f"   ❌ {os.path.basename(script)} missing")
        all_checks_passed = False

# Check 5: Main scripts
print("\n5. Checking Main Scripts...")
main_scripts = ['main.py', 'test_models.py', 'quick_start.py']
for script in main_scripts:
    if os.path.exists(script):
        print(f"   ✓ {script}")
    else:
        print(f"   ❌ {script} missing")
        all_checks_passed = False

# Check 6: Documentation
print("\n6. Checking Documentation...")
docs = ['README.md', 'USAGE_GUIDE.md', 'requirements.txt']
for doc in docs:
    if os.path.exists(doc):
        print(f"   ✓ {doc}")
    else:
        print(f"   ❌ {doc} missing")

# Check 7: Test if training works (minimal test)
print("\n7. Testing Training Functionality...")
try:
    from finetuning.lora_finetuning import train_lora_finetuning
    print("   ✓ Training functions can be imported")
except Exception as e:
    print(f"   ❌ Import error: {e}")
    all_checks_passed = False

# Final summary
print("\n" + "="*70)
if all_checks_passed:
    print("✓ ALL CHECKS PASSED!")
    print("="*70)
    print("\n🚀 Your system is ready for fine-tuning!")
    print("\nNext Steps:")
    print("  1. Quick test (5-10 min): python test_single_model.py")
    print("  2. Train one model: python main.py --train lora")
    print("  3. Train all models: python main.py --train all")
    print("  4. Test models: python test_models.py")
    print("\n💡 Tips:")
    if not torch.cuda.is_available():
        print("  - CPU training is slower. Each model takes 15-30 minutes")
        print("  - Consider using Google Colab for faster GPU training")
    else:
        print("  - GPU detected! Training will be much faster")
    print("  - Start with 'python test_single_model.py' to verify")
    print("  - Models will be saved in models/ directory")
else:
    print("❌ SOME CHECKS FAILED")
    print("="*70)
    print("\nPlease fix the issues above before proceeding.")
    print("Run 'pip install -r requirements.txt' to install missing packages.\n")

print("="*70 + "\n")

