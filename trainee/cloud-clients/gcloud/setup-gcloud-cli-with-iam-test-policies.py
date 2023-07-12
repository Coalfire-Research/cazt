# © 2023 Coalfire
#
# Author: Rodney Beede


import argparse
import os
from pathlib import Path
import random

# Third party
# none

# Useful for referencing external commands and files later
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))



def main(args):
    print(f"[INFO] This simulator does not create any users or credentials in a real GCP account.")


    # Build a user for each IAM policy JSON we have
    iam_json_location = Path(SCRIPT_DIR, "..", "..", "iam_policies")
    for iam_file in sorted(iam_json_location.glob("*.json")):
        username = Path(iam_file).stem + "@" + args.account_id

        print(username)


    print("Setup has ended")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="https://www.coalfire.com/")

    ran_acct_id = str( random.randint(0, (10**12) - 1)).zfill(12)

    parser.add_argument("--account-id", default=ran_acct_id, action="store", type=str,
        help="Account ID for the IAM principal user (customer's account number). Defaults to randomly generated.")

    args = parser.parse_args()
    
    # enforce desired formatting here
    args.account_id = args.account_id.zfill(12)

    main(args)
