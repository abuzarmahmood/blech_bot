# BLECH Bot
## Description
Agent to:
- Assess blech_clust github issues
- Prompt users to provide more information when needed
    - blech_clust version / commit
    - files involved in error or feature request
- Suggest solutions if enough information is provided

# Installation
- Clone the repository
- Install `make install`
- Update `src/blech_clust_path.txt` with the path to the blech_clust repository
- Set up your OpenAI API key:
  - Get your API key from [OpenAI](https://platform.openai.com/api-keys)
  - Set it as an environment variable:
    ```bash
    export OPENAI_API_KEY='your-api-key-here'
    ```
  - For permanent setup, add the above line to your `~/.bashrc` or `~/.zshrc`
- Run the bot `make run`

# Agent System
The system uses two main agents:

- **Code Writer Agent**
  - Analyzes issues and suggests solutions
  - Uses available tools to inspect and modify code
  - Writes code and suggests changes
  - Provides explanations for changes

- **Code Executor Agent**
  - Executes the suggested changes
  - Validates code modifications
  - Reports execution results back to writer agent

# Available Tools:
- **Repository Management**
  - `get_blech_clust_path()`: Get path to blech_clust repo
  - `get_commit_history()`: View git commit history
  - `get_current_git_commit()`: Get current commit hash
  - `change_git_commit()`: Switch to different commit

- **Code Search & Analysis**
  - `search_for_pattern()`: Search for text patterns
  - `search_for_file()`: Find files by name
  - `listdir()`: List directory contents
  - `get_func_code()`: Extract function definitions

- **Code Modification**
  - `search_and_replace()`: Replace text in files
  - `modify_lines()`: Edit specific line ranges
  - `create_file()`: Create new files

- **File Operations**
  - `readfile()`: Read entire file contents
  - `readlines()`: Read specific line ranges

- **Code Execution**
  - `run_python_script()`: Execute Python files
  - `run_bash_script()`: Execute shell scripts
