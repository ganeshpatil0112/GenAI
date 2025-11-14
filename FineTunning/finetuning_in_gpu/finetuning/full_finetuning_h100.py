#!/usr/bin/env python3
"""
H100 Optimized Full Fine-tuning Script
Completely avoids FP16 operations for H100 compatibility
"""

import torch
import json
import os
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset

def load_hr_dataset(file_path):
    """Load and prepare HR dataset"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return Dataset.from_dict({
        'text': [f"### Instruction: {item['instruction']}\n### Response: {item['output']}" 
                 for item in data]
    })

def tokenize_function(examples, tokenizer, max_length=512):
    """Tokenize dataset"""
    return tokenizer(
        examples['text'],
        truncation=True,
        max_length=max_length,
        padding='max_length'
    )

def train_h100_full_finetuning(
    dataset_path='datasets/hr_dataset.json',
    model_name='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
    output_dir='models/hr_full_finetuned',
    epochs=3,
    batch_size=2,
    learning_rate=5e-5
):
    """H100 optimized full fine-tuning - NO FP16"""
    
    print("=" * 50)
    print("H100 FULL FINE-TUNING - HR DATASET")
    print("=" * 50)
    
    # Set H100 environment
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    os.environ['PYTORCH_ALLOC_CONF'] = 'max_split_size_mb:512'
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    
    # Load tokenizer
    print(f"\n1. Loading tokenizer: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Load model with BF16 only
    print(f"\n2. Loading model: {model_name}")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,  # Use BF16 for H100
        device_map='auto',
        low_cpu_mem_usage=True
    )
    
    print(f"   Model loaded with {model.num_parameters():,} parameters")
    print(f"   Model dtype: {model.dtype}")
    
    # Load dataset
    print(f"\n3. Loading dataset from: {dataset_path}")
    dataset = load_hr_dataset(dataset_path)
    print(f"   Dataset size: {len(dataset)} samples")
    
    # Tokenize dataset
    print("\n4. Tokenizing dataset...")
    tokenized_dataset = dataset.map(
        lambda x: tokenize_function(x, tokenizer),
        batched=True,
        remove_columns=dataset.column_names
    )
    
    # H100 optimized training arguments - NO FP16
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=4,
        learning_rate=learning_rate,
        fp16=False,  # Explicitly disable FP16
        bf16=True,   # Use BF16 for H100
        save_strategy='epoch',
        logging_steps=10,
        warmup_steps=100,
        optim='adamw_torch',
        save_total_limit=2,
        report_to='none',
        gradient_checkpointing=True,
        dataloader_pin_memory=False,
        remove_unused_columns=False,
        max_grad_norm=1.0,
        lr_scheduler_type='cosine',
        dataloader_num_workers=0,
        use_cpu=False,
        no_cuda=False,
        # Additional H100 optimizations
        ddp_find_unused_parameters=False,
        dataloader_drop_last=True,
        eval_strategy='no',
        save_steps=500,
        eval_steps=500
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator
    )
    
    # Train
    print("\n5. Starting H100 optimized training...")
    print(f"   Epochs: {epochs}")
    print(f"   Batch size: {batch_size}")
    print(f"   Learning rate: {learning_rate}")
    print(f"   Device: {'GPU' if torch.cuda.is_available() else 'CPU'}")
    print(f"   Precision: BF16")
    print("\n" + "-" * 50)
    
    try:
        trainer.train()
        
        # Save model
        print("\n6. Saving model...")
        trainer.save_model()
        tokenizer.save_pretrained(output_dir)
        
        print(f"✅ Model saved to: {output_dir}")
        return output_dir
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        raise e

if __name__ == "__main__":
    try:
        output_path = train_h100_full_finetuning()
        print(f"\n🎉 H100 training completed successfully!")
        print(f"📁 Model saved to: {output_path}")
    except Exception as e:
        print(f"\n❌ H100 training failed: {e}")
        exit(1)
