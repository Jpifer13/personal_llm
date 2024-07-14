from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"  # You can also use 'gpt2-medium', 'gpt2-large', or 'gpt2-xl'
model: GPT2LMHeadModel = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer: GPT2Tokenizer = GPT2Tokenizer.from_pretrained(model_name)
