# LYRA - AI Prompt Optimization Specialist

<p align="center">
  <em>Transform vague requests into precision-crafted prompts using the 4-D methodology</em>
</p>

LYRA is a master-level AI prompt optimization specialist built on the MCP Agent framework. It transforms any user input into precision-crafted prompts that unlock AI's full potential across all platforms.

## 🎯 The 4-D Methodology

LYRA follows a systematic approach to prompt optimization:

### 1. **DECONSTRUCT**
- Extract core intent, key entities, and context
- Identify output requirements and constraints  
- Map what's provided vs. what's missing

### 2. **DIAGNOSE**
- Audit for clarity gaps and ambiguity
- Check specificity and completeness
- Assess structure and complexity needs

### 3. **DEVELOP**
- Select optimal techniques based on request type:
  - **Creative** → Multi-perspective + tone emphasis
  - **Technical** → Constraint-based + precision focus
  - **Educational** → Few-shot examples + clear structure
  - **Complex** → Chain-of-thought + systematic frameworks
- Assign appropriate AI role/expertise
- Enhance context and implement logical structure

### 4. **DELIVER**
- Construct optimized prompt
- Format based on complexity
- Provide implementation guidance

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd LYRA

# Install dependencies
uv add "mcp-agent"

# Set up API keys
cp examples/lyra_prompt_optimizer/mcp_agent.secrets.yaml.example examples/lyra_prompt_optimizer/mcp_agent.secrets.yaml
# Edit with your OpenAI/Anthropic API keys
```

### CLI Usage
```bash
# Interactive mode
./lyra_cli.py --interactive

# Single prompt optimization
./lyra_cli.py "Write me a marketing email" --platform chatgpt --mode basic

# Batch processing
./lyra_cli.py --file prompts.txt --platform claude --mode detail

# Get help and examples
./lyra_cli.py --examples
```

### Python API
```python
from mcp_agent.workflows.prompt_optimizer import LYRAOptimizer
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

lyra = LYRAOptimizer(llm_factory=OpenAIAugmentedLLM)

async with lyra:
    result = await lyra.generate_str("BASIC using ChatGPT — Write me a marketing email")
    print(result)
```

## 💡 Operating Modes

### **BASIC Mode**
- Quick fix primary issues
- Apply core techniques only  
- Deliver ready-to-use prompt

**Example:**
```
BASIC using ChatGPT — Write me a marketing email
```

### **DETAIL Mode**
- Gather context with smart defaults
- Ask 2-3 targeted clarifying questions
- Provide comprehensive optimization

**Example:**
```
DETAIL using Claude — Help with my resume
```

## 🎨 Supported Platforms

- **ChatGPT/GPT-4:** Structured sections, conversation starters
- **Claude:** Longer context, reasoning frameworks
- **Gemini:** Creative tasks, comparative analysis  
- **Others:** Universal best practices

## 🔧 Optimization Techniques

### Foundation Techniques
- **Role Assignment:** Expert persona selection
- **Context Layering:** Rich background information
- **Output Specifications:** Clear deliverable definitions
- **Task Decomposition:** Breaking complex requests into steps

### Advanced Techniques
- **Chain-of-Thought:** Step-by-step reasoning frameworks
- **Few-Shot Learning:** Relevant examples and patterns
- **Multi-Perspective:** Multiple viewpoint analysis
- **Constraint Optimization:** Boundary and requirement management

## 📋 Example Session

```bash
$ ./lyra_cli.py --interactive

Hello! I'm LYRA, your AI prompt optimizer. I transform vague requests into precision-crafted prompts that deliver better results.

📝 Enter prompt to optimize: DETAIL using ChatGPT — Write me a marketing email

🔄 LYRA is optimizing your prompt...

**Your Optimized Prompt:**
You are an expert marketing copywriter with 10+ years of experience in email marketing.

Create a compelling marketing email that:
- Has a clear subject line that increases open rates
- Uses persuasive but authentic language
- Includes a specific call-to-action
- Is optimized for mobile viewing
- Follows email marketing best practices

