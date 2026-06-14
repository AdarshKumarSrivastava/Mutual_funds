"""
Master Execution Script for Bluestock Mutual Fund Capstone.

This script sequentially runs:
1. Data ETL Pipeline (Extraction, Transformation, Load)
2. Database initialization and loading
3. Jupyter Notebook generation
"""

import subprocess
from pathlib import Path
import sys

def run_script(script_path: Path):
    """Run a given Python script and wait for it to complete."""
    print(f"\n[{'='*40}]")
    print(f"Running {script_path.name}...")
    print(f"[{'='*40}]\n")
    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
        print(f"✅ {script_path.name} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_path.name}: {e}")
        sys.exit(1)

def main():
    """Main execution function to run the full pipeline."""
    base_dir = Path(__file__).resolve().parent / "scripts"
    
    scripts_to_run = [
        base_dir / "etl_pipeline.py",
        base_dir / "load_db.py",
        base_dir / "build_notebooks.py"
    ]
    
    for script in scripts_to_run:
        if not script.exists():
            print(f"Script not found: {script}")
            sys.exit(1)
            
        run_script(script)
        
    print("\n🎉 Full pipeline execution completed successfully!")
    print("You can now launch the dashboard by running:")
    print("python -m streamlit run dashboard/app.py")

if __name__ == "__main__":
    main()
