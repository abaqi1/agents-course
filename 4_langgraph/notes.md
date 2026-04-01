## <span style="color:rgb(181, 76, 230)">Topics</span>:
Ecosystem:
- <span style="color:rgb(181, 76, 230)">Langchain</span> - Build your app with Langchain. chaining agents, prompt templates, memory, allows RAG, lcl - decorative language of langchain. a lot of scaffolding and templating around calling LLMs. allows you to abstract using tools. Glue code to build with many LLM apps. 
	Drawback:- by signing up you are signing up for a lot of glue code and abstractions. its also become extremely simple to contact open AI now. there is less need for some projects to sign p with a heavy FW
We recommend you use LangChain if you want to quickly build agents and autonomous applications. Use [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview), our low-level agent orchestration framework and runtime, when you have more advanced needs that require a combination of deterministic and agentic workflows, heavy customization, and carefully controlled latency.
- <span style="color:rgb(181, 76, 230)">Langraph</span> - A seperate offering independent of langchain. It is all about a platform that focuses of stability, reusability and visibility into agentic workflows, and organise everything into a scalable, repeatable and easily monitoring solutions. It imagines all workflows in the form of a tree. by thinking in this abstract way, they are able to build stability and resiliency. Includes langraph platform that helps deploy with scalability.
	Langraph - the product itself
	Langraph Stui - UI Tooling
	Langraph Platform - hosted solution for deploying\running agents at scale
- <span style="color:rgb(181, 76, 230)">Langsmith</span> - Langraph connects with langsmith but it is seperate. This is for monitoring
	Gives a full tracing system like open AI SDK tracing

## <span style="color:rgb(0, 176, 240)">Setup</span> 
1. Define the state
2. Start the Graph Builder
3. Create a Node
4. Create Edges
5. Compile teh Graph

Define Graph -> Super-Step executes at each invokation of the graph



## <span style="color:rgb(0, 176, 80)">Theory</span>
	Nodes do work
	Edges choose what to do next
1. State represents the current snapshot of graph
2. Nodes are python func that represent agent logic. They receive state as input, do something, and return updated State.
3. Edges are python functions that determine which Node to execute next based on State. they can be fixed or conditional

In Langraph an agent workflow is represented as a graph. State refers current snapshot of affairs. nodes decided how to go from one stage to another. edges decide what to do next.
The graph building\compilation (steps 1-5) happens before your agent starts

`State` is immutable. Node takes a state, runs logic, returns the new state object.
For each of teh fields in your state, you can specifu a speacial function called a `reducer`. Whenever you return a new State, Langraph use sthe reducer function to combine this field with the existing State. Why do we have to have a reducer instead of updating field ourselves? This enables Lnagraph to run multiple nodes cncurrently and combine State without overwritting\GIL issues.

`The Super-Step`
A super step can be considered a single iteration over the graph nodes Nodes that run in parallel are part of the same super-step, while nodes that run sequentially belong to seperate super-steps
- the graph describes one super-step; one interaction between agents and tools to achieve an outcome
- Everu user interaction is a fresh graph.invoke(state) call
- The reducer handles updating state during a super-step but not between super-step
	Checkpointing - Freeze record of the state at each super step
> A super-step can be considered a single iteration over the graph nodes. Nodes that run in parallel are part of the same super-step, while nodes that run sequentially belong to separate super-steps.
> The reducer handles state updates automatically within one super-step, but not between them. That is what checkpointing and memory achieves.

Memory
Every superset is a seperate invocation. each superset is a different invocation of the graph. Checkpointing is how you add memory.
`MemorySaver`: Saves stuff to in memory store
	pass in checkpointer=MemorySaver when compiling the graph
Lanchain gives you info on every superStep and memry allows you to back in tiem and restart in a snapshot of memory and state at any time
Persistent Memory - can be stored in SQL
`SqliteSaver` instead of MemorySaver

LangGraph gives you tools to set the state back to a prior point in time, to branch off:
```
config = {"configurable": {"thread_id": "1", "checkpoint_id": ...}}
graph.invoke(None, config=config)
```
And this allows you to build stable systems that can be recovered and rerun from any prior checkpoint.

Playwrite allows you to launch the browser. langchain tools allow us to wrap over actions that can be done on the browser.
	Armed the agent to drive a browser, do work for you, text you with another tool.
## <span style="color:rgb(255, 0, 0)">Quotes</span>


## <span style="color:rgb(255, 192, 0)">Dev</span> 

LAB - 1
Langraph has you `anotations` to python type hints. This is used to specify reducers.
State objects most commonly are a pydontic object, a typed dict, or anything else.
Edges: START -> Node -> END

LAB - 2
You can wrap a function with a Tool Object
Easy to bund tools to the LLM. Ease of use but flip side is that implementation details are hidden from us
chatbot is added as a node
Tools are also added as a node
	WebSearch Tool: `from langchain_community.utilities import GoogleSerperAPIWrapper`
	Invoke Tool: `tool_search.invoke("What is the capital of France?")`
Edges: Chatbox -> Tools `add_conditional_edge()` (conditional edge based on finish reason)
You also need to make an edge from the tool back to the chatbot
``` Open AI specific lanchain construct
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)
```
Memory
```
# In memory Storage
from langgraph.checkpoint.memory import MemorySaver
graph_builder.compile(checkpointer=memory)

# Persistant Storage
from langgraph.checkpoint.sqlite import SqliteSaver
db_path = "memory.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
sql_memory = SqliteSaver(conn)
graph = graph_builder.compile(checkpointer=sql_memory)
```

LAB - 3
Asynchronous LanGraph
`uv run python -m playwright install`
prompt: Open wired.com and senf me a notification with some of teh latest news
=> Graph workflow, langchain playwright tools, custom text tool, -> opened browser and sent me teh message

LAB - 4 -> SideKick
Complex State, not just messages
If there is a reducer attached to a state var, that will get accumulated (add_messages). but other vars that have no reducer will be come overwritten (other state vars)
```
class State(TypedDict):
	messages: Annotated[List[Any], add_messages]
	success_criteria: str
	feedback_on_work: Optional[str]
	success_criteria_met: bool
	user_input_needed: bool
```
`worker_router` -> routes the control between tools or evaluator

LAB - 5
Side Kick
Search the Web
Control the browser
Send Notifications
Use the file System - `from langchain_community.agent_toolkits import FileManagementToolkit`
Wikipedia
Run Python code  `from langchain_experimental.tools import PythonREPLTool`

```
uv run app.py
```
## <span style="color:rgb(0, 176, 240)"> </span><span style="color:rgb(0, 176, 240)">Links</span>

Lamgsmith Tracing: https://smith.langchain.com/o/05bca053-ef0f-445b-b44d-e19933108349/projects/p/ffdcba08-7c91-4e03-86c6-7404ec9b5bc0?timeModel=%7B%22duration%22%3A%227d%22%7D