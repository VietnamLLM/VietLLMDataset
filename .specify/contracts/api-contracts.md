# VietLLMDataset - API Contracts

## Overview

This document defines the API contracts for the VietLLMDataset system, including REST API endpoints, data schemas, and integration specifications.

## Base API Information

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication
- **Type**: API Key (for future use)
- **Header**: `X-API-Key: <api_key>`
- **Note**: Currently no authentication required for local usage

### Content Types
- **Request**: `application/json`
- **Response**: `application/json`

### Error Handling
All API responses follow a consistent error format:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {
      "field": "Additional error details"
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Core API Endpoints

### 1. Health Check

#### GET /health
Check system health and status.

**Response**:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "1.0.0",
    "model_loaded": true,
    "gpu_available": true,
    "memory_usage": {
      "total": 16384,
      "used": 8192,
      "free": 8192
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

**Status Codes**:
- `200`: System healthy
- `503`: System unhealthy

### 2. Translation Endpoints

#### POST /translate/single
Translate a single text.

**Request Body**:
```json
{
  "text": "Hello, how are you?",
  "source_language": "en",
  "target_language": "vi",
  "max_length": 512,
  "options": {
    "batch_size": 1,
    "quality_threshold": 0.8
  }
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "original_text": "Hello, how are you?",
    "translated_text": "Xin chào, bạn có khỏe không?",
    "source_language": "en",
    "target_language": "vi",
    "confidence_score": 0.95,
    "processing_time": 1.2,
    "quality_metrics": {
      "translation_accuracy": 0.95,
      "fluency_score": 0.92,
      "adequacy_score": 0.98,
      "overall_score": 0.95
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

**Status Codes**:
- `200`: Translation successful
- `400`: Invalid request
- `500`: Translation failed

#### POST /translate/batch
Translate multiple texts in batch.

**Request Body**:
```json
{
  "texts": [
    "What is machine learning?",
    "How does neural networks work?",
    "Explain deep learning concepts."
  ],
  "source_language": "en",
  "target_language": "vi",
  "batch_size": 4,
  "max_length": 512,
  "options": {
    "quality_threshold": 0.8,
    "save_intermediate": true
  }
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "translations": [
      {
        "original_text": "What is machine learning?",
        "translated_text": "Học máy là gì?",
        "confidence_score": 0.96,
        "processing_time": 1.1,
        "quality_metrics": {
          "translation_accuracy": 0.96,
          "fluency_score": 0.94,
          "adequacy_score": 0.97,
          "overall_score": 0.96
        }
      },
      {
        "original_text": "How does neural networks work?",
        "translated_text": "Mạng nơ-ron hoạt động như thế nào?",
        "confidence_score": 0.93,
        "processing_time": 1.3,
        "quality_metrics": {
          "translation_accuracy": 0.93,
          "fluency_score": 0.91,
          "adequacy_score": 0.95,
          "overall_score": 0.93
        }
      },
      {
        "original_text": "Explain deep learning concepts.",
        "translated_text": "Giải thích các khái niệm học sâu.",
        "confidence_score": 0.94,
        "processing_time": 1.0,
        "quality_metrics": {
          "translation_accuracy": 0.94,
          "fluency_score": 0.93,
          "adequacy_score": 0.96,
          "overall_score": 0.94
        }
      }
    ],
    "batch_metrics": {
      "total_processing_time": 3.4,
      "average_processing_time": 1.13,
      "success_count": 3,
      "error_count": 0,
      "quality_distribution": {
        "excellent": 1,
        "good": 2,
        "fair": 0,
        "poor": 0
      }
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

**Status Codes**:
- `200`: Batch translation successful
- `400`: Invalid request
- `500`: Translation failed

### 3. Dataset Endpoints

#### GET /datasets/gpqa
Get GPQA dataset information.

**Query Parameters**:
- `subset`: Dataset subset (main, extended, diamond)
- `limit`: Maximum number of items to return
- `offset`: Number of items to skip

**Response**:
```json
{
  "success": true,
  "data": {
    "dataset": {
      "name": "GPQA",
      "subset": "main",
      "total_items": 1000,
      "subjects": ["Physics", "Chemistry", "Biology"],
      "difficulty_levels": ["Easy", "Medium", "Hard"]
    },
    "items": [
      {
        "id": "gpqa_001",
        "question": "What is the speed of light?",
        "choices": ["3×10⁸ m/s", "3×10⁶ m/s", "3×10¹⁰ m/s", "3×10⁴ m/s"],
        "answer": "3×10⁸ m/s",
        "explanation": "The speed of light in vacuum is approximately 3×10⁸ meters per second.",
        "subject": "Physics",
        "difficulty": "Medium"
      }
    ],
    "pagination": {
      "limit": 10,
      "offset": 0,
      "total": 1000,
      "has_next": true,
      "has_previous": false
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### GET /datasets/aime
Get AIME dataset information.

**Query Parameters**:
- `year`: Dataset year (default: 2025)
- `limit`: Maximum number of items to return
- `offset`: Number of items to skip

**Response**:
```json
{
  "success": true,
  "data": {
    "dataset": {
      "name": "AIME",
      "year": 2025,
      "total_items": 500,
      "subjects": ["Algebra", "Geometry", "Number Theory"],
      "difficulty_levels": ["Level 1", "Level 2", "Level 3"]
    },
    "items": [
      {
        "id": "aime_2025_001",
        "problem": "Find the value of x if 2x + 3 = 7.",
        "solution": "2x + 3 = 7\n2x = 4\nx = 2",
        "year": 2025,
        "problem_number": 1,
        "difficulty": "Level 1",
        "subject": "Algebra"
      }
    ],
    "pagination": {
      "limit": 10,
      "offset": 0,
      "total": 500,
      "has_next": true,
      "has_previous": false
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 4. Translation Pipeline Endpoints

#### POST /pipeline/translate-dataset
Translate an entire dataset.

**Request Body**:
```json
{
  "dataset_name": "gpqa",
  "dataset_config": {
    "subset": "main",
    "translatable_fields": ["question", "choices", "explanation"],
    "sample_size": 100
  },
  "translation_config": {
    "source_language": "en",
    "target_language": "vi",
    "batch_size": 4,
    "max_length": 512,
    "quality_threshold": 0.8
  },
  "output_config": {
    "format": "json",
    "output_dir": "output",
    "save_intermediate": true
  }
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "pipeline_id": "pipeline_12345",
    "status": "running",
    "progress": {
      "total_items": 100,
      "processed_items": 25,
      "percentage": 25.0,
      "estimated_completion": "2024-01-01T00:05:00Z"
    },
    "output_path": "output/gpqa_translated.json",
    "quality_metrics": {
      "average_quality": 0.94,
      "translation_accuracy": 0.95,
      "fluency_score": 0.92,
      "adequacy_score": 0.96
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### GET /pipeline/status/{pipeline_id}
Get pipeline status.

**Response**:
```json
{
  "success": true,
  "data": {
    "pipeline_id": "pipeline_12345",
    "status": "completed",
    "progress": {
      "total_items": 100,
      "processed_items": 100,
      "percentage": 100.0,
      "completed_at": "2024-01-01T00:05:00Z"
    },
    "results": {
      "success_count": 98,
      "error_count": 2,
      "total_processing_time": 300.5,
      "average_processing_time": 3.07
    },
    "output_path": "output/gpqa_translated.json",
    "quality_report": {
      "overall_quality": 0.94,
      "quality_distribution": {
        "excellent": 45,
        "good": 40,
        "fair": 13,
        "poor": 2
      }
    }
  },
  "timestamp": "2024-01-01T00:05:00Z"
}
```

### 5. Quality Assessment Endpoints

#### POST /quality/assess
Assess translation quality.

**Request Body**:
```json
{
  "original_text": "What is machine learning?",
  "translated_text": "Học máy là gì?",
  "source_language": "en",
  "target_language": "vi"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "quality_metrics": {
      "translation_accuracy": 0.96,
      "fluency_score": 0.94,
      "adequacy_score": 0.97,
      "overall_score": 0.96
    },
    "assessment": {
      "grade": "excellent",
      "confidence": 0.95,
      "recommendations": []
    },
    "details": {
      "preserved_meaning": true,
      "grammatical_correctness": true,
      "cultural_appropriateness": true,
      "technical_accuracy": true
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 6. Configuration Endpoints

#### GET /config
Get current configuration.

**Response**:
```json
{
  "success": true,
  "data": {
    "model": {
      "name": "./weight/Hunyuan-MT-Chimera-7B-fp8",
      "batch_size": 4,
      "max_length": 512,
      "device": "cuda",
      "precision": "fp16"
    },
    "datasets": {
      "gpqa": {
        "subset": "main",
        "translatable_fields": ["question", "choices", "explanation"]
      },
      "aime": {
        "year": 2025,
        "translatable_fields": ["problem", "solution"]
      }
    },
    "translation": {
      "source_language": "en",
      "target_language": "vi",
      "quality_threshold": 0.8,
      "retry_attempts": 3
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### PUT /config
Update configuration.

**Request Body**:
```json
{
  "model": {
    "batch_size": 8,
    "max_length": 1024
  },
  "translation": {
    "quality_threshold": 0.9
  }
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "message": "Configuration updated successfully",
    "updated_fields": ["model.batch_size", "model.max_length", "translation.quality_threshold"]
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Error Codes

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Unprocessable Entity
- `429`: Too Many Requests
- `500`: Internal Server Error
- `503`: Service Unavailable

### Application Error Codes
- `INVALID_REQUEST`: Invalid request format
- `MISSING_FIELD`: Required field missing
- `INVALID_LANGUAGE`: Unsupported language code
- `MODEL_NOT_LOADED`: Translation model not loaded
- `TRANSLATION_FAILED`: Translation process failed
- `QUALITY_TOO_LOW`: Translation quality below threshold
- `BATCH_SIZE_EXCEEDED`: Batch size too large
- `MEMORY_INSUFFICIENT`: Insufficient memory
- `DATASET_NOT_FOUND`: Dataset not found
- `PIPELINE_NOT_FOUND`: Pipeline not found

## Rate Limiting

### Limits
- **Single Translation**: 100 requests per minute
- **Batch Translation**: 10 requests per minute
- **Dataset Translation**: 5 requests per minute
- **Quality Assessment**: 50 requests per minute

### Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## Webhooks (Future)

### Pipeline Completion Webhook
```json
{
  "event": "pipeline.completed",
  "pipeline_id": "pipeline_12345",
  "status": "completed",
  "results": {
    "success_count": 98,
    "error_count": 2,
    "output_path": "output/gpqa_translated.json"
  },
  "timestamp": "2024-01-01T00:05:00Z"
}
```

### Error Webhook
```json
{
  "event": "pipeline.error",
  "pipeline_id": "pipeline_12345",
  "error": {
    "code": "TRANSLATION_FAILED",
    "message": "Translation failed for item 25",
    "details": {
      "item_id": "gpqa_025",
      "error_type": "model_error"
    }
  },
  "timestamp": "2024-01-01T00:03:00Z"
}
```

## SDK Examples

### Python SDK
```python
from vietllm_dataset import VietLLMDatasetClient

client = VietLLMDatasetClient(base_url="http://localhost:8000/api/v1")

# Single translation
result = client.translate_single(
    text="Hello, how are you?",
    source_language="en",
    target_language="vi"
)

# Batch translation
results = client.translate_batch(
    texts=["What is AI?", "How does ML work?"],
    source_language="en",
    target_language="vi"
)

# Dataset translation
pipeline = client.translate_dataset(
    dataset_name="gpqa",
    dataset_config={"subset": "main", "sample_size": 100},
    translation_config={"batch_size": 4}
)
```

### JavaScript SDK
```javascript
import { VietLLMDatasetClient } from '@vietllm/dataset-client';

const client = new VietLLMDatasetClient({
  baseUrl: 'http://localhost:8000/api/v1'
});

// Single translation
const result = await client.translateSingle({
  text: 'Hello, how are you?',
  sourceLanguage: 'en',
  targetLanguage: 'vi'
});

// Batch translation
const results = await client.translateBatch({
  texts: ['What is AI?', 'How does ML work?'],
  sourceLanguage: 'en',
  targetLanguage: 'vi'
});
```

## Testing

### Test Data
```json
{
  "test_cases": [
    {
      "name": "simple_translation",
      "input": {
        "text": "Hello, world!",
        "source_language": "en",
        "target_language": "vi"
      },
      "expected_output": {
        "translated_text": "Xin chào, thế giới!",
        "confidence_score": 0.95
      }
    },
    {
      "name": "academic_content",
      "input": {
        "text": "What is the fundamental theorem of calculus?",
        "source_language": "en",
        "target_language": "vi"
      },
      "expected_output": {
        "translated_text": "Định lý cơ bản của giải tích là gì?",
        "confidence_score": 0.92
      }
    }
  ]
}
```

### Performance Benchmarks
- **Single Translation**: < 2 seconds
- **Batch Translation (10 items)**: < 20 seconds
- **Dataset Translation (100 items)**: < 5 minutes
- **Memory Usage**: < 8GB VRAM
- **CPU Usage**: < 80% for CPU processing

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Next Review**: 2024  
**Approved By**: API Design Team
