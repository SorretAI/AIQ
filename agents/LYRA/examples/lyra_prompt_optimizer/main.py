"""
LYRA Prompt Optimizer Example

Demonstrates the LYRA prompt optimization system using the 4-D methodology.
This example shows how to use LYRA to transform vague prompts into precision-crafted ones.
"""

import asyncio
import os
from mcp_agent.app import MCPApp
from mcp_agent.workflows.prompt_optimizer.lyra_optimizer import LYRAOptimizer
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm_anthropic import AnthropicAugmentedLLM

app = MCPApp(name="lyra_prompt_optimizer")

async def interactive_session():
    """Run an interactive LYRA prompt optimization session"""
    
    async with app.run() as mcp_agent_app:
        logger = mcp_agent_app.logger
        
        # Initialize LYRA optimizer with OpenAI as the backend LLM
        # You can also use AnthropicAugmentedLLM for Claude backend
        lyra = LYRAOptimizer(llm_factory=OpenAIAugmentedLLM)
        
        async with lyra:
            logger.info("LYRA Prompt Optimizer initialized")
            
            # Display welcome message
            welcome = lyra.get_welcome_message()
            print("\n" + "="*60)
            print(welcome)
            print("="*60 + "\n")
            
            # Interactive loop
            while True:
                try:
                    user_input = input("\n📝 Enter your prompt to optimize (or 'quit' to exit): ")
                    
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        print("👋 Thanks for using LYRA!")
                        break
                    
                    if not user_input.strip():
                        continue
                    
                    print("\n🔄 LYRA is analyzing and optimizing your prompt...\n")
                    
                    # Optimize the prompt using LYRA
                    result = await lyra.generate_str(user_input)
                    
                    print("✨ " + "="*50)
                    print(result)
                    print("="*50)
                    
                except KeyboardInterrupt:
                    print("\n👋 Thanks for using LYRA!")
                    break
                except Exception as e:
                    logger.error(f"Error during optimization: {e}")
                    print(f"❌ Sorry, I encountered an error: {e}")

async def demo_examples():
    """Run predefined examples to demonstrate LYRA's capabilities"""
    
    async with app.run() as mcp_agent_app:
        logger = mcp_agent_app.logger
        
        # Initialize LYRA
        lyra = LYRAOptimizer(llm_factory=OpenAIAugmentedLLM)
        
        async with lyra:
            logger.info("Running LYRA demonstration examples")
            
            # Example prompts to optimize
            examples = [
                "BASIC using ChatGPT — Write me a marketing email",
                "DETAIL using Claude — Help with my resume",
                "BASIC using Gemini — Create a story about a robot",
                "DETAIL using ChatGPT — Analyze this business proposal for investment potential",
                "BASIC using Other — Explain quantum computing"
            ]
            
            print("\n🚀 LYRA Demonstration Examples")
            print("="*60)
            
            for i, example in enumerate(examples, 1):
                print(f"\n📋 Example {i}: {example}")
                print("-" * 40)
                
                try:
                    result = await lyra.generate_str(example)
                    print(result)
                    print("-" * 40)
                    
                    # Add a small delay between examples
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error in example {i}: {e}")
                    print(f"❌ Error: {e}")

async def batch_optimization():
    """Demonstrate batch optimization of multiple prompts"""
    
    async with app.run() as mcp_agent_app:
        logger = mcp_agent_app.logger
        
        lyra = LYRAOptimizer(llm_factory=OpenAIAugmentedLLM)
        
        async with lyra:
            logger.info("Running batch optimization example")
            
            # Batch of prompts to optimize
            batch_prompts = [
                "Make me a workout plan",
                "Help me learn Python programming",
                "Write a blog post about AI",
                "Analyze market trends for tech stocks",
                "Create a recipe for dinner"
            ]
            
            print("\n📦 Batch Optimization Demo")
            print("="*60)
            
            for i, prompt in enumerate(batch_prompts, 1):
                print(f"\n🔧 Optimizing prompt {i}: '{prompt}'")
                print("-" * 50)
                
                # Default to BASIC mode with ChatGPT for batch processing
                full_request = f"BASIC using ChatGPT — {prompt}"
                
                try:
                    result = await lyra.generate_str(full_request)
                    print(result)
                    
                except Exception as e:
                    logger.error(f"Error optimizing prompt {i}: {e}")
                    print(f"❌ Error: {e}")
                
                print("-" * 50)

def main():
    """Main entry point"""
    
    print("🎯 LYRA Prompt Optimizer")
    print("Choose a mode:")
    print("1. Interactive Session")
    print("2. Demo Examples") 
    print("3. Batch Optimization")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            asyncio.run(interactive_session())
            break
        elif choice == "2":
            asyncio.run(demo_examples())
            break
        elif choice == "3":
            asyncio.run(batch_optimization())
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()