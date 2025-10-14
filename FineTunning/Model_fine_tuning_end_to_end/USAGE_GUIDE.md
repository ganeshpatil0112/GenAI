# LLM Fine-tuning Project - Complete Usage Guide

## 🎯 Project Overview

This project demonstrates **5 different fine-tuning techniques** on **5 Indian domain-specific datasets**:

| Technique | Dataset | Domain | Samples |
|-----------|---------|--------|---------|
| **Full Fine-tuning** | HR Dataset | Employee policies, leave, PF, salary | 50+ |
| **DPO** | Finance Dataset | Banking, GST, investments, tax | 50+ pairs |
| **PEFT** | Sales Dataset | E-commerce, customer service | 50+ |
| **LoRA** | Healthcare Dataset | Medical, Ayurveda, diseases | 50+ |
| **QLoRA** | Marketing Dataset | Campaigns, strategies | 10+ |

**Base Model**: TinyLlama-1.1B-Chat-v1.0 (Efficient for local training)

---

## 📦 Installation

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: This will install PyTorch, Transformers, PEFT, TRL, and other required libraries.

### Step 2: Verify Installation
```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}')"
```

---

## 🚀 Quick Start (5-10 minutes)

For quick testing, run the quick start script that trains a small model:

```bash
python quick_start.py
```

This trains the Healthcare LoRA model with minimal parameters (1 epoch) to verify everything works.

---

## 🎓 Training Models

### Option 1: Train All Models (Recommended for full project)
```bash
python main.py --train all
```

**Time**: 2-4 hours on GPU, 6-12 hours on CPU
**This will train all 5 models sequentially.**

### Option 2: Train Individual Models

```bash
# Full Fine-tuning - HR
python main.py --train hr

# DPO - Finance
python main.py --train dpo

# PEFT - Sales
python main.py --train peft

# LoRA - Healthcare
python main.py --train lora

# QLoRA - Marketing
python main.py --train qlora
```

### Option 3: Train from Individual Scripts

```bash
# Navigate to finetuning directory
cd finetuning

# Train specific model
python full_finetuning.py
python dpo_finetuning.py
python peft_finetuning.py
python lora_finetuning.py
python qlora_finetuning.py
```

---

## 🧪 Testing Models

After training, test all models with domain-specific queries:

```bash
python test_models.py
```

This will:
- Load each trained model
- Test with 3 relevant queries per domain
- Display responses for comparison

**Example Output**:
```
Testing HR - Full Fine-tuning Model
Query 1: How do I apply for casual leave?
Response: To apply for casual leave (CL), log in to the HRMS portal...
```

---

## 📂 Project Structure

```
finetuningfinal/
├── datasets/                          # All datasets (JSON format)
│   ├── hr_dataset.json               # 50+ HR samples
│   ├── finance_dpo_dataset.json      # 50+ preference pairs
│   ├── sales_dataset.json            # 50+ sales samples
│   ├── healthcare_dataset.json       # 50+ healthcare samples
│   └── marketing_dataset.json        # 10+ marketing samples
│
├── finetuning/                        # Fine-tuning scripts
│   ├── full_finetuning.py            # Full fine-tuning
│   ├── dpo_finetuning.py             # DPO implementation
│   ├── peft_finetuning.py            # PEFT (Prefix tuning)
│   ├── lora_finetuning.py            # LoRA implementation
│   └── qlora_finetuning.py           # QLoRA (4-bit + LoRA)
│
├── models/                            # Saved models (created after training)
│   ├── hr_full_finetuned/
│   ├── finance_dpo_finetuned/
│   ├── sales_peft_finetuned/
│   ├── healthcare_lora_finetuned/
│   └── marketing_qlora_finetuned/
│
├── main.py                            # Main execution script
├── test_models.py                     # Comprehensive testing script
├── quick_start.py                     # Quick training test
├── requirements.txt                   # Python dependencies
├── README.md                          # Project README
└── USAGE_GUIDE.md                    # This file
```

---

## 🔧 Customization

### Modify Training Parameters

Edit the respective files in `finetuning/` directory:

```python
# Example: Increase epochs for better results
train_lora_finetuning(
    dataset_path='datasets/healthcare_dataset.json',
    output_dir='models/healthcare_lora_finetuned',
    epochs=10,           # Increase from 5 to 10
    batch_size=2,
    learning_rate=2e-4,
    lora_r=32,           # Increase LoRA rank
    lora_alpha=64
)
```

