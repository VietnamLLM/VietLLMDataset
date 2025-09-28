"""
Translation utilities and pipeline management
"""

import json
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)


class TranslationPipeline:
    """
    Complete translation pipeline for datasets
    """
    
    def __init__(
        self,
        translator,
        dataset_loader,
        output_dir: str = "output",
        save_intermediate: bool = True
    ):
        """
        Initialize translation pipeline
        
        Args:
            translator: Translator instance (e.g., HunyuanTranslator)
            dataset_loader: Dataset loader instance (e.g., GPQALoader)
            output_dir: Output directory for results
            save_intermediate: Whether to save intermediate results
        """
        self.translator = translator
        self.dataset_loader = dataset_loader
        self.output_dir = Path(output_dir)
        self.save_intermediate = save_intermediate
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Track progress
        self.translation_stats = {
            "start_time": None,
            "end_time": None,
            "total_items": 0,
            "successful_translations": 0,
            "failed_translations": 0,
            "fields_translated": []
        }
    
    def run_full_pipeline(
        self,
        dataset_name: str,
        split: str = "train",
        fields_to_translate: Optional[List[str]] = None,
        sample_size: Optional[int] = None
    ) -> Dict:
        """
        Run the complete translation pipeline
        
        Args:
            dataset_name: Name of dataset for output files
            split: Dataset split to load
            fields_to_translate: List of fields to translate (None for all)
            sample_size: Limit to N samples (None for all)
            
        Returns:
            Dictionary with translated dataset and statistics
        """
        self.translation_stats["start_time"] = datetime.now()
        
        try:
            # Step 1: Load dataset
            logger.info(f"Loading dataset: {dataset_name}")
            if sample_size:
                dataset_dict = self.dataset_loader.get_sample_data(sample_size)
            else:
                dataset_dict = self.dataset_loader.load_dataset(split)
            
            self.translation_stats["total_items"] = len(dataset_dict.get("questions", dataset_dict.get("problems", [])))
            
            # Step 2: Determine fields to translate
            if fields_to_translate is None:
                fields_to_translate = self.dataset_loader.get_translatable_fields()
            
            logger.info(f"Translating fields: {fields_to_translate}")
            self.translation_stats["fields_translated"] = fields_to_translate
            
            # Step 3: Translate each field
            for field in fields_to_translate:
                if field in dataset_dict:
                    logger.info(f"Translating field: {field}")
                    
                    try:
                        dataset_dict = self.translator.translate_dataset_field(
                            dataset_dict, 
                            field,
                            output_field=f"{field}_vi"
                        )
                        self.translation_stats["successful_translations"] += len(dataset_dict[field])
                        
                        # Save intermediate results
                        if self.save_intermediate:
                            intermediate_path = self.output_dir / f"{dataset_name}_{field}_translated.json"
                            save_results(
                                {field: dataset_dict[field], f"{field}_vi": dataset_dict[f"{field}_vi"]},
                                str(intermediate_path)
                            )
                            logger.info(f"Saved intermediate results: {intermediate_path}")
                            
                    except Exception as e:
                        logger.error(f"Error translating field {field}: {e}")
                        self.translation_stats["failed_translations"] += len(dataset_dict.get(field, []))
            
            # Step 4: Save final results
            output_path = self.output_dir / f"{dataset_name}_translated.json"
            save_results(dataset_dict, str(output_path))
            
            # Step 5: Generate summary report
            self._generate_summary_report(dataset_name, dataset_dict)
            
            self.translation_stats["end_time"] = datetime.now()
            
            return {
                "translated_dataset": dataset_dict,
                "statistics": self.translation_stats,
                "output_path": str(output_path)
            }
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            self.translation_stats["end_time"] = datetime.now()
            raise
    
    def _generate_summary_report(self, dataset_name: str, dataset_dict: Dict):
        """Generate a summary report of the translation"""
        report = {
            "dataset_name": dataset_name,
            "timestamp": datetime.now().isoformat(),
            "statistics": self.translation_stats,
            "sample_translations": self._get_sample_translations(dataset_dict),
            "model_info": self.translator.get_model_info()
        }
        
        report_path = self.output_dir / f"{dataset_name}_translation_report.json"
        save_results(report, str(report_path))
        logger.info(f"Generated translation report: {report_path}")
    
    def _get_sample_translations(self, dataset_dict: Dict, n_samples: int = 3) -> List[Dict]:
        """Get sample translations for the report"""
        samples = []
        
        # Find translated fields
        translated_fields = [key for key in dataset_dict.keys() if key.endswith("_vi")]
        
        for i in range(min(n_samples, len(list(dataset_dict.values())[0]))):
            sample = {"index": i}
            
            for field in translated_fields:
                original_field = field.replace("_vi", "")
                if original_field in dataset_dict:
                    sample[f"original_{original_field}"] = dataset_dict[original_field][i]
                    sample[f"translated_{original_field}"] = dataset_dict[field][i]
            
            samples.append(sample)
        
        return samples


def save_results(data: Any, output_path: str, format: str = None):
    """
    Save results to file
    
    Args:
        data: Data to save
        output_path: Output file path
        format: Output format (auto-detect from extension if None)
    """
    output_path = Path(output_path)
    
    if format is None:
        format = output_path.suffix.lower()
    
    try:
        if format in ['.json', 'json']:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        elif format in ['.pkl', '.pickle', 'pickle']:
            with open(output_path, 'wb') as f:
                pickle.dump(data, f)
        
        elif format in ['.csv', 'csv']:
            if isinstance(data, dict):
                df = pd.DataFrame(data)
                df.to_csv(output_path, index=False, encoding='utf-8')
            else:
                raise ValueError("CSV format requires dictionary data")
        
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Saved results to: {output_path}")
        
    except Exception as e:
        logger.error(f"Error saving results: {e}")
        raise


def load_results(input_path: str, format: str = None) -> Any:
    """
    Load results from file
    
    Args:
        input_path: Input file path
        format: Input format (auto-detect from extension if None)
        
    Returns:
        Loaded data
    """
    input_path = Path(input_path)
    
    if format is None:
        format = input_path.suffix.lower()
    
    try:
        if format in ['.json', 'json']:
            with open(input_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        elif format in ['.pkl', '.pickle', 'pickle']:
            with open(input_path, 'rb') as f:
                return pickle.load(f)
        
        elif format in ['.csv', 'csv']:
            return pd.read_csv(input_path, encoding='utf-8').to_dict('list')
        
        else:
            raise ValueError(f"Unsupported format: {format}")
        
    except Exception as e:
        logger.error(f"Error loading results: {e}")
        raise