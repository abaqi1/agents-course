# Model Context Protocol (MCP) - Interview Prep Sheet

## 🎯 Executive Summary (30-Second Pitch)

I built a **real-time autonomous trading floor** with 4 AI agents to experiment with the Model Context Protocol (MCP) ecosystem. The system integrates 6+ MCP servers providing 44 tools, real-time market data via Polygon.io, and a shared knowledge graph memory across agents. Each trader has distinct investment strategies (value, momentum, systematic, growth) and autonomously researches, trades, and rebalances portfolios while evolving their strategies over time.

---

## 📊 Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│                    TRADING FLOOR SYSTEM                        │
│                  (4 Autonomous AI Traders)                     │
└────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┬────────────┐
        │                     │                     │            │
        ▼                     ▼                     ▼            ▼
   ┌─────────┐          ┌─────────┐          ┌─────────┐  ┌─────────┐
   │ WARREN  │          │ GEORGE  │          │   RAY   │  │ CATHIE  │
   │(Patient)│          │ (Bold)  │          │(Systemic)│  │(Crypto) │
   │ Trader  │          │ Trader  │          │ Trader  │  │ Trader  │
   └─────────┘          └─────────┘          └─────────┘  └─────────┘
        │                     │                     │            │
        └─────────────────────┴─────────────────────┴────────────┘
                              │
                              ▼
   ┌──────────────────────────────────────────────────────────────┐
   │              TRADER AGENT (OpenAI Agents SDK)                │
   │  • Instructions: Trading strategy & decision making          │
   │  • Tools: Researcher (nested agent), Account operations      │
   │  • MCP Servers: Accounts, Market Data, Notifications         │
   └──────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   ┌──────────┐         ┌──────────┐         ┌──────────┐
   │Researcher│         │  Market  │         │ Accounts │
   │  Agent   │         │   Data   │         │  Server  │
   │(Nested)  │         │  Server  │         │   MCP    │
   └──────────┘         └──────────┘         └──────────┘
        │
        └─────────────────────────────────────────────────┐
                              │                           │
                              ▼                           ▼
   ┌──────────────────────────────────────────────────────────────┐
   │           RESEARCHER MCP SERVERS (3 servers)                 │
   ├──────────────────────────────────────────────────────────────┤
   │ 1. Fetch MCP (mcp-server-fetch)                              │
   │    • Headless browser for web scraping                       │
   │                                                               │
   │ 2. Brave Search MCP (@modelcontextprotocol/server-brave)     │
   │    • Web search via Brave API                                │
   │                                                               │
   │ 3. Memory MCP (mcp-memory-libsql)                            │
   │    • Knowledge graph: entities, observations, relations      │
   │    • Per-agent SQLite database                               │
   │    • Shared across all traders via entity system             │
   └──────────────────────────────────────────────────────────────┘
                              │
                              ▼
   ┌──────────────────────────────────────────────────────────────┐
   │            TRADER MCP SERVERS (3 servers)                    │
   ├──────────────────────────────────────────────────────────────┤
   │ 1. Accounts MCP (accounts_server.py - Custom)                │
   │    • Resources: Account state, Trading strategy              │
   │    • Tools: buy_shares(), sell_shares(), get_holdings()      │
   │                                                               │
   │ 2. Push Notification MCP (push_server.py - Custom)           │
   │    • Tools: send_notification() via Pushover API             │
   │                                                               │
   │ 3. Market Data MCP (Polygon.io OR custom market_server.py)   │
   │    • Tools: get_share_price(), get_snapshot_ticker()         │
   │    • get_last_trade(), technical_indicators(), fundamentals() │
   └──────────────────────────────────────────────────────────────┘
                              │
                              ▼
   ┌──────────────────────────────────────────────────────────────┐
   │                  DATA PERSISTENCE LAYER                      │
   ├──────────────────────────────────────────────────────────────┤
   │ • accounts.db - SQLite (portfolios, transactions, balances)  │
   │ • memory/{trader}.db - SQLite (per-agent knowledge graphs)   │
   │ • Custom tracing/logging system → UI display                 │
   └──────────────────────────────────────────────────────────────┘
                              │
                              ▼
   ┌──────────────────────────────────────────────────────────────┐
   │              GRADIO UI (Real-time Dashboard)                 │
   │  • Live portfolio charts (Plotly)                            │
   │  • Holdings & transactions tables                            │
   │  • Profit/Loss tracking                                      │
   │  • Live execution logs (color-coded by event type)           │
   │  • Auto-refresh every 120 seconds                            │
   └──────────────────────────────────────────────────────────────┘
