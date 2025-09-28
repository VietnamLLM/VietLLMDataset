#!/usr/bin/env python3
"""
Example script for translating AIME dataset from English to Vietnamese
using local Hunyuan-MT-Chimera-7B-fp8 model
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from translation.hunyuan_translator import HunyuanTranslator
from datasets.aime_loader import AIMELoader
from utils.translation_utils import TranslationPipeline
from utils.logging_config import setup_logging


def main():
    """Main translation function"""
    
    # Setup logging
    setup_logging(
        level="INFO",
        log_file="logs/aime_translation.log",
        console_output=True
    )
    
    print("🚀 Starting AIME Dataset Translation")
    print("=" * 50)
    
    try:
        # Initialize components
        print("📦 Initializing Hunyuan-MT-Chimera-7B-fp8 translator from local weights...")
        translator = HunyuanTranslator(
            model_name="./weight/Hunyuan-MT-Chimera-7B-fp8",  # Local model path
            batch_size=2,  # Small batch size for demo
            max_length=1024  # Longer for math problems
        )
        
        print("📚 Initializing AIME dataset loader...")
        aime_loader = AIMELoader(year=2025)
        
        print("🔧 Setting up translation pipeline...")
        pipeline = TranslationPipeline(
            translator=translator,
            dataset_loader=aime_loader,
            output_dir="output/aime",
            save_intermediate=True
        )
        
        # Run translation pipeline
        print("🔄 Running translation pipeline...")
        print("This may take a while depending on your hardware...")
        
        results = pipeline.run_full_pipeline(
            dataset_name="aime_2025",
            split="train",
            sample_size=3,  # Start with 3 samples for demo
            fields_to_translate=["problems", "solutions"]
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
        if len(dataset["problems"]) > 0:
            print(f"\n📝 Sample Translation:")
            print(f"Original Problem: {dataset['problems'][0][:200]}...")
            print(f"Vietnamese Problem: {dataset['problems_vi'][0][:200]}...")
        
    except Exception as e:
        print(f"❌ Error during translation: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())