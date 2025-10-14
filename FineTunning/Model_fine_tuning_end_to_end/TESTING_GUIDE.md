# 🧪 Complete Testing Guide

## ✅ Your Testing Results

Based on the test that just ran, here's what we found:

### **Models Successfully Tested** (4/5):
- ✅ **HR - Full Fine-tuning** (`models/hr_full_finetuned`)
- ✅ **Sales - PEFT** (`models/sales_peft_finetuned`)
- ✅ **Healthcare - LoRA** (`models/healthcare_lora_finetuned`)
- ✅ **Marketing - QLoRA** (`models/marketing_qlora_finetuned`)

### **Missing**:
- ❌ **Finance - DPO** (`models/finance_dpo_finetuned`)

---

## 🎯 Testing Options

### **Option 1: Test All Models** (What you just did)
```bash
python test_models.py
```

**What it does**:
- Tests all 5 models automatically
- Uses predefined queries for each domain
- Shows 3 responses per model
- Takes 5-10 minutes

**Output**: Side-by-side responses from each model

---

### **Option 2: Interactive Testing**
```bash
python test_interactive.py
```

**What it does**:
- Load one model
- Ask your own custom questions
- Get responses in real-time
- Type 'quit' to exit

**Example session**:
```
Query: What are the symptoms of malaria?
Response: [Model generates answer]

Query: How to prevent dengue?
Response: [Model generates answer]

Query: quit
```

**To test different models**, edit `test_interactive.py`:
```python
# Line 81-82, change to:
model_path = "models/hr_full_finetuned"      # For HR model
model_type = "full"

# Or
model_path = "models/sales_peft_finetuned"   # For Sales model
model_type = "peft"

# Or
model_path = "models/marketing_qlora_finetuned"  # For Marketing
model_type = "qlora"
```

---

### **Option 3: Compare Models Side-by-Side**
```bash
python compare_models.py
```

**What it does**:
- Tests same query across multiple models
- Shows how different techniques respond
- Useful for comparing quality
- Takes 10-15 minutes

**Output**: Responses from all models for each query

---

### **Option 4: Test Specific Model with Custom Queries**

Create your own test script:

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Load model
model_path = "models/healthcare_lora_finetuned"
tokenizer = AutoTokenizer.from_pretrained(model_path)

base = AutoModelForCausalLM.from_pretrained(
    'TinyLlama/TinyLlama-1.1B-Chat-v1.0',
    low_cpu_mem_usage=True
)
model = PeftModel.from_pretrained(base, model_path)
model.eval()

# Your custom query
query = "What are symptoms of dengue fever?"
prompt = f"### Instruction: {query}\n### Response:"
inputs = tokenizer(prompt, return_tensors="pt")

