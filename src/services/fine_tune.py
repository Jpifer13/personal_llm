from logging import getLogger
import os
import fitz  # PyMuPDF for PDF processing
from typing import Optional

from src.services import model, tokenizer

from transformers import (
    DataCollatorForLanguageModeling,
    TextDataset,
    Trainer,
    TrainingArguments,
)

logger = getLogger()


def load_dataset(path_to_dataset: str) -> TextDataset:
    """Load dataset from a text file."""
    text_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=path_to_dataset,
        block_size=128,
    )
    logger.info("Dataset loaded.")
    return text_dataset


def convert_pdf_to_text(pdf_path: str) -> str:
    """Convert a PDF to plain text using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    return text


async def fine_tune(path_to_dataset: str) -> Optional[str]:
    """Fine-tune the model using the provided dataset (text file or PDF).

    Args:
        path_to_dataset: The path to the dataset, which can be a .txt or .pdf file.

    Returns:
        Optional[str]: Returns None if the process is successful, otherwise raises an error.
    """
    try:
        # Check if the file is a PDF
        if path_to_dataset.endswith(".pdf"):
            logger.info("PDF detected. Converting PDF to text...")
            # Convert PDF to text
            text_data = convert_pdf_to_text(path_to_dataset)

            # Create a temporary text file for fine-tuning
            text_file_path = path_to_dataset.replace(".pdf", ".txt")
            with open(text_file_path, "w") as f:
                f.write(text_data)

            logger.info(f"Text data from PDF written to {text_file_path}")
            path_to_dataset = text_file_path

        # Fine-tune the model
        logger.info("Fine-tuning model...")
        training_args = TrainingArguments(
            output_dir=f"{os.getcwd()}/results",
            overwrite_output_dir=True,
            num_train_epochs=1,
            per_device_train_batch_size=4,
            save_steps=10_000,
            save_total_limit=2,
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

        # Save the fine-tuned model
        logger.info("Saving fine-tuned model...")
        model.save_pretrained(f"{os.getcwd()}/fine_tuned_models")
        tokenizer.save_pretrained(f"{os.getcwd()}/fine_tuned_models")
        return None
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise e
