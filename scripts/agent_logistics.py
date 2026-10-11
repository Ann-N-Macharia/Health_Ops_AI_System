# agent_langchain.py - the same loop, run by a real LLM through LangChain
# Needs: pip install langchain langchain-openai langgraph langchain-mcp-adapters
# and OPENAI_API_KEY in your .env file.

import asyncio
# from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.mcp import MCPAdapter
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


async def run_logistics_agent(question: str):
    # MCPAdapter infers stdio transport from the .py path
    # For a single local server, pass the script path directly
    async with MCPAdapter(os.getenv("MCP_URL")) as adapter:
        tools = await adapter.list_tools()
        
        model = ChatOpenAI(
            model=os.getenv("LLM_MODEL"),
            temperature=0,
            base_url=os.getenv("LLM_BASE_URL"),    # Ollama
            api_key=os.getenv("LLM_API_KEY")         # dummy key
        )
        
        agent = create_agent(model, tools)
        
        result = await agent.ainvoke(
            {"messages": [("user", question)]},
            {"recursion_limit": 8},
        )

        print(result["messages"][-1].content)
        return result["messages"][-1].content
    
    
if __name__ == "__main__":
    question = "how many units of amoxicillin are there"
    asyncio.run(run_logistics_agent(question))