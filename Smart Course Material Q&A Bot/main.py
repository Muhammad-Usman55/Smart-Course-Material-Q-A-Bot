"""
Smart Course Material Q&A Bot - Main Launcher
Simple launcher for the Streamlit app or CLI demo
"""

import os
import sys
import subprocess
from pathlib import Path

def launch_streamlit():
    """Launch the Streamlit web app"""
    print("🚀 Launching Smart Course Q&A Bot...")
    print("📱 The web interface will open in your browser")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Thanks for using the Smart Course Q&A Bot!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching Streamlit: {e}")
        print("💡 Make sure Streamlit is installed: pip install streamlit")
    except FileNotFoundError:
        print("❌ Could not find Python or Streamlit")
        print("💡 Make sure you're in the right directory and have Python installed")

def show_help():
    """Show help information"""
    print("""
📚 Smart Course Material Q&A Bot
=================================

This is a simple NLP project that allows you to:
• Upload course materials (PDF, TXT, DOCX)
• Choose different AI personalities (Friendly Tutor, Strict Professor, etc.)
• Ask questions about your materials and get intelligent answers
• See source references for each answer

Usage Options:
1. Web Interface (Recommended):
   python main.py
   
2. Direct Streamlit:
   streamlit run app.py

Required Files:
• app.py - Streamlit web interface
• bot_core.py - Core Q&A functionality  
• personalities.py - AI personality definitions
• .env - Contains your Google API key

Setup:
1. Install requirements: pip install -r requirements.txt
2. Add your Google API key to .env file
3. Run: python main.py

🌟 Perfect for viva presentations and demos!
""")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
        return
    
    print("📚 Smart Course Material Q&A Bot")
    print("=================================")
    
    # Check if required files exist
    required_files = ['app.py', 'bot_core.py', 'personalities.py', '.env']
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("💡 Make sure all files are in the current directory")
        return
    
    # Check for API key
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY not found in .env file")
        print("💡 Add your Google API key to the .env file or enter it in the web interface")
        print()
    
    launch_streamlit()
        
main()
       