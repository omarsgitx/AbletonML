#!/usr/bin/env python3
"""
AbletonML Environment Verification Script
Run this script to check if your testing environment is properly configured.
"""

import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.9+")
        return False

def check_node_version():
    """Check if Node.js is installed and version is compatible"""
    print("\n📦 Checking Node.js version...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version} - Compatible")
            return True
        else:
            print("❌ Node.js not found or error running node --version")
            return False
    except FileNotFoundError:
        print("❌ Node.js not installed")
        return False

def check_python_dependencies():
    """Check if required Python packages are installed"""
    print("\n📚 Checking Python dependencies...")
    required_packages = [
        'flask',
        'flask_socketio', 
        'flask_cors',
        'eventlet',
        'socketio'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
            print(f"✅ {package} - Installed")
        except ImportError:
            print(f"❌ {package} - Not installed")
            all_installed = False
    
    return all_installed

def check_abletonml_modules():
    """Check if AbletonML core modules are available"""
    print("\n🎵 Checking AbletonML modules...")
    
    modules = [
        'core.simple_nlp',
        'core.action_mapper', 
        'core.max_controller'
    ]
    
    all_available = True
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module} - Available")
        except ImportError as e:
            print(f"❌ {module} - Not available: {e}")
            all_available = False
    
    return all_available

def test_nlp_parsing():
    """Test basic NLP parsing functionality"""
    print("\n🧠 Testing NLP parsing...")
    try:
        from core.simple_nlp import SimpleNLPModule
        nlp = SimpleNLPModule()
        
        test_commands = [
            "set tempo to 120",
            "create midi track", 
            "add reverb to track 2"
        ]
        
        for command in test_commands:
            result = nlp.parse_command(command)
            if result["intent"]:
                print(f"✅ '{command}' -> {result['intent']}")
            else:
                print(f"❌ '{command}' -> No intent found")
                return False
        
        return True
    except Exception as e:
        print(f"❌ NLP test failed: {e}")
        return False

def main():
    """Run all environment checks"""
    print("🎵 AbletonML Environment Verification")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Node.js Version", check_node_version),
        ("Python Dependencies", check_python_dependencies),
        ("AbletonML Modules", check_abletonml_modules),
        ("NLP Parsing", test_nlp_parsing)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 40)
    print("📊 SUMMARY")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Environment is ready for testing!")
        print("\nNext steps:")
        print("1. Open Ableton Live")
        print("2. Load the Max for Live device")
        print("3. Run 'npm start' to launch AbletonML")
    else:
        print("⚠️  Some issues found. Please fix them before testing.")
        print("\nCommon fixes:")
        print("- Run 'pip install -r requirements.txt'")
        print("- Install Node.js from https://nodejs.org/")
        print("- Make sure you're in the correct directory")

if __name__ == "__main__":
    main()
