import os
import re
from logging import getLogger
from typing import List, Optional

from src.services import model, tokenizer

from datasets import Dataset, load_dataset
from PyPDF2 import PdfReader
from transformers import (
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

logger = getLogger()


def convert_pdf_to_text(pdf_path: str) -> str:
    """Convert a PDF to plain text using PyPDF2.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted plain text from the PDF.
    """
    logger.info(f"Opening PDF file at {pdf_path} for text extraction.")
    text: str = ""

    try:
        with open(pdf_path, "rb") as file:
            reader: PdfReader = PdfReader(file)
            num_pages: int = len(reader.pages)

            logger.info(f"Extracting text from {num_pages} pages.")
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                extracted_text = page.extract_text() or ""
                text += extracted_text

        logger.info("PDF text extraction completed.")
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {e}")
        raise e

    return text


def clean_text(text: str) -> str:
    """Clean and preprocess extracted text.

    Args:
        text (str): The raw text extracted from a PDF.

    Returns:
        str: The cleaned text.
    """
    logger.info("Cleaning extracted text.")
    try:
        # Remove standalone numbers (e.g., page numbers)
        text = re.sub(r"\s*\d+\s*", " ", text)

        # Remove excess newlines
        text = re.sub(r"\n+", "\n", text)

        cleaned_text = text.strip()
        logger.info("Text cleaning completed.")
    except Exception as e:
        logger.error(f"Failed to clean text: {e}")
        raise e

    return cleaned_text


def split_text_into_chunks(
    text: str, tokenizer, max_length: int = 1024
) -> List[List[int]]:
    """Split text into tokenized chunks based on the model's token limit.

    Args:
        text (str): The input text to be tokenized and split.
        tokenizer: The tokenizer for tokenizing the input text.
        max_length (int, optional): The maximum token length for each chunk. Defaults to 1024.

    Returns:
        List[List[int]]: A list of tokenized chunks.
    """
    logger.info(f"Splitting text into chunks with max token length of {max_length}.")
    try:
        tokens = tokenizer(text, return_tensors="pt", truncation=False)["input_ids"][0]
        chunks = [
            tokens[i : i + max_length].tolist()
            for i in range(0, len(tokens), max_length)
        ]
        logger.info(f"Text split into {len(chunks)} chunks.")
    except Exception as e:
        logger.error(f"Failed to split text into chunks: {e}")
        raise e

    return chunks


def create_tokenized_dataset(chunks: List[List[int]]) -> Dataset:
    """Create a Hugging Face dataset from tokenized chunks.

    Args:
        chunks (List[List[int]]): The tokenized chunks.

    Returns:
        Dataset: A Hugging Face dataset containing the tokenized chunks.
    """
    logger.info("Creating a dataset from tokenized chunks.")
    try:
        data = {"input_ids": chunks}
        dataset = Dataset.from_dict(data)
        logger.info("Dataset creation completed.")
    except Exception as e:
        logger.error(f"Failed to create dataset: {e}")
        raise e

    return dataset


async def fine_tune_pdf(path_to_pdf: str) -> Optional[str]:
    """Fine-tune the GPT-2 model using the provided PDF file.

    Args:
        path_to_pdf (str): The path to the PDF file.

    Returns:
        Optional[str]: Returns None if the process is successful, otherwise raises an error.
    """
    try:
        # Convert PDF to text
        logger.info("Starting PDF to text conversion.")
        text_data: str = convert_pdf_to_text(path_to_pdf)

        # Clean the text data
        logger.info("Starting text cleaning.")
        cleaned_text: str = clean_text(text_data)

        # Split the text into chunks
        logger.info("Starting text chunking.")
        text_chunks: List[List[int]] = split_text_into_chunks(cleaned_text, tokenizer)

        # Create a tokenized dataset
        logger.info("Creating tokenized dataset for training.")
        tokenized_dataset: Dataset = create_tokenized_dataset(text_chunks)

        # Save dataset to file for future use
        logger.info("Saving tokenized dataset to file.")
        tokenized_dataset.save_to_disk(f"{os.getcwd()}/datasets")

        # Define data collator for dynamic padding
        data_collator: DataCollatorForLanguageModeling = (
            DataCollatorForLanguageModeling(
                tokenizer=tokenizer,
                mlm=False,  # Not using Masked Language Modeling for GPT-2
            )
        )

        # Fine-tune the model
        logger.info("Starting model fine-tuning.")
        training_args: TrainingArguments = TrainingArguments(
            output_dir=f"{os.getcwd()}/results",
            num_train_epochs=3,
            per_device_train_batch_size=4,
            save_steps=10_000,
            save_total_limit=2,
        )

        trainer: Trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset,
            data_collator=data_collator,
        )

        trainer.train()

        # Save the fine-tuned model
        logger.info("Saving the fine-tuned model.")
        model.save_pretrained(f"{os.getcwd()}/fine_tuned_models")
        tokenizer.save_pretrained(f"{os.getcwd()}/fine_tuned_models")

        logger.info("Model fine-tuning completed successfully.")
        return None
    except Exception as e:
        logger.error(f"Fine-tuning failed: {str(e)}")
        raise e


async def fine_tune(path_to_dataset: str) -> Optional[str]:
    """Fine-tune the model using the provided dataset (text file or PDF).

    Args:
        path_to_dataset: The path to the dataset, which can be a .txt or .pdf file.

    Returns:
        Optional[str]: Returns None if the process is successful, otherwise raises an error.
    """
    try:
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
