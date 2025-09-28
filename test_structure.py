#!/usr/bin/env python3
"""
Test script to validate project structure without requiring heavy dependencies
"""

import sys
import os
from pathlib import Path
import importlib.util

def test_file_structure():
    """Test that all expected files exist"""
    base_path = Path(__file__).parent
    
    expected_files = [
        "README.md",
        "requirements.txt",
        "config.yaml",  
        "setup.py",
        "run_translation.py",
        "USAGE.md",
        "src/__init__.py",
        "src/translation/__init__.py",
        "src/translation/hunyuan_translator.py",
        "src/datasets/__init__.py",
        "src/datasets/gpqa_loader.py",
        "src/datasets/aime_loader.py", 
        "src/utils/__init__.py",
        "src/utils/logging_config.py",
        "src/utils/translation_utils.py",
        "examples/__init__.py",
        "examples/simple_translation_demo.py",
        "examples/translate_gpqa.py",
        "examples/translate_aime.py"
    ]
    
    print("🔍 Testing file structure...")
    missing = []
    
    for file_path in expected_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing.append(file_path)
    
    if missing:
        print(f"\n❌ Missing {len(missing)} files: {missing}")
        return False
    else:
        print(f"\n✅ All {len(expected_files)} expected files found!")
        return True

def test_python_syntax():
    """Test that all Python files have valid syntax"""
    base_path = Path(__file__).parent
    python_files = list(base_path.rglob("*.py"))
    
    print(f"\n🐍 Testing Python syntax for {len(python_files)} files...")
    
    errors = []
    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Test syntax
            compile(content, str(py_file), 'exec')
            print(f"✅ {py_file.relative_to(base_path)}")
            
        except SyntaxError as e:
            print(f"❌ {py_file.relative_to(base_path)}: {e}")
            errors.append((py_file, e))
        except Exception as e:
            print(f"⚠️  {py_file.relative_to(base_path)}: {e}")
    
    if errors:
        print(f"\n❌ Syntax errors in {len(errors)} files")
        return False
    else:
        print(f"\n✅ All Python files have valid syntax!")
        return True

def test_import_structure():
    """Test import structure without actually importing heavy dependencies"""
    print(f"\n📦 Testing import structure...")
    
    # Test basic structure
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    
    try:
        # Test that modules can be found (without actually importing)
        import importlib.util
        
        modules_to_test = [
            "translation.hunyuan_translator",
            "datasets.gpqa_loader", 
            "datasets.aime_loader",
            "utils.logging_config",
            "utils.translation_utils"
        ]
        
        for module_name in modules_to_test:
            spec = importlib.util.find_spec(module_name)
            if spec is not None:
                print(f"✅ {module_name}")
            else:
                print(f"❌ {module_name}")
                return False
        
        print(f"\n✅ All modules can be found!")
        
        # Test that imports would work (but don't actually import heavy deps)
        print(f"\n🔧 Testing imports (syntax only)...")
        lightweight_imports = [
            "utils.logging_config",
        ]
        
        for module_name in lightweight_imports:
            try:
                module = importlib.import_module(module_name)
                print(f"✅ Imported {module_name}")
            except ImportError as e:
                if "torch" in str(e) or "transformers" in str(e) or "datasets" in str(e):
                    print(f"⚠️  {module_name}: Heavy dependencies not installed (expected)")
                else:
                    print(f"❌ {module_name}: {e}")
                    return False
        
        return True
        
    except Exception as e:
        print(f"❌ Import structure test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 VietLLMDataset Project Structure Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Python Syntax", test_python_syntax),
        ("Import Structure", test_import_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Project structure is ready.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run simple demo: python examples/simple_translation_demo.py")
        print("3. Test with sample data: python run_translation.py demo")
        return 0
    else:
        print(f"\n⚠️  {len(results) - passed} tests failed. Please fix issues before proceeding.")
        return 1

if __name__ == "__main__":
    exit(main())