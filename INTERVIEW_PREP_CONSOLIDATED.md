# Agentic AI - Consolidated Interview Prep Sheet

**Quick Reference Guide for Senior Software Engineer Interviews**  
*5 Frameworks | 5 Production Projects | Real-World Experience*

---

## 🎯 30-Second Executive Summary

"I'm a Senior Software Engineer at Bloomberg with 8 total YEO and 2 years of experience building production-grade AI systems. I've architected agentic applications from scratch and used industry frameworks like OpenAI SDK, CrewAI, LangGraph, and MCP to build autonomous multi-agent systems. My experience spans RAG pipelines, multi-agent orchestration, tool integration, and production deployment - from Text2BDD (test generation for 60+ teams) to autonomous trading floors with real-time market data."

---

## 1️⃣ FOUNDATIONS - Building Agentic AI from Scratch

### 🎤 Elevator Pitch
*"I built an AI clone of myself embedded in my personal website (araiz.pro) that captures leads 24/7, answers questions about my background, and sends me real-time SMS notifications when recruiters express interest - all built from scratch using direct OpenAI API calls to deeply understand tool calling mechanics."*

### 🧠 Core Concepts

**Agentic AI Definition**: Programs where LLM outputs control the workflow - characterized by multiple LLM calls, tool use, environment interaction, and autonomy.

**Tool Calling Demystified**: Tools are "glorified if statements" - JSON schemas describe capabilities, LLM decides when to call, and `handle_tool_calls()` routes to appropriate functions. The magic is in clear natural language descriptions.

**Agentic Workflows vs. Agents**:
- **Workflows**: Predefined orchestration (prompt chaining, routing, parallelization, orchestrator-worker, evaluator-optimizer)
- **Agents**: LLMs dynamically direct their own processes with open-ended execution and feedback loops

**Context Engineering > Prompt Engineering**: 
- Prompt Engineering = what to say at a moment in time
- Context Engineering = what the model knows when you say it
- Quality of context matters more than prompt complexity for scaling

**Resources vs. Tools**:
- **Resources**: Provide information to improve LLM expertise (RAG, knowledge bases)
- **Tools**: Give LLM power to carry out actions (API calls, database queries)

### 🚀 Project: Professional Alter Ego Chatbot (www.araiz.pro)

**Problem**: Need 24/7 engagement with recruiters/employers while maintaining professional presence and capturing leads.

**Architecture**:
- **Context Engineering**: LinkedIn profile (PyPDF extraction) + comprehensive career summary loaded into system prompt
- **Tool-Enabled Agent**: 
  - `record_user_details()` - Captures email/name/notes when users express interest
  - `record_unknown_question()` - Logs unanswerable questions for follow-up
  - Both tools send real-time SMS via Pushover API
- **Gradio Chat Interface**: Embedded into personal website with example questions and resume download

**Key Implementation**: Chat loop with tool support - continue calling LLM until `finish_reason != "tool_calls"`, handle tool results, append to message history, repeat.

**Outcome**: Production-ready lead capture system with real-time notifications enabling immediate follow-up with interested parties.

**Tech Stack**: Python, OpenAI API (GPT-4o-mini), Pushover API, Gradio, PyPDF

### 💡 Key Takeaways
- Tool calls are JSON + if statements under the hood - understanding this enables building without frameworks
- Context engineering (what fills the window) is how we scale to thousands of high-quality outputs
- Bias the model through repetition in system prompts to increase probability of desired behavior
- Real-world integration via tools enables agents to interact with external systems (APIs, notifications, databases)

### 🔗 Connection to Bloomberg Work
This foundation enabled building **Text2BDD** - architecting agentic test case generators that synthesize BDD scenarios using RAG pipelines and repository embeddings. Understanding tool calling from scratch was critical for building the evaluator-optimizer pattern where one LLM generates test cases and another validates them against repository constraints.

---

## 2️⃣ OPENAI SDK - Production-Ready Agent Framework

### 🎤 Elevator Pitch
*"I built a Weekly Research Digest system using OpenAI Agents SDK that autonomously researches software engineering and medical news every Monday, executes parallel web searches, synthesizes 5-10 page reports, and delivers via email and SMS - demonstrating production-ready multi-agent orchestration with structured outputs and built-in tracing."*

