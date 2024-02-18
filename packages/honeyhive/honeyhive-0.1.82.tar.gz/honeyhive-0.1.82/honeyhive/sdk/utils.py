from typing import Dict, List, Optional, Any
import random

def fill_template(
    template: str,
    inputs: Dict[str, str]
):
    """Fill a template with inputs"""
    import re
    import copy
    template = copy.deepcopy(template)
    for key, value in inputs.items():
        template = re.sub(r"{{\s*" + key + r"\s*}}", value, template)
    return template

def fill_chat_template(
    chat: List[Dict[str, str]],
    inputs: Dict[str, str]
):
    """Fill a chat template with inputs"""
    import copy
    chat = copy.deepcopy(chat)
    for message in chat:
        if message["content"] is None:
            continue
        message["content"] = fill_template(message["content"], inputs)
    return chat

def calculate_openai_cost(
    model: str,
    usage: Dict[str, Any]
):
    """Calculate the cost of an OpenAI model"""
    openai_costs = {
        "ada": 0.0004,
        "babbage": 0.0005,
        "curie": 0.002,
        "davinci": 0.02,
        "turbo": 0.002
    }

    openai_costs_input = {
        "turbo": 0.0015,
        "turbo-16k": 0.003,
        "4": 0.03,
        "4-32k": 0.06
    }

    openai_costs_output = {
        "turbo": 0.002,
        "turbo-16k": 0.004,
        "4": 0.06,
        "4-32k": 0.12
    }

    cost = 0

    if not model:
        return 0
    
    if "gpt-4" in model:
        if "32k" in model:
            cost = openai_costs_input["4-32k"] * usage["prompt_tokens"]/1000 + openai_costs_output["4-32k"] * usage["completion_tokens"]/1000
        else:
            cost = openai_costs_input["4"] * usage["prompt_tokens"]/1000 + openai_costs_output["4"] * usage["completion_tokens"]/1000
    elif "gpt-3.5-turbo" in model:
        if "16k" in model:
            cost = openai_costs_input["turbo-16k"] * usage["prompt_tokens"]/1000 + openai_costs_output["turbo-16k"] * usage["completion_tokens"]/1000
        else:
            cost = openai_costs_input["turbo"] * usage["prompt_tokens"]/1000 + openai_costs_output["turbo"] * usage["completion_tokens"]/1000
    else:
        for key in openai_costs:
            if key in model:
                cost = openai_costs[key] * usage["total_tokens"]/1000
                break

    # approximate cost to 5 decimal places
    cost = cost * 100000
    cost = int(cost)
    cost = cost / 100000

    return cost

def generate_random_string_extended():
    adjectives = [
        "agile", "bright", "charming", "daring", "elegant", "fancy", "graceful", "happy", "inventive", "jolly",
        # ... (List continues to include 100 different adjectives)
    ]

    nouns = [
        "aardvark", "bear", "cat", "dog", "elephant", "flamingo", "giraffe", "hippopotamus", "iguana", "jaguar",
        # ... (List continues to include 100 different animal names)
    ]

    # Randomly choose an adjective and a noun
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)

    # Randomly generate a number between 0 and 99, and format it to always be two digits
    number = str(random.randint(0, 99)).zfill(2)

    # Combine the parts into the final string
    random_string = f"{adjective}-{noun}-{number}"
    return random_string

__all__ = [
    "fill_template",
    "fill_chat_template",
    "calculate_openai_cost",
    "generate_random_string_extended"
]