```

---

## 🔌 What is MCP? - The USB-C of AI

### **The Problem MCP Solves**

Before MCP, every AI application had custom tool integrations:
- Langchain has `@tool` decorator
- OpenAI has function calling JSON schemas
- Anthropic has Claude tools
- Each framework required different tool formats

**MCP standardizes tool integration** - build once, use everywhere.

### **The Three Components**

```
┌─────────────────────────────────────────────────────────────┐
│                      MCP HOST                               │
│        (Your LLM Application - Agent, Claude Desktop)       │
│  ┌────────────────────────────────────────────────────┐    │
│  │              MCP CLIENT (1:1 with server)          │    │
│  │  • Spawns/connects to MCP servers                  │    │
│  │  • Manages lifecycle (async context)               │    │
│  │  • Translates tools/resources to LLM format        │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                         │ (stdio or SSE)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     MCP SERVER                              │
│  • Exposes tools (functions the LLM can call)               │
│  • Exposes resources (context to inject into prompts)       │
│  • Exposes prompts (reusable prompt templates)              │
└─────────────────────────────────────────────────────────────┘
```

### **Three Configurations of MCP Servers**

1. **Local Server, Local Operations** (e.g., filesystem MCP)
   - Server runs on your machine
   - Accesses local resources (files, databases)
   - No external API calls

2. **Local Server, Remote API** (e.g., Brave Search, Polygon.io) ⭐ **Most Common**
   - Server code runs on your machine
   - Server makes API calls to remote services
   - You configure with API keys
   - Example: `@modelcontextprotocol/server-brave-search`

3. **Remote Managed Server** (e.g., enterprise services)
   - Server runs remotely (hosted by provider)
   - You connect via SSE (Server-Sent Events)
   - Usually paid enterprise services (Plaid, Stripe, PayPal)
   - Can deploy your own with Cloudflare Workers

### **Why Use MCP?**

✅ **Build Once, Use Everywhere**: Same tool works in Claude Desktop, OpenAI Agents, custom apps

✅ **Ecosystem**: 100+ community MCP servers (filesystem, databases, APIs, browser automation)

✅ **Consistency**: Standardized way to incorporate tools across all agents

✅ **Security**: Same trust model as `pip install` - vet the code, then run locally

✅ **Composability**: Mix and match servers for different agent capabilities

### **When NOT to Use MCP**

❌ **Internal-only tools**: If you're not sharing, just use native decorators (`@tool`)

❌ **Simple projects**: Adds complexity for basic use cases

❌ **Rapid prototyping**: Faster to write inline functions initially

**Rule of Thumb**: Use MCP when building reusable tools for multiple agents/applications.

---

## 🏗️ The Trading Floor Project

### **What It Is**

An autonomous multi-agent trading simulation where 4 AI traders:
1. **Research** market news and opportunities
2. **Analyze** financial data and technical indicators
3. **Execute** trades based on their strategies
4. **Evolve** their strategies autonomously over time
5. **Share knowledge** via a distributed knowledge graph

**Real-world Capabilities**:
- Integrates real-time market data (Polygon.io API)
- Manages SQLite portfolios with transaction history
- Sends push notifications on trade execution
- Displays live dashboards with portfolio performance
- Runs continuously on 60-minute intervals

### **The Four Traders**

| Name | Strategy | Personality | Model |
|------|----------|-------------|-------|
| **Warren** | Value investing, long-term holds | Patient | GPT-4o-mini |
| **George** | Momentum trading, bold bets | Aggressive | DeepSeek V3 |
| **Ray** | Systematic diversification | Risk-averse | Gemini 2.5 Flash |
| **Cathie** | Growth/crypto ETFs | Innovation-focused | Grok 3 Mini |

**Key Feature**: Each trader can autonomously **change their own strategy** based on performance.

### **Architecture Highlights**

#### **1. Nested Agent Pattern**
```python
# Trader agent wraps Researcher agent as a tool
researcher_agent = Agent(name="Researcher", ...)
researcher_tool = researcher_agent.as_tool()

trader_agent = Agent(
    name="Warren",
    tools=[researcher_tool],  # Researcher is a tool!
    mcp_servers=[accounts_mcp, market_mcp, push_mcp]
)
```

**Why This Matters**:
- Researcher has different MCP servers (web search, memory)
- Trader has different MCP servers (accounts, market data)
- Clean separation of concerns
- Researcher can be reused by all traders

#### **2. MCP Resources (Not Just Tools!)**

MCP provides three primitives:
- **Tools**: Functions LLM can call
- **Resources**: Context injected into prompts ⭐
- **Prompts**: Reusable prompt templates

**Example - Loading Strategy as Resource**:
```python
# accounts_server.py exposes strategy as MCP resource
@mcp.resource("strategy://{name}")
def get_strategy(name: str) -> str:
    account = Account.get(name)
    return account.strategy

