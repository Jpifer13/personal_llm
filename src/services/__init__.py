import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Check if MPS is available, otherwise fallback to CPU
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"  # You can also use 'gpt2-medium', 'gpt2-large', or 'gpt2-xl'
model: GPT2LMHeadModel = GPT2LMHeadModel.from_pretrained(model_name)

# Move model to the device (MPS or CPU)
model = model.to(device)

tokenizer: GPT2Tokenizer = GPT2Tokenizer.from_pretrained(model_name)
