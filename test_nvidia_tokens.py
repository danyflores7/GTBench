#!/usr/bin/env python3
"""
Script para probar el tracking de tokens con NVIDIA ChatNVIDIA
"""

import sys

from gamingbench.chat.chat import chat_llm

sys.path.append('/Users/danielfloresrojas/Desktop_local/GTBench')

# Mensaje de prueba simple
test_messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is 2+2?"}
]

print("Testing NVIDIA ChatNVIDIA token tracking...")

try:
    result = chat_llm(
        messages=test_messages,
        model="openai/gpt-oss-120b",
        temperature=1,
        max_tokens=50,
        n=1,
        timeout=30,
        stop=None
    )
    
    print(f"Generations: {result['generations']}")
    print(f"Completion tokens: {result['completion_tokens']}")
    print(f"Prompt tokens: {result['prompt_tokens']}")
    print(f"Total tokens: {result['completion_tokens'] + result['prompt_tokens']}")
    
except (ValueError, KeyError, ImportError) as e:
    print(f"Error: {e}")
