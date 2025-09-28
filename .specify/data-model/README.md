# Data Model

This directory contains data models and schemas for the VietLLMDataset system.

## Files

- `README.md`: This file

## Data Model Overview

The VietLLMDataset data model defines:

- **Core Models**: Translation requests, responses, and batch processing
- **Dataset Models**: GPQA and AIME dataset structures
- **Configuration Models**: System and model configuration
- **Quality Models**: Translation quality assessment
- **Error Models**: Error handling and reporting

## Model Categories

### 1. Translation Models
- `TranslationRequest`: Single translation request
- `TranslationResponse`: Translation result
- `BatchTranslationRequest`: Batch translation request
- `BatchTranslationResponse`: Batch translation result

### 2. Dataset Models
- `GPQAItem`: GPQA dataset item structure
- `GPQADataset`: GPQA dataset container
- `AIMEItem`: AIME dataset item structure
- `AIMEDataset`: AIME dataset container

### 3. Configuration Models
- `ModelConfig`: Model configuration
- `DatasetConfig`: Dataset configuration
- `TranslationConfig`: Translation settings

### 4. Quality Models
- `QualityMetrics`: Translation quality metrics
- `QualityReport`: Quality assessment report
- `TranslationValidation`: Translation validation

### 5. Error Models
- `TranslationError`: Translation-specific errors
- `SystemError`: System-level errors
- `ErrorResponse`: API error responses

## Usage

These models are used for:

1. **Data Validation**: Input/output validation
2. **API Serialization**: JSON serialization/deserialization
3. **Database Schema**: Database table definitions
4. **Type Safety**: Type hints and validation
5. **Documentation**: API documentation generation

## Standards

- **Python Dataclasses**: Primary model definition format
- **JSON Schema**: Data validation schemas
- **Type Hints**: Python type annotations
- **Pydantic**: Optional validation framework

## Validation

All data models include:

- **Type Validation**: Data type checking
- **Required Fields**: Mandatory field validation
- **Format Validation**: Data format validation
- **Range Validation**: Numeric range validation
- **Custom Validation**: Business rule validation

## Examples

### Translation Request
```python
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class TranslationRequest:
    text: str
    source_language: str = "en"
    target_language: str = "vi"
    max_length: int = 512
    metadata: Optional[Dict[str, Any]] = None
```

### Translation Response
```python
@dataclass
class TranslationResponse:
    original_text: str
    translated_text: str
    confidence_score: float
    processing_time: float
    quality_metrics: Optional[QualityMetrics] = None
```

## Support

For questions about data models, contact the development team.
