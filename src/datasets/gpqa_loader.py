"""
GPQA Dataset Loader
Loading and processing GPQA (Graduate-Level Google-Proof Q&A) dataset
"""

from datasets import load_dataset
import pandas as pd
from typing import Dict, List, Optional, Union
import logging

logger = logging.getLogger(__name__)


class GPQALoader:
    """
    GPQA Dataset Loader for English to Vietnamese translation
    """
    
    def __init__(self, subset: str = "gpqa_main"):
        """
        Initialize GPQA loader
        
        Args:
            subset: GPQA subset to load ('gpqa_main', 'gpqa_extended', 'gpqa_diamond')
        """
        self.subset = subset
        self.dataset = None
        self.available_subsets = ["gpqa_main", "gpqa_extended", "gpqa_diamond"]
        
        if subset not in self.available_subsets:
            logger.warning(f"Subset '{subset}' not in known subsets: {self.available_subsets}")
    
    def load_dataset(self, split: str = "train") -> Dict:
        """
        Load GPQA dataset
        
        Args:
            split: Dataset split to load
            
        Returns:
            Dataset dictionary
        """
        try:
            logger.info(f"Loading GPQA dataset: {self.subset}, split: {split}")
            
            # Load from Hugging Face datasets
            self.dataset = load_dataset("Idavidrein/gpqa", self.subset, split=split)
            
            # Convert to dictionary format
            dataset_dict = {
                "questions": [],
                "choices": [],
                "correct_answers": [],
                "explanations": [],
                "metadata": []
            }
            
            for item in self.dataset:
                # Question text
                dataset_dict["questions"].append(item.get("Question", ""))
                
                # Multiple choice options
                choices = []
                for choice_key in ["A", "B", "C", "D"]:
                    if choice_key in item:
                        choices.append(f"{choice_key}: {item[choice_key]}")
                dataset_dict["choices"].append("\n".join(choices))
                
                # Correct answer
                dataset_dict["correct_answers"].append(item.get("Correct Answer", ""))
                
                # Explanation
                dataset_dict["explanations"].append(item.get("Explanation", ""))
                
                # Metadata
                metadata = {
                    "subject": item.get("Subject", ""),
                    "difficulty": item.get("Difficulty", ""),
                    "question_type": item.get("Question Type", "")
                }
                dataset_dict["metadata"].append(metadata)
            
            logger.info(f"Loaded {len(dataset_dict['questions'])} GPQA examples")
            return dataset_dict
            
        except Exception as e:
            logger.error(f"Error loading GPQA dataset: {e}")
            # Return empty structure if loading fails
            return {
                "questions": [],
                "choices": [],
                "correct_answers": [],
                "explanations": [],
                "metadata": []
            }
    
    def get_translatable_fields(self) -> List[str]:
        """Get list of fields that should be translated"""
        return ["questions", "choices", "explanations"]
    
    def prepare_for_translation(self, dataset_dict: Dict) -> Dict:
        """
        Prepare dataset for translation by combining relevant text fields
        
        Args:
            dataset_dict: Dataset dictionary
            
        Returns:
            Prepared dataset dictionary
        """
        prepared_dict = dataset_dict.copy()
        
        # Combine question and choices for better context
        combined_texts = []
        for i, (question, choices) in enumerate(zip(dataset_dict["questions"], dataset_dict["choices"])):
            combined_text = f"Question: {question}\n\nAnswer choices:\n{choices}"
            combined_texts.append(combined_text)
        
        prepared_dict["combined_question_choices"] = combined_texts
        
        return prepared_dict
    
    def save_translated_dataset(
        self, 
        dataset_dict: Dict, 
        output_path: str,
        format: str = "json"
    ):
        """
        Save translated dataset to file
        
        Args:
            dataset_dict: Translated dataset dictionary
            output_path: Output file path
            format: Output format ('json', 'csv', 'jsonl')
        """
        try:
            if format == "json":
                import json
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(dataset_dict, f, ensure_ascii=False, indent=2)
            
            elif format == "csv":
                df = pd.DataFrame(dataset_dict)
                df.to_csv(output_path, index=False, encoding='utf-8')
            
            elif format == "jsonl":
                import json
                with open(output_path, 'w', encoding='utf-8') as f:
                    for i in range(len(dataset_dict["questions"])):
                        item = {key: values[i] for key, values in dataset_dict.items() 
                               if isinstance(values, list) and i < len(values)}
                        f.write(json.dumps(item, ensure_ascii=False) + '\n')
            
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            logger.info(f"Saved translated GPQA dataset to {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving dataset: {e}")
            raise
    
    def get_sample_data(self, n_samples: int = 5) -> Dict:
        """
        Get a small sample of the dataset for testing
        
        Args:
            n_samples: Number of samples to return
            
        Returns:
            Sample dataset dictionary
        """
        if self.dataset is None:
            dataset_dict = self.load_dataset()
        else:
            dataset_dict = {
                "questions": [item["Question"] for item in self.dataset],
                "choices": [],
                "correct_answers": [item["Correct Answer"] for item in self.dataset],
                "explanations": [item["Explanation"] for item in self.dataset]
            }
            
            for item in self.dataset:
                choices = []
                for choice_key in ["A", "B", "C", "D"]:
                    if choice_key in item:
                        choices.append(f"{choice_key}: {item[choice_key]}")
                dataset_dict["choices"].append("\n".join(choices))
        
        # Return first n_samples
        sample_dict = {}
        for key, values in dataset_dict.items():
            if isinstance(values, list):
                sample_dict[key] = values[:n_samples]
            else:
                sample_dict[key] = values
        
        return sample_dict