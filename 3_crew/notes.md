## <span style="color:rgb(181, 76, 230)">Topics</span>:
Crew AI - Crew Agent framework
Serper - Google search API 

## <span style="color:rgb(0, 176, 240)">Setup</span> 

Install & Upgrade crew libs in uv environment:
`uv tool upgrade crewai`
`uv lock --upgrade`
`uv sync`

0. Install - `uv tool install crewai`
1. Create the project with: `crewai create crew my_project`
2. Fill in the config YAML files to define the Agents and Tasks
3. Complete the crew.py module to create the Agents, Tasks and Crew, referencing the config
4. Update main.py to set any inputs
5. Run with `crewai run`

## <span style="color:rgb(0, 176, 80)">Theory</span>
CrewAI Enterprise: A multi-agent platform for deploying running and monitoring Agentic AI
CrewAI UI Studio: A no-code / lo-code product for creating mult-agent solution
CrewAI open-source framework: Orchestrate high performance AI agents with ease and scale.
	<span style="color:rgb(0, 176, 80)">CrewAI Crews</span>: Autonomous solutions with AI Teams of agents with different roles
		You need autonomous problem-solving, creative collaborations, or exploratory tasks
		This will be out focus in this chapter
	CrewAI Flows: Structured autonomous automations by dividing complex tasks into precise workflows
		You require deterministic outcomes, autitibily, or precise control over execution

<span style="color:rgb(0, 176, 80)">Core Concepts</span>:
	More terminology, marginally more prescriptive
	Code or YAML Configuration 
- Agent: An autonomous unit, with an LLM - role, goal, backstory, memory, tools
- Task: A specific assignment to be carried out - description, expected output, agnet
- Crew: a team of Agents and Tasks - can be sequential or hierarchical

Tools - equipping agents with capabilities
Concept - Information passed from 1 task to another
<span style="color:rgb(0, 176, 80)">Memory</span> - This is a more prescriptive and opinionated feature of Crew. You can do this manually or use Crew's construct of memory
	Pro: You get up and running quickly and you can use all their code
	Con: There is a learning curve and it obscures some of the detail of how prompt engineering works behind the scenes
	Tradeoff for developers - you got ess visibility into it - harded to debug
1. Short Term Memory - Temp storage of recent interactions and outcomes using RAG with vector DBs
2. Long Term Memory - Preserve valuable insights and learnings, building knowledge over time in a SQL DB 
3. Entity Memory (similar to short term mem) - Info about people, places, and concepts encountered during tasks, facilitating deeper understanding and relationship mapping. Uses RAG for storing entity information.
Contextual Memory - umbrella term for Crew for ST, LT and E memory
User Memory - Stores user-specific info and preferences, enhancing personalization and user experience

Code Execution
The problem was to write a function to code a sequence math problem thats approximately pi

Traces: available just like OpenAI SDK: https://app.crewai.com/crewai_plus/ephemeral_trace_batches/eecf5266-c7e4-4878-ad19-d9074a8ad3f7?access_code=TRACE-2d010beeb1

Advanced CrewAI Techniques:

## <span style="color:rgb(255, 0, 0)">Quotes</span>


## <span style="color:rgb(255, 192, 0)">Dev</span> 

<span style="color:rgb(255, 192, 0)">Lab 1 - Debate</span>
CrewAI uses a simple LiteLLM under the hood to interface with almost any LLM, opposite of Langchain
It al comes together with a `crew.py` file with decorators: @CrewBase, @agent, @task, @crew

doesn't work in notebooks. Crew uses uv for project mgmt and config
`uv tool install crewai`
`crewai create crew debate` -> creates an entire directory structure (scaffolding). 
`crewai run`

Cadence: `process=Process.sequential` - the order is determined by the order of @task decorators in crew.py

<span style="color:rgb(255, 192, 0)">Lab 2 - Financial Researcher</span>
```
context:
- research_task #Makes it so that the output of the researchtask is an input of this task but a gormatted input doesn't need to be plugged into the template like {company}
  
from crewai_tools import SerperDevTool
@agent
def researcher(self) -> Agent:
return Agent(
config=self.agents_config['researcher'],
verbose=True,
tools=[SerperDevTool()]

)
```

<span style="color:rgb(255, 192, 0)">LAB 3 - Stock Picker</span>
1. Structured Outputs
	Required that tasks perform conforming to a particular JSON schema
	Implementing Pydantic outputs
2. Custom Tool
	Custom tool arms an agent with sending a message to me with pushover
	set pydantic object  and supply it as. a schema to the crewAI Tool
3. Hierarchical Process
	Pass in an Agent or an LLM that will take care of assigning tasks to agents 
```
	manager = Agent(
	config=self.agents_config['manager'],
	allow_delegation=True.   #Equivalent to handoffs
)
```
4. Memory
	`from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory, RAGStorage, LTMSQLiteStorage`
There were 3 files, db, vector stores created with the memory Libs but there wasn't any visibility in it.

<span style="color:rgb(255, 192, 0)">Lab 4 - Giving coding skills to an Agent</span>
	Note: docker agent worked in bash terminal, not zsh
You can have an agent that cna wriet code and eecute in a Docker container, look at results, interpret them and investigate results.
```
Agent(
	allow_code_execution=True,
	code_execution_mode="safe".     
	#This is where crew's framework magic can is really clutch
)
```

Traces: available just like OpenAI SDK: https://app.crewai.com/crewai_plus/ephemeral_trace_batches/eecf5266-c7e4-4878-ad19-d9074a8ad3f7?access_code=TRACE-2d010beeb1

<span style="color:rgb(255, 192, 0)">Lab 5 - Engineering Team</span>
- Engineering Lead
- Backend Engineer
- Frontend Engineer
- Test Engineer
```
uv add gradio
uv run app.py
```

<span style="color:rgb(255, 192, 0)">Challenge</span>:
Team builds a whole system piece by piece not just 1 module
Add structured outputs and dynamic creation of tasks
Creating and running a task object at run time is possible. so that agents can autonomously build a more dynamic system
	crewAI concept docs 
	you can specify a callback when you create a task, thats when you can potentially create a new task
	Completeing 1 task can dynamically call and create other tasks
	Task guardrails are there too
Tasks can have callback functions that are called subsequently when the task is complete 