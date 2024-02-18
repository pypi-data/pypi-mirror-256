tools_dict = {
    "get_current_weather": {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit to use. Infer this from the users location.",
                    },
                },
                "required": ["location", "format"],
            },
        }
    },
    ### Add more
}

def tools(tool_names):
    if type(tool_names) == str:
        tool_names = [tool_names]
    list_tools = []
    for tool in tool_names:
        list_tools.append(tools_dict[tool])
    return list_tools



# hh.tools("get_current_weather")