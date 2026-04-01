## <span style="color:rgb(181, 76, 230)">Things to Explore</span>:
Async<span style="color:rgb(255, 192, 0)"> </span>Python - Very important to understand

Open AI SDK Core Conepts:
1. [**Agents**](https://openai.github.io/openai-agents-python/agents): LLMs configured with instructions, tools, guardrails, and handoffs
2. [**Handoffs**](https://openai.github.io/openai-agents-python/handoffs/): A specialized tool call used by the Agents SDK for transferring control between agents
3. [**Guardrails**](https://openai.github.io/openai-agents-python/guardrails/): Configurable safety checks for input and output validation
4. [**Sessions**](https://github.com/openai/openai-agents-python#sessions): Automatic conversation history management across agent runs
5. [**Tracing**](https://openai.github.io/openai-agents-python/tracing/): Built-in tracking of agent runs, allowing you to view, debug and optimize your workflows
## <span style="color:rgb(0, 176, 240)">Setup</span> 
Open AI Agents SDK
Constructs:
	`Agents` - represent LLMs
	`Handoffs` - represents interactions
	`Guardrails` - represent controls


setup `sendgrid` emailing client
## <span style="color:rgb(0, 176, 80)">Theory</span>

Lab 2 - Building a sales development rep
- A workflow of agent calls
	- Used agents constructs to spin up lightweight sales agents and then a4th agent to pick the one generating the best sales emails
- An agent that can use a tool
	- `@function_tool` decorator turns function into tool
	- You can turn a function into a tool or You can also have an `agent be converted into a tool` (scenario generator as atool for scenario reviewer.)
	- Handoffs and Agents-as-tools are similar
		- In both cases, an Agent can collaborate with another Agent
		- With tools, control passes back - so you are calling tool as an agent but maintaining control
		- With handoffs, control passes across
- An agent that can call on other agents - Tools vs Handoffs
	- Sales manager calls 3 agents as tools to generate the 3 emails
	- Then there is a handoff to the email manager
	- manager uses the subject writer and html converter as a tool

Lab 3
##### Structured Outputs
- Agent can output in pydantic python types: `NameCheckOutput`
- functions can be decorated with `input_guardrail`
##### Guardrails
- Guardrails can't just be if statements in python code, coz guardrails can themselves be agents
- They can only be applied to the input of the first agent or the output of the last agent - designed to protect your model against inappropriate inputs and also to protect against inappropriate guardrails
- tripwire construct used by open AI SDK

## <span style="color:rgb(255, 0, 0)">Quotes</span>
Autonomy also opens you up to agents going into infinite loops (e.g. "you can call this tool as many times as you want until satisfied")

	If you ask a model for reasoning behind decisions, its more likely to make better decisions. You always have to remind yourself taht while we treat models like thers a bit of humanity to them, it is rather just the strange side affect of great token prediction. Because its predicting teh best most likey token next, you ask it to predict tokens refectling on a reason then it is more likely to me more consistent and coherent with its output
## <span style="color:rgb(255, 192, 0)">Dev</span> 
AsyncPython - lightweight version of multithreading. doesn't involve multiple threads at a processor level or even different processes. 
- so its lightweight alternative too threading or multiprocessing. 
- LLMs have a lot of waiting for IO.
- functions defined by `async def` are coroutines
- you just `await` to run a coroutine, which schedules it for execution within an event loop
- While a coroutine is waiting, the `event loop` can run other coroutines
- Its a manual approach to implementing multithreading that only works when someone is blocked on waiting for some IO
- ITS LIGHTWEIGHT TOO. USED UBIQUITOUSLY IN AGENTIC FRAMEWORKS
- So in some ways its kind of fake multithreading or brute force multithreading, implemented manually by teh evnt loop as opposed to at the OS level
1. Create an instance of Agent
2. Use with trace() to track the agent
3. Call runner.run() to run the agent

<span style="color:rgb(255, 192, 0)">Trace</span>: Gave. a full debug trace of a single call to the LLM, packaged up in the Traces console on the open AI website

<span style="color:rgb(255, 192, 0)">LAB 4</span> - Deep Research 
Build your own DR agent Using Tools, Structured Outputs and Hosted Tools
Hosted Tools
	WebSearchTool - this is what we will use in this lab
	FileSearchTool
	ComputerTool
How does a model create objects as outputs. its all JSON CONVERSIONS UNDER TEH HOOD WITH PYDANTIC
## <span style="color:rgb(0, 176, 240)"> </span><span style="color:rgb(0, 176, 240)">Links</span>

Made an account on sendGrid for email agent: https://app.sendgrid.com/
Traces for Open AI SDK can be found here: https://platform.openai.com/logs?api=traces
Open AI SDK Doc: https://github.com/openai/openai-agents-python


Michael Janosko
