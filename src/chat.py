from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import MessageParam

# Load environment variables
load_dotenv()


# Constants
MODEL = "claude-haiku-5-5"
# Cost per million tokens
COST_INPUT = 0.1
COST_OUTPUT = 0.5


# Create anthropic client
# Key is taken from .env 'ANTHROPIC_API_KEY'
client = Anthropic()


# Calculate total token cost
# Round to 6 digits
def total_cost(in_tokens: int, out_tokens: int) -> float:
    input_cost = (in_tokens / 1_000_000) * COST_INPUT
    output_cost = (out_tokens / 1_000_000) * COST_OUTPUT
    return round(input_cost + output_cost, 6)


def call_llm(messages: list[MessageParam], patient_data: str) -> dict:
    SYSTEM_PROMPT = f"""You are the receptionist at a pathology lab. Always reply in one short, friendly sentence.
Only provide answers based on below patient details. DO NOT makeup answers. For any other request, respond "Sorry, I cannot help you with that".

**Patient Details (first row headers):**
PID · Name · Test · Status
{patient_data}"""  # noqa: E501

    # Make LLM call
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=messages,
        thinking={
            "type": "adaptive",
            "display": "summarized",
        },
        output_config={
            "effort": "low",
        },
    )

    # Construct the response message
    resp_thinking = ""
    resp_message = ""
    for block in response.content:
        if block.type == "thinking":
            resp_thinking += block.thinking
        elif block.type == "text":
            resp_message += block.text

    usage = response.usage
    return {
        "thinking": resp_thinking,
        "content": resp_message,
        "usage": (
            f"tokens in={usage.input_tokens} "
            f"out={usage.output_tokens} "
            f"cost=${total_cost(usage.input_tokens, usage.output_tokens):.6f}"
        ),
    }


def mock_call_llm(messages: list[MessageParam], patient_data: str) -> dict:
    print("\n --- ")
    for item in messages:
        print(item)
    print(" --- \n")

    return {
        "thinking": "dummy thinking",
        "content": "dummy message",
        "usage": (f"tokens in={0} " f"out={0} " f"cost=${0.00:.6f}"),
    }


def get_patient_data() -> str | None:
    """Ask and get required patient data. None if no data is present"""
    # Data storage {PID: data}
    DATA = {
        "4444": "4444 · James Bond · CBC · ready",
        "5555": "5555 · Jane Doe · Lipid profile · pending, expected tomorrow 5 PM",  # noqa: E501
    }

    # Get patient id
    pid = input("Enter your PID: ").strip()
    # Return data for PID else None
    return DATA.get(pid)


def chat() -> None:
    # Get patient data
    patient_data = get_patient_data()
    if patient_data is None:
        print("\n --- Invalid Request --- \n")
        return

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
        response = call_llm(messages, patient_data)
        print("Thinking:", response["thinking"])
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
