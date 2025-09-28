#!/usr/bin/env python3
"""
Simple demonstration of Hunyuan-MT-Chimera-7B-fp8 translation functionality using local weights
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from translation.hunyuan_translator import HunyuanTranslator


def main():
    """Simple translation demo"""
    
    print("🚀 Hunyuan-MT-Chimera-7B-fp8 Translation Demo")
    print("=" * 50)
    
    # Example texts to translate
    sample_texts = [
        "What is the capital of France?",
        "Explain the concept of machine learning.",
        "Solve for x: 2x + 5 = 13",
        "The quick brown fox jumps over the lazy dog.",
        "In mathematics, a prime number is a natural number greater than 1."
    ]
    
    try:
        print("📦 Loading Hunyuan-MT-Chimera-7B-fp8 model from local weights...")
        print("Note: Using local model weights from ./weight/Hunyuan-MT-Chimera-7B-fp8")
        
        translator = HunyuanTranslator(
            model_name="./weight/Hunyuan-MT-Chimera-7B-fp8",
            batch_size=2,
            max_length=256
        )
        
        print("\n🔄 Translating sample texts...")
        print("-" * 40)
        
        for i, text in enumerate(sample_texts, 1):
            print(f"\n[{i}] Original: {text}")
            
            try:
                # Translate single text
                translation = translator.translate_single(text)
                print(f"    Vietnamese: {translation}")
                
            except Exception as e:
                print(f"    Error: {e}")
        
        print("\n🔄 Batch translation demo...")
        print("-" * 40)
        
        # Batch translation
        batch_translations = translator.translate_batch(
            sample_texts[:3],  # First 3 texts
            show_progress=True
        )
        
        for orig, trans in zip(sample_texts[:3], batch_translations):
            print(f"Original: {orig}")
            print(f"Vietnamese: {trans}")
            print()
        
        print("✅ Demo completed successfully!")
        
        # Show model info
        print("\n📋 Model Information:")
        model_info = translator.get_model_info()
        for key, value in model_info.items():
            print(f"   • {key}: {value}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nNote: Make sure you have:")
        print("1. Installed all requirements: pip install -r requirements.txt")
        print("2. Internet connection for model download")
        print("3. Sufficient GPU memory (or CPU will be used)")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())