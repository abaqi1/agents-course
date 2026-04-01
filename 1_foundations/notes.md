## <span style="color:rgb(181, 76, 230)">Things to Explore</span>:
- n8n
- automatic philips hue connection with LLMs
- Exploring llm actions with other LLMs with pydantic structures

## <span style="color:rgb(0, 176, 240)">Setup</span> 
Cursor - IDE
UV - For virtual Environments
API - Open AI and DeepSeek 

## <span style="color:rgb(0, 176, 80)">Theory</span>
#### Agents and Agentic Architecture\Patterns
One or more of these defines Agentic AI for most people
1. Multiple LLM calls
2. LLMs with ability to use Tools (hallmark ability - litmus test of whether an LLM is agentic)
3. An environment where LLMs interact
4. A Planner to coordinate activities
5. Autonomy (giving some ability to LLM to control what happens)

- Starting at the no FWs end so that when we build up towards the stuff that gets us abstracted away from the basics, we have a good idea of what's going on. 
- A<span style="color:rgb(0, 176, 80)"> tool call is a glorified if statement</span> - In theory you don't have to mention the tool call option in the system prompt but it always helps. Repetition always works well. Increase the probability of the LLM using your tool and get in the habit of <span style="color:rgb(0, 176, 80)">BIASsing</span> the model to output tokens that are consistent with your objective. 
- Good to remind yourself every OIAW that it is an LLM and at any given point just basically predicting the next token or word. - <span style="color:rgb(0, 176, 80)">Its hard to wrap the head around but predicting next tokens is also what causes an LLM to use a tool call.</span>
#### Agentic Systems vs Agentic Workflows:
The lines here are blurred
- Workflows are systems where LLMs and tools are orchestrated through predefined code paths
	1. Prompt Chaining - step by step sequenced well defined tasks. Frame each task to be very effective.
	2. Routing - Direct an input to a specialised sub-task ensuring separation of concerns
	3. Parallelisation - Breaking down tasks and running multiple subtasks concurrently
	4. Orchestrator - Worker - Complex tasks are broken down dynamically and combined
	5. Evaluator-Optimizer - LLM output is validated by another (Text2BDD)
- Agents are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks
	1. Open Ended
	2. Feedback Loops
	3. No fixed Path
	Risks:
	4. Unpredictable path
	5. Unpredictable output
	6. Unpredictable costs
	Solutions:
	7. Monitoring
	8. Guardrails

Exercise: Evaluator-Optimizor worflow as a design pattern for llm to check other LLMs answer. and used structured outputs as a means to communicate with the evaluator. 
#### Orchestrating LLMs 

Autonomy and Tools
Project: Talking Resume

#### Resources and Tools

#### Agentic Frameworks

##### Frameworks

- You can connect directly to LLMs and don't always need to use the framework

No Framework == Need MCP - this protocol allows models and data providers and APIs

- OpenAI Agents - Light weight SDK

- Crew AI - No Code

- Langraph - Complex and heavy learning curve. you are signing up for the ecosystem

- AutoGen - Also very powerful

- & Many More - Gotta way in tradeoffs

  

#### Resources vs Tools
Resources
	Provide aLLM with resources to improve the LLM's expertise. Smart techniques -> RAG
	
Tools
	Give an LLM the power to carry out actions like query a DB or message other LLMS - Giving it some autonomy. Sounds a little magical but the rality is rather mundane

Diagrams of Theory vs Reality
## <span style="color:rgb(255, 0, 0)">Quotes</span>
- <span style="color:rgb(255, 0, 0)">When we make a call to one of the big LLMs, there are trillions of floating point calculations that happen under the hood</span>

- <span style="color:rgb(181, 76, 230)">AI Agents are programs where LLM outputs control the workflow</span>

## Prompt Engineering vs Context Engineering

The secret to building truly effective AI agents has <span style="color:rgb(255, 0, 0)">less to do</span> with the complexity of the code you write, and <span style="color:rgb(255, 0, 0)">everything to do</span> with the quality of the context you provide.

	Context Engineering is the discipline of designing and building dynamic systems that provides the right information and tools, in the right format, at the right time, to give a LLM everything it needs to accomplish a task.

Then came **Context Engineering**, which sounds like Prompt Engineering’s boring cousin — until you realize it’s what makes everything _actually_ work at scale.

<span style="color:rgb(255, 0, 0)">Think of it like this</span>:

- <span style="color:rgb(255, 0, 0)">Prompt Engineering</span> focuses on _what to say_ to the model at a moment in time.
- <span style="color:rgb(255, 0, 0)">Context Engineering </span>focuses on _what the model knows_ when you say it — and _why_ it should care.

> If Prompt Engineering is writing a brilliant instruction…  
> Context Engineering is deciding what happens _before_ and _after_ that instruction — what’s remembered, what’s pulled from memory or tools, how the whole thing’s framed.

So no, these aren’t competing practices.

> Prompt Engineering is one small part of the much bigger machine that Context Engineering builds.

 Relationship Between the Two

> <span style="color:rgb(255, 192, 0)">Prompt Engineering is what you do _inside_ the context window.  
> Context Engineering is how you decide _what fills_ the window.</span>

You can engineer a killer prompt. But if it gets buried behind 6K tokens of irrelevant chat history or poorly formatted retrieved docs? **Game over.**

> So yeah — prompt engineering is still important. But it lives inside the container that context engineering builds.

- <span style="color:rgb(255, 192, 0)">Prompt Engineering is how we _started_</span>. It’s the quick-and-dirty hack to bend LLMs to your will.
-<span style="color:rgb(255, 192, 0)"> Context Engineering is how we _scale</span>_. It’s the real design work behind reliable LLM-powered systems.

> Prompt engineering gets you the first good output
> ==Context engineering makes sure the 1,000th output is still good.==
## <span style="color:rgb(255, 192, 0)">Dev</span> 
Start Ollama: `!ollama pull llama3.2`
Open the web UI: http://localhost:11434 and see the message "Ollama is running"
`ollama pull <model_name>` downloads a model locally
`ollama ls` lists all the models you've downloaded
`ollama rm <model_name>` deletes the specified model from your downloads

Structured outputs:
`chat.completions.parse(model, messages, response_format)`

### LinkedIn
downloaded as pdf and had a summary. loaded pdf and summary into a system prompt. Initiated chat session with gradio. Asking about mysyelf. Then implemented up an optimizer evaluator to judge the response. this bot uses a structured output with a pydantic model

##### Lab 4 - Building your own alter ego... will include Tool use
- Make an acoount on pushover.net for the Push notifications

Tool use is just JSON and if statements - The tool description JSON describes the capability of being able to call an underlying function which has the code.
- This is why both tool desc and each inputs descs are needed in natural language. 
- This is the info thats sent to the model LLM saying to it that you have the ability to do this, so tell me if you want me to run it from you and I'll tell you the answer. 
- List of tools looks like the list of messages that go into model. 
- LLMs are good at understanding JSON coz its in a lot of their training data.
##### Tool Call Desmystified: 
Write a function that runs when the LLM decides to call a tool -> `handle_tool_calls(tool_calls):` extract JSON and check what name of tool call is and then call the function
## <span style="color:rgb(0, 176, 240)"> </span><span style="color:rgb(0, 176, 240)">Links</span>
- Anthropic - Building effective agents - https://www.anthropic.com/engineering/building-effective-agents
- Benchmarks: https://www.vellum.ai/llm-leaderboard