### 🧠 Core Concepts

**Agents as First-Class Citizens**: Lightweight wrappers around LLMs with instructions, tools, and model config. Simple API: `Agent(name, instructions, model, tools, output_type)`. Agents can be converted to tools via `agent.as_tool()` for composability.

**Tools Made Simple**: `@function_tool` decorator automatically converts Python functions to tools - no JSON boilerplate needed.

**Structured Outputs**: Pydantic models define output schemas for type-safe agent responses: `result.final_output_as(MyPydanticModel)`. Automatic JSON validation eliminates parsing errors.

**Handoffs - The Key Differentiator**: Specialized mechanism for agent-to-agent control transfer where control passes **across** (delegation) vs. tools where control passes **back** (function calls). Agent defines `handoffs=[other_agent]` and target needs `handoff_description`.

**Guardrails**: Input/output validation using `@input_guardrail` and `@output_guardrail` decorators. Guardrails can themselves be agents for sophisticated validation. Returns `GuardrailFunctionOutput` with `tripwire_triggered` flag.

**Tracing - Critical for Production**: `trace()` context manager provides comprehensive debugging with full visibility into agent reasoning, tool calls, handoffs, and token usage. View traces at `platform.openai.com/traces`. Essential for complex multi-agent systems.

**Async Python**: Built on async/await for I/O-bound operations. `asyncio.gather()` enables parallel agent execution - lightweight alternative to threading.

### 🚀 Project: Weekly Research Digest Agent

**Problem**: Stay current in software engineering and medicine without manual weekly research.

**Multi-Agent Architecture**:
1. **Planner Agent** - Analyzes query, creates structured search plan (5 targeted searches) using Pydantic `WebSearchPlan`
2. **Search Agent** - Executes parallel web searches using OpenAI's `WebSearchTool`, summarizes results
3. **Writer Agent** - Synthesizes findings into 5-10 page markdown reports with structured `ReportData` output
4. **Email Agent** - Formats report as HTML and sends via SendGrid (can be invoked via handoff or orchestration)
5. **Notification Agent** - Sends SMS alerts via Pushover API

**Agent Collaboration Patterns**:
- **Orchestration Pattern** (current): ResearchManager orchestrates sequential agent calls
- **Handoff Pattern** (demonstrated): Writer Agent can hand off to Email Agent for formatting/delivery
- Handoffs enable true agent autonomy vs. tools which are function calls

**Key Technical Decisions**:
- Async Python for parallel search execution using `asyncio.create_task()`
- Structured outputs (Pydantic) ensure type safety between agents
- Shared model instance across agents for consistency
- Tracing provides observability for debugging multi-agent workflows

**Use Cases**: 
- Weekly automation: Software engineering/AI news every Monday
- Medical news digest for physician spouse
- Delivery via email (formatted HTML) and SMS (brief summary)

**Outcome**: Production system delivering personalized research digests, demonstrating real-world agentic patterns with cost-effective model usage (GPT-4o-mini).

**Tech Stack**: Python, OpenAI Agents SDK, GPT-4o-mini, WebSearchTool, SendGrid, Pushover, Pydantic, AsyncIO

### 💡 Key Takeaways
- Agent composition (breaking complex tasks into specialized agents) improves reliability and maintainability
- Handoffs vs. Tools: Use handoffs when control should pass across (delegation), tools when control returns (function calls)
- Structured outputs eliminate parsing errors and provide type safety for agent communication
- Async patterns significantly reduce latency for I/O-bound operations (parallel searches)
- Tracing is essential for debugging - tracks entire execution path across agents, handoffs, and tool calls
- Model flexibility: Easy to swap providers via OpenAI-compatible APIs (DeepSeek, Gemini, Groq)

### 🔗 Connection to Bloomberg Work
The orchestration patterns learned here directly apply to **ONCL Buddy** - where multiple agents handle different aspects of failure analysis: one queries LIGO historical data, another fetches current logs, and a third synthesizes root-cause assessment. The structured outputs ensure consistent failure classification across triage workflows, reducing on-call engineer response time.

---

## 3️⃣ CREWAI - Multi-Agent Team Orchestration

