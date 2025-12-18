#!/usr/bin/env python3
"""
Example usage of OpenRouter API with gpt-oss-120b model using the project's LLM interface.
This demonstrates the same functionality as test_response.py but using the project's abstraction.
"""

import os
from llm import create_client, get_response_from_llm

# Set your API key
# os.environ["OPENROUTER_API_KEY"] = "sk-or-v1-your-key-here"

def main():
    # Create the OpenRouter client
    client, model = create_client("openai/gpt-oss-120b")
    
    print("=" * 60)
    print("OpenRouter API Example - Multi-turn Conversation")
    print("=" * 60)
    
    # First question
    print("\n[Turn 1] User: How many r's are in the word 'strawberry'?")
    
    content1, msg_history1 = get_response_from_llm(
        msg="How many r's are in the word 'strawberry'?",
        client=client,
        model=model,
        system_message="You are a helpful assistant.",
        msg_history=[],
    )
    
    print(f"\n[Turn 1] Assistant: {content1}")
    
    # Check if reasoning was provided
    if msg_history1 and len(msg_history1) > 0:
        last_msg = msg_history1[-1]
        if 'reasoning_details' in last_msg:
            print(f"\n[Turn 1] Reasoning provided: ✓")
            # Optionally print the reasoning
            # print(f"Reasoning: {last_msg['reasoning_details']}")
    
    # Follow-up question - challenge the answer
    print("\n" + "-" * 60)
    print("\n[Turn 2] User: Are you sure? Think carefully.")
    
    content2, msg_history2 = get_response_from_llm(
        msg="Are you sure? Think carefully.",
        client=client,
        model=model,
        system_message="You are a helpful assistant.",
        msg_history=msg_history1,  # Pass previous conversation history
    )
    
    print(f"\n[Turn 2] Assistant: {content2}")
    
    # Check if reasoning was provided in second turn
    if msg_history2 and len(msg_history2) > 0:
        last_msg = msg_history2[-1]
        if 'reasoning_details' in last_msg:
            print(f"\n[Turn 2] Reasoning provided: ✓")
    
    print("\n" + "=" * 60)
    print(f"Conversation completed successfully!")
    print(f"Total turns: {len(msg_history2)}")
    print("=" * 60)

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY environment variable is not set")
        print("Please set it with: export OPENROUTER_API_KEY='sk-or-v1-your-key-here'")
        exit(1)
    
    main()
