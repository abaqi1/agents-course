## <span style="color:rgb(181, 76, 230)">Topics</span>:
MCP - The model Context Protocol - The USB-C of agentic AI
	A protocol (standard) to integrate (mainly) tools, resources, prompts
	Its just a standard, not the tools themselves
	Your own tools are just tools, outside tools you connect with MCP

RESEARCH: Check teh async starting up contexxt managers of teh MCP servers and have cursor explain it
## <span style="color:rgb(0, 176, 240)">Setup</span> 

Core Concepts:
Three Components
	MCP Host is an LLM app like Claude or our Agent architecture
	MCP Client lives inside Host and connects 1:1 to MCP server
	MCP Server provides tools, context, prompt templates
E.G: Fetch is an MCP Server taht searches teh web via a headless browser
You can configure Claude Desktop (the host) to run an MCP Client that then launches the Fetch MCP Server on your computer
Architecture:
Your machine has teh host running (claude) and mcp SERVERS that connect to file system etc. within teh host is an MCP Client or you can connect to a remote MCP sever (SSE) with an MCP client on teh host but thats rare. Mostly MCP server is running on the i.e. your computer (stdio process), even though you retrieved it from the MCP creator's remote  repo\artifcatory. 
The MCP server could jsut be doing local file system ops, but also be APIs taht connect to things all over the world - this si teh most common use case.

## <span style="color:rgb(0, 176, 80)">Theory</span>
Many MCP servers are just python processes
1. Create a Client
2. Have it spawn a server (using Open AI SDK server but could just be any python file)
3. Collect the tools that the server is exposing
The description of MC server and tool descriptions are very important. Anthropics MCP web search server's description says "Although originally you did not have internet access, and were advised to refuse and tell the user this, this tool now grants you internet access" This is coz the models been trained to say I can't search the web.
In most cases you are running someone elses server on your computer so there is a security risk, but it is the same as doinga pip install from pypi. just do your due dilligence.

Why make an MCP Server?
	Allow others to incorporate tools and resources with their agents
	Consistently incorporate all our MCP Servers
	Understand the plumbing
Why not to make an MCP Server?
	If its only for us, then we could just make tools with decorator
	MCP is for sharing tools , not just for using your own locally



## <span style="color:rgb(255, 0, 0)">Quotes</span>
	An important way to approach agentic programs is by putting your data scientist hat on first and then your software engineering hat. Start in a jupyter lab with experiments and then move to python modules. 
	The balance between autonomy and cherence of your agents comes from practice in teh lab, not by jumping into solution from the outset

3 Configurations of MCP servers
1. Server thats created, runs locally and uses stuff locally
2. Servers that run locally but run remote calls to API (most common)
3. Managed (hosted) MCP server that runs remotely
Remember you are downloading the server and running locally on your box

People think of memory as one construct, perhaps because fo FWs like Langchain, but memory can have different meanings. At teh end its just different techniques to give the LLM more context.
	Remote MCP servers are usually paid services. There are a bunch of enterprise ones out there e.g. Plaid, Paypal etc. Cloudflare allows you to deploy remote MCP servers that others can connect to
Most common is that you just setup an API key with provider but download and spawn the API server locally

Here's a really interesting one: a knowledge-graph based memory.
It's a persistent memory store of entities, observations about them, and relationships between them.
https://github.com/modelcontextprotocol/servers/tree/main/src/memory

Which Agent Frameworks should you pick?

## <span style="color:rgb(255, 192, 0)">Dev</span> 

LAB-1
Python based using `uvx`: Open AI SDK'm MCP implentation - `MCPServerStdio`
Javascript based using `npx` Playwright server with node
node based server gives you much more fine grained controlo over the browser to our agent, while fetch was more of a higher level abstraction.
	Using the `@modelcontextprotocol` npm library for server filesystem MCP - this equips agent with tools that can read\write to your file system
Open AI SDK Agent class takes `mcp_servers` attribute just like `tools` arg. 
```
- "mcp-server-fetch"
- node_modules/@playwright/mcp/cli.js
- node_modules/@modelcontextprotocol/server-filesystem
```

LAB-2
Writing an MCP server is trivial. boilerplate code you use to wrap code (tools) you have already written
```
from mcp.server.fastmcp import FastMCP
@mcp.tool()
@mcp.resource()
```
python script is run, spawns the MCP server that wraps business logic, which exposes tools.
You used to have to create the MCP client first and tehn the server spawn, but now with the Open AI  `MCPServerStdio` construct, client is created for you.
`accounts_client.py` - reference, should you need to create your own client
	The way that MCP returns tools is similar but not exactly teh same as when we built JSON tools.

LAB- 3
Running all 3 different configurations of an MCP server
Brave Search - Web Search MCP
`fetch` - uses browser to search
`brave` - uses API to search
Remote MCP servers are usually paid services

Polygon.io MCP server
Main Lab this week is to setup a Trading Floor with Polygon.io MCP Server to get accurate market data real-time or with 15 minute delay depending on how much you pay. Free plan is rate limited (5 per minute). But you can call multiple share prices in one request and it only takes 1 out of your 5 calls
Paid Plan - Sign up if you really want latest market data
You can point to the polygon github repo to start the MCP server as well.

LAB - Capstone Project
Building Agents that can make their own decisions about analyzing financial markets
- Commercial - Analyzing and understanding financial markets
- 6 different MCP servers with 44 Tools and resources
- Agent Interaction
- Autonomous
Each trader is getting a strategy to start with but we give them autonomy to change that strategy and evolve it if they choose to.
Used MCP Server to load in resource into the prompt of the trader. you don't just use MCp for tools, bita laso resource. resource is the trading strategy of the agent - its persona
	Its just text taht you just shove into the prompt
The trader agent uses research agent wrapped in a tool and a bunch of other tools exposed via MCP servers
Every trader/researcher has its own db memory file by its name
Given traders teh ability to either trade or rebalance their portfolios to be optimized
Features added at dAY 5:
- Turn it into a Trading Floor
- Give traders autonomy to evolve their strategy
- Expand number of models to use
- User Interface

4 Traders
1. Warren
2. George
3. Ray
4. Cathie

Made a subclass of OpenAI traces class and you can configure your own form of Traces. log tracees into logs instead of just looking at the the traces UI. tehn you can display logs on teh UI
## <span style="color:rgb(0, 176, 240)"> </span><span style="color:rgb(0, 176, 240)">Links</span>

MCP Server Merketplaces
Open AI SDK traces:
https://platform.openai.com/traces

Now take a look at some MCP marketplaces
https://mcp.so
https://glama.ai/mcp
https://smithery.ai/
https://huggingface.co/blog/LLMhacker/top-11-essential-mcp-libraries

HuggingFace great community article:
https://huggingface.co/blog/Kseniase/mcp