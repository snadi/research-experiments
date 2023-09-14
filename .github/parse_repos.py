import os
import logging as log
import json

def get_repos():
    repos = {}
    script_dir = os.path.dirname(__file__)
    java_repo_file = os.path.join(script_dir, "java-repo-list.txt")
    python_repo_file = os.path.join(script_dir, "python-repo-list.txt")

    repos["java"] = parse_repo_file(java_repo_file)
    repos["python"] = parse_repo_file(python_repo_file)
    return repos

def parse_repo_file(repo_file):
    repos =[]
    with open(repo_file, 'r') as jfile:
        for line in jfile:
            reponame, commit = line.strip().split('#')
            reponame = reponame.split(':')[-1]
            repos.append({"repo": reponame, "commit": commit})          
    return repos

if __name__ == "__main__":
    libraries = get_repos()

    print(json.dumps(libraries))
    