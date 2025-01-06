"""
Create workflow for ai agents
"""

# We'll always have to start by creating a llm_config object to configure our agents
import os
api_key = os.getenv('OPENAI_API_KEY')
llm_config = {
    "model": "gpt-4o", 
    "api_key": api_key,
    "cache": None
    }

import autogen
from autogen.code_utils import create_virtual_env
from autogen.coding import CodeBlock, LocalCommandLineCodeExecutor
from autogen import ConversableAgent, AssistantAgent, UserProxyAgent
from autogen.code_utils import create_virtual_env
from pprint import pprint as pp
import datetime

# Start logging with logger_type and the filename to log to
# Get username
user = os.path.basename(os.path.expanduser('~'))
machine = os.uname().nodename
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"runtime_{user}_{machine}_{timestamp}.log"
logging_session_id = autogen.runtime_logging.start(
        logger_type="file", 
        config={"filename": log_filename},
        )
print("Logging session ID: " + str(logging_session_id))

from tools import (
    get_blech_clust_path,
    search_for_pattern,
    search_and_replace,
    modify_lines,
    get_func_code,
    readlines,
    listdir,
    search_for_file,
    readfile,
    get_commit_history,
    get_current_git_commit,
    change_git_commit,
    create_file,
    run_python_script,
    run_bash_script,
)

blech_clust_path = get_blech_clust_path()
if blech_clust_path == '':
    raise ValueError("Blech clust path not found, please set the path in the src directory")

##############################
# Create agents
##############################
tool_funcs = [
    get_blech_clust_path,
    search_for_pattern,
    search_and_replace,
    modify_lines,
    get_func_code,
    readlines,
    listdir,
    search_for_file,
    readfile,
    get_current_git_commit,
    get_commit_history,
    change_git_commit,
    create_file,
    run_python_script,
    run_bash_script,
    ]


# tool_funcs.append(llm_ception)

# chat_result = llm_ception(
#     system_message = '',
#     command_message = 'Get the path to the blech_clust repo',
#     )

executor = LocalCommandLineCodeExecutor(
    # virtual_env_context=venv_context,
    timeout=200,
    work_dir="coding",
    functions=tool_funcs,
)

def reflection_message(recipient, messages, sender, config):
    return f'''Review the following content. 
            \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}'''

system_message = """
You are a helpful AI assistant called "BlechBot", that edits code to solve issues for the blech_clust repo.
The code is located at `/home/abuzarmahmood/projects/blech_clust`
Solve tasks using your coding and language skills.
If you are asked about blech_clust with a different path, assume it is the same repository, and adjust paths to point to the local repository.
If you are provided with error traces, suggest solutions only after reading the code from the files present in the error trace. Use the python functions provided to you to read the files and edit them as necessary to debug the issue. If suggesting changes to code, always add comments to show where you have made changes and why.
 Always make sure you are using all the tools available to you so as to ask the user to do minimal tasks.
 blech_clust is a very big repository. As far as possible, avoid listing ALL files, or reading full files.
In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
    1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
    2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
Reply "TERMINATE" in the end when everything is done.
"""

# Agent that writes code
code_writer_agent = AssistantAgent(
# code_writer_agent = ConversableAgent(
    name="code_writer_agent",
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
    system_message = system_message,
)

formatted_funcs = executor.format_functions_for_prompt()

code_executor_agent = ConversableAgent(
    name="code_executor_agent",
    llm_config=False,
    human_input_mode="ALWAYS",
    default_auto_reply=
    "Please continue. If everything is done, reply 'TERMINATE'.",
)

# Register the tool signature with the assistant agent.
for this_func in tool_funcs:
    code_writer_agent.register_for_llm(
            name = this_func.__name__, 
            description = this_func.__doc__,
            )(this_func)
    code_executor_agent.register_for_execution(
            name=this_func.__name__)(this_func)



##############################
# Start the chat
##############################


print('Enter the message for the code writer agent: (type END to finish)')
lines = []
while True:
    line = input()
    if line == 'END':
        break
    lines.append(line)

message = '\n'.join(lines)

message += f"""
{formatted_funcs}

As far as possible, avoid the following: 
1) listing ALL files, 
2) reading full files,
3) asking the user to make changes to the code.
"""

chat_result = code_executor_agent.initiate_chat(
    code_writer_agent,
    message=message,
        )

usage_including_cached_inference = chat_result.cost['usage_including_cached_inference']
total_cost = usage_including_cached_inference['total_cost']
print(f"Total cost of session: {total_cost:.2f} USD")

rating_msg = "Please rate the assistant on a scale of 1-5 (higher = better): "
rating = input(rating_msg)
while not rating.isdigit() or int(rating) not in range(1, 6):
    rating = input(rating_msg)

# Ask for any feedback
print("Please provide any feedback for the assistant: (type END to finish)")
lines = []
while True:
    line = input()
    if line == 'END':
        break
    lines.append(line)

autogen.runtime_logging.stop()
