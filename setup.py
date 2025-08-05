#!/usr/bin/env python
"""
Setup script for NexusStore AI Chat Enhancement
"""
import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def setup_environment():
    """Set up the development environment"""
    print("🚀 Setting up NexusStore AI Chat Enhancement...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing Python packages"):
        return False
    
    # Check if .env exists, if not create from example
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from .env.example")
            print("📝 Please edit .env file and add your OpenAI API key")
        else:
            print("⚠️  .env.example not found, creating basic .env")
            with open('.env', 'w') as f:
                f.write("DEBUG=True\n")
                f.write("SECRET_KEY=your-secret-key-here\n")
                f.write("OPENAI_API_KEY=your-openai-api-key-here\n")
    else:
        print("✅ .env file already exists")
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating database migrations"):
        return False
    
    if not run_command("python manage.py migrate", "Applying database migrations"):
        return False
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("⚠️  Static files collection failed, but continuing...")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Get API key from: https://platform.openai.com/api-keys")
    print("3. Run: python manage.py runserver")
    print("4. Visit: http://127.0.0.1:8000")
    print("\n💡 The chatbot will work in basic mode without API key")
    print("   but AI features require a valid OpenAI API key")
    
    return True

if __name__ == "__main__":
    success = setup_environment()
    if not success:
        print("\n❌ Setup failed! Please check the errors above.")
        sys.exit(1)
    else:
        print("\n✅ Ready to run your AI-powered NexusStore!")
