# VietLLMDataset - Data Model

## Overview

This document defines the data models and schemas used throughout the VietLLMDataset system. The data model covers input datasets, translation outputs, configuration data, and internal processing structures.

## Core Data Models

### 1. Translation Request Model

#### TranslationRequest
```python
@dataclass
class TranslationRequest:
    text: str
    source_language: str = "en"
    target_language: str = "vi"
    max_length: int = 512
    batch_id: Optional[str] = None
    request_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
```

**Fields**:
- `text`: Source text to translate
- `source_language`: Source language code (default: "en")
- `target_language`: Target language code (default: "vi")
- `max_length`: Maximum length for translation
- `batch_id`: Identifier for batch processing
- `request_id`: Unique request identifier
- `metadata`: Additional metadata for the request

### 2. Translation Response Model

#### TranslationResponse
```python
@dataclass
class TranslationResponse:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence_score: Optional[float] = None
    processing_time: Optional[float] = None
    request_id: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
```

**Fields**:
- `original_text`: Original source text
- `translated_text`: Translated text
- `source_language`: Source language code
- `target_language`: Target language code
- `confidence_score`: Translation confidence score (0.0-1.0)
- `processing_time`: Time taken for translation (seconds)
- `request_id`: Unique request identifier
- `error_message`: Error message if translation failed
- `metadata`: Additional metadata

### 3. Batch Translation Model

#### BatchTranslationRequest
```python
@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str = "en"
    target_language: str = "vi"
    batch_size: int = 4
    max_length: int = 512
    batch_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
```

#### BatchTranslationResponse
```python
@dataclass
class BatchTranslationResponse:
    translations: List[TranslationResponse]
    batch_id: Optional[str] = None
    total_processing_time: float
    success_count: int
    error_count: int
    metadata: Optional[Dict[str, Any]] = None
```

## Dataset Models

### 1. GPQA Dataset Model

#### GPQAItem
```python
@dataclass
class GPQAItem:
    id: str
    question: str
    choices: List[str]
    answer: str
    explanation: str
    subject: str
    difficulty: str
    source: str
    translated_question: Optional[str] = None
    translated_choices: Optional[List[str]] = None
    translated_explanation: Optional[str] = None
    translation_metadata: Optional[Dict[str, Any]] = None
```

**Fields**:
- `id`: Unique identifier for the item
- `question`: The question text
- `choices`: List of multiple choice options
- `answer`: Correct answer
- `explanation`: Explanation for the answer
- `subject`: Subject category
- `difficulty`: Difficulty level
- `source`: Source of the question
- `translated_question`: Vietnamese translation of question
- `translated_choices`: Vietnamese translations of choices
- `translated_explanation`: Vietnamese translation of explanation
- `translation_metadata`: Metadata about translation process

#### GPQADataset
```python
@dataclass
class GPQADataset:
    items: List[GPQAItem]
    subset: str
    total_items: int
    subjects: List[str]
    difficulty_levels: List[str]
    metadata: Optional[Dict[str, Any]] = None
```

### 2. AIME Dataset Model

#### AIMEItem
```python
@dataclass
class AIMEItem:
    id: str
    problem: str
    solution: str
    year: int
    problem_number: int
    difficulty: str
    subject: str
    translated_problem: Optional[str] = None
    translated_solution: Optional[str] = None
    translation_metadata: Optional[Dict[str, Any]] = None
```

**Fields**:
- `id`: Unique identifier for the item
- `problem`: The mathematical problem
- `solution`: Solution to the problem
- `year`: Year of the AIME exam
- `problem_number`: Problem number in the exam
- `difficulty`: Difficulty level
- `subject`: Mathematical subject
- `translated_problem`: Vietnamese translation of problem
- `translated_solution`: Vietnamese translation of solution
- `translation_metadata`: Metadata about translation process