# Client reads resource into prompt
strategy = await read_strategy_resource("warren")
message = f"Your strategy: {strategy}\nNow analyze market and trade."
```

**Benefit**: Strategy updates persist and dynamically load into agent prompts.

#### **3. Shared Knowledge Graph Memory**

Each trader has their own memory database but shares entities:

```python
# researcher_mcp_server_params
{
    "command": "npx",
    "args": ["-y", "mcp-memory-libsql"],
    "env": {"LIBSQL_URL": f"file:./memory/{name}.db"}
}
```

**How It Works**:
1. Warren researches Apple → stores entity "AAPL" with observations
2. George queries memory → retrieves Warren's AAPL research
3. Collective intelligence builds over time

**Tools Provided by Memory MCP**:
- `create_entities(name, entityType, observations)`
- `create_relations(from, to, relationType)`
- `read_graph()` - retrieve full knowledge graph
- `search_nodes(query)` - semantic search over entities
- `open_nodes([names])` - retrieve specific entities

#### **4. Custom MCP Server Implementation**

**Writing an MCP server is trivial** - just wrap existing code:

```python
# accounts_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Accounts")

@mcp.resource("account://{name}")
def get_account(name: str) -> str:
    account = Account.get(name)
    return account.report()  # JSON string

@mcp.tool()
def buy_shares(name: str, symbol: str, quantity: int, rationale: str) -> str:
    """Buy shares of a stock"""
    account = Account.get(name)
    return account.buy_shares(symbol, quantity, rationale)

@mcp.tool()
def sell_shares(name: str, symbol: str, quantity: int, rationale: str) -> str:
    """Sell shares of a stock"""
    account = Account.get(name)
    return account.sell_shares(symbol, quantity, rationale)
```

**That's it!** Run with: `uv run accounts_server.py`

#### **5. Async MCP Server Lifecycle Management**

MCP servers are spawned/managed via async context managers:

```python
from contextlib import AsyncExitStack
from agents.mcp import MCPServerStdio

async def run_with_mcp_servers(self):
    # Context manager ensures proper cleanup
    async with AsyncExitStack() as stack:
        trader_mcp_servers = [
            await stack.enter_async_context(
                MCPServerStdio(params, client_session_timeout_seconds=120)
            )
            for params in trader_mcp_server_params
        ]
        
        # Nested stack for researcher servers
        async with AsyncExitStack() as stack2:
            researcher_mcp_servers = [
                await stack2.enter_async_context(
                    MCPServerStdio(params, client_session_timeout_seconds=120)
                )
                for params in researcher_mcp_server_params(self.name)
            ]
            
            await self.run_agent(trader_mcp_servers, researcher_mcp_servers)
    # Servers automatically shut down on context exit
```

**Why AsyncExitStack?**:
- Manages multiple MCP server lifecycles
- Ensures cleanup even on exceptions
- Handles stdio process spawning/termination
- Timeout management for hanging servers

#### **6. Multi-Model Architecture**

Each trader can use a different LLM provider:

```python
model_names = [
    "gpt-4.1-mini",              # OpenAI
    "deepseek-chat",             # DeepSeek
    "gemini-2.5-flash-preview",  # Google
    "grok-3-mini-beta",          # xAI
]

def get_model(model_name: str):
    if "deepseek" in model_name:
        return OpenAIChatCompletionsModel(
            model=model_name,
            openai_client=AsyncOpenAI(
                base_url="https://api.deepseek.com/v1",
                api_key=deepseek_api_key
            )
        )
    # ... similar for Gemini, Grok
```

**Why This Matters**: Compare model performance on same task (trading strategy execution).

#### **7. Custom Tracing & Logging System**

Built custom tracer to log agent execution to UI:

```python
# tracers.py
from agents import TraceProcessor

class LogTracer(TraceProcessor):
    def process_trace(self, trace):
        if trace.type == "generation":
            write_log(agent_name, "generation", trace.content)
        elif trace.type == "function":
            write_log(agent_name, "function", f"{trace.name}({trace.args})")
        # ... custom logic
