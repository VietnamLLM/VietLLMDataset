#!/usr/bin/env python3
"""
Test script to verify local Hunyuan-MT-Chimera-7B-fp8 model loading
"""

import sys
from pathlib import Path
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_local_model():
    """Test if local model can be loaded and used"""
    
    print("🧪 Testing Local Hunyuan-MT-Chimera-7B-fp8 Model")
    print("=" * 50)
    
    # Check if model directory exists
    model_path = "./weight/Hunyuan-MT-Chimera-7B-fp8"
    if not os.path.exists(model_path):
        print(f"❌ Model directory not found: {model_path}")
        print("Please ensure the Hunyuan-MT-Chimera-7B-fp8 weights are placed in the weight directory")
        return False
    
    # Check for required files
    required_files = [
        "config.json",
        "tokenizer.json", 
        "tokenizer_config.json",
        "model.safetensors.index.json"
    ]
    
    missing_files = []
    for file in required_files:
        file_path = os.path.join(model_path, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required model files: {missing_files}")
        return False
    
    print("✅ Model directory and required files found")
    
    try:
        # Import translator
        from translation.hunyuan_translator import HunyuanTranslator
        
        print("📦 Loading Hunyuan-MT-Chimera-7B-fp8 translator...")
        translator = HunyuanTranslator(
            model_name=model_path,
            batch_size=1,
            max_length=128
        )
        
        print("✅ Model loaded successfully!")
        
        # Test translation
        test_text = "Hello, how are you today?"
        print(f"\n🔄 Testing translation...")
        print(f"Input: {test_text}")
        
        result = translator.translate_single(test_text)
        print(f"Output: {result}")
        
        if result and result.strip():
            print("✅ Translation test successful!")
            return True
        else:
            print("❌ Translation returned empty result")
            return False
            
    except Exception as e:
        print(f"❌ Error during model loading or translation: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    success = test_local_model()
    
    if success:
        print("\n🎉 All tests passed! The local model is working correctly.")
        print("You can now use the translation scripts:")
        print("  python examples/simple_translation_demo.py")
        print("  python run_translation.py demo")
    else:
        print("\n❌ Tests failed. Please check the model setup.")
        
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())