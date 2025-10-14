# LLM Fine-tuning Project with Indian Datasets

This project demonstrates 5 different fine-tuning techniques on various Indian domain-specific datasets:

## Fine-tuning Techniques

1. **Full Fine-tuning** - HR Dataset (Indian employee queries, policies, leave management)
2. **DPO (Direct Preference Optimization)** - Finance Dataset (Indian banking, investments, GST)
3. **PEFT** - Sales Dataset (Indian retail, e-commerce, customer interactions)
4. **LoRA** - Healthcare Dataset (Indian medical queries, Ayurveda, health policies)
5. **QLoRA** - Marketing Dataset (Indian market campaigns, regional strategies)

## Base Model

Using **TinyLlama-1.1B-Chat-v1.0** for efficient local training

## Project Structure

```
finetuningfinal/
├── datasets/               # All Indian-flavored datasets
│   ├── hr_dataset.json
│   ├── finance_dpo_dataset.json
│   ├── sales_dataset.json
│   ├── healthcare_dataset.json
│   └── marketing_dataset.json
├── models/                 # Saved fine-tuned models
├── finetuning/            # Fine-tuning scripts
│   ├── full_finetuning.py
│   ├── dpo_finetuning.py
│   ├── peft_finetuning.py
│   ├── lora_finetuning.py
│   └── qlora_finetuning.py
├── test_models.py         # Testing script
├── main.py               # Main execution script
└── requirements.txt
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Train All Models
```bash
python main.py --train-all
```

### Train Specific Model
```bash
python main.py --train hr      # Full fine-tuning
python main.py --train dpo     # DPO fine-tuning
python main.py --train peft    # PEFT fine-tuning
python main.py --train lora    # LoRA fine-tuning
python main.py --train qlora   # QLoRA fine-tuning
```

### Test Models
```bash
python test_models.py
```

## Dataset Sizes

- HR Dataset: 500+ samples
- Finance DPO Dataset: 500+ preference pairs
- Sales Dataset: 500+ samples
- Healthcare Dataset: 500+ samples
- Marketing Dataset: 500+ samples

## Hardware Requirements

- GPU: NVIDIA GPU with 8GB+ VRAM (recommended)
- RAM: 16GB+ system RAM
- Storage: 20GB+ free space

## Notes

- All code is function-based (no classes/objects)
- Datasets are authentically Indian-flavored
- Models saved in `models/` directory
- Training logs available in respective directories

