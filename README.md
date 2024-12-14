# BLECH Bot
## Description
Agent to:
- Assess blech_clust github issues
- Prompt users to provide more information when needed
    - blech_clust version / commit
    - files involved in error or feature request
- Suggest solutions if enough information is provided

# Operations can be broken down into a multi-agent system:
- **Agent 1**
- - Gathers sufficient information to assess the issue
- - - blech_clust version / commit
- - - files involved in error or feature request
- **Agent 2**
- - Loads relevant code-snippets and documentation to use as reference
- **Agent 3**
- - Search and replace suggestor
- - Returns commands to search and replace strings to modify code, given the information provided by Agent 1 and 2
- **Agent 4**
- - Suggests solutions based on the information provided by Agent 1, 2, and 3

Agents 1,2 and 3 can be implemented in a nested fashion, where Agent 1 calls Agent 2, and Agent 2 calls Agent 3. Agent 4 can be implemented as a separate agent that calls Agents 1, 2, and 3.

# Available Tools:
- Search and replace tool
- - Search for a string in a file and replace it with another string
- Code execution tool
- - Execute code snippets in a specified environment