### 🎤 Elevator Pitch
*"I built a crypto trading platform powered by two AI crews: one that autonomously researches trending cryptocurrencies and makes investment decisions, and another that designs, codes, and tests the full-stack trading application - demonstrating hierarchical and sequential multi-agent workflows with memory systems and code execution in Docker containers."*

### 🧠 Core Concepts

**Agents - Specialized Team Members**: Autonomous units with LLM, role, goal, backstory, memory, and tools. Defined via YAML config or Python `@agent` decorator. Agents can have different LLMs (GPT-4o for managers, GPT-4o-mini for workers).

**Tasks - Specific Assignments**: Defined assignments with description, expected output, and assigned agent. Tasks reference outputs from other tasks via `context` parameter. Output can be structured (Pydantic) or unstructured (markdown/text).

**Crews - Team Orchestration**: Teams of agents/tasks working together.
- **Sequential Process**: Tasks execute in order (determined by `@task` decorator order)
- **Hierarchical Process**: Manager agent delegates tasks to specialized agents dynamically

**Tools - Extending Capabilities**: Built-in tools (SerperDevTool, FileReadTool) and custom tools via `BaseTool` class with Pydantic schemas. Tools enable real-world system interaction.

**Structured Outputs**: Pydantic models define output schemas for tasks - ensures consistent, validated outputs critical for downstream processing.

**Memory Systems - The Differentiator**:
- **Short-Term Memory**: RAG-based vector storage for recent interactions
- **Long-Term Memory**: SQLite storage for persistent learnings
- **Entity Memory**: RAG-based storage for people, places, concepts
- **User Memory**: User-specific preferences
- Enables agents to learn and improve over time

**Code Execution**: Agents write, execute, and test code in isolated Docker containers (`allow_code_execution=True`, `code_execution_mode="safe"`). Agents iterate on code, see results, and fix issues autonomously.

**Hierarchical Process**: Manager agent (powerful LLM) coordinates team, delegates tasks dynamically based on context (`allow_delegation=True`).

**Project Structure**: `@CrewBase` class decorator with `@agent`, `@task`, `@crew` decorators auto-collecting components. YAML files define configs - clean separation of config and logic.

**Context Passing**: Tasks automatically receive outputs from previous tasks via `context` parameter - no manual formatting needed.

### 🚀 Project: Crypto Trading Platform with Multi-Agent Crew

**Problem**: Build a personal crypto trading platform that autonomously researches opportunities AND builds the full-stack application to manage trading.

**Multi-Crew System**:

**Crew 1: Crypto Research & Selection (Hierarchical)**
1. **Trending Crypto Finder** - Searches news (SerperDevTool), identifies 2-3 trending cryptocurrencies
2. **Crypto Researcher** - Provides analysis (market position, technical analysis, outlook)
3. **Crypto Picker** - Selects best opportunity, sends push notification (custom PushNotificationTool)
4. **Manager Agent** - Coordinates research workflow, delegates dynamically

**Crew 2: Engineering Team (Sequential)**
1. **Engineering Lead** - Designs backend architecture for account management (GPT-4o)
2. **Backend Engineer** - Implements Python backend with Binance API integration, executes code in Docker
3. **Frontend Engineer** - Builds Gradio UI for transactions, deposits, withdrawals, portfolio
4. **Test Engineer** - Writes comprehensive unit tests, executes in Docker

**Key Technical Decisions**:
- Structured outputs (Pydantic) for type-safe data flow between crews
- Memory systems: Long-term prevents duplicate picks, entity tracks crypto metadata
- Custom tools: Binance API integration for real-time prices and trading
- Code execution: Docker-based verification before delivery
- Hierarchical (research) vs. Sequential (engineering) for different workflow needs
- Context passing: Frontend receives backend code, tests receive both backend and frontend

**Custom Binance API Tool**: `BaseTool` implementation fetching real-time prices and executing trades.

**System Workflow**:
1. Research crew identifies and selects trending crypto
2. Engineering crew designs and builds full-stack platform (backend + frontend + tests)
3. Python backend server runs locally, Gradio UI provides web interface
4. Integration with Binance API for real-time data and order execution

**Outcome**: End-to-end autonomous system that researches opportunities AND builds the infrastructure to act on them - demonstrating how multi-crew systems handle complex workflows from research to deployment.

