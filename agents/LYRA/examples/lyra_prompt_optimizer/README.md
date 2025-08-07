# LYRA Prompt Optimizer

LYRA is a master-level AI prompt optimization specialist that transforms vague requests into precision-crafted prompts using the **4-D methodology**.

## The 4-D Methodology

1. **DECONSTRUCT** - Extract core intent, key entities, and context
2. **DIAGNOSE** - Audit for clarity gaps and ambiguity  
3. **DEVELOP** - Apply optimization techniques based on request type
4. **DELIVER** - Construct optimized prompt with guidance

## Quick Start

1. **Setup credentials:**
   ```bash
   cp mcp_agent.secrets.yaml.example mcp_agent.secrets.yaml
   # Edit mcp_agent.secrets.yaml with your API keys
   ```

2. **Install dependencies:**
   ```bash
   cd /path/to/LYRA
   uv add "mcp-agent"
   ```

3. **Run LYRA:**
   ```bash
   cd examples/lyra_prompt_optimizer
   uv run main.py
   ```

## Usage Examples

### Basic Mode (Quick Optimization)
```
BASIC using ChatGPT — Write me a marketing email
```

### Detail Mode (With Clarifying Questions)
```
DETAIL using Claude — Help with my resume
```

### Supported Platforms
- **ChatGPT/GPT-4** - Structured sections, conversation starters
- **Claude** - Longer context, reasoning frameworks  
- **Gemini** - Creative tasks, comparative analysis
- **Other** - Universal best practices

## Optimization Techniques

### Foundation Techniques
- Role assignment
- Context layering
- Output specifications
- Task decomposition

### Advanced Techniques
- Chain-of-thought reasoning
- Few-shot learning examples
- Multi-perspective analysis
- Constraint optimization

### Request Type Strategies
- **Creative** → Multi-perspective + tone emphasis
- **Technical** → Constraint-based + precision focus
- **Educational** → Few-shot examples + clear structure
- **Complex** → Chain-of-thought + systematic frameworks

## Operating Modes

### BASIC Mode
- Quick fix for primary issues
- Apply core techniques only
- Deliver ready-to-use prompt

### DETAIL Mode
- Gather context with smart defaults
- Ask 2-3 targeted clarifying questions
- Provide comprehensive optimization

## Example Session

```
📝 Enter your prompt to optimize: DETAIL using ChatGPT — Write me a marketing email

🔄 LYRA is analyzing and optimizing your prompt...

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
1. What specific product or service are you promoting in this email?
2. Who is your target audience (demographics, interests, pain points)?
3. What's the primary goal - drive sales, increase sign-ups, or build awareness?
```

## Integration with MCP Agent Framework

LYRA is built on the MCP Agent framework and can be:

- **Standalone** - Run as an independent prompt optimization service
- **Integrated** - Embedded into other MCP Agent workflows
- **Composable** - Combined with other workflow patterns

## Configuration

Customize LYRA's behavior in `mcp_agent.config.yaml`:

```yaml
lyra:
  default_platform: chatgpt
  default_mode: basic
  enable_batch_processing: true
  max_clarifying_questions: 3
```

## API Usage

```python
from mcp_agent.workflows.prompt_optimizer import LYRAOptimizer
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

lyra = LYRAOptimizer(llm_factory=OpenAIAugmentedLLM)

async with lyra:
    result = await lyra.generate_str("BASIC using ChatGPT — Write me a marketing email")
    print(result)
```