```

**Benefit**: Real-time execution visibility in Gradio UI with color-coded events.

#### **8. Trading Workflow (Alternating Pattern)**

Traders alternate between two modes:

**Trade Mode** (Iteration 1, 3, 5...):
- Use researcher to find opportunities
- Analyze market data
- Execute new trades based on strategy
- Send notification with summary

**Rebalance Mode** (Iteration 2, 4, 6...):
- Review existing portfolio
- Research news affecting holdings
- Rebalance positions
- Optionally evolve strategy

```python
async def run(self):
    message = (
        trade_message(...) if self.do_trade 
        else rebalance_message(...)
    )
    await Runner.run(self.agent, message, max_turns=30)
    self.do_trade = not self.do_trade  # Toggle for next run
```

**Why Alternate?**: Separates exploration (new opportunities) from exploitation (portfolio optimization).

---

## 🔧 Technical Deep-Dives (Interview Q&A Prep)

### **Q: Explain the MCP client-server architecture and communication protocols.**

**A**: MCP uses a client-server model with two communication protocols:

#### **1. stdio (Standard Input/Output)** ⭐ Most Common
```python
mcp_server_params = {
    "command": "uvx",  # or "npx", "uv run", "python"
    "args": ["mcp-server-fetch"],
    "env": {"API_KEY": "..."}
}

# OpenAI SDK spawns server as subprocess
server = MCPServerStdio(mcp_server_params)
```

**How it works**:
1. Client spawns server as subprocess
2. Communication via stdin/stdout (JSON-RPC)
3. Server lifecycle tied to client process
4. Clean shutdown via context manager

**Pros**: 
- Simple, no network config
- Works offline
- Secure (local process)

**Cons**:
- Can't share server across clients
- Each client spawns own server instance

#### **2. SSE (Server-Sent Events)** - Rare
```python
mcp_server_params = {
    "url": "https://mcp-server.example.com",
    "headers": {"Authorization": "Bearer ..."}
}
```

**Use case**: Remote managed services (enterprise APIs).

---

### **Q: How do MCP resources differ from tools? When would you use each?**

**A**:

| Feature | Tools | Resources |
|---------|-------|-----------|
| **Purpose** | Execute actions | Provide context |
| **LLM Interaction** | LLM decides when to call | Loaded into prompt automatically or on-demand |
| **Format** | Function with parameters | Text/JSON data |
| **Execution** | Runs code | Returns data |

**Tools Example**:
```python
@mcp.tool()
def buy_shares(symbol: str, quantity: int) -> str:
    """Execute a stock purchase"""
    return account.buy_shares(symbol, quantity)
```

**Resources Example**:
```python
@mcp.resource("account://{name}")
def get_account(name: str) -> str:
    """Current account state (injected into prompt)"""
    return json.dumps(account.to_dict())
```

**When to Use**:
- **Tools**: Actions with side effects (buy, sell, send notification)
- **Resources**: Static/dynamic context (account balance, strategy, market conditions)

**In Trading Floor**:
- Tools: `buy_shares()`, `sell_shares()`, `search_web()`, `send_notification()`
- Resources: Account state, trading strategy

**Benefit**: Resources reduce tool calls - data is pre-loaded into prompt vs LLM asking for it.

---

### **Q: Explain the knowledge graph memory architecture and why it's useful.**

**A**: The memory MCP provides a **persistent entity-relationship store** with semantic search.

#### **Schema**:
```
Entities: {name, entityType, observations[]}
Relations: {from, to, relationType}
```

#### **Example Flow**:
```python
# Warren researches Apple
create_entities([{
    "name": "AAPL",
    "entityType": "stock",
    "observations": [
        "Released new iPhone in Q1 2026",
        "P/E ratio: 28",
        "Strong cash position"
    ]
}])

create_relations([{
    "from": "AAPL",
    "to": "Consumer Electronics",
    "relationType": "operates_in"
}])

# Later, George queries memory
results = search_nodes("consumer electronics stocks")
# Returns: AAPL entity with Warren's observations
```

#### **Why It's Powerful**:

1. **Persistent Learning**: Knowledge survives across agent runs
2. **Shared Intelligence**: All traders benefit from each other's research
3. **Semantic Search**: Query by meaning, not exact text match
4. **Structured Retrieval**: Entities + relations = queryable graph

#### **Architecture in Trading Floor**:
- Each trader has separate database: `memory/warren.db`, `memory/george.db`
- But they all use the same entity names (e.g., "AAPL", "Tesla")
- Researcher agent loads/stores entities during research
- Trader queries memory before making decisions

**Real-world analog**: Like a shared company wiki that auto-updates as team members research.

---

### **Q: How do you handle MCP server failures and timeouts?**

**A**: Multi-layered error handling:

#### **1. Client-Side Timeout**
```python
MCPServerStdio(
    params,
    client_session_timeout_seconds=120  # Kill server after 2 min inactivity
)
```

#### **2. Context Manager Cleanup**
```python
async with AsyncExitStack() as stack:
    servers = [await stack.enter_async_context(MCPServerStdio(p)) for p in params]
    # Do work
    # Servers auto-cleanup on exception or normal exit
