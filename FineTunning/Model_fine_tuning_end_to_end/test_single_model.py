"""
Test training a single model end-to-end
"""

print("\n" + "="*60)
print("Testing LoRA Fine-tuning - Healthcare Model")
print("Training with minimal parameters (1 epoch)")
print("="*60 + "\n")

from finetuning.lora_finetuning import train_lora_finetuning

try:
    # Train with minimal settings
    output = train_lora_finetuning(
        dataset_path='datasets/healthcare_dataset.json',
        model_name='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
        output_dir='models/healthcare_lora_test',
        epochs=1,  # Just 1 epoch
        batch_size=2,
        learning_rate=2e-4,
        lora_r=8,  # Small rank
        lora_alpha=16
    )
    
    print("\n" + "="*60)
    print("✓ TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"\nModel saved at: {output}")
    print("\nNow testing the trained model...")
    
    # Test the model
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from peft import PeftModel
    
    print("\nLoading trained model...")
    tokenizer = AutoTokenizer.from_pretrained(output)
    base_model = AutoModelForCausalLM.from_pretrained(
        'TinyLlama/TinyLlama-1.1B-Chat-v1.0',
        low_cpu_mem_usage=True
    )
    model = PeftModel.from_pretrained(base_model, output)
    model.eval()
    
    # Test query
    query = "What are symptoms of dengue fever?"
    prompt = f"### Instruction: {query}\n### Response:"
    
    print(f"\nTest Query: {query}")
    print("\nGenerating response...")
    
    inputs = tokenizer(prompt, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = response.split("### Response:")[-1].strip()
    
    print("\n" + "-"*60)
    print("Response:")
    print("-"*60)
    print(response)
    print("-"*60)
    
    print("\n" + "="*60)
    print("✓ END-TO-END TEST SUCCESSFUL!")
    print("="*60)
    print("\nThe model trained and can generate responses!")
    print("You can now train all models with: python main.py --train all\n")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

