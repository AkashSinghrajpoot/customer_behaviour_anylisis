"""
Setup script to initialize the project.

Run this once after cloning to set up the environment.
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    """Run a command and report status."""
    print(f"\n{'='*60}")
    print(f"📌 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {description} - Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"Error: {str(e)}")
        return False

def main():
    """Main setup function."""
    print("\n" + "="*60)
    print("🚀 Customer Relationship Analytics Dashboard Setup")
    print("="*60)

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required!")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

    # Create virtual environment (optional)
    use_venv = input("\n📦 Create virtual environment? (y/n): ").lower() == 'y'
    if use_venv:
        if sys.platform == 'win32':
            if not run_command("python -m venv venv && venv\\Scripts\\activate", 
                             "Creating virtual environment"):
                print("\n⚠️  Virtual environment creation had issues")
        else:
            if not run_command("python3 -m venv venv && source venv/bin/activate",
                             "Creating virtual environment"):
                print("\n⚠️  Virtual environment creation had issues")

    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("\n❌ Dependency installation failed!")
        sys.exit(1)

    # Create directories if needed
    print(f"\n{'='*60}")
    print("📁 Creating necessary directories...")
    print(f"{'='*60}")
    
    directories = [
        'data/raw',
        'data/processed',
        'backend/models',
        'logs',
        'notebooks/outputs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}")

    # Summary
    print(f"\n{'='*60}")
    print("✨ Setup Complete!")
    print(f"{'='*60}")
    print("\n📝 Next steps:")
    print("1. Fill 'data/bank_marketing_part1_Data.csv' with your banking dataset")
    print("2. Run: python run.py develop")
    print("3. Open: http://localhost:5000")
    print("\n📚 Documentation:")
    print("- Quick Start: QUICKSTART.md")
    print("- Full Guide: README.md")
    print("- API Docs: docs/API_DOCUMENTATION.md")
    print("- Architecture: docs/ARCHITECTURE.md")
    print("- Interview Prep: docs/INTERVIEW_GUIDE.md")
    print("\n🧪 Run tests: python -m pytest tests/ -v")
    print("\nHappy coding! 🚀\n")

if __name__ == '__main__':
    main()