```

#### **3. Agent-Level Error Handling**
```python
async def run(self):
    try:
        await self.run_with_trace()
    except Exception as e:
        print(f"Error running trader {self.name}: {e}")
        # Log to database, send alert, etc.
```

#### **4. Graceful Degradation in Prompts**

If Polygon.io (real-time data) fails, fallback to local market data:
```python
if is_realtime_polygon:
    market_mcp = polygon_api_server()
else:
    market_mcp = local_market_server()  # EOD data only
```

Update agent instructions:
```python
note = "You have access to realtime data" if realtime else "You have EOD data only"
instructions = f"... {note}"
```

#### **5. Rate Limiting Awareness**

Polygon.io free tier: 5 calls/minute

Strategy:
- Batch requests (multiple tickers in one call)
- Use researcher to make API calls (not trader directly)
- Fall back to web scraping via Fetch MCP if rate limited

**Prompt Engineering**:
```python
researcher_instructions = """
If web search raises rate limit error, use your fetch tool to scrape websites instead.
"""
```

---

### **Q: Why use nested agents (Trader → Researcher) instead of giving Trader all tools?**

**A**: Separation of concerns and encapsulation.

#### **Without Nesting** (Monolithic):
```python
trader = Agent(
    tools=[
        buy_shares, sell_shares, get_holdings,  # Trading
        search_web, fetch_page, wikipedia,      # Research
        get_share_price, get_technicals,        # Market data
        create_entity, search_graph             # Memory
    ]
)
```

**Problems**:
- ❌ 10+ tools = decision paralysis for LLM
- ❌ Mixed concerns (trading + research) in one prompt
- ❌ Can't reuse researcher for other traders
- ❌ Harder to trace which tools are for what

#### **With Nesting** (Compositional):
```python
researcher = Agent(
    name="Researcher",
    instructions=researcher_instructions(),  # Research-specific prompts
    mcp_servers=[fetch_mcp, brave_mcp, memory_mcp]  # Research tools only
)

trader = Agent(
    name="Warren",
    instructions=trader_instructions(),  # Trading-specific prompts
    tools=[researcher.as_tool()],  # Researcher is ONE tool from trader's perspective
    mcp_servers=[accounts_mcp, market_mcp, push_mcp]  # Trading tools only
)
```

**Benefits**:
- ✅ Researcher is reusable (all 4 traders use same researcher)
- ✅ Clear tool scoping (trader sees 5 tools, not 15)
- ✅ Better prompts (research vs trading instructions separate)
- ✅ Easier debugging (trace researcher separately)
- ✅ Modularity (swap researcher implementation without touching trader)

**Real-world Analog**: Like having a research analyst (researcher) report to a portfolio manager (trader).

---

### **Q: How does the trading floor scheduler work? Why the 60-minute interval?**

**A**: Async event loop with market hours awareness:

```python
# trading_floor.py
async def run_every_n_minutes():
    traders = create_traders()
    while True:
        if RUN_EVEN_WHEN_MARKET_IS_CLOSED or is_market_open():
            # Run all traders concurrently
            await asyncio.gather(*[trader.run() for trader in traders])
        else:
            print("Market is closed, skipping run")
        await asyncio.sleep(RUN_EVERY_N_MINUTES * 60)
```

#### **Design Decisions**:

**1. Why Concurrent Execution?**
```python
await asyncio.gather(*[trader.run() for trader in traders])
```
- All 4 traders run in parallel (not sequential)
- Reduces total execution time (4x faster)
- Each trader is independent (no shared state during execution)

**2. Why 60 Minutes?**
- Market conditions don't change drastically every second
- Rate limits (Polygon.io: 5 calls/min free tier)
- LLM API costs (each run = 30-50K tokens per trader)
- Realistic trading cadence (not HFT)

**Configurable** via `.env`:
```bash
RUN_EVERY_N_MINUTES=60  # Change to 5 for testing, 1440 for daily
RUN_EVEN_WHEN_MARKET_IS_CLOSED=false  # Set true for demos
```

**3. Market Hours Check**:
```python
def is_market_open() -> bool:
    now = datetime.now(timezone('America/New_York'))
    if now.weekday() >= 5:  # Saturday, Sunday
        return False
    market_open = now.replace(hour=9, minute=30)
    market_close = now.replace(hour=16, minute=0)
    return market_open <= now <= market_close
