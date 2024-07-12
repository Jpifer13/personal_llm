from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"  # You can also use 'gpt2-medium', 'gpt2-large', or 'gpt2-xl'
model: GPT2LMHeadModel = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer: GPT2Tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Set pad_token to eos_token
tokenizer.pad_token = tokenizer.eos_token


async def generate_text(
    prompt: str, max_length: int = 50
):
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=max_length,
    )
    outputs = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        num_beams=3,
        early_stopping=True,
        pad_token_id=tokenizer.eos_token_id,
    )
    generated_texts = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_texts
