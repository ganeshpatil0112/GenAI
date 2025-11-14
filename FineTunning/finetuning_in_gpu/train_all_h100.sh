#!/bin/bash
# H100 Training Script - Train All Models
# Optimized for H100 GPU with BF16 precision

set -e

echo "🚀 H100 Training All Models"
echo "=========================="

# Load H100 environment
source h100_env.sh 2>/dev/null || {
    export CUDA_VISIBLE_DEVICES=0
    export PYTORCH_ALLOC_CONF=max_split_size_mb:512
    export TOKENIZERS_PARALLELISM=false
    export NCCL_P2P_DISABLE=1
    export NCCL_IB_DISABLE=1
}

# Activate Python environment
source h100_env/bin/activate

# Check GPU
echo "🔍 Checking H100 GPU..."
python3 -c "
import torch
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'GPU count: {torch.cuda.device_count()}')
if torch.cuda.is_available():
    print(f'GPU: {torch.cuda.get_device_name(0)}')
    print(f'Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f}GB')
"

# Create models directory
mkdir -p models

echo ""
echo "📊 Training HR Model (Full Fine-tuning)..."
echo "=========================================="
python finetuning/full_finetuning_h100.py \
    --dataset_path "datasets/hr_dataset.json" \
    --output_dir "models/hr_full_finetuned" \
    --epochs 3 \
    --batch_size 2 \
    --learning_rate 5e-5

echo ""
echo "🏥 Training Healthcare Model (LoRA)..."
echo "====================================="
python finetuning/lora_finetuning.py \
    --dataset_path "datasets/healthcare_dataset.json" \
    --output_dir "models/healthcare_lora_finetuned" \
    --epochs 3 \
    --batch_size 4 \
    --learning_rate 2e-4

echo ""
echo "🛒 Training Sales Model (PEFT)..."
echo "================================="
python finetuning/peft_finetuning.py \
    --dataset_path "datasets/sales_dataset.json" \
    --output_dir "models/sales_peft_finetuned" \
    --epochs 3 \
    --batch_size 4 \
    --learning_rate 2e-4

echo ""
echo "📢 Training Marketing Model (QLoRA)..."
echo "====================================="
python finetuning/qlora_finetuning.py \
    --dataset_path "datasets/marketing_dataset.json" \
    --output_dir "models/marketing_qlora_finetuned" \
    --epochs 3 \
    --batch_size 2 \
    --learning_rate 2e-4

echo ""
echo "💰 Training Finance Model (DPO)..."
echo "==================================="
python finetuning/dpo_finetuning.py \
    --dataset_path "datasets/finance_dpo_dataset.json" \
    --output_dir "models/finance_dpo_finetuned" \
    --epochs 2 \
    --batch_size 2 \
    --learning_rate 1e-5

echo ""
echo "✅ All models trained successfully!"
echo "=================================="
echo "📁 Models saved in: models/"
echo ""
echo "🎯 Next step: Deploy API with ./deploy_h100_api.sh"
