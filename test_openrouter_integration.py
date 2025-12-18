#!/usr/bin/env python3
"""
Test script to verify OpenRouter API integration with gpt-oss-120b model.
"""

import os
from llm import create_client, get_response_from_llm

def test_basic_response():
    """Test basic response from the model."""
    print("Testing basic response from openai/gpt-oss-120b...")
    
    # Make sure API key is set
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY environment variable not set")
        return False
    
    # Create client
    client, model = create_client("openai/gpt-oss-120b")
    
    # Get response
    msg = "How many r's are in the word 'strawberry'?"
    system_message = "You are a helpful assistant."
    
    try:
        content, msg_history = get_response_from_llm(
            msg=msg,
            client=client,
            model=model,
            system_message=system_message,
            print_debug=True,
        )
        
        print("\n" + "="*60)
        print("SUCCESS! Response received:")
        print("="*60)
        print(f"Content: {content}")
        print(f"\nMessage history length: {len(msg_history)}")
        
        # Check if reasoning_details is preserved
        if msg_history and len(msg_history) > 0:
            last_msg = msg_history[-1]
            if 'reasoning_details' in last_msg:
                print(f"\n✓ Reasoning details preserved in message history")
            else:
                print(f"\n✗ No reasoning details found (this is okay if model didn't return any)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multi_turn():
    """Test multi-turn conversation with reasoning preservation."""
    print("\n\nTesting multi-turn conversation...")
    
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY environment variable not set")
        return False
    
    client, model = create_client("openai/gpt-oss-120b")
    
    # First turn
    msg1 = "How many r's are in the word 'strawberry'?"
    system_message = "You are a helpful assistant."
    
    try:
        content1, msg_history1 = get_response_from_llm(
            msg=msg1,
            client=client,
            model=model,
            system_message=system_message,
            msg_history=[],
        )
        
        print(f"\nFirst response: {content1}")
        
        # Second turn - challenge the answer
        msg2 = "Are you sure? Think carefully."
        content2, msg_history2 = get_response_from_llm(
            msg=msg2,
            client=client,
            model=model,
            system_message=system_message,
            msg_history=msg_history1,
        )
        
        print(f"\nSecond response: {content2}")
        print(f"\n✓ Multi-turn conversation successful")
        print(f"Message history length: {len(msg_history2)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("OpenRouter API Integration Test")
    print("="*60)
    
    # Test basic response
    test1 = test_basic_response()
    
    # Test multi-turn
    test2 = test_multi_turn()
    
    print("\n" + "="*60)
    print("Test Summary:")
    print("="*60)
    print(f"Basic response: {'✓ PASS' if test1 else '✗ FAIL'}")
    print(f"Multi-turn conversation: {'✓ PASS' if test2 else '✗ FAIL'}")
    print("="*60)