**Tech Stack**: Python, CrewAI, GPT-4o/GPT-4o-mini/Claude Sonnet, SerperDevTool, Binance API, Gradio, Docker, SQLite, Pydantic, uv package management

### 💡 Key Takeaways
- Crew composition: Combining multiple crews enables end-to-end solutions (research → development → deployment)
- Memory for state: Long-term memory prevents duplicates, entity memory tracks context over time
- Structured outputs ensure consistent data flow between research and engineering crews
- Hierarchical vs. Sequential: Use hierarchical for dynamic decision-making, sequential for deterministic workflows
- Code execution enables agents to verify their code works before delivery
- Custom tools demonstrate real-world integration with external services
- Context passing eliminates manual data formatting between tasks
- Multi-model strategy: Powerful models (GPT-4o) for managers/leads, efficient models (GPT-4o-mini) for workers

### 🔗 Connection to Bloomberg Work
The multi-agent orchestration patterns here directly apply to **LIGO Test Observability Platform** development - where different agents could handle data collection (backend integration agent), visualization (frontend component agent), and analysis (metrics calculation agent). The hierarchical pattern is similar to how I coordinate cross-team strategy alignment - a manager agent delegates specialized tasks to domain experts, just like coordinating 60+ engineering teams using centralized automation frameworks.

---

## 4️⃣ LANGGRAPH - State Machine Orchestration

### 🎤 Elevator Pitch
*"I built Sidekick - an autonomous multi-agent system with worker-evaluator pattern that serves as my testing ground for evaluating AI frameworks, tools, and MCP servers. It implements checkpointing for crash recovery, async execution for browser automation, and integrates 10+ tools including Playwright, code execution, and file management - all orchestrated via LangGraph's state machine architecture."*

### 🧠 Core Concepts

**LangGraph - State Machine Framework**: Low-level agent orchestration modeling workflows as state machines (graphs). Independent from LangChain, provides production-ready control flow.

**State Management**:
- State is a typed dict/Pydantic model representing current snapshot
- **Reducers**: Functions that merge new state with existing state (enables concurrent node execution)
- Example: `add_messages` reducer appends to message list without overwriting
- Critical for safe parallel execution

**Nodes (The Workers)**: Python functions containing agent logic - receive current state, perform work, return updated state. Can be LLM calls, tool invocations, or business logic.

**Edges (The Routers)**: Determine next node based on state.
- **Fixed edges**: Always go to same node
- **Conditional edges**: Route based on logic (e.g., tool calls vs final answer)

**The Super-Step (Execution Model)**: 
- One super-step = one complete graph traversal (one user interaction)
- Each `graph.invoke()` is a fresh super-step
- Nodes running in parallel = same super-step
- Nodes running sequentially = separate super-steps

**Checkpointing & Memory - Production Critical**:
- Reducers handle state within super-step
- Checkpointing handles state *between* super-steps
- **MemorySaver**: In-memory storage (dev/testing)
- **SqliteSaver**: Persistent storage (production)
- **Time-travel**: Can rewind to any checkpoint and branch off for debugging

**Why LangGraph Over Raw OpenAI API**:
- Built-in state management and memory
- Concurrent node execution with safe state merging (reducers)
- Checkpoint-based debugging and recovery
- Visual graph representation (Mermaid diagrams)
- Production-ready persistence and error handling

**LangSmith - Observability**: Full trace visualization of every LLM call, tool invocation, and state transition. Token usage and latency tracking. Critical for debugging production issues.

### 🚀 Project: Sidekick - Autonomous Multi-Agent Testing Ground

**What It Is**: Autonomous system that:
1. Takes user request + success criteria
2. Uses 10+ tools to complete task
3. Self-evaluates work quality
4. Iterates until success or needs human input
5. Maintains conversation memory across sessions

**Architecture Highlights**:

**Multi-Agent Pattern: Worker-Evaluator**
- **Worker Agent**: Task execution with tool access (browser, code, files, search)
- **Evaluator Agent**: Quality assessment using structured outputs (Pydantic validation)
- **Feedback Loop**: Worker receives evaluator feedback and re-attempts if needed

