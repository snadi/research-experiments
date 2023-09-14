import os
import argparse
import pandas as pd
import json
import numpy as np

def analyze_repo(repo_dir):

   
    data_file_path = os.path.join(repo_dir, "output.json")
                  
    with open(data_file_path, "r") as data_file:
        data = json.load(data_file)

    median_count = np.median([x["count"] for x in data])

    return f"{median_count:.2f}"
      

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse and display reports')
    parser.add_argument('--outputdir', type=str, help='output folder containing results')

    args = parser.parse_args()
    outputdir = args.outputdir

    print(f"# Results Overview")
    print(f"| Lang | Repo | Median modification count|")
    print(f"| --- | --: | --: |")

    for lang in ['java', 'python']:
        lang_dir = os.path.join(args.outputdir, lang)
        
        for repo in os.listdir(lang_dir):
            repo_dir = os.path.join(lang_dir, repo)
            print(f"| {lang} | {repo} | {analyze_repo(repo_dir)} |")

