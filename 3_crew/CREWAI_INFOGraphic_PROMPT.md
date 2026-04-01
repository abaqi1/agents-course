# CrewAI Infographic Generation Prompt for NANO BANANA PRO

## Main Prompt

Create a professional, educational infographic about CrewAI Framework - a multi-agent AI orchestration platform. The design should be modern, technical, and visually organized with clear sections, icons, and flow diagrams.

## Visual Style
- **Color Scheme**: Modern tech palette - primary blue (#0066FF), secondary purple (#6B46C1), accent green (#10B981), neutral grays for text
- **Style**: Clean, minimalist, technical illustration style with subtle gradients
- **Layout**: Vertical scroll-friendly layout with clear sections and visual hierarchy
- **Typography**: Bold sans-serif headers, readable body text
- **Icons**: Modern, flat design icons for each concept

## Content Structure & Visual Elements

### HEADER SECTION (Top)
- **Title**: "CrewAI Framework: Multi-Agent AI Orchestration" in large, bold text
- **Subtitle**: "Build autonomous AI teams that collaborate to solve complex problems"
- **Logo/Icon**: Abstract representation of multiple connected AI agents forming a team

### SECTION 1: Core Building Blocks (Left Column, Top)
**Title**: "Core Components"

**1. AGENTS** (with icon of person/robot figure)
- Visual: Single agent card/box with labeled components inside
- Text: "Autonomous AI units - the building blocks of CrewAI"
- Show: One agent card broken down into its construct components:
  - **Role**: What the agent does (e.g., "Researcher", "Engineer")
  - **Goal**: What the agent aims to achieve
  - **Backstory**: Context and expertise that shapes behavior
  - **LLM**: The language model powering the agent (can vary per agent)
  - **Tools**: External capabilities (APIs, search, custom functions)
  - **Memory**: Context retention (enabled/disabled)
- Visual element: LLM brain icon at center, with components arranged around it
- Sub-text: "Each agent is a specialized AI unit with defined purpose and capabilities"

**2. TASKS** (with icon of checklist/clipboard)
- Visual: Task box with labeled components, connected to other tasks
- Text: "Specific assignments - the work to be done"
- Show: One task box broken down into its construct components:
  - **Description**: What needs to be accomplished
  - **Expected Output**: What the task should produce
  - **Agent Assignment**: Which agent performs this task
  - **Context**: References to other tasks (for data flow)
  - **Output Format**: Structured (Pydantic) or unstructured (text/markdown)
- Visual element: Task box with input arrow (context) and output arrow (result)
- Sub-text: "Tasks define specific work assignments with clear inputs and outputs"
- Show connection: Task 1 output → Task 2 context → Task 3 context (demonstrating context passing)

**3. CREWS** (with icon of team/group)
- Visual: Large container box holding multiple agents and tasks
- Text: "Orchestrated teams of agents and tasks working together"
- Show: Crew box containing agent cards and task boxes
- Visual element: Process indicators (Sequential vs Hierarchical)

### SECTION 2: Process Types (Center, Top)
**Title**: "Execution Processes"

**Sequential Process** (Left side)
- Visual: Horizontal flow diagram
- Icon: Linear arrow → → →
- Text: "Tasks execute in order, one after another"
- Show: Task boxes in a straight line with sequential numbering

**Hierarchical Process** (Right side)
- Visual: Tree/organizational chart structure
- Icon: Manager at top, workers below
- Text: "Manager agent delegates tasks to specialized agents"
- Show: Manager agent at top, branching to worker agents below
- Visual element: Decision/delegation nodes

### SECTION 3: Advanced Features (Right Column, Top)
**Title**: "Advanced Capabilities"

**TOOLS** (with icon of wrench/toolbox)
- Visual: Tools connected to agent cards
- Text: "Extend agent capabilities (web search, APIs, custom functions)"
- Show: Tool icons (search, API, custom) attached to agent cards
- Examples: SerperDevTool, Binance API, PushNotificationTool

**MEMORY SYSTEMS** (with icon of brain/database)
- Visual: Four memory types as connected nodes
- Text: "Context retention across sessions"
- Show: Four boxes:
  - Short-Term Memory (RAG/Vector DB icon)
  - Long-Term Memory (SQLite/DB icon)
  - Entity Memory (RAG icon with entity tags)
  - User Memory (user profile icon)

**CODE EXECUTION** (with icon of code/Docker container)
- Visual: Code block inside Docker container
- Text: "Safe code generation and testing in isolated containers"
- Show: Python code snippet inside a Docker container box
- Visual element: Safety shield around container

**STRUCTURED OUTPUTS** (with icon of JSON/schema)
- Visual: Pydantic model structure diagram
- Text: "Type-safe task results with Pydantic models"
- Show: Schema diagram with fields and types
- Visual element: Validation checkmark

### SECTION 4: Workflow Example (Center, Middle)
**Title**: "Example: Crypto Trading Platform Crew"

**Visual Flow Diagram**:
1. **Research Crew** (Hierarchical) - Left side
   - Manager Agent (top)
   - Crypto Finder Agent → Crypto Researcher Agent → Crypto Picker Agent (below)
   - Connected with delegation arrows
   - Memory icons attached

2. **Engineering Crew** (Sequential) - Right side
   - Engineering Lead → Backend Engineer → Frontend Engineer → Test Engineer
   - Connected in linear sequence
   - Code execution icons on Backend and Test engineers
   - Tools (Binance API) attached to Backend Engineer

3. **Connection**: Arrow from Research Crew to Engineering Crew showing data flow

### SECTION 5: Technical Stack (Bottom Left)
**Title**: "Technology Stack"
- Visual: Technology logos/icons in a grid
- Items: Python, Docker, Pydantic, YAML, LiteLLM, Gradio
- Each with small icon and label

### SECTION 6: Key Benefits (Bottom Right)
**Title**: "Why CrewAI?"
- Visual: Checkmark list with icons
- Items:
  - ✓ Fast development with built-in features
  - ✓ Multi-model support (OpenAI, Anthropic, local)
  - ✓ Built-in memory and code execution
  - ✓ Clean YAML + decorator pattern
  - ✓ Production-ready observability

### FOOTER (Bottom)
- **Tagline**: "Orchestrate high-performance AI agents with ease and scale"
- **Visual**: Small connected network of agent nodes
- **Credits/Version**: "CrewAI Framework"

## Visual Flow Requirements
- Use connecting lines/arrows to show relationships
- Color-code different types of elements (agents = blue, tasks = purple, tools = green)
- Use consistent spacing and alignment
- Make it scannable - important concepts should stand out
- Include subtle background patterns or grids for structure

## Specific Visual Details
- **Agent Cards**: Rounded rectangles with icon, role name, and small tool icons
- **Task Boxes**: Rectangular boxes with task name and context indicators
- **Crew Container**: Large rounded rectangle with border containing agents and tasks
- **Memory Icons**: Different shapes for each memory type (circle, square, hexagon, triangle)
- **Process Indicators**: Different arrow styles (solid for sequential, dashed for hierarchical)
- **Tool Connections**: Small lines/connectors from tools to agents

## Text Hierarchy
- **Main Title**: 48-60pt, bold, primary blue
- **Section Titles**: 24-32pt, bold, dark gray
- **Concept Names**: 18-20pt, semi-bold, primary color
- **Descriptions**: 12-14pt, regular, dark gray
- **Labels**: 10-12pt, regular, medium gray

## Additional Visual Elements
- Subtle gradient backgrounds for sections
- Shadow effects on cards/boxes for depth
- Icons should be consistent style (flat, modern, minimal)
- Use arrows and connectors to show data flow and relationships
- Include small code snippets or YAML examples as visual elements (stylized, not full code)

---

## Alternative: Simplified Single-Page Version

If the above is too complex, create a simplified version with:

1. **Header**: Title and subtitle
2. **Central Diagram**: Large CrewAI ecosystem diagram showing:
   - Crew container in center
   - Agents around the perimeter
   - Tasks flowing between agents
   - Tools attached to agents
   - Memory systems connected
3. **Side Panels**: 
   - Left: Process types (Sequential vs Hierarchical)
   - Right: Key features (Tools, Memory, Code Execution, Structured Outputs)
4. **Footer**: Tech stack and benefits

---

## Prompt for Image Generator (Concise Version)

"Create a professional technical infographic about CrewAI multi-agent AI framework. Modern design with blue/purple/green color scheme. Show: 1) Core components: AGENTS construct (breakdown showing Role, Goal, Backstory, LLM, Tools, Memory as labeled components within an agent card), TASKS construct (breakdown showing Description, Expected Output, Agent Assignment, Context, Output Format as labeled components within a task box with input/output arrows), CREWS (container holding agents and tasks), 2) Two process types (Sequential linear flow vs Hierarchical tree structure), 3) Advanced features (Tools, Memory systems, Code execution, Structured outputs) as labeled sections, 4) Example workflow diagram showing Research Crew and Engineering Crew, 5) Technology stack icons, 6) Key benefits checklist. Use clean lines, arrows for connections, consistent iconography, professional typography. Vertical layout suitable for documentation or presentation. Technical illustration style, minimalist, educational."
