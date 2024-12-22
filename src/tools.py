"""
Tools for the agents to use.
"""

import os
import sys

def get_blech_clust_path() -> str:
    """
    Return path to blech_clust repo
    """
    return '/home/abuzarmahmood/projects/blech_clust'

def search_and_replace(
        file_path : str,
        search_text : str, 
        replace_text : str,
        ) -> bool:
    """
    Search and replace text in a file

    Inputs:
        - file_path : Path to file
        - search_text : Text to search for
        - replace_text : Text to replace with

    Returns:
        - True if successful, False if search_text not found
    """
    # make backup
    import shutil
    import ast

    shutil.copy2(file_path, file_path + '.bak')

    with open(file_path, 'r') as file:
        file_data = file.read()

    # Check for exact match
    if search_text not in file_data:
        print(f"Search text not found in file: {file_path}")
        return False

    new_data = file_data.replace(search_text, replace_text)

    with open(file_path, 'w') as file:
        file.write(new_data)

    # Check that file is valid
    try:
        ast.parse(new_data)
    except SyntaxError as e:
        print('Editing file created a syntax error')
        print(f"Syntax error in file: {file_path}")
        print(e)
        # Restore backup
        shutil.copy2(file_path + '.bak', file_path)
        os.remove(file_path + '.bak')
        return False

    return True

def listdir(
        directory : str, 
        extension : str = None, 
        ) -> str: 
    """List contents of a directory
    Inputs:
        - Directory : Path to directory
        - Extension (optional) : Only return files with the given extension
    """
    if extension:
        ext_str = f"-iname '*.{extension}'"
    else:
        ext_str = ""
    run_str = f"find {directory} " + ext_str
    print(run_str)
    # out = os.system(run_str)
    out = os.popen(run_str).read() 
    return out

def readfile(filepath : str) -> str:
    """Read the contents of a file
    Inputs:
        - Filepath
    """
    with open(filepath, 'r') as file:
        data = file.read()
    return data

def get_current_git_commit() -> str:
    """Get the current git commit
    """
    # out = os.system("git rev-parse HEAD")
    out = os.popen("git rev-parse HEAD").read()
    return out

def change_git_commit(commit: str) -> str:
    """Change the current git commit
    Inputs:
        - Commit
    """
    # os.system(f"git checkout {commit}")
    out = os.popen(f"git checkout {commit}").read()
    return out
