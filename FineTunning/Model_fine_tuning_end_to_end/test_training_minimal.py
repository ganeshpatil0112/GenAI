"""
Minimal training test - trains for just 2 steps to verify code works
"""

import torch
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import Dataset
from peft import get_peft_model, LoraConfig, TaskType
import os

print("="*60)
print("MINIMAL TRAINING TEST - LoRA (2 steps only)")
print("="*60)

try:
    # Load minimal dataset (just 3 samples)
    print("\n1. Loading minimal dataset...")
    with open('datasets/healthcare_dataset.json', 'r', encoding='utf-8') as f:
        data = json.load(f)[:3]  # Only 3 samples
    
    dataset = Dataset.from_dict({
        'text': [f"### Instruction: {item['instruction']}\n### Response: {item['output']}" 
                 for item in data]
    })
    print(f"   ✓ Loaded {len(dataset)} samples")
    
    # Load tokenizer and model
    print("\n2. Loading model (TinyLlama)...")
    model_name = 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,  # CPU uses float32
        low_cpu_mem_usage=True
    )
    print("   ✓ Model loaded")
    
    # Apply LoRA
    print("\n3. Applying LoRA configuration...")
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,  # Small rank for testing
        lora_alpha=16,
        lora_dropout=0.1,
        target_modules=["q_proj", "v_proj"],
        bias="none"
    )
    
    model = get_peft_model(model, lora_config)
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    print(f"   ✓ LoRA applied: {trainable:,} / {total:,} params trainable ({100*trainable/total:.2f}%)")
    
    # Tokenize
    print("\n4. Tokenizing dataset...")
    def tokenize_function(examples):
        return tokenizer(
            examples['text'],
            truncation=True,
            max_length=256,  # Shorter for testing
            padding='max_length'
        )
    
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=dataset.column_names
    )
    print("   ✓ Dataset tokenized")
    
    # Training arguments (minimal)
    print("\n5. Setting up training (2 steps only)...")
    output_dir = 'models/test_minimal'
    os.makedirs(output_dir, exist_ok=True)
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        max_steps=2,  # Only 2 steps for testing
        per_device_train_batch_size=1,
        learning_rate=2e-4,
        logging_steps=1,
        save_strategy='no',  # Don't save
        report_to='none'
    )
    
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator
    )
    print("   ✓ Trainer initialized")
    
    # Train for 2 steps
    print("\n6. Training for 2 steps...")
    print("-" * 60)
    trainer.train()
    print("-" * 60)
    
    print("\n" + "="*60)
    print("✓ TRAINING TEST SUCCESSFUL!")
    print("="*60)
    print("\n✨ All training scripts should work correctly!")
    print("   Note: You're on CPU, so actual training will be slower.")
    print("   Expect 15-30 minutes per model on CPU.\n")
    
except Exception as e:
    print(f"\n❌ Error during training test: {str(e)}")
    import traceback
    traceback.print_exc()