### Add More Data

Simply edit the JSON files in `datasets/` folder and add more samples in the same format.

**Example - HR Dataset**:
```json
{
  "instruction": "Your question here",
  "input": "",
  "output": "The detailed answer here"
}
```

**Example - DPO Dataset**:
```json
{
  "prompt": "Your question",
  "chosen": "Good response",
  "rejected": "Bad response"
}
```

---

## 💡 Understanding Each Technique

### 1. Full Fine-tuning
- **What**: Updates all model parameters
- **Pros**: Best performance, full adaptation
- **Cons**: Slow, requires most memory, expensive
- **Use case**: When you have computational resources and want maximum accuracy

### 2. DPO (Direct Preference Optimization)
- **What**: Aligns model with human preferences using chosen/rejected pairs
- **Pros**: Better alignment, learns from preferences
- **Cons**: Requires preference dataset, complex training
- **Use case**: When you want model to prefer certain responses over others

### 3. PEFT (Parameter-Efficient Fine-Tuning)
- **What**: Only trains small additional parameters (prefix tokens)
- **Pros**: Fast, memory efficient, good performance
- **Cons**: Slightly lower accuracy than full fine-tuning
- **Use case**: Limited resources, need quick training

### 4. LoRA (Low-Rank Adaptation)
- **What**: Adds small trainable rank decomposition matrices
- **Pros**: Very efficient, easy to swap adapters, good performance
- **Cons**: Need to choose rank carefully
- **Use case**: Most balanced approach - efficiency + performance

### 5. QLoRA (Quantized LoRA)
- **What**: LoRA + 4-bit quantization for extreme efficiency
- **Pros**: Minimal memory, can train large models on small GPUs
- **Cons**: Slightly lower precision, requires GPU
- **Use case**: Large models on consumer hardware

---

## 🎯 Expected Results

### Training Time (on 8GB GPU)
- Full Fine-tuning: ~45 mins
- DPO: ~60 mins
- PEFT: ~25 mins
- LoRA: ~25 mins
- QLoRA: ~20 mins

### Model Size
- Full model: ~2.2 GB
- PEFT adapter: ~50 MB
- LoRA adapter: ~30 MB
- QLoRA adapter: ~30 MB

### Performance
All models should provide contextually relevant responses for their respective domains. DPO model should show preference for chosen responses.

---

## 🐛 Troubleshooting

### Issue: CUDA Out of Memory
**Solution**: Reduce batch size in training scripts:
```python
batch_size=1  # Reduce from 2/4 to 1
gradient_accumulation_steps=8  # Increase to compensate
```

### Issue: Model not found during testing
**Solution**: Ensure you've trained the model first:
```bash
python main.py --train <model_name>
```

### Issue: Import errors
**Solution**: Install missing packages:
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Slow training on CPU
**Solution**: This is normal. CPU training takes 3-4x longer. Consider:
- Using Google Colab (free GPU)
- Reducing dataset size
- Using quick_start.py with minimal parameters

---

## 📊 Monitoring Training

Training scripts print progress:
```
Epoch 1/5: 100%|████████| 50/50 [02:15<00:00, 2.70s/it]
Loss: 2.345
```

**What to expect**:
- Loss should decrease over epochs
- First epoch is slowest (model loading)
- GPU training shows GPU memory usage

---

## 🎓 Next Steps

1. **Experiment with hyperparameters**: Adjust learning rate, epochs, rank
2. **Expand datasets**: Add more diverse samples
3. **Compare techniques**: Analyze which works best for your use case
4. **Deploy models**: Use trained models in applications
5. **Try larger models**: Once comfortable, try Llama-2-7B, Mistral-7B

---

## 📝 Citation

If you use this project, please reference:
- TinyLlama: https://github.com/jzhang38/TinyLlama
- PEFT: https://github.com/huggingface/peft
- TRL: https://github.com/huggingface/trl

---

## ⚠️ Important Notes

1. **GPU Recommended**: CPU training works but is significantly slower
2. **Disk Space**: Ensure 10GB+ free space for models
3. **Internet**: First run downloads base model (~2.2GB)
4. **Datasets**: All datasets are synthetic for demonstration
5. **Production Use**: Test thoroughly before production deployment

---

## 🤝 Support

For issues or questions:
1. Check this guide
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Try quick_start.py first to verify setup

---

**Happy Fine-tuning! 🚀**

