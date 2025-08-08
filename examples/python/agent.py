from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.tools.mcp import MCPClient
from strands_tools import http_request

# Define a naming-focused system prompt
NAMING_SYSTEM_PROMPT = """
You are an assistant that helps to name open source projects.

When providing open source project name suggestions, always provide
one or more available domain names and one or more available GitHub
organization names that could be used for the project.

Before providing your suggestions, use your tools to validate
that the domain names are not already registered and that the GitHub
organization names are not already used.
"""

# Load an MCP server that can determine if a domain name is available
domain_name_tools = MCPClient(
    lambda: stdio_client(StdioServerParameters(command="uvx", args=["fastdomaincheck-mcp-server"]))
)

# Use a pre-built Strands Agents tool that can make requests to GitHub
# to determine if a GitHub organization name is available
github_tools = [http_request]

with domain_name_tools:
    # Define the naming agent with tools and a system prompt
    tools = domain_name_tools.list_tools_sync() + github_tools
    naming_agent = Agent(system_prompt=NAMING_SYSTEM_PROMPT, tools=tools)

    # Run the naming agent with the end user's prompt
    naming_agent("I need to name an open source project for building AI agents.")
