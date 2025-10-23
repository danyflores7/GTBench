#!/usr/bin/env python3
"""
Script para debuggear la estructura de datos de NVIDIA ChatNVIDIA
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

print("Testing NVIDIA ChatNVIDIA raw response structure...")

try:
    chat = ChatNVIDIA(
        model="openai/gpt-oss-120b",
        api_key=os.environ["NVIDIA_API_KEY"],
        temperature=1,
        top_p=1,
        max_tokens=50,
    )
    
    generations = chat.generate(
        [test_messages],
        stop=None,
    )
    
    print("\n=== GENERATIONS STRUCTURE ===")
    print(f"Type: {type(generations)}")
    print(f"Dir: {[attr for attr in dir(generations) if not attr.startswith('_')]}")
    
    print("\n=== LLM_OUTPUT ===")
    print(f"llm_output type: {type(generations.llm_output)}")
    print(f"llm_output content:")
    pprint(generations.llm_output)
    
    print("\n=== GENERATIONS CONTENT ===")
    for i, gen_list in enumerate(generations.generations):
        print(f"Generation {i}:")
        for j, gen in enumerate(gen_list):
            print(f"  Gen {j}: {gen.message.content}")
            print(f"  Type: {type(gen)}")
            print(f"  Dir: {[attr for attr in dir(gen) if not attr.startswith('_')]}")
            if hasattr(gen, 'generation_info'):
                print(f"  generation_info: {gen.generation_info}")
    
    # Buscar tokens en diferentes lugares
    print("\n=== SEARCHING FOR TOKENS ===")
    
    # En llm_output
    if generations.llm_output:
        for key, value in generations.llm_output.items():
            print(f"llm_output['{key}']: {value}")
    
    # En generation_info de cada generación
    for i, gen_list in enumerate(generations.generations):
        for j, gen in enumerate(gen_list):
            if hasattr(gen, 'generation_info') and gen.generation_info:
                print(f"generations[{i}][{j}].generation_info: {gen.generation_info}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
