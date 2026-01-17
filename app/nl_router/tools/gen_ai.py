
from google.genai import types

get_weather_declaration = types.FunctionDeclaration(
  name="get_weather",
  description="Gets the current weather temperature for a given location.",
  parameters={
      "type": "object",
      "properties": {"location": {"type": "string"}},
      "required": ["location"],
  },
)
get_weather_tool = types.Tool(function_declarations=[get_weather_declaration])