```

**Production Considerations**:
- Could use cron/scheduler instead of infinite loop
- Could add exponential backoff on failures
- Could use message queue (Celery/RQ) for scaling

---

### **Q: Explain the custom tracing system and how it integrates with the UI.**

**A**: Built custom `TraceProcessor` to log agent events to SQLite for UI display.

#### **Architecture**:

```
┌─────────────────────────────────────────────────────────┐
│        OpenAI Agents SDK (Built-in Tracing)            │
│  • Every LLM call, tool call, response tracked         │
│  • Emits trace events to registered processors         │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│           LogTracer (Custom TraceProcessor)             │
│  • Receives trace events                               │
│  • Filters by type (generation, function, etc.)        │
│  • Writes to SQLite database                           │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│               Database (logs table)                     │
│  Schema: (agent_name, timestamp, type, message)        │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│          Gradio UI (Polling Every 0.5s)                 │
│  • Reads last N logs from database                     │
│  • Color-codes by type (generation=yellow, etc.)       │
│  • Displays in scrollable HTML div                     │
└─────────────────────────────────────────────────────────┘
```

#### **Implementation**:

**1. Custom Tracer**:
```python
# tracers.py
from agents import TraceProcessor
from database import write_log

class LogTracer(TraceProcessor):
    def process_trace(self, trace):
        agent_name = extract_agent_name(trace)
        
        if trace.type == "agent":
            write_log(agent_name, "agent", f"Starting {trace.name}")
        elif trace.type == "generation":
            write_log(agent_name, "generation", trace.content)
        elif trace.type == "function":
            write_log(agent_name, "function", f"{trace.name}({trace.args})")
        elif trace.type == "response":
            write_log(agent_name, "response", trace.content)
```

**2. Register Tracer**:
```python
# trading_floor.py
from agents import add_trace_processor

add_trace_processor(LogTracer())  # Now all agents log to DB
```

**3. Database Schema**:
```sql
CREATE TABLE logs (
    agent_name TEXT,
    timestamp TEXT,
    type TEXT,  -- 'trace', 'agent', 'function', 'generation', 'response', 'account'
    message TEXT
)
```

**4. UI Polling**:
```python
# app.py
def get_logs(self, previous=None) -> str:
    logs = read_log(self.name, last_n=13)  # Last 13 events
    html = ""
    for timestamp, type, message in logs:
        color = COLOR_MAP[type]  # Yellow for generation, green for function, etc.
        html += f"<span style='color:{color}'>{timestamp} : [{type}] {message}</span><br/>"
    
    if html != previous:
        return html  # Update UI
    return gr.update()  # No change, skip re-render

# Gradio timer polls every 0.5 seconds
log_timer = gr.Timer(value=0.5)
log_timer.tick(fn=get_logs, inputs=[previous_log], outputs=[log_display])
```

**Why Not Use OpenAI Traces UI?**
- Need logs in app UI (Gradio), not external dashboard
- Want custom filtering/coloring
- Need to correlate logs with portfolio changes

**Alternative Considered**: Stream logs via websocket, but polling is simpler for MVP.

---

### **Q: What are the key trade-offs between agent autonomy and coherence?**

**A**: This is the central tension in multi-agent systems.

#### **Autonomy vs Coherence Spectrum**:

```
Full Autonomy ←────────────────────────────→ Full Coherence
(Chaotic)                                    (Rigid)

• Agents decide    • Agents follow      • Agents execute
  everything         guidelines with       strict rules
• No constraints    freedom              • No deviation
• Creative but    • Balanced           • Predictable but
  unpredictable                            inflexible