#### AIMEDataset
```python
@dataclass
class AIMEDataset:
    items: List[AIMEItem]
    year: int
    total_items: int
    subjects: List[str]
    difficulty_levels: List[str]
    metadata: Optional[Dict[str, Any]] = None
```

## Configuration Models

### 1. Model Configuration

#### ModelConfig
```python
@dataclass
class ModelConfig:
    name: str
    batch_size: int = 4
    max_length: int = 512
    device: str = "auto"
    precision: str = "fp16"
    cache_dir: Optional[str] = None
    trust_remote_code: bool = False
    use_auth_token: bool = False
```

**Fields**:
- `name`: Model name or path
- `batch_size`: Batch size for processing
- `max_length`: Maximum sequence length
- `device`: Device to use (auto, cpu, cuda)
- `precision`: Model precision (fp16, fp32)
- `cache_dir`: Cache directory for model
- `trust_remote_code`: Trust remote code flag
- `use_auth_token`: Use authentication token

### 2. Dataset Configuration

#### DatasetConfig
```python
@dataclass
class DatasetConfig:
    name: str
    subset: Optional[str] = None
    year: Optional[int] = None
    translatable_fields: List[str] = None
    output_format: str = "json"
    output_dir: str = "output"
    sample_size: Optional[int] = None
```

**Fields**:
- `name`: Dataset name
- `subset`: Dataset subset (for GPQA)
- `year`: Dataset year (for AIME)
- `translatable_fields`: Fields to translate
- `output_format`: Output format (json, csv, jsonl)
- `output_dir`: Output directory
- `sample_size`: Sample size for testing

### 3. Translation Configuration

#### TranslationConfig
```python
@dataclass
class TranslationConfig:
    source_language: str = "en"
    target_language: str = "vi"
    save_intermediate: bool = True
    quality_threshold: float = 0.8
    retry_attempts: int = 3
    timeout: int = 300
```

**Fields**:
- `source_language`: Source language code
- `target_language`: Target language code
- `save_intermediate`: Save intermediate results
- `quality_threshold`: Quality threshold for validation
- `retry_attempts`: Number of retry attempts
- `timeout`: Timeout for translation requests

## Processing Models

### 1. Translation Pipeline Model

#### TranslationPipelineConfig
```python
@dataclass
class TranslationPipelineConfig:
    model_config: ModelConfig
    dataset_config: DatasetConfig
    translation_config: TranslationConfig
    logging_config: LoggingConfig
    output_config: OutputConfig
```

#### TranslationPipelineState
```python
@dataclass
class TranslationPipelineState:
    status: str  # pending, running, completed, failed
    current_batch: int
    total_batches: int
    processed_items: int
    total_items: int
    start_time: datetime
    end_time: Optional[datetime] = None
    error_count: int = 0
    success_count: int = 0
```

### 2. Quality Validation Model

#### QualityMetrics
```python
@dataclass
class QualityMetrics:
    translation_accuracy: float
    fluency_score: float
    adequacy_score: float
    overall_score: float
    confidence_score: float
    processing_time: float
    error_rate: float
```

#### QualityReport
```python
@dataclass
class QualityReport:
    metrics: QualityMetrics
    total_translations: int
    successful_translations: int
    failed_translations: int
    average_processing_time: float
    quality_distribution: Dict[str, int]
    recommendations: List[str]
```

## Output Models

### 1. Output Format Models

#### JSONOutput
```python
@dataclass
class JSONOutput:
    data: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    quality_report: Optional[QualityReport] = None
```

#### CSVOutput
```python
@dataclass
class CSVOutput:
    file_path: str
    headers: List[str]
    rows: List[List[str]]
    metadata: Dict[str, Any]
```

#### JSONLOutput
```python
@dataclass
class JSONLOutput:
    file_path: str
    lines: List[Dict[str, Any]]
    metadata: Dict[str, Any]
```

### 2. Logging Models

