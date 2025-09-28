# Usage Guide - VietLLMDataset Translation Project

This guide provides detailed instructions on how to use the VietLLMDataset translation project.

## 🚀 Getting Started

### Prerequisites

1. **Python Environment**: Python 3.8 or higher
2. **GPU (Recommended)**: CUDA-compatible GPU with 8GB+ VRAM
3. **Internet Connection**: For downloading models and datasets
4. **Disk Space**: At least 10GB free space

### Installation Steps

```bash
# 1. Clone repository
git clone https://github.com/VietnamLLM/VietLLMDataset.git
cd VietLLMDataset

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify installation
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import transformers; print(f'Transformers: {transformers.__version__}')"
```

## 🎯 Quick Start Examples

### 1. Simple Demo (5 minutes)

Test the translation functionality with sample texts:

```bash
python examples/simple_translation_demo.py
```

This will:
- Load the Hunyuan-MT model
- Translate 5 sample English texts to Vietnamese
- Show both single and batch translation examples

### 2. Command Line Interface

Use the main script with different options:

```bash
# Run demo
python run_translation.py demo

# Translate GPQA sample (5 questions)
python run_translation.py gpqa --sample-size 5

# Translate AIME problems (3 problems)
python run_translation.py aime --sample-size 3 --aime-year 2025

# Full GPQA translation with custom settings
python run_translation.py gpqa --batch-size 2 --max-length 1024 --output-dir my_output
```

### 3. Programmatic Usage

```python
# Basic translation
from src.translation.hunyuan_translator import HunyuanTranslator

translator = HunyuanTranslator()
result = translator.translate_single("What is artificial intelligence?")
print(f"Vietnamese: {result}")
```

## 📚 Dataset Translation Workflows

### GPQA Dataset Translation

GPQA (Graduate-Level Google-Proof Q&A) contains academic questions across multiple subjects.

```bash
# Quick start - translate 10 sample questions
python examples/translate_gpqa.py

# Full translation with specific subset
python run_translation.py gpqa --gpqa-subset gpqa_extended --batch-size 4

# Large scale translation (all data)
python run_translation.py gpqa --gpqa-subset gpqa_main --max-length 1024
```

**GPQA Features:**
- 3 subsets: `gpqa_main`, `gpqa_extended`, `gpqa_diamond`
- Fields translated: questions, multiple choice options, explanations
- Typical size: 448 questions (gpqa_main)

### AIME Dataset Translation

AIME contains mathematical competition problems with detailed solutions.

```bash
# Quick start - translate 3 sample problems
python examples/translate_aime.py

# Specific year and settings
python run_translation.py aime --aime-year 2025 --max-length 1024 --batch-size 2

# Focus on specific fields
python -c "
from src.translation.hunyuan_translator import HunyuanTranslator
from src.datasets.aime_loader import AIMELoader

translator = HunyuanTranslator()
loader = AIMELoader(2025)
data = loader.get_sample_data(2)
translated = translator.translate_dataset_field(data, 'problems')
print(translated['problems_vi'][0])
"
```

**AIME Features:**
- Mathematical competition problems
- Fields translated: problems, solutions
- Complex mathematical notation and formulas

## ⚙️ Configuration Options

### Model Configuration

```python
translator = HunyuanTranslator(
    model_name="./weight/Hunyuan-MT-Chimera-7B-fp8",  # Local model path
    device="cuda",                                    # cuda, cpu, auto
    batch_size=4,                                    # Batch size for processing
    max_length=512                                   # Maximum sequence length
)
```

### Translation Settings

```python
# Single text translation
translation = translator.translate_single(
    text="Your English text here",
    source_lang="en",
    target_lang="vi"
)

# Batch translation with progress
translations = translator.translate_batch(
    texts=["Text 1", "Text 2", "Text 3"],
    source_lang="en",
    target_lang="vi",
    show_progress=True
)
```

### Pipeline Configuration

```python
from src.utils.translation_utils import TranslationPipeline

pipeline = TranslationPipeline(
    translator=translator,
    dataset_loader=loader,
    output_dir="custom_output",     # Output directory
    save_intermediate=True          # Save progress files
)

results = pipeline.run_full_pipeline(
    dataset_name="my_dataset",
    split="train",
    sample_size=100,                # Limit to 100 samples
    fields_to_translate=["questions", "explanations"]
)
```

## 📁 Output Structure

After translation, you'll find organized output files:

```
output/
├── gpqa/                          # GPQA translations
│   ├── gpqa_main_translated.json  # Full translated dataset
│   ├── gpqa_main_questions_translated.json  # Intermediate results
│   └── gpqa_main_translation_report.json    # Summary report
├── aime/                          # AIME translations
│   ├── aime_2025_translated.json
│   └── aime_2025_translation_report.json
└── logs/                          # Log files
    ├── gpqa_translation.log
    └── aime_translation.log
```

### Output Formats

**JSON Format (default):**
```json
{
  "questions": ["What is...?", "How does...?"],
  "questions_vi": ["Cái gì là...?", "Làm thế nào...?"],
  "explanations": ["This explains...", "The reason is..."],
  "explanations_vi": ["Điều này giải thích...", "Lý do là..."]
}
```

**CSV Format:**
```bash
# Save as CSV
python -c "
from src.datasets.gpqa_loader import GPQALoader
loader = GPQALoader()
data = {...}  # Your translated data
loader.save_translated_dataset(data, 'output.csv', format='csv')
"
```

## 🔧 Advanced Usage

### Custom Dataset Integration

