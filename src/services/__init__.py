import os

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Check if MPS is available, otherwise fallback to CPU
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
# model = None
# tokenizer = None

# If directory os.getcwd()/fine_tuned_models does not exists, run the model there if not run gpt2
if os.path.exists(f"{os.getcwd()}/fine_tuned_models"):
    model_path = f"{os.getcwd()}/fine_tuned_models"

    # Load fine-tuned model and tokenizer
    model: GPT2LMHeadModel = GPT2LMHeadModel.from_pretrained(model_path)
    tokenizer: GPT2Tokenizer = GPT2Tokenizer.from_pretrained(model_path)
else:
    # Load pre-trained GPT-2 model and tokenizer
    model_name = "gpt2"  # You can also use 'gpt2-medium', 'gpt2-large', or 'gpt2-xl'
    model: GPT2LMHeadModel = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer: GPT2Tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Move model to the device (MPS or CPU)
model = model.to(device)

