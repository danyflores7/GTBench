#!/usr/bin/env python3
"""
Script para probar diferentes modelos de NVIDIA
"""

import sys
import os
import json
from pprint import pprint

sys.path.append('/Users/danielfloresrojas/Desktop_local/GTBench')

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.schema import SystemMessage, HumanMessage

# Mensaje de prueba simple
test_messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is 2+2? Answer in one word.")
]

print("Testing different NVIDIA models...")

# Modelos a probar
models_to_test = [
    "meta/llama-3.1-8b-instruct",  # Modelo que sabemos que funciona bien
    "openai/gpt-oss-120b",        # El modelo original que estamos probando
    "microsoft/phi-3-mini-128k-instruct"  # Otro modelo alternativo
]

for model_name in models_to_test:
    print(f"\n=== TESTING MODEL: {model_name} ===")
    
    try:
        chat = ChatNVIDIA(
            model=model_name,
            api_key=os.environ["NVIDIA_API_KEY"],
            temperature=1,
            top_p=1,
            max_completion_tokens=50,  # Usar max_completion_tokens en lugar de max_tokens
        )
        
        generations = chat.generate(
            [test_messages],
            stop=None,
        )
        
        print(f"Response: '{generations.generations[0][0].message.content}'")
        print(f"llm_output: {generations.llm_output}")
        print(f"generation_info: {generations.generations[0][0].generation_info}")
        
        # Buscar tokens en cualquier lugar
        if generations.llm_output:
            for key, value in generations.llm_output.items():
                if 'token' in key.lower():
                    print(f"Found tokens in llm_output['{key}']: {value}")
        
        gen_info = generations.generations[0][0].generation_info
        if gen_info:
            for key, value in gen_info.items():
                if 'token' in key.lower():
                    print(f"Found tokens in generation_info['{key}']: {value}")
        
    except Exception as e:
        print(f"Error with {model_name}: {e}")