#### LogEntry
```python
@dataclass
class LogEntry:
    timestamp: datetime
    level: str
    message: str
    module: str
    function: str
    line_number: int
    metadata: Optional[Dict[str, Any]] = None
```

#### TranslationLog
```python
@dataclass
class TranslationLog:
    request_id: str
    batch_id: Optional[str]
    start_time: datetime
    end_time: datetime
    processing_time: float
    success: bool
    error_message: Optional[str]
    quality_metrics: Optional[QualityMetrics]
```

## Validation Models

### 1. Data Validation

#### ValidationResult
```python
@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
```

#### FieldValidation
```python
@dataclass
class FieldValidation:
    field_name: str
    is_required: bool
    data_type: type
    validation_rules: List[str]
    is_valid: bool
    error_message: Optional[str] = None
```

### 2. Translation Validation

#### TranslationValidation
```python
@dataclass
class TranslationValidation:
    original_text: str
    translated_text: str
    is_valid: bool
    quality_score: float
    error_types: List[str]
    suggestions: List[str]
```

## Error Models

### 1. Error Types

#### TranslationError
```python
@dataclass
class TranslationError:
    error_type: str
    error_message: str
    request_id: Optional[str]
    batch_id: Optional[str]
    timestamp: datetime
    context: Optional[Dict[str, Any]] = None
```

#### SystemError
```python
@dataclass
class SystemError:
    error_type: str
    error_message: str
    component: str
    timestamp: datetime
    stack_trace: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
```

### 2. Error Handling

#### ErrorResponse
```python
@dataclass
class ErrorResponse:
    error_code: str
    error_message: str
    error_details: Optional[Dict[str, Any]] = None
    timestamp: datetime
    request_id: Optional[str] = None
```

## Metadata Models

### 1. Processing Metadata

#### ProcessingMetadata
```python
@dataclass
class ProcessingMetadata:
    start_time: datetime
    end_time: datetime
    processing_time: float
    memory_usage: float
    gpu_usage: Optional[float]
    batch_size: int
    model_name: str
    version: str
```

### 2. Translation Metadata

#### TranslationMetadata
```python
@dataclass
class TranslationMetadata:
    model_name: str
    model_version: str
    translation_time: float
    confidence_score: float
    quality_score: float
    language_pair: str
    batch_id: Optional[str]
    request_id: Optional[str]
```

## Database Schema (if applicable)

### 1. Translation History Table
```sql
CREATE TABLE translation_history (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(255) UNIQUE,
    batch_id VARCHAR(255),
    original_text TEXT,
    translated_text TEXT,
    source_language VARCHAR(10),
    target_language VARCHAR(10),
    processing_time FLOAT,
    quality_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Quality Metrics Table
```sql
CREATE TABLE quality_metrics (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(255),
    translation_accuracy FLOAT,
    fluency_score FLOAT,
    adequacy_score FLOAT,
    overall_score FLOAT,
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Data Flow Models

### 1. Input Data Flow
```
Raw Dataset → Validation → Preprocessing → Translation Request
```

### 2. Processing Data Flow
```
Translation Request → Model Processing → Quality Validation → Translation Response
```

### 3. Output Data Flow
```
Translation Response → Format Conversion → Output Generation → Storage
```

## API Models

### 1. REST API Models

#### APIResponse
```python
@dataclass
class APIResponse:
    success: bool
    data: Optional[Any] = None
    error: Optional[ErrorResponse] = None
    metadata: Optional[Dict[str, Any]] = None
```

#### TranslationAPIRequest
```python
@dataclass
class TranslationAPIRequest:
    text: str
    source_language: str = "en"
    target_language: str = "vi"
    options: Optional[Dict[str, Any]] = None
```

#### TranslationAPIResponse
```python
@dataclass
class TranslationAPIResponse:
    translated_text: str
    confidence_score: float
    processing_time: float
    quality_metrics: Optional[QualityMetrics] = None
```

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Next Review**: 2024  
**Approved By**: Data Architecture Team