**Advanced State Management**:
```
State = {
    messages: Annotated[List[Any], add_messages],  # Accumulates (reducer)
    success_criteria: str,                         # Overwrites
    feedback_on_work: Optional[str],               # Overwrites
    success_criteria_met: bool,                    # Overwrites
    user_input_needed: bool                        # Overwrites
}
```
- Messages accumulate for conversation history
- Other fields overwrite for latest state
- Enables concurrent execution without race conditions

**Async Execution**: 
- Fully async architecture using `asyncio`
- `graph.ainvoke()` for non-blocking execution
- `nest_asyncio` handles nested event loops (Playwright + Gradio)
- Tool execution: `await tool.arun()` for non-blocking I/O

**Structured Outputs (Type Safety)**: `EvaluatorOutput` Pydantic model with feedback, success criteria met flag, and user input needed flag - guaranteed JSON schema compliance.

**Tool Integration (10+ Tools)**:
1. Browser Automation (Playwright) - navigate, extract text, click elements
2. Web Search (Google Serper API) - real-time information
3. Knowledge Base (Wikipedia API) - structured knowledge
4. Code Execution (PythonREPLTool) - dynamic Python in sandbox
5. File Management - read, write, list, copy files
6. Notifications (Pushover API) - alert on completion

**Conditional Routing**:
- Worker → Tools (if tool calls) → Worker → Evaluator → (Worker if failed) → END
- Routes based on state: tool calls presence, success criteria met, user input needed

**Use Cases**:
- Autonomous web research (navigate sites, extract content, notify)
- Code generation and execution (write Python, run, return results)
- Data analysis workflows (web search → research → file creation)
- Development assistant (find docs, summarize, explain)
- MCP Server integration testing
- Framework comparison experiments

**Outcome**: Production-grade testing ground for evaluating new frameworks, tools, and MCP servers with comprehensive observability and error recovery.

**Tech Stack**: Python, LangGraph, LangChain, OpenAI GPT-4o-mini, Playwright, SQLite, Gradio, Pydantic, AsyncIO, LangSmith

### 💡 Key Takeaways
- State machines > linear chains for complex agent workflows
- Reducers enable safe concurrent execution without race conditions
- Checkpointing is essential for production (crash recovery, debugging, branching)
- Structured outputs eliminate JSON parsing errors
- Async architecture required for browser automation + real-time UIs
- LangGraph provides production-readiness that raw LLM APIs don't
- Time-travel debugging enables rewinding to any checkpoint and trying alternate paths

### 🔗 Connection to Bloomberg Work
The state machine orchestration and checkpointing patterns directly apply to **PXC Environment Provisioning System** - where different stages (validation → resource allocation → deployment → verification) need to be tracked, and failures require rewinding to previous checkpoints. The worker-evaluator pattern is similar to **ONCL Buddy's** architecture: one agent analyzes failures, another evaluates root cause, and feedback loops enable iterative refinement of triage assessments. The observability provided by LangSmith mirrors the observability systems I built in **LIGO Test Observability Platform** - full visibility into execution history, metrics, and system behavior.

---

## 5️⃣ MCP (MODEL CONTEXT PROTOCOL) - The USB-C of AI

### 🎤 Elevator Pitch
*"I built a real-time autonomous trading floor with 4 AI traders using the Model Context Protocol ecosystem, integrating 6+ MCP servers providing 44 tools, real-time market data via Polygon.io, and a shared knowledge graph memory. Each trader has distinct investment strategies and autonomously researches, trades, and evolves their strategies over time - demonstrating MCP as the standardized way to build reusable, composable AI tools."*

### 🧠 Core Concepts

**What is MCP?**: Model Context Protocol standardizes tool integration - build once, use everywhere. Before MCP, every framework had custom tool formats. MCP is the "USB-C of AI."

**Three Components**:
1. **MCP Host**: Your LLM application (agent, Claude Desktop)
2. **MCP Client**: Spawns/connects to servers, manages lifecycle, translates tools to LLM format (1:1 with server)
3. **MCP Server**: Exposes tools (functions), resources (context), prompts (templates)

**Three MCP Server Configurations**:
1. **Local Server, Local Operations** (e.g., filesystem) - no external APIs
2. **Local Server, Remote API** ⭐ Most Common (e.g., Brave Search, Polygon.io) - server runs locally, makes API calls
3. **Remote Managed Server** (e.g., enterprise services) - server runs remotely, connect via SSE