# Generate
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response.split("### Response:")[-1].strip())
```

---

## 📊 Sample Test Queries by Domain

### **HR Model**:
```
- How do I apply for casual leave?
- What is the work from home policy?
- How is gratuity calculated?
- What are the company holidays?
- How to claim medical reimbursement?
```

### **Finance Model** (if trained):
```
- What is the current GST rate for restaurants?
- How can I save income tax legally?
- Explain PPF scheme
- What is the difference between SIP and lumpsum?
- How to manage credit card bills?
```

### **Sales Model**:
```
- Customer wants to return a product
- How to handle delivery delay complaint?
- Explain EMI options for laptop purchase
- Customer asking about COD availability
- How to handle angry customer?
```

### **Healthcare Model**:
```
- What are symptoms of dengue fever?
- How to manage diabetes with Indian diet?
- What are Ayurvedic remedies for acidity?
- How to treat common cold at home?
- What vaccinations are mandatory for children?
```

### **Marketing Model**:
```
- Create Diwali campaign for e-commerce
- How to use influencer marketing for beauty brand?
- Develop loyalty program for fashion retail
- Create content marketing strategy
- Design regional marketing strategy for Tamil Nadu
```

---

## 🎨 Understanding Your Results

### **What Good Responses Look Like**:
- ✅ Relevant to the question
- ✅ Uses Indian context (GST, PF, Diwali, etc.)
- ✅ Detailed and informative
- ✅ Structured and readable
- ✅ Accurate information

### **What Needs Improvement**:
- ❌ Off-topic or irrelevant
- ❌ Too short or too long
- ❌ Repetitive
- ❌ Incorrect information
- ❌ Doesn't use Indian context

### **From your test results, we saw**:
- ✅ HR model generates relevant leave/policy information
- ✅ Sales model handles customer service scenarios
- ✅ Healthcare model provides Ayurvedic remedies
- ✅ Marketing model creates campaign strategies
- ⚠️ Some responses could be more detailed (1 epoch training)

---

## 💡 Tips for Better Results

### **If responses are not good enough**:

1. **Train for more epochs**:
```bash
# Edit the training script to increase epochs from 3 to 5-10
python main.py --train lora  # with modified epochs
```

2. **Add more training data**:
- Edit JSON files in `datasets/` folder
- Add 50-100 more samples per domain

3. **Adjust generation parameters**:
```python
# In test scripts, modify:
max_new_tokens=300,     # Longer responses
temperature=0.7,        # Lower (0.5) = more focused, Higher (0.9) = more creative
top_p=0.9,             # Nucleus sampling
```

4. **Try different models**:
- Use larger base model (Llama-2-7B instead of TinyLlama)
- More parameters = better quality (but slower)

---

## 📈 Evaluating Model Performance

### **Manual Evaluation Criteria**:

| Criteria | Score | Notes |
|----------|-------|-------|
| **Relevance** | 1-5 | Does it answer the question? |
| **Accuracy** | 1-5 | Is the information correct? |
| **Completeness** | 1-5 | Is it detailed enough? |
| **Context** | 1-5 | Uses Indian context appropriately? |
| **Fluency** | 1-5 | Natural and readable? |

### **Example Evaluation**:

**Query**: "How to apply for leave?"

**HR Model Response**: 
> "To apply for casual leave, log in to myHRMS portal..."

**Scores**:
- Relevance: 5/5 ✅ (Directly answers)
- Accuracy: 4/5 ✅ (Mostly correct process)
- Completeness: 4/5 ✅ (Good details)
- Context: 5/5 ✅ (Uses HRMS, Indian terms)
- Fluency: 4/5 ✅ (Readable)

**Total**: 22/25 (88%) - **Good!**

---

## 🔧 Troubleshooting

### **Problem**: Model generates gibberish
**Solution**: 
- Train for more epochs
- Check if dataset is correct
- Reduce learning rate

### **Problem**: Responses too short
**Solution**:
- Increase `max_new_tokens` in test script
- Add longer examples to training data

### **Problem**: Model not found error
**Solution**:
```bash
# Check which models exist
ls models/

# Retrain missing model
python main.py --train <model_name>
```

### **Problem**: Out of memory during testing
**Solution**:
```python
# Test one model at a time
# Or reduce batch size in generation
```

---

## 📝 Testing Checklist

- [x] Tested all trained models (4/5)
- [ ] Tested with custom queries (interactive)
- [ ] Compared models side-by-side
- [ ] Evaluated response quality
- [ ] Documented which model works best for which task
- [ ] Identified areas for improvement
- [ ] Retrained with more epochs if needed

---

## 🎯 Next Steps

### **Immediate**:
1. ✅ Test all models (Done!)
2. Try interactive testing: `python test_interactive.py`
3. Compare models: `python compare_models.py`

### **Short-term**:
4. Evaluate response quality
5. Note which models need improvement
6. Retrain with more epochs (5-10)

### **Long-term**:
7. Add more training data
8. Try larger base models
9. Deploy best-performing models
10. Build application using the models

---

## 🚀 Quick Commands Reference

```bash
# Test all models
python test_models.py

# Interactive testing
python test_interactive.py

# Compare models
python compare_models.py

# Retrain a model with more epochs
python main.py --train lora

# Check trained models
ls models/
```

---

## 🎉 Congratulations!

You've successfully:
- ✅ Trained 4-5 models
- ✅ Tested them with domain-specific queries
- ✅ Generated responses

**Your models are working!** 🎊

Now you can:
- Use them in applications
- Improve them with more training
- Deploy them for real use cases
- Experiment with different techniques

---

**Happy Testing! 🧪**

