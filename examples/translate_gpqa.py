#!/usr/bin/env python3
"""
Example script for translating GPQA dataset from English to Vietnamese
using Hunyuan-MT model
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from translation.hunyuan_translator import HunyuanTranslator
from datasets.gpqa_loader import GPQALoader
from utils.translation_utils import TranslationPipeline
from utils.logging_config import setup_logging


def main():
    """Main translation function"""
    
    # Setup logging
    setup_logging(
        level="INFO",
        log_file="logs/gpqa_translation.log",
        console_output=True
    )
    
    print("🚀 Starting GPQA Dataset Translation")
    print("=" * 50)
    
    try:
        # Initialize components
        print("📦 Initializing Hunyuan-MT translator...")
        translator = HunyuanTranslator(
            model_name="Tencent-Hunyuan/Hunyuan-MT",  # You may need to adjust this
            batch_size=2,  # Small batch size for demo
            max_length=512
        )
        
        print("📚 Initializing GPQA dataset loader...")
        gpqa_loader = GPQALoader(subset="gpqa_main")
        
        print("🔧 Setting up translation pipeline...")
        pipeline = TranslationPipeline(
            translator=translator,
            dataset_loader=gpqa_loader,
            output_dir="output/gpqa",
            save_intermediate=True
        )
        
        # Run translation pipeline
        print("🔄 Running translation pipeline...")
        print("This may take a while depending on your hardware...")
        
        results = pipeline.run_full_pipeline(
            dataset_name="gpqa_main",
            split="train",
            sample_size=5,  # Start with 5 samples for demo
            fields_to_translate=["questions", "choices", "explanations"]
        )
        
        # Print results summary
        print("\n✅ Translation completed!")
        print("=" * 50)
        print(f"📊 Statistics:")
        stats = results["statistics"]
        print(f"   • Total items: {stats['total_items']}")
        print(f"   • Successful translations: {stats['successful_translations']}")
        print(f"   • Failed translations: {stats['failed_translations']}")
        print(f"   • Duration: {stats['end_time'] - stats['start_time']}")
        print(f"   • Output saved to: {results['output_path']}")
        
        # Show a sample
        dataset = results["translated_dataset"]
        if len(dataset["questions"]) > 0:
            print(f"\n📝 Sample Translation:")
            print(f"Original Question: {dataset['questions'][0][:200]}...")
            print(f"Vietnamese Question: {dataset['questions_vi'][0][:200]}...")
        
    except Exception as e:
        print(f"❌ Error during translation: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())