**Why Use MCP**:
- ✅ Build once, use everywhere (works in Claude Desktop, OpenAI Agents, custom apps)
- ✅ Ecosystem: 100+ community MCP servers
- ✅ Consistency: Standardized tool incorporation across agents
- ✅ Security: Same trust model as `pip install` - vet code, run locally
- ✅ Composability: Mix and match servers for different capabilities

**When NOT to Use MCP**:
- ❌ Internal-only tools (just use native decorators)
- ❌ Simple projects (adds complexity)
- ❌ Rapid prototyping (faster to write inline functions)

**Rule of Thumb**: Use MCP when building reusable tools for multiple agents/applications.

**MCP Primitives**:
- **Tools**: Functions LLM can call (actions with side effects)
- **Resources**: Context injected into prompts ⭐ Often overlooked (static/dynamic data)
- **Prompts**: Reusable prompt templates

**Communication Protocols**:
- **stdio (Standard Input/Output)**: Most common - client spawns server as subprocess, communication via stdin/stdout (JSON-RPC)
- **SSE (Server-Sent Events)**: Rare - remote managed services (enterprise APIs)

### 🚀 Project: Autonomous Trading Floor with 4 AI Traders

**Problem**: Build a system that autonomously researches crypto opportunities, makes trading decisions, and evolves strategies over time while sharing collective intelligence.

**The Four Traders**:
| Name | Strategy | Personality | Model |
|------|----------|-------------|-------|
| Warren | Value investing | Patient | GPT-4o-mini |
| George | Momentum trading | Aggressive | DeepSeek V3 |
| Ray | Systematic diversification | Risk-averse | Gemini 2.5 Flash |
| Cathie | Growth/crypto ETFs | Innovation | Grok 3 Mini |

**Key Feature**: Each trader can autonomously **change their own strategy** based on performance.

**Architecture Highlights**:

**1. Nested Agent Pattern**:
- Trader agent wraps Researcher agent as a tool
- Researcher has different MCP servers (web search, memory)
- Trader has different MCP servers (accounts, market data)
- Clean separation: research vs. trading concerns
- Researcher reused by all 4 traders

**2. MCP Resources (Not Just Tools!)**:
- Strategy loaded as MCP resource (dynamically injected into prompts)
- Account state exposed as resource (pre-loaded context vs. LLM asking for it)
- Resources reduce tool calls - data is pre-loaded vs. requested

**3. Shared Knowledge Graph Memory**:
- Each trader has separate database but shares entities (e.g., "AAPL", "Tesla")
- Warren researches Apple → stores entity with observations
- George queries memory → retrieves Warren's research
- Collective intelligence builds over time
- Tools: `create_entities()`, `create_relations()`, `read_graph()`, `search_nodes()`, `open_nodes()`

**4. Custom MCP Server Implementation**:
- Writing MCP server is trivial - wrap existing code with decorators
- `accounts_server.py`: Exposes account resources and buy/sell tools
- `push_server.py`: Send notifications via Pushover
- `market_server.py`: Fallback for free-tier market data
- Run with: `uv run accounts_server.py`

**5. Async MCP Server Lifecycle**:
- `AsyncExitStack` manages multiple MCP server lifecycles
- Ensures cleanup even on exceptions
- Handles stdio process spawning/termination
- Timeout management for hanging servers

**6. Multi-Model Architecture**:
- Each trader uses different LLM provider (OpenAI, DeepSeek, Gemini, xAI)
- Compare model performance on same task (trading execution)

**7. Custom Tracing System**:
- Built custom `TraceProcessor` to log agent events to SQLite for UI display
- Real-time execution visibility in Gradio with color-coded events

**8. Trading Workflow (Alternating Pattern)**:
- **Trade Mode** (odd iterations): Research opportunities, execute new trades
- **Rebalance Mode** (even iterations): Review portfolio, rebalance, evolve strategy
- Separates exploration (new opportunities) from exploitation (optimization)

**MCP Servers Integrated**:

**Trader MCP Servers (3)**:
1. Accounts MCP (custom) - Resources: account state, strategy; Tools: buy/sell shares
2. Push Notification MCP (custom) - Tools: send_notification()
3. Market Data MCP (Polygon.io OR custom) - Tools: get prices, technicals, fundamentals