```python
# Create custom dataset loader
class MyDatasetLoader:
    def load_dataset(self, split="train"):
        return {
            "texts": ["Text 1", "Text 2"],
            "labels": ["Label 1", "Label 2"]
        }
    
    def get_translatable_fields(self):
        return ["texts"]

# Use with pipeline
loader = MyDatasetLoader()
pipeline = TranslationPipeline(translator, loader)
results = pipeline.run_full_pipeline("my_data")
```

### Batch Processing Large Datasets

```python
# Process in chunks for large datasets
def process_large_dataset(dataset, chunk_size=100):
    total_items = len(dataset["questions"])
    
    for i in range(0, total_items, chunk_size):
        chunk = {
            key: values[i:i+chunk_size] 
            for key, values in dataset.items()
        }
        
        # Process chunk
        translated_chunk = translator.translate_dataset_field(chunk, "questions")
        
        # Save intermediate results
        save_results(translated_chunk, f"chunk_{i}.json")
        
        print(f"Processed {min(i+chunk_size, total_items)}/{total_items}")
```

### Error Handling and Recovery

```python
import logging
from src.utils.logging_config import setup_logging

# Setup detailed logging
setup_logging(level="DEBUG", log_file="debug.log")

try:
    # Your translation code
    results = pipeline.run_full_pipeline(...)
    
except Exception as e:
    logging.error(f"Translation failed: {e}")
    
    # Check intermediate files for partial results
    import glob
    intermediate_files = glob.glob("output/*/intermediate_*.json")
    print(f"Found {len(intermediate_files)} intermediate files")
```

## 🚨 Troubleshooting

### Common Issues and Solutions

1. **CUDA Out of Memory**
   ```bash
   # Solution 1: Reduce batch size
   python run_translation.py gpqa --batch-size 1
   
   # Solution 2: Use CPU
   python run_translation.py gpqa --device cpu
   
   # Solution 3: Reduce max length
   python run_translation.py gpqa --max-length 256
   ```

2. **Model Download Issues**
   ```python
   # Check internet connection and disk space
   import torch
   print(f"CUDA available: {torch.cuda.is_available()}")
   
   # Manual model download
   from transformers import AutoTokenizer
   tokenizer = AutoTokenizer.from_pretrained("./weight/Hunyuan-MT-Chimera-7B-fp8", local_files_only=True)
   ```

3. **Dataset Loading Problems**
   ```python
   # Test dataset access
   from datasets import load_dataset
   try:
       dataset = load_dataset("Idavidrein/gpqa", "gpqa_main")
       print(f"Dataset loaded: {len(dataset)} items")
   except Exception as e:
       print(f"Dataset error: {e}")
   ```

### Performance Optimization

1. **GPU Utilization**
   ```bash
   # Monitor GPU usage
   nvidia-smi
   
   # Optimize batch size
   python run_translation.py gpqa --batch-size 8  # Try different sizes
   ```

2. **Memory Management**
   ```python
   # Clear GPU memory between runs
   import torch
   torch.cuda.empty_cache()
   ```

3. **Parallel Processing**
   ```python
   # Use multiple processes for CPU-bound tasks
   from multiprocessing import Pool
   
   def translate_chunk(chunk):
       return translator.translate_batch(chunk)
   
   with Pool(4) as pool:
       results = pool.map(translate_chunk, text_chunks)
   ```

## 📊 Monitoring and Analytics

### Translation Quality Assessment

```python
# Sample quality check
def assess_translation_quality(original, translated, sample_size=5):
    samples = list(zip(original[:sample_size], translated[:sample_size]))
    
    for i, (orig, trans) in enumerate(samples, 1):
        print(f"\n--- Sample {i} ---")
        print(f"EN: {orig}")
        print(f"VI: {trans}")
        print(f"Length ratio: {len(trans)/len(orig):.2f}")
```

### Progress Tracking

```python
# Real-time progress monitoring
from tqdm import tqdm
import time

def translate_with_monitoring(texts, translator):
    results = []
    
    for text in tqdm(texts, desc="Translating"):
        start_time = time.time()
        result = translator.translate_single(text)
        duration = time.time() - start_time
        
        results.append(result)
        
        # Log statistics
        print(f"Translation time: {duration:.2f}s, Length: {len(result)}")
    
    return results
```

## 🤝 Integration Examples

### Jupyter Notebook Integration

```python
# In Jupyter notebook
%load_ext autoreload
%autoreload 2

import sys
sys.path.append('src')

from translation.hunyuan_translator import HunyuanTranslator
from datasets.gpqa_loader import GPQALoader

# Interactive translation
translator = HunyuanTranslator()
text = input("Enter English text: ")
result = translator.translate_single(text)
print(f"Vietnamese: {result}")
```

### Web API Integration

```python
from flask import Flask, request, jsonify
from src.translation.hunyuan_translator import HunyuanTranslator

app = Flask(__name__)
translator = HunyuanTranslator()

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        translation = translator.translate_single(text)
        return jsonify({
            'original': text,
            'translation': translation
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## 💡 Best Practices

1. **Start Small**: Always test with sample data first
2. **Monitor Resources**: Keep an eye on GPU memory and disk space
3. **Save Intermediate Results**: Enable intermediate saving for long runs
4. **Quality Checks**: Manually review sample translations
5. **Documentation**: Keep track of translation parameters and results

## 📞 Getting Help

- **Documentation**: Check this guide and README.md
- **Issues**: Report bugs on GitHub Issues
- **Community**: Join discussions on GitHub Discussions
- **Logs**: Check log files for detailed error information

---

Happy translating! 🇻🇳✨