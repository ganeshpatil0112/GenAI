#!/usr/bin/env python3
"""
H100 Optimized PEFT Fine-tuning Script for Sales Dataset
Uses BF16 precision and H100 optimizations
"""

import torch
import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import Dataset
from peft import get_peft_model, LoraConfig, TaskType

def load_sales_dataset(file_path):
    """Load and prepare Sales dataset"""
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

def train_h100_peft_finetuning(
    dataset_path='datasets/sales_dataset.json',
    model_name='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
    output_dir='models/sales_peft_finetuned',
    epochs=3,
    batch_size=4,
    learning_rate=2e-4,
    lora_rank=16,
    lora_alpha=32
):
    """H100 optimized PEFT fine-tuning - NO FP16"""
    
    print("=" * 50)
    print("H100 PEFT FINE-TUNING - SALES DATASET")
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
    
    # Configure PEFT (LoRA)
    print(f"\n3. Configuring PEFT...")
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=lora_rank,
        lora_alpha=lora_alpha,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.1,
        bias="none"
    )
    
    # Freeze base model first
    for param in model.parameters():
        param.requires_grad = False
    
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()
    
    # Ensure model is in training mode
    model.train()
    
    # Verify gradients are enabled
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"   Trainable parameters: {trainable_params:,}")
    
    # Double-check that LoRA parameters have gradients enabled
    for name, param in model.named_parameters():
        if 'lora' in name.lower():
            param.requires_grad = True
            print(f"   LoRA param {name}: requires_grad={param.requires_grad}")
    
    # Load dataset
    print(f"\n4. Loading dataset from: {dataset_path}")
    dataset = load_sales_dataset(dataset_path)
    print(f"   Dataset size: {len(dataset)} samples")
    
    # Tokenize dataset
    print("\n5. Tokenizing dataset...")
    tokenized_dataset = dataset.map(
        lambda x: tokenize_function(x, tokenizer),
        batched=True,
        remove_columns=dataset.column_names
    )
    
    # H100 optimized training arguments - NO FP16, NO gradient checkpointing
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
        gradient_checkpointing=False,  # Disable gradient checkpointing for LoRA
        dataloader_pin_memory=False,
        remove_unused_columns=False,
        max_grad_norm=1.0,
        lr_scheduler_type='cosine',
        dataloader_num_workers=0,
        use_cpu=False,
        no_cuda=False,
        ddp_find_unused_parameters=False  # Disable DDP unused parameter detection
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
    
    # Final gradient check before training
    trainable_count = sum(1 for p in model.parameters() if p.requires_grad)
    print(f"\n   Final check: {trainable_count} parameters require gradients")
    
    # Train
    print("\n6. Starting H100 optimized PEFT training...")
    print(f"   Epochs: {epochs}")
    print(f"   Batch size: {batch_size}")
    print(f"   Learning rate: {learning_rate}")
    print(f"   PEFT rank: {lora_rank}")
    print(f"   Device: {'GPU' if torch.cuda.is_available() else 'CPU'}")
    print(f"   Precision: BF16")
    print("\n" + "-" * 50)
    
    try:
        trainer.train()
        
        # Save model
        print("\n7. Saving model...")
        trainer.save_model()
        tokenizer.save_pretrained(output_dir)
        
        print(f"✅ Model saved to: {output_dir}")
        return output_dir
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        raise e

if __name__ == "__main__":
    try:
        output_path = train_h100_peft_finetuning()
        print(f"\n🎉 H100 PEFT training completed successfully!")
        print(f"📁 Model saved to: {output_path}")
    except Exception as e:
        print(f"\n❌ H100 PEFT training failed: {e}")
        exit(1)
