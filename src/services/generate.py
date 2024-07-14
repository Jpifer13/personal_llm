from src.services import model, tokenizer

# Set pad_token to eos_token
tokenizer.pad_token = tokenizer.eos_token


async def generate_text(
    prompt: str, max_length: int = 1000
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
    generated_texts = ""
    for output in outputs:
        generated_texts += tokenizer.decode(output, skip_special_tokens=True)

    return generated_texts
