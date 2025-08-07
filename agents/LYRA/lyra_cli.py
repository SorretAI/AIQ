#!/usr/bin/env python3
"""
LYRA CLI - Command Line Interface for Prompt Optimization

A simple command-line interface for the LYRA prompt optimization system.
Transform any prompt using the 4-D methodology directly from the terminal.
"""

import asyncio
import argparse
import sys
import os
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from mcp_agent.app import MCPApp
from mcp_agent.workflows.prompt_optimizer.lyra_optimizer import LYRAOptimizer, AIPlatform, OptimizationMode
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm_anthropic import AnthropicAugmentedLLM

app = MCPApp(name="lyra_cli")

def print_banner():
    """Print LYRA CLI banner"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                           LYRA CLI                           ║
║              AI Prompt Optimization Specialist              ║
║                      4-D Methodology                        ║
╚══════════════════════════════════════════════════════════════╝
""")

async def optimize_single_prompt(prompt: str, platform: str = "chatgpt", mode: str = "basic", backend: str = "openai"):
    """Optimize a single prompt"""
    
    # Choose LLM factory based on backend
    llm_factory = OpenAIAugmentedLLM if backend == "openai" else AnthropicAugmentedLLM
    
    async with app.run() as mcp_agent_app:
        lyra = LYRAOptimizer(llm_factory=llm_factory)
        
        async with lyra:
            # Format the prompt with platform and mode
            formatted_prompt = f"{mode.upper()} using {platform} — {prompt}"
            
            print(f"🔄 Optimizing prompt with {mode} mode for {platform}...")
            print(f"📝 Original: {prompt}")
            print("-" * 60)
            
            try:
                result = await lyra.generate_str(formatted_prompt)
                print(result)
                return True
            except Exception as e:
                print(f"❌ Error: {e}")
                return False

async def interactive_mode(backend: str = "openai"):
    """Run interactive optimization session"""
    
    llm_factory = OpenAIAugmentedLLM if backend == "openai" else AnthropicAugmentedLLM
    
    async with app.run() as mcp_agent_app:
        lyra = LYRAOptimizer(llm_factory=llm_factory)
        
        async with lyra:
            print(lyra.get_welcome_message())
            print("\n💡 Type 'help' for examples, 'quit' to exit")
            print("=" * 60)
            
            while True:
                try:
                    user_input = input("\n📝 Enter prompt to optimize: ").strip()
                    
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        print("👋 Thanks for using LYRA!")
                        break
                    
                    if user_input.lower() == 'help':
                        print_help_examples()
                        continue
                    
                    if not user_input:
                        continue
                    
                    print("\n🔄 LYRA is optimizing your prompt...")
                    print("-" * 50)
                    
                    result = await lyra.generate_str(user_input)
                    print(result)
                    print("-" * 50)
                    
                except KeyboardInterrupt:
                    print("\n👋 Thanks for using LYRA!")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")

def print_help_examples():
    """Print usage examples"""
    print("""
📚 LYRA Usage Examples:

Basic Examples:
• BASIC using ChatGPT — Write me a marketing email
• BASIC using Claude — Create a workout plan  
• BASIC using Gemini — Write a story about robots

Detail Examples (with clarifying questions):
• DETAIL using ChatGPT — Help me optimize my LinkedIn profile
• DETAIL using Claude — Analyze this business proposal
• DETAIL using Gemini — Create educational content about climate change

Platform Options: ChatGPT, Claude, Gemini, Other
Mode Options: BASIC (quick fix) or DETAIL (comprehensive)

Tips:
- Be specific about your target AI platform for best results
- Use DETAIL mode for complex or professional requests
- Use BASIC mode for quick improvements
""")

async def batch_process_file(file_path: str, platform: str = "chatgpt", mode: str = "basic", backend: str = "openai"):
    """Process prompts from a file"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            prompts = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    print(f"📦 Processing {len(prompts)} prompts from {file_path}")
    print(f"🎯 Platform: {platform}, Mode: {mode}, Backend: {backend}")
    print("=" * 60)
    
    llm_factory = OpenAIAugmentedLLM if backend == "openai" else AnthropicAugmentedLLM
    
    async with app.run() as mcp_agent_app:
        lyra = LYRAOptimizer(llm_factory=llm_factory)
        
        async with lyra:
            success_count = 0
            
            for i, prompt in enumerate(prompts, 1):
                print(f"\n🔧 [{i}/{len(prompts)}] Processing: '{prompt[:50]}...'")
                print("-" * 50)
                
                formatted_prompt = f"{mode.upper()} using {platform} — {prompt}"
                
                try:
                    result = await lyra.generate_str(formatted_prompt)
                    print(result)
                    success_count += 1
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                print("-" * 50)
                
                # Small delay between requests
                if i < len(prompts):
                    await asyncio.sleep(1)
            
            print(f"\n✅ Completed! Successfully processed {success_count}/{len(prompts)} prompts")
            return success_count == len(prompts)

def main():
    """Main CLI entry point"""
    
    parser = argparse.ArgumentParser(
        description="LYRA - AI Prompt Optimization Specialist",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Write me a blog post"
  %(prog)s --platform claude --mode detail "Help with my resume"  
  %(prog)s --interactive
  %(prog)s --file prompts.txt --platform chatgpt --mode basic
        """
    )
    
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Prompt to optimize (use --interactive for interactive mode)"
    )
    
    parser.add_argument(
        "--platform", "-p",
        choices=["chatgpt", "claude", "gemini", "other"],
        default="chatgpt",
        help="Target AI platform (default: chatgpt)"
    )
    
    parser.add_argument(
        "--mode", "-m",
        choices=["basic", "detail"],
        default="basic",
        help="Optimization mode (default: basic)"
    )
    
    parser.add_argument(
        "--backend", "-b",
        choices=["openai", "anthropic"],
        default="openai",
        help="LLM backend for LYRA (default: openai)"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "--file", "-f",
        help="Process prompts from file (one per line)"
    )
    
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Show usage examples"
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.examples:
        print_help_examples()
        return
    
    if args.interactive:
        asyncio.run(interactive_mode(args.backend))
    elif args.file:
        success = asyncio.run(batch_process_file(args.file, args.platform, args.mode, args.backend))
        sys.exit(0 if success else 1)
    elif args.prompt:
        success = asyncio.run(optimize_single_prompt(args.prompt, args.platform, args.mode, args.backend))
        sys.exit(0 if success else 1)
    else:
        # Default to interactive mode if no prompt provided
        asyncio.run(interactive_mode(args.backend))

if __name__ == "__main__":
    main()