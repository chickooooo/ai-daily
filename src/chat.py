from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import MessageParam

# Load environment variables
load_dotenv()


# Constants
MODEL = "claude-haiku-4-5"
# Cost per million tokens
COST_INPUT = 1
COST_OUTPUT = 5


# Create anthropic client
# Key is taken from .env 'ANTHROPIC_API_KEY'
client = Anthropic()


# Calculate total token cost
# Round to 6 digits
def total_cost(in_tokens: int, out_tokens: int) -> float:
    input_cost = (in_tokens / 1_000_000) * COST_INPUT
    output_cost = (out_tokens / 1_000_000) * COST_OUTPUT
    return round(input_cost + output_cost, 6)


def call_llm(messages: list[MessageParam]) -> dict:
    # Make LLM call
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        system=(
            "You are the receptionist at a pathology lab. "
            "Always reply in one short, friendly sentence."
        ),
        messages=messages,
    )

    # Construct the response message
    resp_message = ""
    for block in response.content:
        if block.type == "text":
            resp_message += block.text

    usage = response.usage
    return {
        "content": resp_message,
        "usage": (
            f"tokens in={usage.input_tokens} "
            f"out={usage.output_tokens} "
            f"cost=${total_cost(usage.input_tokens, usage.output_tokens):.6f}"
        ),
    }


def mock_call_llm(messages: list[MessageParam]) -> dict:
    print("\n --- ")
    for item in messages:
        print(item)
    print(" --- \n")

    return {
        "content": "dummy message",
        "usage": (f"tokens in={0} " f"out={0} " f"cost=${0.00:.6f}"),
    }


def chat() -> None:
    # Will hold all messages in a conversation
    messages = []

    # Limit of 5 user messages per session
    i = 1
    while i < 6:
        # Get the user input and handle quit
        user_input = input("> ").strip()
        if user_input.lower() == "quit":
            break
        elif user_input == "":
            continue

        # Add user message to messages
        messages.append({"role": "user", "content": user_input})

        # Make LLM call & print response
        response = mock_call_llm(messages)
        print("AI:", response["content"])
        print("Usage:", response["usage"], "\n")

        # Add LLM message to messages
        messages.append({"role": "assistant", "content": response["content"]})

        i += 1

    if i == 6:
        print("\n --- Session limit (5) exhausted --- \n")


if __name__ == "__main__":
    print("\n --- Welcome --- \n")
    chat()
    print("\n --- Thank you --- \n")