**Researcher MCP Servers (3)**:
1. Fetch MCP (mcp-server-fetch) - Headless browser for web scraping
2. Brave Search MCP (@modelcontextprotocol/server-brave) - Web search
3. Memory MCP (mcp-memory-libsql) - Knowledge graph with entities, observations, relations

**Trading Floor Scheduler**:
- Async event loop running every 60 minutes
- Market hours awareness (skip when closed)
- Concurrent execution: All 4 traders run in parallel (`asyncio.gather()`)
- Reduces total execution time (4x faster)

**Real-World Capabilities**:
- Integrates real-time market data (Polygon.io API)
- Manages SQLite portfolios with transaction history
- Sends push notifications on trade execution
- Displays live dashboards with portfolio performance (Gradio + Plotly)
- Runs continuously on 60-minute intervals

**Outcome**: Production-grade autonomous trading simulation with 44 total tools, real-time data, shared memory, and multi-model support - demonstrating MCP as the standard for reusable tool integration.

**Tech Stack**: Python, MCP, OpenAI Agents SDK, GPT-4o-mini/DeepSeek/Gemini/Grok, Polygon.io, Brave Search, LibSQL Memory, SQLite, Gradio, Pydantic, AsyncIO, Pushover

### 💡 Key Takeaways
- **MCP standardizes tool integration** - the "USB-C of AI"
- **Resources are underutilized** - powerful for dynamic context injection, reduce tool calls
- **Nested agents > monolithic agents** - better tool scoping (5 tools vs. 15), clearer prompts, reusability
- **Knowledge graphs enable collective intelligence** - shared memory across agents, persistent learning
- **Autonomy needs guardrails** - balance freedom with coherence (soft constraints in prompts)
- **Async lifecycle management is critical** - proper cleanup prevents resource leaks
- **Custom MCP servers are trivial** - wrap existing code with decorators
- **Tool descriptions are first-class** - LLM quality depends on clear, specific descriptions

### 🔗 Connection to Bloomberg Work
The standardized tool integration approach is similar to how I built **centralized automation frameworks** used by 60+ teams - shared step repositories enable consistent, scalable BDD automation. The knowledge graph memory pattern mirrors **Text2BDD's** approach: embedding all steps, scenarios, and examples into vector databases for semantic search, enabling collective intelligence across teams. The multi-agent coordination with shared memory is analogous to how **LIGO Test Observability Platform** aggregates execution data from 60+ teams into a centralized system for cross-team insights. The async lifecycle management patterns apply directly to managing Jenkins Pipeline jobs feeding Kafka Queues for test execution monitoring.

---

## 🎯 Cross-Cutting Themes & Interview Soundbites

### **When to Use Each Framework**

| Framework | Best For | Trade-offs |
|-----------|----------|-----------|
| **Raw OpenAI API** | Deep understanding, lightweight apps, custom workflows | Manual state management, no built-in observability |
| **OpenAI SDK** | Production agents, structured outputs, multi-agent handoffs | Requires understanding of SDK abstractions |
| **CrewAI** | Multi-agent teams, memory systems, code execution | Less visibility into prompts, framework conventions |
| **LangGraph** | Complex state machines, checkpointing, concurrent execution | Steeper learning curve, more boilerplate |
| **MCP** | Reusable tools across frameworks, standardized integration | Adds complexity for simple use cases |

### **Production Patterns I've Implemented**

1. **Worker-Evaluator Pattern**: Agent generates output, evaluator validates, feedback loop enables iteration (Sidekick, ONCL Buddy)
2. **Nested Agents**: Outer agent delegates to specialized inner agents as tools (Trading Floor, Text2BDD)
3. **Structured Outputs**: Pydantic models ensure type-safe LLM communication (all projects)
4. **Checkpointing**: State persistence for crash recovery and debugging (Sidekick, LIGO)
5. **Async Orchestration**: Parallel execution for I/O-bound operations (Research Digest, Trading Floor)
6. **Memory Systems**: Short-term (RAG), long-term (SQLite), knowledge graphs (Trading Floor, Text2BDD)
7. **Context Engineering**: Dynamic prompt injection with success criteria, temporal context, feedback (all projects)
8. **Multi-Model Architecture**: Easy model swapping for cost optimization and comparison (Trading Floor, Research Digest)