```

#### **Trading Floor Position: High Autonomy**

**Autonomous Decisions**:
1. ✅ Research what to investigate (no predefined stocks)
2. ✅ Decide when to buy/sell (no forced trades)
3. ✅ Choose position sizes (no fixed allocations)
4. ✅ Evolve strategy over time (`change_strategy()` tool)

**Coherence Mechanisms**:
1. ✅ Success criteria in prompts ("maximize profits according to strategy")
2. ✅ Tool constraints (can't short, can't trade on margin, balance > 0)
3. ✅ Researcher nested agent (structured research, not random browsing)
4. ✅ Shared memory (collective intelligence reduces redundant research)
5. ✅ Alternating trade/rebalance (prevents chaotic behavior)

#### **Real Example from Testing**:

**High Autonomy Failure**:
- Cathie (crypto trader) decided to abandon crypto and become a dividend investor
- Changed strategy completely off-script
- Interesting but defeats purpose of comparing strategies

**Solution Applied**:
```python
trader_instructions = f"""
You are {name}, a {strategy_type} trader.
You CAN evolve your strategy, but stay true to your core philosophy.
"""
```

**Lesson**: Autonomy needs **guardrails** (soft constraints in prompts), not hard-coded rules.

#### **The Balance**:

| Too Much Autonomy | Too Much Coherence |
|-------------------|-------------------|
| Agents go off-script | Agents feel like scripts |
| Unpredictable behavior | No emergent behavior |
| Hard to debug | Boring, no learning |
| Creative but risky | Safe but limited |

**Best Practice**:
1. Start with high coherence (detailed prompts, constraints)
2. Iteratively loosen constraints (give autonomy)
3. Add guardrails when failures occur
4. Monitor and adjust based on outcomes

**In Trading Floor**: ~70% autonomy, 30% coherence
- Autonomy: What to research, when to trade, position sizes, strategy evolution
- Coherence: Must use researcher, must send notification, must stay in character

---

### **Q: What are MCP best practices you learned from this project?**

**A**:

#### **1. Server Lifecycle Management**

✅ **DO**: Use `AsyncExitStack` for multiple MCP servers
```python
async with AsyncExitStack() as stack:
    servers = [await stack.enter_async_context(MCPServerStdio(p)) for p in params]
    # Guaranteed cleanup
```

❌ **DON'T**: Manually manage server processes (risk of orphaned processes)

---

#### **2. Client Session Timeouts**

✅ **DO**: Set reasonable timeouts
```python
MCPServerStdio(params, client_session_timeout_seconds=120)
```

**Why**: Some operations (web scraping, API calls) take time. Default 30s is too short.

---

#### **3. Tool vs Resource Decision**

✅ **DO**: Use resources for context, tools for actions
```python
@mcp.resource("account://{name}")  # Static context
def get_account(name: str) -> str:
    return account.to_json()

@mcp.tool()  # Action with side effect
def buy_shares(name: str, symbol: str, quantity: int) -> str:
    return account.buy_shares(symbol, quantity)
```

---

#### **4. Tool Descriptions Matter**

✅ **DO**: Write detailed, specific tool descriptions
```python
@mcp.tool()
def buy_shares(name: str, symbol: str, quantity: int, rationale: str) -> str:
    """
    Buy shares of a stock.
    
    Args:
        name: Your account name (e.g., 'warren')
        symbol: Stock ticker symbol (e.g., 'AAPL')
        quantity: Number of shares to buy (must be positive integer)
        rationale: Explain why you're buying (for transaction log)
    
    Returns:
        Updated account details with new holdings and balance
    """
```

**Why**: LLM needs to understand when/how to call tool. Vague descriptions = wrong calls.

---

#### **5. Error Handling in Tools**

✅ **DO**: Return descriptive error messages (not exceptions)
```python
@mcp.tool()
def buy_shares(symbol: str, quantity: int) -> str:
    try:
        return account.buy_shares(symbol, quantity)
    except ValueError as e:
        return f"Error: {str(e)}. Please try a different quantity or symbol."
```

**Why**: LLM can react to error message and retry. Exception kills execution.

---

#### **6. Rate Limiting Strategies**

✅ **DO**: Document rate limits in instructions
```python
researcher_instructions = """
You have access to web search (5 calls/min limit).
If rate limited, use fetch tool to scrape websites instead.
"""
```

✅ **DO**: Batch API calls when possible
```python
# Polygon API allows multiple tickers in one call
get_share_price("AAPL,MSFT,GOOGL")  # 1 API call, not 3
```

---

#### **7. MCP Server Selection**

✅ **DO**: Prefer community servers when available
- `mcp-server-fetch` > custom web scraper
- `@modelcontextprotocol/server-brave-search` > custom search
- `mcp-memory-libsql` > custom memory store

**Why**: Battle-tested, maintained, documented

✅ **DO**: Write custom servers for domain-specific logic
- `accounts_server.py` (custom trading logic)
- `market_server.py` (custom fallback for free tier)

---

#### **8. Security & Vetting**

✅ **DO**: Vet MCP servers before running
- Check GitHub stars, maintainer reputation
- Review source code (especially for filesystem access)
- Use official `@modelcontextprotocol` servers when possible

❌ **DON'T**: Blindly `npx -y` random MCP servers (like `pip install` from untrusted sources)

---

#### **9. Debugging MCP Issues**

✅ **DO**: Test servers in isolation first
```bash
# Test server manually
uvx mcp-server-fetch

