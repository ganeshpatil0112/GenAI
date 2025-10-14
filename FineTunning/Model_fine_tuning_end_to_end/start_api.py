"""
Quick Start Script for API Server
Starts the API server with optimal settings
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("✓ All API dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\nInstalling required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_api.txt"])
        return True

def check_models():
    """Check if models are available"""
    models_dir = "models"
    if not os.path.exists(models_dir):
        print(f"❌ Models directory not found: {models_dir}")
        print("   Please train models first using: python main.py --train all")
        return False
    
    model_paths = [
        "models/hr_full_finetuned",
        "models/sales_peft_finetuned",
        "models/healthcare_lora_finetuned",
        "models/marketing_qlora_finetuned"
    ]
    
    found = 0
    for path in model_paths:
        if os.path.exists(path):
            found += 1
            print(f"✓ Found: {path}")
    
    if found == 0:
        print("❌ No trained models found")
        print("   Train models first: python main.py --train all")
        return False
    
    print(f"\n✓ Found {found} trained model(s)")
    return True

def start_server():
    """Start the API server"""
    print("\n" + "="*60)
    print("Starting LLM API Server")
    print("="*60)
    print("\nAPI will be available at:")
    print("  - http://localhost:8000")
    print("  - http://localhost:8000/docs (Interactive API docs)")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    try:
        import uvicorn
        uvicorn.run(
            "api_server:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("LLM API Server - Quick Start")
    print("="*60 + "\n")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check models
    if not check_models():
        print("\n⚠️  Warning: Some models are missing")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Start server
    start_server()

