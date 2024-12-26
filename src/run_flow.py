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

from tools import (
    get_blech_clust_path,
    search_and_replace,
    get_func_code_3,
    listdir,
    search_for_file,
    readfile,
    get_current_git_commit,
    change_git_commit,
)

##############################
# Create agents
##############################

# venv_dir = ".env_llm"
# venv_context = create_virtual_env(venv_dir)

tool_funcs = [
    get_blech_clust_path,
    search_and_replace,
    listdir,
    search_for_file,
    readfile,
    get_current_git_commit,
    change_git_commit,
    get_func_code_3,
    ]

executor = LocalCommandLineCodeExecutor(
    # virtual_env_context=venv_context,
    timeout=200,
    work_dir="coding",
    functions=tool_funcs,
)
# print(
#     executor.execute_code_blocks(
#         code_blocks=[CodeBlock(language="python", code="import sys; print(sys.executable)")])
# )
# # exit()

def reflection_message(recipient, messages, sender, config):
    return f'''Review the following content. 
            \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}'''

# basic_reviewer = AssistantAgent(
#     name="Basic_Information_Reviewer",
#     llm_config=llm_config,
#     system_message="""
#     You are a helpful and very capable agent for gathering initial information
#     for any blech_clust related issues.
#     If you are asked a question, make sure you gather
#     1) what commit of blech_clust the issue is at
#     2) what files are involved in the issue
#     If this information is not initially provided, ask the user to provide it
#     """
# )
# 
# code_reviewer = AssistantAgent(
#     name="Code_Research_Agent",
#     llm_config=llm_config,
#     system_message=f"""
#     You are a helpful and very capable agent for gathering code and
#     documentation for the blech_clust issue at hand.
#     You are provided with the following tools: {[x.__name__ for x in tool_funcs]}
#     You should extract documentation and code for the relevant issue and provide it.
#     """
# )
# 
# meta_reviewer = AssistantAgent(
#     name="Meta_Reviewer",
#     llm_config=llm_config,
#     system_message="""
#     You are a meta reviewer, you aggregate and review
#     the work of other reviewers and give a final recommendation for how the code should
#     be edited
#     """
# )

# code_editor = autogen.AssistantAgent(
#     name="Code_Edit_Suggestion_Agent",
#     llm_config=llm_config,
#     system_message="""
#     You are a helpful and very capable agent for executing edits to code and testing
#     whether the edits resolved the issue.
#     You are provided with tools to edit code given snippts of code provided to you.
#     Provide exact snippets in SEARCH and REPLACE clauses.
# """
# )

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

# code_writer_agent_system_message = code_writer_agent.system_message
formatted_funcs = executor.format_functions_for_prompt()

# 
# code_writer_agent = AssistantAgent(
#     name="code_writer_agent",
#     llm_config=llm_config,
#     code_execution_config=False,
#     human_input_mode="NEVER",
#     system_message = code_writer_agent_system_message,
# )


# Code executor agent
# code_executor_agent = UserProxyAgent( 
code_executor_agent = ConversableAgent(
    name="code_executor_agent",
    llm_config=False,
    # code_execution_config={"executor": executor},
    # code_execution_config={"work_dir":"coding", "use_docker":False}
    human_input_mode="ALWAYS",
    default_auto_reply=
    "Please continue. If everything is done, reply 'TERMINATE'.",
)

# tool_reviewer = AssistantAgent(
#      name="Tool_Reviewer",
#      llm_config=llm_config,
#      system_message=f"""
#      You are a helpful and very capable agent for reviewing the tools used by the code writer.
#      You are provided with the following tools: {[x.__name__ for x in tool_funcs]}
#      You should review the tools used by the code writer and provide feedback on whether all appropriate tools were used. 
#      """,
#      default_auto_reply="Please continue. If everything is done, reply 'TERMINATE'.",
#      )


# Register the tool signature with the assistant agent.
for this_func in tool_funcs:
    code_writer_agent.register_for_llm(
            name = this_func.__name__, 
            description = this_func.__doc__,
            )(this_func)
    code_executor_agent.register_for_execution(
            name=this_func.__name__)(this_func)
    # tool_reviewer.register_for_llm(
    #         name = this_func.__name__, 
    #         description = this_func.__doc__,
    #         )(this_func)

# # Register the tool function with the user proxy agent.
# user_proxy.register_for_execution(name="calculator")(calculator)


