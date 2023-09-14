from pydriller import Repository
from argparse import ArgumentParser
from datetime import datetime
import json
import os

lang_extensions={
    'python': '.py',
    'java': '.java',
}

def main():
    parser = ArgumentParser()
    parser.add_argument('--path', help='path to the repository')
    parser.add_argument('--language', help='language of the repository')
    parser.add_argument('--topn', help='top n modified functions')
    parser.add_argument('--outputdir', help='directory where the output file will be stored')
    args = parser.parse_args()

    topn = int(args.topn)

    modified_functions = {}

    try:
        commits = Repository(
            args.path, 
            only_in_branch='master',
            only_modifications_with_file_types=[lang_extensions[args.language]], 
            since=datetime(2023, 1, 1)
        ).traverse_commits()
    except:
        # if master branch does not exist, use main branch
        commits = Repository(
            args.path, 
            only_in_branch='main',
            only_modifications_with_file_types=[lang_extensions[args.language]], 
            since=datetime(2023, 1, 1)
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

    # get top n modified functions in json format

    sorted_modified_functions = sorted(modified_functions.items(), key=lambda x: x[1], reverse=True)
    topn_modified_functions = sorted_modified_functions[:topn]
    topn_modified_functions = [{'function': x[0], 'count': x[1]} for x in topn_modified_functions]

    output_file = os.path.join(args.outputdir, "output.json")
    with open(output_file, "w") as outfile:
        outfile.write(json.dumps(topn_modified_functions, indent=4, sort_keys=False))
    
if __name__ == "__main__":
    main()