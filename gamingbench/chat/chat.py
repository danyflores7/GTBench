
import os
from langchain.schema import SystemMessage, HumanMessage, AIMessage


def estimate_tokens(text, model_name="gpt-3.5-turbo"):  # noqa: ARG001
    """Estimate token count for text using simple heuristics."""
    if not text:
        return 0
    
    # Simple heuristic: ~4 characters per token for most models
    # This is approximate but gives us a reasonable estimate
    return max(1, len(text) // 4)


# Streaming handler removed: forcing non-streaming generate() for gpt-oss-20b


def write_to_file(file_path, content):
    """Write content to a file using UTF-8 encoding."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def chat_llm(  # noqa
    messages,
    model,
    temperature,
    max_tokens,
    n,  # noqa: N803 - mantener compatibilidad con llamadas existentes
    timeout,
    stop,
    return_tokens=False,
    chat_seed=0,
    model_kwargs=None,  # New parameter for additional model configuration
):
    """Unified chat interface across providers (OpenAI, NVIDIA, Anyscale, DeepInfra).

    Parameters
    - messages: list of dicts with 'role' and 'content'
    - model: string model identifier
    - temperature: float temperature
    - max_tokens: int max tokens for completion
    - n: int number of generations to sample
    - timeout: request timeout
    - stop: optional stop sequence
    - return_tokens: unused flag kept for API compatibility
    - chat_seed: unused, kept for compatibility
    - model_kwargs: dict of additional model-specific parameters (e.g., reasoning settings)
    """
    # Ruta NVIDIA primero para evitar colisiones con el patrón "gpt" genérico
    if model == "openai/gpt-oss-20b" or model.endswith("gpt-oss-20b"):
        # Use non-streaming generate() for GPT-OSS-20B
        iterated_query = True
        resolved_model = model if "/" in model else "openai/gpt-oss-20b"
        module = __import__('langchain_nvidia_ai_endpoints', fromlist=['ChatNVIDIA'])
        chat_nvidia_cls = getattr(module, 'ChatNVIDIA')
        
        # Default model_kwargs for gpt-oss-20b (disable reasoning by default)
        default_kwargs = {
            "reasoning_effort": "low",
            "stream_reasoning": False,
            "reasoning": False,
        }
        
        # Override with provided model_kwargs if any
        if model_kwargs is not None:
            default_kwargs.update(model_kwargs)
        
        chat = chat_nvidia_cls(
            model=resolved_model,
            api_key=os.environ["NVIDIA_API_KEY"],
            temperature=temperature,
            top_p=1,
            max_tokens=max_tokens,
            model_kwargs=default_kwargs,
        )
    elif (model == "openai/gpt-oss-120b" or model.endswith("gpt-oss-120b")):
        iterated_query = True  # si n>1, iteramos manualmente
        resolved_model = model if "/" in model else "openai/gpt-oss-120b"
        # Import dinámico para evitar dependencias innecesarias al importar el módulo
        module = __import__('langchain_nvidia_ai_endpoints', fromlist=['ChatNVIDIA'])
        chat_nvidia_cls = getattr(module, 'ChatNVIDIA')
        chat = chat_nvidia_cls(
            model=resolved_model,
            api_key=os.environ["NVIDIA_API_KEY"],
            temperature=temperature,
            top_p=1,
            max_tokens=max_tokens,
            # request_timeout=timeout,  # descomentar si tu versión lo soporta
        )
    elif "gpt" in model:
        iterated_query = False
        # gpt-5 requires max_completion_tokens instead of max_tokens
        is_gpt5 = model.startswith("gpt-5") or model == "gpt-5"
        chat_kwargs = dict(
            model_name=model,
            openai_api_key=os.environ['OPENAI_API_KEY'],
            n=n,
            request_timeout=timeout,
        )
        # For GPT-5, only temperature=1 is supported; otherwise use provided temperature
        if is_gpt5:
            chat_kwargs["temperature"] = 1
        else:
            chat_kwargs["temperature"] = temperature
        if is_gpt5:
            chat_kwargs["model_kwargs"] = {"max_completion_tokens": max_tokens}
        else:
            chat_kwargs["max_tokens"] = max_tokens
        module = __import__('langchain_openai', fromlist=['ChatOpenAI'])
        chat_openai_cls = getattr(module, 'ChatOpenAI')
        chat = chat_openai_cls(**chat_kwargs)
    elif 'Open-Orca/Mistral-7B-OpenOrca' == model:
        iterated_query = True
        module = __import__('langchain_community.chat_models', fromlist=['ChatAnyscale'])
        chat_anyscale_cls = getattr(module, 'ChatAnyscale')
        chat = chat_anyscale_cls(
            temperature=temperature,
            anyscale_api_key=os.environ['ANYSCALE_API_KEY'],
            max_tokens=max_tokens,
            n=1,
            model_name=model,
            request_timeout=timeout,
        )
    else:
        # deepinfra
        iterated_query = True
        module = __import__('langchain_openai', fromlist=['ChatOpenAI'])
        chat_openai_cls = getattr(module, 'ChatOpenAI')
        chat = chat_openai_cls(
            model_name=model,
            openai_api_key=os.environ['DEEPINFRA_API_KEY'],
            temperature=temperature,
            max_tokens=max_tokens,
            n=1,
            request_timeout=timeout,
            openai_api_base="https://api.deepinfra.com/v1/openai",
        )

    longchain_msgs = []
    for msg in messages:
        if msg['role'] == 'system':
            longchain_msgs.append(SystemMessage(content=msg['content']))
        elif msg['role'] == 'user':
            longchain_msgs.append(HumanMessage(content=msg['content']))
        elif msg['role'] == 'assistant':
            longchain_msgs.append(AIMessage(content=msg['content']))
        else:
            raise NotImplementedError
    if n > 1 and iterated_query:
        response_list = []
        total_completion_tokens = 0
        total_prompt_tokens = 0
        for i in range(n):
            # Use non-streaming generate() for all models (gpt-oss-20b included)
            generations = chat.generate(
                [longchain_msgs],
                stop=[stop] if stop is not None else None,
            )
            responses = [chat_gen.message.content for chat_gen in generations.generations[0]]
            
            response_list.append(responses[0])
            
            # Manejar diferentes formatos de token_usage según el proveedor
            if generations.llm_output:
                if 'token_usage' in generations.llm_output:
                    token_usage = generations.llm_output['token_usage']
                elif 'usage' in generations.llm_output:
                    token_usage = generations.llm_output['usage']
                else:
                    token_usage = {}
            else:
                token_usage = {}
            
            completion_tokens = token_usage.get('completion_tokens', 0)
            prompt_tokens = token_usage.get('prompt_tokens', 0)
            
            # Si no hay información de tokens, estimarlos manualmente para esta iteración
            if completion_tokens == 0 and prompt_tokens == 0:
                # Estimar prompt tokens de todos los mensajes
                prompt_text = ""
                for msg in messages:
                    prompt_text += msg.get('content', '')
                prompt_tokens = estimate_tokens(prompt_text)
                
                # Estimar completion tokens de la respuesta actual
                completion_tokens = estimate_tokens(responses[0])
            
            total_completion_tokens += completion_tokens
            total_prompt_tokens += prompt_tokens
        responses = response_list
        completion_tokens = total_completion_tokens
        prompt_tokens = total_prompt_tokens
    else:
        # Use non-streaming generate() for all models
        generations = chat.generate(
            [longchain_msgs],
            stop=[stop] if stop is not None else None,
        )
        responses = [chat_gen.message.content for chat_gen in generations.generations[0]]
        
        # Manejar diferentes formatos de token_usage según el proveedor
        if generations.llm_output:
            if 'token_usage' in generations.llm_output:
                token_usage = generations.llm_output['token_usage']
            elif 'usage' in generations.llm_output:
                token_usage = generations.llm_output['usage']
            else:
                token_usage = {}
        else:
            token_usage = {}
        
        completion_tokens = token_usage.get('completion_tokens', 0)
        prompt_tokens = token_usage.get('prompt_tokens', 0)

    # Si no hay información de tokens, estimarlos manualmente
    if completion_tokens == 0 and prompt_tokens == 0:
        # Estimar prompt tokens de todos los mensajes
        prompt_text = ""
        for msg in messages:
            prompt_text += msg.get('content', '')
        prompt_tokens = estimate_tokens(prompt_text)
        
        # Estimar completion tokens de las respuestas
        completion_text = ""
        for response in responses:
            completion_text += str(response)
        completion_tokens = estimate_tokens(completion_text)

    return {
        'generations': responses,
        'completion_tokens': completion_tokens,
        'prompt_tokens': prompt_tokens
    }
