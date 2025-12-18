# OpenRouter API Integration

This document describes the integration of OpenRouter API with the `gpt-oss-120b` model in the project.

## Changes Made

### 1. Model Configuration (`llm_withtools.py`)
- Updated `OPENAI_MODEL` constant from `'gpt-5'` to `'openai/gpt-oss-120b'`
- This is now the default model when `OPENAI_API_KEY` is not available but `OPENROUTER_API_KEY` is set

### 2. Client Creation (`llm.py`)
- Added support for `openai/gpt-oss-120b` in the `AVAILABLE_LLMS` list
- Updated `create_client()` function to create an OpenRouter API client for the gpt-oss-120b model:
  ```python
  client = openai.OpenAI(
      api_key=os.environ.get("OPENROUTER_API_KEY", ""),
      base_url="https://openrouter.ai/api/v1"
  )
  ```

### 3. Response Handling (`llm.py`)
- Added dedicated handling for `openai/gpt-oss-120b` in `get_response_from_llm()`
- Implemented reasoning support using OpenRouter's reasoning feature:
  ```python
  extra_body={
      "reasoning": {"enabled": True},
      "provider": {"sort": "price"}
  }
  ```
- Preserves `reasoning_details` in message history for multi-turn conversations

### 4. Tool Support (`llm_withtools.py`)
- Updated `get_response_withtools()` to support OpenRouter API with reasoning for tool calls
- Updated `check_for_tool_use()` to detect tool calls from OpenRouter responses
- Updated `convert_tool_info()` to format tool definitions compatible with OpenRouter's function calling format

## Environment Setup

To use the OpenRouter API, you need to set the `OPENROUTER_API_KEY` environment variable:

```bash
export OPENROUTER_API_KEY="sk-or-v1-your-api-key-here"
```

You can obtain an API key from [OpenRouter](https://openrouter.ai/).

## Features

### Reasoning Support
The integration enables OpenRouter's reasoning feature, which:
- Provides internal reasoning steps before generating the final response
- Preserves reasoning details in message history for multi-turn conversations
- Helps the model think through problems more carefully

### Multi-turn Conversations
The implementation properly handles multi-turn conversations by:
- Preserving `reasoning_details` from previous turns
- Passing the complete message history including reasoning to subsequent API calls
- Allowing the model to continue reasoning from where it left off

### Tool Calling
The model supports function/tool calling:
- Tools are defined using the standard OpenAI function calling format
- Tool calls and results are properly handled
- Compatible with the existing tool infrastructure in the project

## Testing

A test script is provided to verify the integration:

```bash
python test_openrouter_integration.py
```

This script tests:
1. Basic response generation
2. Multi-turn conversations with reasoning preservation
3. Proper handling of message history

## Usage Example

```python
from llm import create_client, get_response_from_llm

# Create client
client, model = create_client("openai/gpt-oss-120b")

# Get response
content, msg_history = get_response_from_llm(
    msg="What is the capital of France?",
    client=client,
    model=model,
    system_message="You are a helpful assistant.",
)

print(content)
```

For multi-turn conversations:

```python
# First turn
content1, msg_history1 = get_response_from_llm(
    msg="How many r's are in strawberry?",
    client=client,
    model=model,
    system_message="You are a helpful assistant.",
    msg_history=[],
)

# Second turn - preserves reasoning from first turn
content2, msg_history2 = get_response_from_llm(
    msg="Are you sure? Count again.",
    client=client,
    model=model,
    system_message="You are a helpful assistant.",
    msg_history=msg_history1,  # Pass previous history
)
```

## Model Selection

The project will automatically use the OpenRouter model when:
1. `OPENROUTER_API_KEY` is set in the environment
2. `OPENAI_API_KEY` is not set (or you explicitly specify the model)

The model selection logic in `coding_agent.py`:
```python
self.code_model = OPENAI_MODEL if os.getenv('OPENAI_API_KEY') else CLAUDE_MODEL
```

Since `OPENAI_MODEL` is now `'openai/gpt-oss-120b'`, the system will use OpenRouter when the API key is available.

## Benefits of gpt-oss-120b

- **Model selection**: Uses the OpenRouter model identifier `openai/gpt-oss-120b`
- **Reasoning capabilities**: Built-in reasoning support helps with complex problems
- **OpenAI-compatible API**: Works with existing OpenAI client libraries
- **Good performance**: 120B parameter model provides strong performance for coding tasks