##############################
# Create chats
##############################

# review_chats = [ # This is our nested chat
#     {
#      "recipient": basic_reviewer, 
#      "message": reflection_message, 
#      "summary_method": "reflection_with_llm",
#      "summary_args": 
#         {
#         "summary_prompt" : 
#         "Return review into as JSON object only:"
#         "{'Reviewer': '', 'Review': ''}. Here Reviewer should be your role",
#         },
#      "max_turns": 1},
#     
#     {
#      "recipient": code_reviewer, 
#      "message": reflection_message, 
#      "summary_method": "reflection_with_llm",
#      "summary_args": {"summary_prompt" : 
#         "Return review into as JSON object only:"
#         "{'Reviewer': '', 'Review': ''}.",},
#      "max_turns": 1},
#        
#      {"recipient": meta_reviewer, 
#       "message": "Aggregrate feedback from all reviewers and give final suggestions on the writing.", 
#       "max_turns": 1},
# ]
# 
# 

# review_chats = [
#         {
#             "recipient": tool_reviewer,
#             message: "Please make sure this plan of actions uses all the tools/functions avaiable to us so as to ask the user for minimal input.",
#             "max_turns": 1,
#             },
#         ]
# 
# code_writer_agent.register_nested_chats(
#     review_chats,
#     trigger=code_executor_agent,
# )


##############################
# Start the chat
##############################

message = """
I got the following error in blech_clust, can you edit the code to help me debug it?

(blech_clust) cmazzio@cmazzio-Precision-Tower-5810:~/Desktop/blech_clust$ python blech_units_characteristics.py $DIR
/home/cmazzio/anaconda3/envs/blech_clust/lib/python3.8/site-packages/tqdm/std.py:666: FutureWarning: The Panel class is removed from pandas. Accessing it from the top-level namespace will also be removed in the next version
  from pandas import Panel
============================================================
Attempting blech_units_characteristics.py, started at 2024-12-13 13:56:52
============================================================
Loading spikes
Spike trains loaded from following dig-ins
0. /spike_trains/dig_in_14 (Group) ''
1. /spike_trains/dig_in_15 (Group) ''
2. /spike_trains/dig_in_16 (Group) ''
Traceback (most recent call last):
  File "blech_units_characteristics.py", line 73, in <module>
    this_dat.get_sequestered_data()
  File "/home/cmazzio/Desktop/blech_clust/utils/ephys_data/ephys_data.py", line 1065, in get_sequestered_data
    self.get_sequestered_spikes()
  File "/home/cmazzio/Desktop/blech_clust/utils/ephys_data/ephys_data.py", line 1005, in get_sequestered_spikes
    this_seq_spikes = self.spikes[taste_ind][this_row['trial_inds']]
IndexError: list index out of range
"""

# chat_result = code_executor_agent.initiate_chat(
#     code_writer_agent,
#     message=message
# )

###############################
# Create chat structure such that
# 1) code_writer_agent suggests a plan of action
# 2) tool_reviewer agent makes sure all tools are being used
# 3) if so, code is sent to code_exectuor_agent

# chat_structure = [
#          # {
#          #     "recipient": code_writer_agent,
#          #     "message": message,
#          #     "max_turns": 1,
#          #     },
#         {
#             "recipient": tool_reviewer,
#             "message": "Please make sure this plan of actions uses all the tools/functions avaiable to us so as to ask the user for minimal input.",
#             "summary_method": "last_msg",
#             "max_turns": 1,
#             },
#          # {
#          #     "recipient": code_writer_agent,
#          #     "message": message,
#          #     "max_turns": 1,
#          #     },
#          # {
#          #     "recipient": code_executor_agent,
#          #     "message": "Please execute the code to debug the error.",
#          #     "max_turns": 1,
#         ]
# 
# # code_writer_agent.register_nested_chats(
# #     chat_structure,
# #     trigger= lambda sendor : sendor == code_executor_agent,
# #     )
# 
# code_executor_agent.register_nested_chats(
#     chat_structure,
#     trigger = code_writer_agent,
#     )


# message = input("Enter message: ")

message += f"""
{formatted_funcs}

As far as possible, 
1) avoid listing ALL files, 
2) reading full files,
3) asking the user to make changes to the code.
"""

chat_result = code_executor_agent.initiate_chat(
    code_writer_agent,
    message=message,
        )
