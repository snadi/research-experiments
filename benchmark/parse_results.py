import os
import argparse
import pandas as pd
import json
import matplotlib.pyplot as plt

def plot_lang_chart(lang_dir):

    # Initialize a dictionary to store repo counts
    repo_counts = {}

    # Loop through directories in the data directory
    for repo_dir in os.listdir(lang_dir):
        # Check if the entry is a directory
        if os.path.isdir(os.path.join(lang_dir, repo_dir)):
            # Construct the path to the data JSON file
            data_file_path = os.path.join(lang_dir, repo_dir, "output.json")
            
            # Check if the data file exists
            if os.path.exists(data_file_path):
                # Read the data from the JSON file
                with open(data_file_path, "r") as data_file:
                    data = json.load(data_file)
                

                repo_info_file_path = os.path.join(lang_dir, repo_dir, "repo_info.json")
                
                with open(repo_info_file_path, "r") as repo_info_file:
                    repo_info = json.load(repo_info_file)
                repo_name = repo_info['simplename']
            
                
                # Organize data by repository
                if repo_name not in repo_counts:
                    repo_counts[repo_name] = []
                
                for item in data:
                    repo_counts[repo_name].append(item["count"])

    # Create a boxplot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(repo_counts.values(), vert=False)
    ax.set_yticklabels(repo_counts.keys())
    ax.set_xlabel('Count')
    ax.set_title('Distribution of Counts by Repository')

    plt.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse and display reports')
    parser.add_argument('--outputdir', type=str, help='output folder containing results')

    args = parser.parse_args()
    outputdir = args.outputdir

    for lang in ['java', 'python']:
        lang_dir = os.path.join(args.outputdir, lang)
            
        plot_lang_chart(lang_dir)

