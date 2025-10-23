#!/usr/bin/env python3
"""
Script para probar gpt-oss-20b
"""

import sys
import os

sys.path.append('/Users/danielfloresrojas/Desktop_local/GTBench')

from gamingbench.chat.chat import chat_llm

# Mensaje de prueba simple
test_messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is 3+5?"}
]

print("Testing GPT-OSS-20B...")

try:
    result = chat_llm(
        messages=test_messages,
        model="openai/gpt-oss-20b",
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
    
except Exception as e:
    print(f"Error: {e}")