### **Tech Stack Expertise**

**Languages**: Python (primary), TypeScript, JavaScript

**AI/ML**: OpenAI, DeepSeek, Claude, Gemini, Grok, Ollama

**Frameworks**: OpenAI SDK, CrewAI, LangChain/LangGraph/LangSmith, HuggingFace

**Tools & Infrastructure**: MCP Servers, Pydantic, AsyncIO, Docker, Gradio, Playwright, Selenium

**APIs & Services**: Polygon.io, Brave Search, Pushover, SendGrid, Wikipedia, Google Serper

**Data & Memory**: FAISS, Chroma, SQLite, PostgreSQL, RAG pipelines, vector embeddings

**Web**: React, Next.js, Redux

**DevOps**: Jenkins, Kafka, Docker, CI/CD pipelines

### **Key Differentiators**

1. **Production Experience**: Not just tutorials - built systems serving 60+ teams at Bloomberg (Text2BDD, ONCL Buddy, LIGO)
2. **Framework Fluency**: Deep experience across 5+ frameworks - can choose right tool for the job
3. **Foundational Understanding**: Built from scratch before using frameworks - understand abstractions vs. treating as magic
4. **Real-World Integration**: Experience with APIs, databases, async execution, error handling, observability
5. **Multi-Agent Orchestration**: Implemented worker-evaluator, hierarchical, sequential, and nested agent patterns
6. **Standardization Advocate**: Used MCP to build reusable tools, similar to centralized automation frameworks at Bloomberg

### **Interview Conversation Starters**

- "At Bloomberg, I architected Text2BDD - an agentic test case generator serving 60+ teams. Would you like to hear about the RAG pipeline design or the evaluator-optimizer pattern?"
- "I've built autonomous systems from scratch and with 4+ frameworks. Let me walk you through the trade-offs I've learned."
- "My trading floor project integrates 44 tools via MCP - the standardized way to build reusable AI components. It's like how I built centralized automation frameworks at Bloomberg."
- "I have a US patent for an anomaly detection system using ensemble ML models for test log analysis. The foundation of that work now powers my agentic systems."
- "I believe in shifting testing to the left - building quality into the SDLC. That philosophy drives how I architect agentic systems with evaluator agents and structured outputs."

---

## 📈 Quantifiable Impact

**Bloomberg (2022-Present)**:
- Built tools serving **60+ engineering teams** across AIM/TOMS/PORT
- Architected **Text2BDD** enabling teams to expand automation coverage without manual step writing
- Created **ONCL Buddy** reducing on-call triage time through intelligent failure analysis
- Contributed to **LIGO Test Observability Platform** used enterprise-wide for execution history and metrics

**Dell (2017-2022)**:
- **US Patent US11513927B1** for ML-powered log analysis system
- Built embedding-based anomaly detection for test failure remediation
- Automated functional test suites across Python, Java, JavaScript
- Created data visualization dashboards with Pandas, NumPy, Matplotlib, Plotly

**Personal Projects (2024-2026)**:
- **5 production-grade agentic applications** (Alter Ego, Research Digest, Trading Floor, Sidekick, Crypto Platform)
- Integrated **6+ MCP servers** with **44 total tools**
- Implemented **4 multi-agent patterns** (worker-evaluator, nested, hierarchical, sequential)
- Deployed systems with **real-time market data, push notifications, email delivery**

---

## 🚀 What's Next

**Immediate Goals**:
- Scale Sidekick to LangGraph Cloud for multi-user support
- Add more MCP servers (database, email, calendar) to Trading Floor
- Implement evaluation metrics (success rate, token efficiency) across projects
- Build domain-specific variants (code reviewer agent, research assistant agent)

**Career Goals**:
- Bring production-grade agentic AI systems to new organization
- Push boundaries of AI-powered automation and developer tooling
- Lead development of intelligent testing, triage, and quality assurance tools
- Continue shifting testing to the left with BDD and agentic systems

---

**Last Updated**: February 2026  
**Contact**: www.araiz.pro (with embedded AI alter ego!)  
**Location**: Chicago, IL (Hybrid/Remote)  
**Immigration Status**: US Permanent Resident (Green Card) - No sponsorship required
