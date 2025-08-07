"""
LYRA Prompt Optimization Workflow

A specialized workflow that implements the 4-D methodology for prompt optimization:
- DECONSTRUCT: Extract core intent and requirements
- DIAGNOSE: Identify gaps and improvement opportunities  
- DEVELOP: Apply optimization techniques based on request type
- DELIVER: Construct optimized prompt with guidance
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from mcp_agent.workflows.llm.augmented_llm import AugmentedLLM
from mcp_agent.agents.agent import Agent
import re


class AIPlatform(Enum):
    CHATGPT = "chatgpt"
    CLAUDE = "claude"
    GEMINI = "gemini"
    OTHER = "other"


class OptimizationMode(Enum):
    BASIC = "basic"
    DETAIL = "detail"


class RequestType(Enum):
    CREATIVE = "creative"
    TECHNICAL = "technical"
    EDUCATIONAL = "educational"
    COMPLEX = "complex"


@dataclass
class OptimizationRequest:
    """Structured representation of a prompt optimization request"""
    original_prompt: str
    target_platform: AIPlatform
    mode: OptimizationMode
    request_type: Optional[RequestType] = None
    context: Optional[str] = None
    constraints: Optional[List[str]] = None
    output_requirements: Optional[str] = None


@dataclass
class OptimizationResult:
    """Result of prompt optimization with improvements and guidance"""
    optimized_prompt: str
    improvements: List[str]
    techniques_applied: List[str]
    pro_tip: Optional[str] = None
    clarifying_questions: Optional[List[str]] = None


class LYRAOptimizer(AugmentedLLM):
    """
    LYRA - Master-level AI prompt optimization specialist
    
    Implements the 4-D methodology:
    1. DECONSTRUCT - Extract core intent and requirements
    2. DIAGNOSE - Identify improvement opportunities
    3. DEVELOP - Apply optimization techniques
    4. DELIVER - Construct optimized prompt
    """
    
    def __init__(self, llm_factory, **kwargs):
        # Create the core optimizer agent
        optimizer_agent = Agent(
            name="lyra_optimizer",
            instruction="""You are LYRA, a master-level AI prompt optimization specialist.
            You transform any user input into precision-crafted prompts using the 4-D methodology.
            
            Your responses should be precise, helpful, and focused on delivering better AI results.""",
            server_names=[]  # LYRA doesn't need external MCP servers for core optimization
        )
        
        super().__init__(agent=optimizer_agent, llm_factory=llm_factory, **kwargs)
        
        self.optimization_techniques = {
            RequestType.CREATIVE: ["multi_perspective", "tone_emphasis", "creative_constraints"],
            RequestType.TECHNICAL: ["constraint_based", "precision_focus", "technical_specifications"],
            RequestType.EDUCATIONAL: ["few_shot_examples", "clear_structure", "learning_objectives"],
            RequestType.COMPLEX: ["chain_of_thought", "systematic_frameworks", "task_decomposition"]
        }
        
        self.platform_adaptations = {
            AIPlatform.CHATGPT: "structured_sections_conversation_starters",
            AIPlatform.CLAUDE: "longer_context_reasoning_frameworks",
            AIPlatform.GEMINI: "creative_tasks_comparative_analysis",
            AIPlatform.OTHER: "universal_best_practices"
        }

    def get_welcome_message(self) -> str:
        """Return the required welcome message"""
        return """Hello! I'm LYRA, your AI prompt optimizer. I transform vague requests into precise, effective prompts that deliver better results.

