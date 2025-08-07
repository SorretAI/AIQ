"""
Tests for LYRA Prompt Optimizer

Tests the 4-D methodology implementation and core optimization functionality.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from mcp_agent.workflows.prompt_optimizer.lyra_optimizer import (
    LYRAOptimizer,
    OptimizationRequest,
    OptimizationResult,
    AIPlatform,
    OptimizationMode,
    RequestType
)


class TestLYRAOptimizer:
    """Test suite for LYRA prompt optimization workflow"""

    @pytest.fixture
    def mock_llm_factory(self):
        """Mock LLM factory for testing"""
        mock_llm = AsyncMock()
        mock_llm.generate_str.return_value = "Test response"
        mock_llm.generate_structured.return_value = {"test": "data"}
        
        factory = MagicMock()
        factory.return_value = mock_llm
        return factory

    @pytest.fixture
    async def lyra_optimizer(self, mock_llm_factory):
        """Create LYRA optimizer instance for testing"""
        optimizer = LYRAOptimizer(llm_factory=mock_llm_factory)
        return optimizer

    def test_welcome_message(self, lyra_optimizer):
        """Test that welcome message is properly formatted"""
        welcome = lyra_optimizer.get_welcome_message()
        
        assert "LYRA" in welcome
        assert "prompt optimizer" in welcome
        assert "ChatGPT, Claude, Gemini, or Other" in welcome
        assert "DETAIL" in welcome
        assert "BASIC" in welcome

    @pytest.mark.asyncio
    async def test_parse_request_basic_chatgpt(self, lyra_optimizer):
        """Test parsing a basic ChatGPT request"""
        user_input = "BASIC using ChatGPT — Write me a marketing email"
        
        request = await lyra_optimizer.parse_request(user_input)
        
        assert request.target_platform == AIPlatform.CHATGPT
        assert request.mode == OptimizationMode.BASIC
        assert "marketing email" in request.original_prompt

    @pytest.mark.asyncio
    async def test_parse_request_detail_claude(self, lyra_optimizer):
        """Test parsing a detail Claude request"""
        user_input = "DETAIL using Claude — Help with my resume"
        
        request = await lyra_optimizer.parse_request(user_input)
        
        assert request.target_platform == AIPlatform.CLAUDE
        assert request.mode == OptimizationMode.DETAIL
        assert "resume" in request.original_prompt

    @pytest.mark.asyncio
    async def test_parse_request_auto_complexity_detection(self, lyra_optimizer):
        """Test automatic complexity detection"""
        complex_input = "Create a comprehensive strategic analysis framework"
        
        request = await lyra_optimizer.parse_request(complex_input)
        
        # Should auto-detect as DETAIL mode due to complexity indicators
        assert request.mode == OptimizationMode.DETAIL

    @pytest.mark.asyncio
    async def test_deconstruct_step(self, lyra_optimizer):
        """Test the DECONSTRUCT step of 4-D methodology"""
        request = OptimizationRequest(
            original_prompt="Write a blog post",
            target_platform=AIPlatform.CHATGPT,
            mode=OptimizationMode.BASIC
        )
        
        # Mock the LLM response for deconstruction
        lyra_optimizer.llm.generate_structured.return_value = {
            "core_intent": "Create written content for a blog",
            "key_entities": ["blog", "post", "content"],
            "provided_context": "Basic request for blog content",
            "missing_context": "Topic, audience, length, tone",
            "output_requirements": "Blog post format",
            "constraints": []
        }
        
        result = await lyra_optimizer.deconstruct(request)
        
        assert "core_intent" in result
        assert "blog" in str(result.get("key_entities", []))

    @pytest.mark.asyncio
    async def test_diagnose_step(self, lyra_optimizer):
        """Test the DIAGNOSE step of 4-D methodology"""
        request = OptimizationRequest(
            original_prompt="Write something",
            target_platform=AIPlatform.CHATGPT,
            mode=OptimizationMode.BASIC
        )
        
        deconstruction = {
            "core_intent": "Create content",
            "missing_context": "Topic, format, audience"
        }
        
        # Mock diagnosis response
        lyra_optimizer.llm.generate_structured.return_value = {
            "clarity_issues": ["Vague request"],
            "specificity_problems": ["No specific topic"],
            "completeness_gaps": ["Missing audience info"],
            "structure_needs": ["Output format unclear"],
            "platform_opportunities": ["Can use structured sections"]
        }
        
        result = await lyra_optimizer.diagnose(request, deconstruction)
        
        assert "clarity_issues" in result
        assert "specificity_problems" in result

    @pytest.mark.asyncio
    async def test_classify_request_type(self, lyra_optimizer):
        """Test request type classification"""
        creative_deconstruction = {
            "core_intent": "Write a creative story",
            "key_entities": ["story", "creative", "narrative"]
        }
        
        lyra_optimizer.llm.generate_str.return_value = "CREATIVE"
        
        request_type = await lyra_optimizer.classify_request_type(creative_deconstruction)
        
        assert request_type == RequestType.CREATIVE

    @pytest.mark.asyncio
    async def test_develop_optimization(self, lyra_optimizer):
        """Test the DEVELOP step of 4-D methodology"""
        request = OptimizationRequest(
            original_prompt="Write a story",
            target_platform=AIPlatform.CHATGPT,
            mode=OptimizationMode.BASIC
        )
        
        deconstruction = {"core_intent": "Creative writing"}
        diagnosis = {"clarity_issues": ["Too vague"]}
        request_type = RequestType.CREATIVE
        
        # Mock development response
        lyra_optimizer.llm.generate_structured.return_value = {
            "optimized_prompt": "You are a creative writing expert. Write an engaging short story...",
            "applied_techniques": ["role_assignment", "multi_perspective"],
            "key_improvements": ["Added creative role", "Specified story structure"]
        }
        
        result = await lyra_optimizer.develop_optimization(
            request, deconstruction, diagnosis, request_type
        )
        
        assert "optimized_prompt" in result
        assert "applied_techniques" in result
        assert "key_improvements" in result

    @pytest.mark.asyncio
    async def test_generate_clarifying_questions(self, lyra_optimizer):
        """Test generation of clarifying questions for DETAIL mode"""
        deconstruction = {
            "core_intent": "Create marketing content",
            "missing_context": "Target audience, product details, campaign goals"
        }
        
        lyra_optimizer.llm.generate_str.return_value = """
        What specific product or service are you promoting?
        Who is your target audience?
        What's the main goal of this campaign?
        """
        
        questions = await lyra_optimizer.generate_clarifying_questions(deconstruction)
        
        assert len(questions) >= 2
        assert any("product" in q.lower() for q in questions)

    @pytest.mark.asyncio
    async def test_generate_pro_tip(self, lyra_optimizer):
        """Test generation of usage guidance"""
        request = OptimizationRequest(
            original_prompt="Test prompt",
            target_platform=AIPlatform.CHATGPT,
            mode=OptimizationMode.BASIC
        )
        
        optimization = {"optimized_prompt": "Optimized test prompt"}
        
        lyra_optimizer.llm.generate_str.return_value = "Test your prompt with different examples to ensure consistency."
        
        tip = await lyra_optimizer.generate_pro_tip(request, optimization)
        
        assert isinstance(tip, str)
        assert len(tip) > 10

    def test_format_response_simple(self, lyra_optimizer):
        """Test simple response formatting"""
        result = OptimizationResult(
            optimized_prompt="Optimized prompt here",
            improvements=["Better clarity", "Added structure"],
            techniques_applied=["role_assignment"]
        )
        
        formatted = lyra_optimizer.format_response(result, is_simple=True)
        
        assert "Your Optimized Prompt:" in formatted
        assert "What Changed:" in formatted
        assert result.optimized_prompt in formatted

    def test_format_response_complex(self, lyra_optimizer):
        """Test complex response formatting"""
        result = OptimizationResult(
            optimized_prompt="Optimized prompt here",
            improvements=["Better clarity", "Added structure", "Enhanced context"],
            techniques_applied=["role_assignment", "chain_of_thought"],
            pro_tip="Use this with specific examples",
            clarifying_questions=["What's your goal?", "Who's the audience?"]
        )
        
        formatted = lyra_optimizer.format_response(result, is_simple=False)
        
        assert "Your Optimized Prompt:" in formatted
        assert "Key Improvements:" in formatted
        assert "Techniques Applied:" in formatted
        assert "Pro Tip:" in formatted
        assert "Questions to consider:" in formatted

    @pytest.mark.asyncio
    async def test_optimization_techniques_mapping(self, lyra_optimizer):
        """Test that optimization techniques are properly mapped"""
        assert RequestType.CREATIVE in lyra_optimizer.optimization_techniques
        assert RequestType.TECHNICAL in lyra_optimizer.optimization_techniques
        assert RequestType.EDUCATIONAL in lyra_optimizer.optimization_techniques
        assert RequestType.COMPLEX in lyra_optimizer.optimization_techniques
        
        creative_techniques = lyra_optimizer.optimization_techniques[RequestType.CREATIVE]
        assert "multi_perspective" in creative_techniques
        assert "tone_emphasis" in creative_techniques

    def test_platform_adaptations_mapping(self, lyra_optimizer):
        """Test that platform adaptations are properly configured"""
        assert AIPlatform.CHATGPT in lyra_optimizer.platform_adaptations
        assert AIPlatform.CLAUDE in lyra_optimizer.platform_adaptations
        assert AIPlatform.GEMINI in lyra_optimizer.platform_adaptations
        assert AIPlatform.OTHER in lyra_optimizer.platform_adaptations
        
        chatgpt_adaptation = lyra_optimizer.platform_adaptations[AIPlatform.CHATGPT]
        assert "structured_sections" in chatgpt_adaptation

    @pytest.mark.asyncio
    async def test_full_optimization_workflow(self, lyra_optimizer):
        """Test the complete optimization workflow"""
        user_input = "BASIC using ChatGPT — Write me a blog post"
        
        # Mock all the intermediate steps
        lyra_optimizer.llm.generate_structured.side_effect = [
            # Deconstruct response
            {
                "core_intent": "Create blog content",
                "key_entities": ["blog", "post"],
                "provided_context": "Basic request",
                "missing_context": "Topic, audience",
                "output_requirements": "Blog post",
                "constraints": []
            },
            # Diagnose response
            {
                "clarity_issues": ["Vague topic"],
                "specificity_problems": ["No specific subject"],
                "completeness_gaps": ["Missing audience"],
                "structure_needs": ["Format unclear"],
                "platform_opportunities": ["Use sections"]
            },
            # Develop response
            {
                "optimized_prompt": "You are an expert blogger. Write a well-structured blog post...",
                "applied_techniques": ["role_assignment", "clear_structure"],
                "key_improvements": ["Added blogging expertise", "Structured format"]
            }
        ]
        
        # Mock classification response
        lyra_optimizer.llm.generate_str.side_effect = [
            "CREATIVE",  # Classification
            "Use engaging headlines to increase readability."  # Pro tip
        ]
        
        result = await lyra_optimizer.optimize_prompt(user_input)
        
        assert isinstance(result, OptimizationResult)
        assert result.optimized_prompt
        assert result.improvements
        assert result.techniques_applied
        assert result.pro_tip


class TestOptimizationModels:
    """Test the data models used in optimization"""

    def test_optimization_request_creation(self):
        """Test creating an OptimizationRequest"""
        request = OptimizationRequest(
            original_prompt="Test prompt",
            target_platform=AIPlatform.CHATGPT,
            mode=OptimizationMode.BASIC
        )
        
        assert request.original_prompt == "Test prompt"
        assert request.target_platform == AIPlatform.CHATGPT
        assert request.mode == OptimizationMode.BASIC

    def test_optimization_result_creation(self):
        """Test creating an OptimizationResult"""
        result = OptimizationResult(
            optimized_prompt="Optimized prompt",
            improvements=["Better clarity"],
            techniques_applied=["role_assignment"]
        )
        
        assert result.optimized_prompt == "Optimized prompt"
        assert result.improvements == ["Better clarity"]
        assert result.techniques_applied == ["role_assignment"]

    def test_enum_values(self):
        """Test enum value assignments"""
        assert AIPlatform.CHATGPT.value == "chatgpt"
        assert AIPlatform.CLAUDE.value == "claude"
        assert OptimizationMode.BASIC.value == "basic"
        assert OptimizationMode.DETAIL.value == "detail"
        assert RequestType.CREATIVE.value == "creative"