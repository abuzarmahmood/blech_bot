"""
Tools for the agents to use.
"""

import os
import sys

src_dir = os.path.dirname(os.path.abspath(__file__))

def get_blech_clust_path() -> str:
    """
    Return path to blech_clust repo
    """
    blech_path_path = os.path.join(src_dir, 'blech_clust_path.txt')
    print(f'Looking for blech_clust_path.txt at {blech_path_path}')
    if not os.path.exists(blech_path_path):
        print("blech_clust_path.txt not found")
        return 'blech_clust_path.txt not found'
    blech_path = open(blech_path_path, 'r').read().strip() 
    print(f'blech_clust_path.txt found, path: {blech_path}')
    return blech_path

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

    print('Search and replace successful')
    return True

def readlines(
        file_path : str,
        start_line : int,
        end_line : int,
        ) -> str:
    """
    Read lines from a file

    Inputs:
        - file_path : Path to file
        - start_line : Start line
        - end_line : End line

    Returns:
        - Lines from file
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    return "".join(lines[start_line:end_line])

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
        ext_str = f"-iname '*{extension}'"
    else:
        ext_str = ""
    run_str = f"find {directory} " + ext_str
    print(run_str)
    # out = os.system(run_str)
    out = os.popen(run_str).read() 
    return out

def search_for_file(
        directory : str,
        filename : str,
        ) -> str:
    """Search for a file in a directory
    Inputs:
        - Directory : Path to directory
        - Filename : Name of file

    Returns:
        - Path to file
    """
    run_str = f"find {directory} -iname {filename}"
    print(run_str)
    # out = os.system(run_str)
    out = os.popen(run_str).read()
    if out:
        return out
    else:
        return "File not found"

def readfile(filepath : str) -> str:
    """Read the contents of a file
    Inputs:
        - Filepath
    """
    with open(filepath, 'r') as file:
        data = file.read()
    return data

def git_fetch() -> str:
    """Fetch from git
    """
    # out = os.system("git fetch")
    out = os.popen("git fetch").read()
    return out

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
    git_fetch()
    out = os.popen(f"git checkout {commit}").read()
    return out

def get_func_code(
        module_path : str,
        func_name : str,
        ) -> str:
    """Get the code for a function
    Needs to load the module and get the source code for the function

    Inputs:
        - module_path : Path to module
        - func_name : Name of function
    
    Returns:
        - Code for function
    """
    import inspect
    import importlib.util
    spec = importlib.util.spec_from_file_location("module.name", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    func = getattr(module, func_name)
    return inspect.getsource(func)

def get_func_code_2(
        module_path : str,
        func_name : str,
        ) -> str:
    """Use ast to get the code for a function

    Inputs:
        - module_path : Path to module
        - func_name : Name of function

    Returns:
        - Code for function
    """
    import ast
    with open(module_path, 'r') as file:
        tree = ast.parse(file.read())
    wanted_func = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            wanted_func = node
            break
    if wanted_func is None:
        return "Function not found, it may be a class method or not in the file"
    else:
        return ast.unparse(wanted_func)

def get_func_code_3(
        module_path : str,
        func_name : str,
        ) -> str:
    """Use simple search to get the code for a function

    Inputs:
        - module_path : Path to module
        - func_name : Name of function

    Returns:
        - Code for function
    """

    with open(module_path, 'r') as file:
        lines = file.readlines()

    # Find all function definitions
    import re
    match_pattern = re.compile(r'def\s+.*\(')
    func_defs = re.findall(match_pattern, "\n".join(lines)) 
    # Get line numbers for each function definition
    func_def_lines = [i for i, line in enumerate(lines) if match_pattern.findall(line)]
    func_def_line_map = {func_def_lines[i]: func_defs[i] for i in range(len(func_defs))}

    # Find range of lines for wanted function
    for i, this_num in enumerate(func_def_lines):
        if func_name in func_def_line_map[this_num]:
            start_line = this_num
            try:
                end_line = func_def_lines[i+1] - 1
            except IndexError:
                end_line = len(lines)
            break

    # Get code for function
    code = "".join(lines[start_line:end_line])
    return code
