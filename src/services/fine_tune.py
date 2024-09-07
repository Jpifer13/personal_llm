from logging import getLogger
import os

from src.services import model, tokenizer

from transformers import DataCollatorForLanguageModeling, TextDataset, Trainer, TrainingArguments

logger = getLogger()


def load_dataset(path_to_dataset):
    text_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=path_to_dataset,
        block_size=128,
    )
    logger.info("Dataset loaded.")
    return text_dataset


async def fine_tune(path_to_dataset: str):
    try:
        # Fine-tune the model
        logger.info("Fine-tuning model...")
        training_args = TrainingArguments(
            output_dir=f"{os.getcwd()}/results",
            overwrite_output_dir=True,
            num_train_epochs=1,
            per_device_train_batch_size=4,
            save_steps=10_000,
            save_total_limit=2
        )

        logger.info("Loading dataset...")
        train_dataset = load_dataset(path_to_dataset)
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False,
        )

        logger.info("Training model...")
        trainer = Trainer(
            model=model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
        )

        trainer.train()
        logger.info("Saving fine-tuned model...")
        model.save_pretrained(f"{os.getcwd()}/fine_tuned_models")
        tokenizer.save_pretrained(f"{os.getcwd()}/fine_tuned_models")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise e
