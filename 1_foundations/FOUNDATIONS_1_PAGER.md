# Agentic AI Foundations - Technical Summary & Personal Project

## Core Concepts Mastered

### 1. **Agentic AI Fundamentals**
- **Definition**: Programs where LLM outputs control the workflow
- **Key Characteristics**:
  - Multiple LLM calls
  - LLMs with ability to use Tools (hallmark of agentic systems)
  - Environment where LLMs interact
  - Planner to coordinate activities
  - Autonomy (LLM controls what happens)

### 2. **Tool Use - The Foundation of Agentic Systems**
- **Tool calls are glorified if statements**: JSON schema describes function capabilities
- LLM receives tool descriptions in natural language
- LLM decides when to call tools based on context
- `handle_tool_calls()` function extracts JSON and routes to appropriate functions
- Tool descriptions must be clear and natural language (LLMs excel at understanding JSON from training data)

### 3. **Agentic Workflows vs. Agentic Systems**
**Workflows** - Predefined code paths orchestrating LLMs and tools:
1. **Prompt Chaining** - Sequential, well-defined tasks with framed prompts
2. **Routing** - Direct input to specialized sub-tasks (separation of concerns)
3. **Parallelization** - Break down tasks and run subtasks concurrently
4. **Orchestrator-Worker** - Complex tasks broken down dynamically and combined
5. **Evaluator-Optimizer** - LLM output validated by another LLM (e.g., Text2BDD)

**Agents** - LLMs dynamically direct their own processes:
- Open-ended execution
- Feedback loops
- No fixed path
- **Risks**: Unpredictable path, output, and costs
- **Solutions**: Monitoring and guardrails

### 4. **Context Engineering vs. Prompt Engineering**
- **Prompt Engineering**: What to say to the model at a moment in time (inside the context window)
- **Context Engineering**: What the model knows when you say it (what fills the window)
- Context Engineering is how we scale - ensures the 1,000th output is still good
- Quality of context > complexity of code

### 5. **Structured Outputs**
- Pydantic models for type-safe LLM responses
- `chat.completions.parse(model, messages, response_format)` for structured parsing
- Enables reliable communication between LLMs (e.g., evaluator-optimizer pattern)

### 6. **Resources vs. Tools**
- **Resources**: Provide LLM with information to improve expertise (RAG, knowledge bases)
- **Tools**: Give LLM power to carry out actions (query DB, message other LLMs, API calls)

---

## Personal Project: Professional Alter Ego Chatbot (www.araiz.pro)

### Problem Statement
As a Senior Software Engineer actively seeking opportunities, I needed a way to engage with potential recruiters and employers 24/7, answer questions about my background, and capture leads - all while maintaining a professional presence. I built an AI clone of myself embedded in my personal website.

### Architecture

**Core Components:**
1. **Context Engineering**: 
   - LinkedIn profile extracted via PDF reader (`pypdf`)
   - Comprehensive summary document with career history, skills, projects, and job preferences
   - Both loaded into system prompt for rich context

2. **Tool-Enabled Agent**:
   - **Record User Details Tool**: Captures email, name, and notes when users express interest
   - **Record Unknown Question Tool**: Logs questions the agent couldn't answer for follow-up
   - Both tools use Pushover API for real-time SMS notifications

3. **Gradio Chat Interface**:
   - Professional chat UI with example questions
   - Embedded into personal website (www.araiz.pro)
   - Resume download capability integrated

### Implementation Highlights

```python
# Tool definition (JSON schema)
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested...",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address..."},
            "name": {"type": "string", "description": "The user's name..."},
            "notes": {"type": "string", "description": "Additional context..."}
        },
        "required": ["email"]
    }
}

# Tool call handler (the "if statement")
def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        })
    return results

# Main chat loop with tool support
def chat(self, message, history):
    messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
    done = False
    while not done:
        response = self.openai.chat.completions.create(
            model="gpt-4o-mini", 
            messages=messages, 
            tools=tools
        )
        if response.choices[0].finish_reason == "tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = self.handle_tool_calls(tool_calls)
            messages.append(message)
            messages.extend(results)
        else:
            done = True
    return response.choices[0].message.content
```

### Key Features

**Context Engineering:**
- Rich system prompt with career summary, LinkedIn profile, contact info, and job preferences
- Instructions for tool usage and follow-up messaging
- Professional tone calibrated for recruiters and employers

**Tool Integration:**
- **Pushover API**: Real-time SMS notifications when users express interest or ask unanswerable questions
- Automatic lead capture with context (name, email, conversation notes)
- Unknown question logging for continuous improvement

**User Experience:**
- Example questions guide visitors (career, skills, projects, contact)
- Professional, engaging responses as if talking to potential employer
- Seamless handoff: agent asks for contact info and records it
- Resume download available on website

**Deployment:**
- Gradio app deployed and embedded into www.araiz.pro
- Production-ready with error handling and tool call management
- Real-time notifications enable immediate follow-up with interested parties

### Technical Stack
- **Framework**: OpenAI API (direct, no framework)
- **Language**: Python 3.12+
- **Model**: GPT-4o-mini
- **Tools**: Pushover API (SMS notifications)
- **UI**: Gradio ChatInterface
- **Deployment**: Embedded in personal website (www.araiz.pro)
- **File Processing**: PyPDF for LinkedIn profile extraction

### Key Learnings & Best Practices

1. **Tool Calls Demystified**: Under the hood, tool calls are JSON schemas + if statements - the magic is in clear natural language descriptions
2. **Context Engineering**: Quality of context (what fills the window) matters more than prompt complexity
3. **Bias the Model**: Repetition in system prompts increases probability of desired behavior (tool usage, tone, etc.)
4. **Tool Description Quality**: Natural language descriptions are critical - LLMs need to understand when and why to use tools
5. **Real-World Integration**: Tools enable agents to interact with external systems (APIs, databases, notifications)
6. **Production Considerations**: Error handling, graceful degradation, and monitoring (via Pushover notifications)

### Production Considerations

- **Cost Management**: GPT-4o-mini for cost-effective conversations
- **Error Handling**: Graceful handling of tool call failures
- **Monitoring**: Pushover notifications for real-time awareness of user interactions
- **Context Management**: Efficient loading of LinkedIn profile and summary
- **User Privacy**: Clear communication about data collection and follow-up

---

## Interview Talking Points

**Why Build from Scratch (No Framework)?**
- Deep understanding of tool calling mechanism (JSON + if statements)
- Full control over context engineering and system prompts
- Lightweight, no dependencies beyond OpenAI SDK
- Foundation for understanding higher-level frameworks

**Architecture Decisions:**
- **Context Engineering**: Rich system prompt with career summary and LinkedIn profile
- **Tool Design**: Two focused tools (lead capture, question logging) with clear purposes
- **Real-Time Notifications**: Pushover integration for immediate awareness
- **Professional Tone**: Calibrated for recruiters and employers

**Real-World Application:**
- Solves actual career networking problem
- Demonstrates understanding of agentic AI fundamentals
- Shows ability to integrate tools (Pushover API)
- Production deployment on personal website
- Continuous improvement via unknown question logging

**Technical Depth:**
- Understanding of tool calling mechanism (not just using a framework)
- Context engineering for reliable outputs
- Production considerations (error handling, monitoring, deployment)


