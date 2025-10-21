
import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatAnyscale
from langchain.schema import SystemMessage, HumanMessage, AIMessage


def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


def chat_llm(messages, model, temperature, max_tokens, n, timeout, stop, return_tokens=False, chat_seed=0):
    if "gpt" in model:
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
        chat = ChatOpenAI(**chat_kwargs)
    elif 'Open-Orca/Mistral-7B-OpenOrca' == model:
        iterated_query = True
        chat = ChatAnyscale(temperature=temperature,
                            anyscale_api_key=os.environ['ANYSCALE_API_KEY'],
                            max_tokens=max_tokens,
                            n=1,
                            model_name=model,
                            request_timeout=timeout)
    else:
        # deepinfra
        iterated_query = True
        chat = ChatOpenAI(model_name=model,
                          openai_api_key=os.environ['DEEPINFRA_API_KEY'],
                          temperature=temperature,
                          max_tokens=max_tokens,
                          n=1,
                          request_timeout=timeout,
                          openai_api_base="https://api.deepinfra.com/v1/openai")

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
        for n in range(n):
            generations = chat.generate([longchain_msgs], stop=[
                stop] if stop is not None else None)
            responses = [
                chat_gen.message.content for chat_gen in generations.generations[0]]
            response_list.append(responses[0])
            completion_tokens = generations.llm_output['token_usage']['completion_tokens']
            prompt_tokens = generations.llm_output['token_usage']['prompt_tokens']
            total_completion_tokens += completion_tokens
            total_prompt_tokens += prompt_tokens
        responses = response_list
        completion_tokens = total_completion_tokens
        prompt_tokens = total_prompt_tokens
    else:
        generations = chat.generate([longchain_msgs], stop=[
            stop] if stop is not None else None)
        responses = [
            chat_gen.message.content for chat_gen in generations.generations[0]]
        completion_tokens = generations.llm_output['token_usage']['completion_tokens']
        prompt_tokens = generations.llm_output['token_usage']['prompt_tokens']

    return {
        'generations': responses,
        'completion_tokens': completion_tokens,
        'prompt_tokens': prompt_tokens
    }
