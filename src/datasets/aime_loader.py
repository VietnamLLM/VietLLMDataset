"""
AIME Dataset Loader
Loading and processing AIME (American Invitational Mathematics Examination) dataset
"""

from datasets import load_dataset
import pandas as pd
from typing import Dict, List, Optional, Union
import logging
import json
import requests

logger = logging.getLogger(__name__)


class AIMELoader:
    """
    AIME Dataset Loader for English to Vietnamese translation
    """
    
    def __init__(self, year: Optional[int] = 2025):
        """
        Initialize AIME loader
        
        Args:
            year: AIME year to focus on (default: 2025)
        """
        self.year = year
        self.dataset = None
    
    def load_dataset(self, split: str = "train") -> Dict:
        """
        Load AIME dataset
        
        Args:
            split: Dataset split to load
            
        Returns:
            Dataset dictionary
        """
        try:
            logger.info(f"Loading AIME dataset for year: {self.year}")
            
            # Try to load from Hugging Face datasets
            # Note: Actual dataset name may vary, using a common math dataset as fallback
            try:
                # Try loading AIME-specific dataset
                self.dataset = load_dataset("hendrycks/competition_math", split=split)
                # Filter for AIME-style problems
                aime_problems = [item for item in self.dataset if "AIME" in str(item.get("type", "")).upper()]
                
            except Exception as e:
                logger.warning(f"Could not load specific AIME dataset: {e}")
                # Load general math competition dataset
                self.dataset = load_dataset("hendrycks/competition_math", split=split)
                # Take a subset that represents AIME-style problems
                aime_problems = [item for item in self.dataset if item.get("level", "") in ["Level 3", "Level 4", "Level 5"]][:50]
            
            # Convert to dictionary format
            dataset_dict = {
                "problems": [],
                "solutions": [],
                "answers": [],
                "difficulty_levels": [],
                "topics": [],
                "metadata": []
            }
            
            for item in aime_problems:
                # Problem statement
                dataset_dict["problems"].append(item.get("problem", ""))
                
                # Solution
                dataset_dict["solutions"].append(item.get("solution", ""))
                
                # Answer (often numeric for AIME)
                dataset_dict["answers"].append(str(item.get("answer", "")))
                
                # Difficulty level
                dataset_dict["difficulty_levels"].append(item.get("level", "Unknown"))
                
                # Topic/Subject
                dataset_dict["topics"].append(item.get("type", "Mathematics"))
                
                # Metadata
                metadata = {
                    "year": self.year,
                    "problem_type": "AIME-style",
                    "subject": item.get("subject", "Mathematics"),
                    "source": item.get("source", "Competition Math")
                }
                dataset_dict["metadata"].append(metadata)
            
            # If we still don't have enough problems, create some sample AIME-style problems
            if len(dataset_dict["problems"]) < 5:
                dataset_dict = self._create_sample_aime_problems()
            
            logger.info(f"Loaded {len(dataset_dict['problems'])} AIME-style problems")
            return dataset_dict
            
        except Exception as e:
            logger.error(f"Error loading AIME dataset: {e}")
            # Return sample problems if loading fails
            return self._create_sample_aime_problems()
    
    def _create_sample_aime_problems(self) -> Dict:
        """Create sample AIME-style problems for demonstration"""
        return {
            "problems": [
                "Find the number of positive integers n ≤ 1000 such that gcd(n, 1000) = 1.",
                "Let S be the set of all positive integers that have exactly four positive divisors. Find the sum of the first 10 elements of S.",
                "A regular hexagon with side length 4 is inscribed in a circle. Find the area of the region inside the circle but outside the hexagon.",
                "Find the remainder when 2^100 is divided by 125.",
                "In triangle ABC, angle A = 60°, AB = 8, and AC = 6. Find the length of the median from A to side BC."
            ],
            "solutions": [
                "We need to find the number of positive integers n ≤ 1000 that are relatively prime to 1000. Since 1000 = 2³ × 5³, we use Euler's totient function: φ(1000) = 1000 × (1 - 1/2) × (1 - 1/5) = 1000 × 1/2 × 4/5 = 400.",
                "Numbers with exactly four positive divisors are either p³ (where p is prime) or pq (where p and q are distinct primes). The first 10 such numbers are: 6, 8, 10, 14, 15, 21, 22, 26, 27, 33. Their sum is 202.",
                "The area of the circle is π × (4√3/√3)² = 48π/3 = 16π. The area of the regular hexagon is 6 × (√3/4) × 4² = 24√3. The area outside the hexagon is 16π - 24√3.",
                "We use Euler's theorem. Since gcd(2, 125) = 1 and φ(125) = 100, we have 2^100 ≡ 1 (mod 125). Therefore, the remainder is 1.",
                "Using the median length formula in a triangle: m_a² = (2b² + 2c² - a²)/4. First find a using the law of cosines: a² = 8² + 6² - 2(8)(6)cos(60°) = 64 + 36 - 48 = 52. Then m_a² = (2(64) + 2(36) - 52)/4 = 148/4 = 37. So m_a = √37."
            ],
            "answers": ["400", "202", "16π - 24√3", "1", "√37"],
            "difficulty_levels": ["Level 4", "Level 4", "Level 3", "Level 4", "Level 3"],
            "topics": ["Number Theory", "Number Theory", "Geometry", "Number Theory", "Geometry"],
            "metadata": [
                {"year": self.year, "problem_type": "AIME-style", "subject": "Number Theory", "source": "Sample"},
                {"year": self.year, "problem_type": "AIME-style", "subject": "Number Theory", "source": "Sample"},
                {"year": self.year, "problem_type": "AIME-style", "subject": "Geometry", "source": "Sample"},
                {"year": self.year, "problem_type": "AIME-style", "subject": "Number Theory", "source": "Sample"},
                {"year": self.year, "problem_type": "AIME-style", "subject": "Geometry", "source": "Sample"}
            ]
        }
    
    def get_translatable_fields(self) -> List[str]:
        """Get list of fields that should be translated"""
        return ["problems", "solutions"]
    
    def prepare_for_translation(self, dataset_dict: Dict) -> Dict:
        """
        Prepare dataset for translation
        
        Args:
            dataset_dict: Dataset dictionary
            
        Returns:
            Prepared dataset dictionary
        """
        prepared_dict = dataset_dict.copy()
        
        # Combine problem and solution for better context
        combined_texts = []
        for i, (problem, solution) in enumerate(zip(dataset_dict["problems"], dataset_dict["solutions"])):
            combined_text = f"Problem: {problem}\n\nSolution: {solution}"
            combined_texts.append(combined_text)
        
        prepared_dict["combined_problem_solution"] = combined_texts
        
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
                    for i in range(len(dataset_dict["problems"])):
                        item = {key: values[i] for key, values in dataset_dict.items() 
                               if isinstance(values, list) and i < len(values)}
                        f.write(json.dumps(item, ensure_ascii=False) + '\n')
            
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            logger.info(f"Saved translated AIME dataset to {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving dataset: {e}")
            raise
    
    def get_sample_data(self, n_samples: int = 3) -> Dict:
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
            dataset_dict = self.load_dataset()
        
        # Return first n_samples
        sample_dict = {}
        for key, values in dataset_dict.items():
            if isinstance(values, list):
                sample_dict[key] = values[:n_samples]
            else:
                sample_dict[key] = values
        
        return sample_dict