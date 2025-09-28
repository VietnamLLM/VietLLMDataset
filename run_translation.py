#!/usr/bin/env python3
"""
Main script for running dataset translations
Supports both GPQA and AIME datasets with command-line arguments
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from translation.hunyuan_translator import HunyuanTranslator
from datasets.gpqa_loader import GPQALoader
from datasets.aime_loader import AIMELoader
from utils.translation_utils import TranslationPipeline
from utils.logging_config import setup_logging


def main():
    """Main function with CLI arguments"""
    
    parser = argparse.ArgumentParser(
        description="Translate datasets from English to Vietnamese using local Hunyuan-MT-Chimera-7B-fp8"
    )
    
    parser.add_argument(
        "dataset",
        choices=["gpqa", "aime", "demo"],
        help="Dataset to translate using Hunyuan-MT-Chimera-7B-fp8"
    )
    
    parser.add_argument(
        "--model-name",
        default="./weight/Hunyuan-MT-Chimera-7B-fp8",
        help="Hunyuan-MT-Chimera-7B-fp8 local model path"
    )
    
    parser.add_argument(
        "--batch-size",
        type=int,
        default=4,
        help="Batch size for translation"
    )
    
    parser.add_argument(
        "--max-length",
        type=int,
        default=512,
        help="Maximum sequence length"
    )
    
    parser.add_argument(
        "--sample-size",
        type=int,
        default=None,
        help="Number of samples to translate (None for all)"
    )
    
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Output directory"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level"
    )
    
    parser.add_argument(
        "--device",
        choices=["auto", "cuda", "cpu"],
        default="auto",
        help="Device to use for translation"
    )
    
    # GPQA specific arguments
    parser.add_argument(
        "--gpqa-subset",
        choices=["gpqa_main", "gpqa_extended", "gpqa_diamond"],
        default="gpqa_main",
        help="GPQA subset to use"
    )
    
    # AIME specific arguments
    parser.add_argument(
        "--aime-year",
        type=int,
        default=2025,
        help="AIME year"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(
        level=args.log_level,
        log_file=f"logs/{args.dataset}_translation.log",
        console_output=True
    )
    
    print(f"🚀 Starting {args.dataset.upper()} Dataset Translation")
    print("=" * 60)
    print(f"Model: {args.model_name}")
    print(f"Device: {args.device}")
    print(f"Batch Size: {args.batch_size}")
    print(f"Sample Size: {args.sample_size or 'All'}")
    print("-" * 60)
    
    try:
        # Initialize translator
        print("📦 Initializing Hunyuan-MT-Chimera-7B-fp8 translator from local weights...")
        translator = HunyuanTranslator(
            model_name=args.model_name,
            device=args.device if args.device != "auto" else None,
            batch_size=args.batch_size,
            max_length=args.max_length
        )
        
        # Dataset-specific initialization
        if args.dataset == "gpqa":
            print(f"📚 Loading GPQA dataset (subset: {args.gpqa_subset})...")
            loader = GPQALoader(subset=args.gpqa_subset)
            dataset_name = f"gpqa_{args.gpqa_subset}"
            
        elif args.dataset == "aime":
            print(f"📚 Loading AIME dataset (year: {args.aime_year})...")
            loader = AIMELoader(year=args.aime_year)
            dataset_name = f"aime_{args.aime_year}"
            
        elif args.dataset == "demo":
            print("🎯 Running simple translation demo...")
            # Simple demo
            sample_texts = [
                "What is the capital of France?",
                "Explain quantum mechanics in simple terms.",
                "Solve the equation: x² + 5x + 6 = 0"
            ]
            
            print("Translating sample texts...")
            for i, text in enumerate(sample_texts, 1):
                translation = translator.translate_single(text)
                print(f"[{i}] EN: {text}")
                print(f"    VI: {translation}")
                print()
            
            print("✅ Demo completed!")
            return 0
        
        # Setup pipeline
        print("🔧 Setting up translation pipeline...")
        pipeline = TranslationPipeline(
            translator=translator,
            dataset_loader=loader,
            output_dir=f"{args.output_dir}/{args.dataset}",
            save_intermediate=True
        )
        
        # Run translation
        print("🔄 Running translation pipeline...")
        print("This may take a while depending on your hardware and dataset size...")
        
        results = pipeline.run_full_pipeline(
            dataset_name=dataset_name,
            split="train",
            sample_size=args.sample_size
        )
        
        # Print results
        print("\n✅ Translation completed!")
        print("=" * 60)
        stats = results["statistics"]
        print(f"📊 Results Summary:")
        print(f"   • Dataset: {args.dataset.upper()}")
        print(f"   • Total items: {stats['total_items']}")
        print(f"   • Successful translations: {stats['successful_translations']}")
        print(f"   • Failed translations: {stats['failed_translations']}")
        print(f"   • Duration: {stats['end_time'] - stats['start_time']}")
        print(f"   • Output: {results['output_path']}")
        
        # Show sample if available
        dataset = results["translated_dataset"]
        sample_field = "questions" if "questions" in dataset else "problems"
        
        if sample_field in dataset and len(dataset[sample_field]) > 0:
            print(f"\n📝 Sample Translation:")
            print(f"Original: {dataset[sample_field][0][:150]}...")
            print(f"Vietnamese: {dataset[f'{sample_field}_vi'][0][:150]}...")
        
        print(f"\n🎉 All done! Check the output directory: {args.output_dir}/{args.dataset}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Translation interrupted by user")
        return 1
        
    except Exception as e:
        print(f"❌ Error during translation: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())