**What I need to know:**
- **Target AI:** ChatGPT, Claude, Gemini, or Other
- **Prompt Style:** DETAIL (I'll ask clarifying questions first) or BASIC (quick optimization)

**Examples:**
- "DETAIL using ChatGPT — Write me a marketing email"
- "BASIC using Claude — Help with my resume"

Just share your rough prompt and I'll handle the optimization!"""

    async def parse_request(self, user_input: str) -> OptimizationRequest:
        """Parse user input to extract optimization parameters"""
        
        # Extract platform
        platform = AIPlatform.OTHER
        for p in AIPlatform:
            if p.value.lower() in user_input.lower():
                platform = p
                break
                
        # Extract mode
        mode = OptimizationMode.BASIC
        if "detail" in user_input.lower():
            mode = OptimizationMode.DETAIL
        elif "basic" in user_input.lower():
            mode = OptimizationMode.BASIC
        else:
            # Auto-detect complexity
            complexity_indicators = ["professional", "comprehensive", "detailed", "complex", "analysis", "strategy"]
            if any(indicator in user_input.lower() for indicator in complexity_indicators):
                mode = OptimizationMode.DETAIL
        
        # Extract the actual prompt (remove mode/platform instructions)
        prompt_text = user_input
        for prefix in ["detail using", "basic using", "chatgpt", "claude", "gemini", "other"]:
            prompt_text = re.sub(rf"{prefix}[^\w]*", "", prompt_text, flags=re.IGNORECASE)
        prompt_text = re.sub(r"^[—-]+\s*", "", prompt_text.strip())
        
        return OptimizationRequest(
            original_prompt=prompt_text.strip(),
            target_platform=platform,
            mode=mode
        )

    async def deconstruct(self, request: OptimizationRequest) -> Dict[str, Any]:
        """Step 1: DECONSTRUCT - Extract core intent and requirements"""
        
        deconstruction_prompt = f"""
        Analyze this prompt request and extract key information:
        
        Original: "{request.original_prompt}"
        
        Extract:
        1. Core intent (what does the user really want?)
        2. Key entities mentioned
        3. Context provided vs missing
        4. Output requirements (explicit or implied)
        5. Constraints mentioned
        
        Respond in JSON format with these keys: core_intent, key_entities, provided_context, missing_context, output_requirements, constraints
        """
        
        result = await self.generate_structured(
            message=deconstruction_prompt,
            response_model=dict
        )
        
        return result

    async def diagnose(self, request: OptimizationRequest, deconstruction: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2: DIAGNOSE - Identify gaps and improvement opportunities"""
        
        diagnosis_prompt = f"""
        Diagnose issues with this prompt:
        
        Original: "{request.original_prompt}"
        Core intent: {deconstruction.get('core_intent', 'Unknown')}
        
        Audit for:
        1. Clarity gaps and ambiguity
        2. Specificity issues
        3. Completeness problems
        4. Structure needs
        5. Platform optimization opportunities for {request.target_platform.value}
        
        Respond with: clarity_issues, specificity_problems, completeness_gaps, structure_needs, platform_opportunities
        """
        
        result = await self.generate_structured(
            message=diagnosis_prompt,
            response_model=dict
        )
        
        return result

    async def classify_request_type(self, deconstruction: Dict[str, Any]) -> RequestType:
        """Classify the request to determine optimization strategy"""
        
        classification_prompt = f"""
        Based on this analysis, classify the request type:
        
        Core intent: {deconstruction.get('core_intent', '')}
        Key entities: {deconstruction.get('key_entities', '')}
        
        Choose ONE:
        - CREATIVE: Writing, storytelling, brainstorming, artistic tasks
        - TECHNICAL: Code, analysis, research, factual tasks
        - EDUCATIONAL: Teaching, explaining, learning, tutorials
        - COMPLEX: Multi-step, strategic, comprehensive tasks
        
        Respond with only the classification: CREATIVE, TECHNICAL, EDUCATIONAL, or COMPLEX
        """
        
        result = await self.generate_str(message=classification_prompt)
        
        try:
            return RequestType(result.strip().lower())
        except ValueError:
            return RequestType.COMPLEX  # Default fallback

    async def develop_optimization(
        self, 
        request: OptimizationRequest, 
        deconstruction: Dict[str, Any],
        diagnosis: Dict[str, Any],
        request_type: RequestType
    ) -> Dict[str, Any]:
        """Step 3: DEVELOP - Apply optimization techniques"""
        
        techniques = self.optimization_techniques[request_type]
        platform_adaptation = self.platform_adaptations[request.target_platform]
        
        development_prompt = f"""
        Develop an optimized prompt using these techniques:
        
        Original: "{request.original_prompt}"
        Request type: {request_type.value}
        Target platform: {request.target_platform.value}
        
        Apply these techniques: {', '.join(techniques)}
        Platform adaptation: {platform_adaptation}
        
        Issues to fix:
        - Clarity: {diagnosis.get('clarity_issues', [])}
        - Specificity: {diagnosis.get('specificity_problems', [])}
        - Completeness: {diagnosis.get('completeness_gaps', [])}
        
        Create an optimized prompt that:
        1. Assigns appropriate AI role/expertise
        2. Enhances context and clarity
        3. Implements logical structure
        4. Applies platform-specific formatting
        5. Addresses all identified issues
        
        Respond with: optimized_prompt, applied_techniques, key_improvements
        """
        
        result = await self.generate_structured(
            message=development_prompt,
            response_model=dict
        )
        
        return result

    async def generate_clarifying_questions(self, deconstruction: Dict[str, Any]) -> List[str]:
        """Generate 2-3 targeted clarifying questions for DETAIL mode"""
        
        questions_prompt = f"""
        Based on this analysis, generate 2-3 targeted clarifying questions:
        
        Core intent: {deconstruction.get('core_intent', '')}
        Missing context: {deconstruction.get('missing_context', '')}
        
        Questions should:
        - Fill critical information gaps
        - Be specific and actionable
        - Help improve the final prompt
        
        Return as a simple list, one question per line.
        """
        
        result = await self.generate_str(message=questions_prompt)
        return [q.strip() for q in result.split('\n') if q.strip()]

    async def generate_pro_tip(self, request: OptimizationRequest, optimization: Dict[str, Any]) -> str:
        """Generate usage guidance for the optimized prompt"""
        
        tip_prompt = f"""
        Generate a concise pro tip for using this optimized prompt:
        
        Platform: {request.target_platform.value}
        Optimization: {optimization.get('optimized_prompt', '')[:200]}...
        
        Provide actionable advice for getting the best results.
        Keep it to 1-2 sentences.
        """
        
        return await self.generate_str(message=tip_prompt)

    async def optimize_prompt(self, user_input: str) -> OptimizationResult:
        """
        Main optimization method implementing the 4-D methodology
        """
        
        # Parse the request
        request = await self.parse_request(user_input)
        
        # 1. DECONSTRUCT
        deconstruction = await self.deconstruct(request)
        
        # 2. DIAGNOSE  
        diagnosis = await self.diagnose(request, deconstruction)
        
        # Classify request type
        request_type = await self.classify_request_type(deconstruction)
        
        # 3. DEVELOP
        optimization = await self.develop_optimization(request, deconstruction, diagnosis, request_type)
        
        # 4. DELIVER - Prepare final result
        result = OptimizationResult(
            optimized_prompt=optimization.get('optimized_prompt', ''),
            improvements=optimization.get('key_improvements', []),
            techniques_applied=optimization.get('applied_techniques', [])
        )
        
        # Add clarifying questions for DETAIL mode
        if request.mode == OptimizationMode.DETAIL:
            result.clarifying_questions = await self.generate_clarifying_questions(deconstruction)
        
        # Add pro tip
        result.pro_tip = await self.generate_pro_tip(request, optimization)
        
        return result

    def format_response(self, result: OptimizationResult, is_simple: bool = True) -> str:
        """Format the optimization result according to complexity"""
        
        if is_simple:
            return f"""**Your Optimized Prompt:**
{result.optimized_prompt}

**What Changed:** {', '.join(result.improvements[:3])}"""
        
        else:
            response = f"""**Your Optimized Prompt:**
{result.optimized_prompt}

**Key Improvements:**
"""
            for improvement in result.improvements:
                response += f"• {improvement}\n"
            
            response += f"\n**Techniques Applied:** {', '.join(result.techniques_applied)}"
            
            if result.pro_tip:
                response += f"\n\n**Pro Tip:** {result.pro_tip}"
            
            if result.clarifying_questions:
                response += "\n\n**Questions to consider:**\n"
                for i, question in enumerate(result.clarifying_questions, 1):
                    response += f"{i}. {question}\n"
            
            return response

    async def generate_str(self, message: str, **kwargs) -> str:
        """
        Override to implement LYRA's optimization workflow
        """
        
        # Check if this is the initial greeting
        if not hasattr(self, '_greeted'):
            self._greeted = True
            return self.get_welcome_message()
        
        # Process optimization request
        try:
            result = await self.optimize_prompt(message)
            
            # Determine if this is a simple or complex request
            is_simple = len(result.improvements) <= 3 and not result.clarifying_questions
            
            return self.format_response(result, is_simple)
            
        except Exception as e:
            return f"I encountered an issue optimizing your prompt: {str(e)}. Please try rephrasing your request."