import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from config import model_name
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable not set")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")

parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

for _ in range(20):
    function_responses = []

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, temperature=0, tools=[available_functions]
        ),
    )
    candidates = response.candidates
    for candidate in candidates:
        messages.append(candidate.content)

    if not response.usage_metadata:
        raise RuntimeError("Response is missing usage metadata")

    if response.function_calls is not None:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)

            if not function_call_result.parts:
                raise Exception("Empty parts list")
            if function_call_result.parts[0].function_response is None:
                raise Exception("Empty FunctionResponse object")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Empty .response field of the FunctionResponse object")
            function_responses.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    if function_responses:
        messages.append(types.Content(role="user", parts=function_responses))

    if not response.function_calls:
        if args.verbose:
            print("User prompt: ", messages[0].parts[0].text)
            print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
            print("Response tokens: ", response.usage_metadata.candidates_token_count)
        print("Final response:")
        print(response.text)
        break
