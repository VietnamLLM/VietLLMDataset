# VietLLMDataset

A comprehensive template project for translating English datasets (GPQA, AIME 2025) to Vietnamese using the **Tencent-Hunyuan/Hunyuan-MT** model. This project provides a complete pipeline for dataset loading, translation, and result management.

## 🚀 Features

- **Hunyuan-MT Integration**: Easy-to-use wrapper for Tencent-Hunyuan/Hunyuan-MT translation model
- **Multiple Dataset Support**: Built-in loaders for GPQA and AIME datasets
- **Batch Processing**: Efficient batch translation with progress tracking
- **Flexible Pipeline**: Modular design for easy customization and extension
- **Comprehensive Logging**: Detailed logging and error handling
- **Multiple Output Formats**: JSON, CSV, and JSONL output support
- **Sample Scripts**: Ready-to-run examples for both datasets

## 📋 Requirements

- Python 3.8+
- PyTorch 2.0+
- Transformers 4.30+
- CUDA-compatible GPU (recommended) or CPU

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/VietnamLLM/VietLLMDataset.git
cd VietLLMDataset
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install the package (optional):**
```bash
pip install -e .
```

## 🏗️ Project Structure

```
VietLLMDataset/
├── src/
│   ├── translation/
│   │   ├── __init__.py
│   │   └── hunyuan_translator.py     # Hunyuan-MT wrapper
│   ├── datasets/
│   │   ├── __init__.py
│   │   ├── gpqa_loader.py           # GPQA dataset loader
│   │   └── aime_loader.py           # AIME dataset loader
│   └── utils/
│       ├── __init__.py
│       ├── logging_config.py        # Logging configuration
│       └── translation_utils.py     # Pipeline utilities
├── examples/
│   ├── simple_translation_demo.py   # Basic demo
│   ├── translate_gpqa.py           # GPQA translation script
│   └── translate_aime.py           # AIME translation script
├── config.yaml                     # Configuration file
├── requirements.txt                # Dependencies
└── README.md                      # This file
```

## 🚀 Quick Start

### 1. Simple Translation Demo

Test the Hunyuan-MT model with sample texts:

```bash
python examples/simple_translation_demo.py
```

### 2. GPQA Dataset Translation

Translate GPQA dataset:

```bash
python examples/translate_gpqa.py
```

### 3. AIME Dataset Translation

Translate AIME problems:

```bash
python examples/translate_aime.py
```

## 💻 Usage Examples

### Basic Translation

```python
from src.translation.hunyuan_translator import HunyuanTranslator

# Initialize translator
translator = HunyuanTranslator(
    model_name="Tencent-Hunyuan/Hunyuan-MT",
    batch_size=4,
    max_length=512
)

# Translate single text
result = translator.translate_single("What is machine learning?")
print(result)  # Output: Vietnamese translation

# Translate multiple texts
texts = ["Hello world", "How are you?", "Good morning"]
translations = translator.translate_batch(texts)
```

### Dataset Translation Pipeline

```python
from src.translation.hunyuan_translator import HunyuanTranslator
from src.datasets.gpqa_loader import GPQALoader
from src.utils.translation_utils import TranslationPipeline

# Setup components
translator = HunyuanTranslator()
loader = GPQALoader(subset="gpqa_main")
pipeline = TranslationPipeline(translator, loader, output_dir="output")

# Run translation
results = pipeline.run_full_pipeline(
    dataset_name="gpqa_sample",
    sample_size=10,
    fields_to_translate=["questions", "explanations"]
)
```

### Custom Dataset Loading

```python
from src.datasets.gpqa_loader import GPQALoader

# Load GPQA dataset
loader = GPQALoader(subset="gpqa_main")
dataset = loader.load_dataset(split="train")

# Get sample data for testing
sample = loader.get_sample_data(n_samples=5)

# Save translated results
loader.save_translated_dataset(dataset, "output/gpqa_translated.json")
```

## ⚙️ Configuration

Edit `config.yaml` to customize settings:

```yaml
model:
  name: "Tencent-Hunyuan/Hunyuan-MT"
  batch_size: 4
  max_length: 512

datasets:
  gpqa:
    subset: "gpqa_main"
    translatable_fields: ["questions", "choices", "explanations"]
  
  aime:
    year: 2025
    translatable_fields: ["problems", "solutions"]

translation:
  source_language: "en"
  target_language: "vi"
  save_intermediate: true
```

## 📊 Supported Datasets

### GPQA (Graduate-Level Google-Proof Q&A)
- **Subsets**: `gpqa_main`, `gpqa_extended`, `gpqa_diamond`
- **Fields**: Questions, multiple choice options, explanations
- **Use Case**: Academic question-answering in Vietnamese

### AIME (American Invitational Mathematics Examination)
- **Year**: 2025 (configurable)
- **Fields**: Mathematical problems, detailed solutions
- **Use Case**: Mathematical reasoning in Vietnamese

## 🔧 Advanced Features

### Custom Translation Fields

```python
# Translate specific fields only
translator.translate_dataset_field(
    dataset_dict, 
    field_name="questions",
    output_field="questions_vietnamese"
)
```

### Batch Processing with Progress

```python
translations = translator.translate_batch(
    texts, 
    show_progress=True,
    batch_size=8
)
```

### Error Handling and Logging

```python
from src.utils.logging_config import setup_logging

# Setup comprehensive logging
setup_logging(
    level="INFO",
    log_file="logs/translation.log",
    console_output=True
)
```

## 📈 Performance Tips

1. **GPU Usage**: Ensure CUDA is available for faster translation
2. **Batch Size**: Adjust batch size based on GPU memory
3. **Max Length**: Set appropriate max_length for your content
4. **Sample Testing**: Start with small samples before full datasets

## 🔍 Troubleshooting

### Common Issues

1. **Model Loading Error**:
   - Ensure internet connection for model download
   - Check available disk space (models are large)
   - Verify Hugging Face Hub access

2. **CUDA Out of Memory**:
   - Reduce batch_size in configuration
   - Use CPU instead: `device="cpu"`
   - Clear GPU memory between runs

3. **Dataset Loading Issues**:
   - Check internet connection for dataset download
   - Verify dataset names and splits
   - Review sample data first

### System Requirements

- **Minimum**: 8GB RAM, CPU only
- **Recommended**: 16GB+ RAM, CUDA GPU with 8GB+ VRAM
- **Storage**: 10GB+ free space for models and data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-dataset`
3. Make your changes and add tests
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Tencent-Hunyuan/Hunyuan-MT](https://huggingface.co/Tencent-Hunyuan/Hunyuan-MT) for the translation model
- [Hugging Face](https://huggingface.co/) for the datasets and transformers library
- [VietnamLLM](https://github.com/VietnamLLM) community for Vietnamese NLP resources

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/VietnamLLM/VietLLMDataset/issues)
- **Discussions**: [GitHub Discussions](https://github.com/VietnamLLM/VietLLMDataset/discussions)
- **Email**: contact@vietnamllm.org

---

**Happy Translating! 🇻🇳✨**