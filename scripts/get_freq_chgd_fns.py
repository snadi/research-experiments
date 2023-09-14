from pydriller import Repository
from argparse import ArgumentParser
from datetime import datetime
import json
import os

lang_extensions={
    'python': '.py',
    'java': '.java',
}

def get_modified_functions(repo_path, lastcommit, lang):
    modified_functions = {}

    commits = Repository(
        repo_path, 
        to_commit=lastcommit,
        only_modifications_with_file_types=[lang_extensions[lang]], 
        since=datetime(2023, 8, 1)
    ).traverse_commits()
  

    for commit in commits:
        for modified_file in commit.modified_files:
            changed_methods = modified_file.changed_methods
            for changed_method in changed_methods:
                method_path = f"{modified_file.new_path}#{changed_method.name}"
                if method_path not in modified_functions.keys():
                    modified_functions[method_path] = 1
                else:
                    modified_functions[method_path] += 1

    return modified_functions

def main():
    parser = ArgumentParser()
    parser.add_argument('--path', help='path to the repository')
    parser.add_argument('--language', help='language of the repository')
    parser.add_argument('--topn', help='top n modified functions')
    parser.add_argument('--lastcommit', help='the last commit to be considered when analyzing the history')
    parser.add_argument('--outputdir', help='directory where the output file will be stored')
    args = parser.parse_args()

    topn = int(args.topn)


    modified_functions = get_modified_functions(args.path, args.lastcommit, args.language) 

    # sorted_modified_functions = sorted(modified_functions.items(), key=lambda x: x[1], reverse=True)
    # topn_modified_functions = sorted_modified_functions[:topn]
    # topn_modified_functions = [{'function': x[0], 'count': x[1]} for x in topn_modified_functions]

    output_file = os.path.join(args.outputdir, "output.json")
    with open(output_file, "w") as outfile:
        outfile.write(json.dumps(modified_functions, indent=4, sort_keys=False))
    
if __name__ == "__main__":
    main()