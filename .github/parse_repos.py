import os
import logging as log
import json

def get_repos():
    repos = []
    script_dir = os.path.dirname(__file__)
    java_repo_file = os.path.join(script_dir, "java-repo-list.txt")
    python_repo_file = os.path.join(script_dir, "python-repo-list.txt")

    repos.extend(parse_repo_file(java_repo_file, lang='java'))
    repos.extend(parse_repo_file(python_repo_file, lang='python'))
    return repos

def parse_repo_file(repo_file, lang):
    repos =[]
    with open(repo_file, 'r') as jfile:
        for line in jfile:
            reponame, commit = line.strip().split('#')
            reponame = reponame.split(':')[-1]
            reponame = reponame.split('.git')[0]
            repos.append({"name": reponame, "commit": commit, "language": lang})          
    return repos

if __name__ == "__main__":
    libraries = get_repos()

    print(json.dumps(libraries))
    