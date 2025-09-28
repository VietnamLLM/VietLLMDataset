"""
Hunyuan-MT-Chimera-7B-fp8 Translation Module
Using local Hunyuan-MT-Chimera-7B-fp8 model for English to Vietnamese translation
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import List, Optional, Union
import logging
from tqdm import tqdm
import time

logger = logging.getLogger(__name__)


class HunyuanTranslator:
    """
    Hunyuan-MT-Chimera-7B-fp8 Translator for English to Vietnamese translation
    """

    def __init__(
        self,
        model_name: str = "./weight/Hunyuan-MT-Chimera-7B-fp8",
        device: Optional[str] = None,
        batch_size: int = 4,
        max_length: int = 512
    ):
        """
        Initialize the Hunyuan-MT-Chimera-7B-fp8 translator

        Args:
            model_name: The local model path (default: ./weight/Hunyuan-MT-Chimera-7B-fp8)
            device: Device to run the model on (auto-detect if None)
            batch_size: Batch size for translation
            max_length: Maximum sequence length
        """
        self.model_name = model_name
        self.batch_size = batch_size
        self.max_length = max_length

        # Auto-detect device if not specified
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        logger.info(f"Using device: {self.device}")

        # Initialize model and tokenizer
        self._load_model()

    def _load_model(self):
        """Load the Hunyuan-MT-Chimera-7B-fp8 model and tokenizer from local path"""
        try:
            logger.info(f"Loading local model: {self.model_name}")

            # Load tokenizer from local path
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                local_files_only=True
            )

            # Load model from local path
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                dtype="auto",
                device_map="auto"
            )

            # Move model to device
            self.model.to(self.device)
            self.model.eval()

            logger.info(
                "Local Hunyuan-MT-Chimera-7B-fp8 model loaded successfully")

        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise

    def translate_single(
        self,
        text: str,
        source_lang: str = "en",
        target_lang: str = "vi"
    ) -> str:
        """
        Translate a single text string

        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            Translated text
        """
        if not text.strip():
            return ""

        try:
            # Prepare input with language codes
            input_text = f"<{source_lang}2{target_lang}> {text}"

            # Tokenize input
            inputs = self.tokenizer(
                input_text,
                return_tensors="pt",
                max_length=self.max_length,
                truncation=True,
                padding=True
            ).to(self.device)

            # Generate translation
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=self.max_length,
                    num_beams=4,
                    early_stopping=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )

            # Decode output
            translated_text = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )

            return translated_text.strip()

        except Exception as e:
            logger.error(f"Translation error for text '{text[:50]}...': {e}")
            return ""

    def translate_batch(
        self,
        texts: List[str],
        source_lang: str = "en",
        target_lang: str = "vi",
        show_progress: bool = True
    ) -> List[str]:
        """
        Translate a batch of texts

        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language code
            show_progress: Whether to show progress bar

        Returns:
            List of translated texts
        """
        if not texts:
            return []

        translated_texts = []

        # Process in batches
        iterator = range(0, len(texts), self.batch_size)
        if show_progress:
            iterator = tqdm(iterator, desc="Translating batches")

        for i in iterator:
            batch_texts = texts[i:i + self.batch_size]
            batch_translations = []

            for text in batch_texts:
                translation = self.translate_single(
                    text, source_lang, target_lang)
                batch_translations.append(translation)

                # Small delay to prevent overwhelming the GPU
                if self.device == "cuda":
                    time.sleep(0.01)

            translated_texts.extend(batch_translations)

        return translated_texts

    def translate_dataset_field(
        self,
        dataset_dict: dict,
        field_name: str,
        output_field: Optional[str] = None,
        source_lang: str = "en",
        target_lang: str = "vi"
    ) -> dict:
        """
        Translate a specific field in a dataset dictionary

        Args:
            dataset_dict: Dictionary containing dataset
            field_name: Name of field to translate
            output_field: Name of output field (default: field_name + "_vi")
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            Updated dataset dictionary with translations
        """
        if field_name not in dataset_dict:
            raise ValueError(f"Field '{field_name}' not found in dataset")

        if output_field is None:
            output_field = f"{field_name}_{target_lang}"

        logger.info(f"Translating field '{field_name}' to '{output_field}'")

        # Get texts to translate
        texts = dataset_dict[field_name]
        if isinstance(texts, str):
            texts = [texts]

        # Translate
        translations = self.translate_batch(texts, source_lang, target_lang)

        # Add to dataset
        dataset_dict[output_field] = translations

        return dataset_dict

    def get_model_info(self) -> dict:
        """Get information about the loaded model"""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "batch_size": self.batch_size,
            "max_length": self.max_length,
            "vocab_size": len(self.tokenizer) if hasattr(self, 'tokenizer') else None
        }
