# © 2023-2025 Coalfire
#
# Author: Rodney Beede
#
# Just adds "powershell" to front of gcloud command


import argparse
import base64
import os
from pathlib import Path
import random
import re
import shutil
import subprocess


# Third party
# none

# Useful for referencing external commands and files later
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))



def main(args):
    print(f"[INFO] This tool assumes the gcloud command is available in the system path.")

    cmd_result = subprocess.run(
        ["powershell", "gcloud", "info"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True
        )

    if not cmd_result or not cmd_result.stdout:
        print("Failed to run gcloud info", file=subprocess.STDERR)
        exit(255)
        
    match = re.search(r"Installation Root: \[([^\]]+)", cmd_result.stdout.decode("utf-8"))
    
    if not match:
        print("Failed to find Installation Root in gcloud info output", file=subprocess.STDERR)
        exit(254)
    else:
        gcloud_install_root = match.group(1)
        print(f"[INFO] gcloud Installation Root was {gcloud_install_root}")
    
    source_path = Path(SCRIPT_DIR, "lib")
    destination_path = Path(gcloud_install_root, "lib")
    
    print(f"[INFO] Recursively copying {source_path} to {destination_path}")
    
    shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
    
    
    
    print("Setup has ended")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="https://www.coalfire.com/")

    # None today, but in-place for future usage

    args = parser.parse_args()
    
    main(args)