Context needed:
- What product/service are you promoting?
- Who is your target audience?
- What's the main goal (sales, sign-ups, awareness)?
- What tone should the email have (professional, casual, urgent)?

Format: Provide the subject line, email body, and CTA separately.

**Key Improvements:**
• Added expert role assignment for authority
• Specified clear deliverables and structure
• Included mobile optimization consideration
• Added context-gathering questions for personalization

**Techniques Applied:** role_assignment, constraint_based, clear_structure

**Pro Tip:** Use A/B testing with different subject lines to optimize open rates.

**Questions to consider:**
1. What specific product or service are you promoting?
2. Who is your target audience (demographics, interests, pain points)?
3. What's the primary goal - drive sales, increase sign-ups, or build awareness?
```

## 🏗️ Architecture

LYRA is built as a specialized workflow within the MCP Agent framework:

```
LYRA Optimizer
├── 4-D Methodology Engine
│   ├── Deconstruct (Intent Extraction)
│   ├── Diagnose (Gap Analysis)  
│   ├── Develop (Technique Application)
│   └── Deliver (Prompt Construction)
├── Request Classification
│   ├── Platform Detection (ChatGPT/Claude/Gemini/Other)
│   ├── Mode Selection (Basic/Detail)
│   └── Type Classification (Creative/Technical/Educational/Complex)
├── Optimization Techniques Library
│   ├── Foundation Techniques
│   ├── Advanced Techniques
│   └── Platform-Specific Adaptations
└── Response Formatting
    ├── Simple Format (Basic requests)
    ├── Complex Format (Detail requests)
    └── Guidance Generation (Pro tips, questions)
```

## 🧪 Testing

```bash
# Run the test suite
cd LYRA
uv run pytest tests/workflows/prompt_optimizer/ -v

# Test specific functionality
uv run pytest tests/workflows/prompt_optimizer/test_lyra_optimizer.py::TestLYRAOptimizer::test_4d_methodology -v
```

## 🔄 Integration with MCP Agent Framework

LYRA seamlessly integrates with the existing MCP Agent ecosystem:

- **Composable:** Can be combined with other workflow patterns
- **Extensible:** Easy to add new optimization techniques
- **Configurable:** Customizable via MCP Agent config files
- **Observable:** Full logging and monitoring support

### Use as a Workflow Component
```python
from mcp_agent.workflows.orchestrator import Orchestrator
from mcp_agent.workflows.prompt_optimizer import LYRAOptimizer

# Use LYRA as part of a larger orchestrated workflow
orchestrator = Orchestrator(
    available_agents=[finder_agent, writer_agent],
    planner=LYRAOptimizer(llm_factory=OpenAIAugmentedLLM)  # LYRA as planner
)
```

## 📚 Advanced Usage

### Batch Processing
```python
prompts = [
    "Create a workout plan",
    "Write a business proposal", 
    "Explain quantum computing"
]

for prompt in prompts:
    result = await lyra.optimize_prompt(f"BASIC using ChatGPT — {prompt}")
    print(f"Optimized: {result.optimized_prompt}")
```

### Custom Configuration
```yaml
# mcp_agent.config.yaml
lyra:
  default_platform: chatgpt
  default_mode: basic
  max_clarifying_questions: 3
  enable_batch_processing: true
  
  optimization_techniques:
    creative: ["multi_perspective", "tone_emphasis", "creative_constraints"]
    technical: ["constraint_based", "precision_focus", "technical_specifications"]
```

## 🤝 Contributing

We welcome contributions to improve LYRA! Areas for enhancement:

- New optimization techniques
- Additional platform adaptations
- Enhanced request classification
- Performance improvements
- Additional test coverage

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on the [MCP Agent framework](https://github.com/lastmile-ai/mcp-agent)
- Inspired by Anthropic's research on effective AI agents
- Implements Model Context Protocol standards

---

**Transform your prompts. Unlock AI's potential. Experience LYRA.**