# Or use MCP inspector
npx @modelcontextprotocol/inspector uvx mcp-server-fetch
```

✅ **DO**: Check server logs
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

#### **10. Composability**

✅ **DO**: Design agents to accept `mcp_servers` as parameters
```python
def create_agent(mcp_servers: List[MCPServer]) -> Agent:
    return Agent(tools=[], mcp_servers=mcp_servers)

# Easy to swap configurations
dev_servers = [local_market_mcp]
prod_servers = [polygon_mcp, brave_mcp, memory_mcp]

agent = create_agent(prod_servers)
```

**Why**: Makes testing easier (mock servers) and enables configuration-driven agent behavior.

---

## 💡 Key Technical Achievements

### **1. Production-Ready Architecture**
- ✅ Async execution with proper cleanup
- ✅ SQLite persistence (accounts, memory, logs)
- ✅ Error handling and graceful degradation
- ✅ Configurable via environment variables
- ✅ Real-time UI with live updates

### **2. Advanced Agent Patterns**
- ✅ Nested agents (Trader → Researcher)
- ✅ Multi-agent orchestration (4 concurrent traders)
- ✅ Shared knowledge graph memory
- ✅ Strategy evolution over time

### **3. MCP Ecosystem Integration**
- ✅ 6+ MCP servers (3 trader, 3 researcher)
- ✅ 44 total tools available
- ✅ Custom MCP servers (accounts, push, market)
- ✅ Community MCP servers (fetch, brave, memory)
- ✅ Multi-protocol support (stdio)

### **4. Multi-Model Experimentation**
- ✅ OpenAI (GPT-4o-mini)
- ✅ DeepSeek (DeepSeek V3)
- ✅ Google (Gemini 2.5 Flash)
- ✅ xAI (Grok 3 Mini)
- ✅ Comparative performance analysis

### **5. Real-World Integration**
- ✅ Polygon.io API (real-time market data)
- ✅ Pushover API (push notifications)
- ✅ Brave Search API (web search)
- ✅ Gradio UI (live dashboard)

---

## 📚 Key Takeaways for Interviews

### **What I Built**:
Real-time autonomous trading floor with:
- 4 AI traders with distinct strategies
- 6+ MCP servers providing 44 tools
- Shared knowledge graph memory
- Real-time market data integration
- Production UI with live portfolio tracking
- Multi-model support (GPT, DeepSeek, Gemini, Grok)

### **What I Learned**:

1. **MCP standardizes tool integration** - the "USB-C of AI"
2. **Resources are underutilized** - powerful for dynamic context injection
3. **Nested agents > monolithic agents** - better scoping and reusability
4. **Knowledge graphs enable collective intelligence** - shared memory across agents
5. **Autonomy needs guardrails** - balance freedom with coherence
6. **Async lifecycle management is critical** - proper cleanup prevents resource leaks
7. **Custom MCP servers are trivial** - wrap existing code with decorators
8. **Tool descriptions are first-class** - LLM quality depends on them

### **How I Use It**:
- **MCP Server Testing**: Evaluate new servers before production use
- **Multi-Model Comparison**: Test LLM performance on real-world task
- **Agent Pattern Learning**: Practice production-grade multi-agent systems
- **Real-World Integration**: Experience with APIs, databases, async execution

### **What's Next**:
- Add more traders (momentum, technical analysis, news-driven)
- Integrate more MCP servers (news APIs, SEC filings, social sentiment)
- Implement portfolio optimization algorithms
- Add backtesting with historical data
- Deploy to cloud with scheduled runs
- Build evaluation metrics (Sharpe ratio, win rate, drawdown)

---

## 🎓 Resources

- **MCP Spec**: https://spec.modelcontextprotocol.io/
- **MCP Servers Marketplace**: https://mcp.so, https://glama.ai/mcp, https://smithery.ai/
- **OpenAI Agents SDK**: https://github.com/openai/openai-agents-python
- **My Notes**: `notes.md` in project folder
- **Code**: `trading_floor.py`, `traders.py`, `accounts.py`, `app.py`

---

**Last Updated**: February 2026  
**Technologies**: Python 3.12, MCP, OpenAI Agents SDK, Polygon.io, Brave Search, LibSQL Memory, SQLite, Gradio, Pydantic, AsyncIO
