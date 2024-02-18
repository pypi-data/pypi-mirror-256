# my_streamlit_app/cli.py
from .ODA1 import main
import subprocess

def main1():
    subprocess.call(["streamlit", "run", "gvision\\ODA1.py"])

if __name__ == "__main__":
    main1()
