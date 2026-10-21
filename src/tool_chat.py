from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import (
    Message,
    MessageParam,
    ToolParam,
    ToolResultBlockParam,
)

# Load environment variables
load_dotenv()


# Constants
MODEL = "claude-haiku-5-5"
# Cost per million tokens
COST_INPUT = 0.1
COST_OUTPUT = 0.5
CHAT_LIMIT = 10

# System prompt
SYSTEM_PROMPT = (
    "You are the receptionist at a pathology lab. "
    "Always reply in one short, friendly sentence."
)


# Create anthropic client
# Key is taken from .env 'ANTHROPIC_API_KEY'
client = Anthropic()


# Calculate total token cost
# Round to 6 digits
def total_cost(in_tokens: int, out_tokens: int) -> float:
    input_cost = (in_tokens / 1_000_000) * COST_INPUT
    output_cost = (out_tokens / 1_000_000) * COST_OUTPUT
    return round(input_cost + output_cost, 6)


def get_report_status(pid: str) -> str:
    """Return report status for the given PID.
    'No data found for given pid' if no data is present."""
    # Data storage {PID: data}
    DATA = {
        "4444": {
            "id": "4444",
            "name": "James Bond",
            "test": "CBC",
            "status": "ready",
        },
        "5555": {
            "id": "5555",
            "name": "Jane Doe",
            "test": "Lipid profile",
            "status": "pending, expected tomorrow 5 PM",
        },
    }

    if pid not in DATA:
        return "No data found for given pid"
    return DATA[pid]["status"]


REPORT_STATUS_TOOL: ToolParam = {
    "name": "get_report_status",
    "description": (
        "Get the status of a report using its PID. "
        "Returns the status or None if no report data exists."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "pid": {
                "type": "string",
                "description": "The patient's ID (PID).",
            }
        },
        "required": ["pid"],
    },
}


def process_response(response: Message) -> dict:
    # Response content
    thinking = ""
    text = ""
    tool_use = []

    for block in response.content:
        if block.type == "thinking":
            thinking += block.thinking

        elif block.type == "text":
            text += block.text

        elif block.type == "tool_use":
            tool_use.append(
                {
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                }
            )

    usage = response.usage
    processed = {
        "stop_reason": response.stop_reason,
        "thinking": thinking,
        "text": text,
        "tool_use": tool_use,
        "usage": (
            f"tokens in={usage.input_tokens} "
            f"out={usage.output_tokens} "
            f"cost=${total_cost(usage.input_tokens, usage.output_tokens):.6f}"
        ),
    }

    print("Stop Reason:", processed["stop_reason"])
    print("Thinking:", processed["thinking"])
    print("Text:", processed["text"])
    print("Tool Use:", processed["tool_use"])
    print("Usage:", processed["usage"], "\n")

    return processed


def call_llm(messages: list[MessageParam]) -> Message:
    # Define tools
    tools = [REPORT_STATUS_TOOL]

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
        output_config={"effort": "low"},
        tools=tools,
    )

    return response


def get_tool_results(
    tool_use_data: list[dict],
    user_pid: str,
) -> list[ToolResultBlockParam]:
    # Results of tool use
    tool_results = []
    for item in tool_use_data:
        if item["name"] == "get_report_status":
            requested_pid = item["input"]["pid"]

            # If PID mismatch
            if requested_pid != user_pid:
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": item["id"],
                        "content": f"Access denied: this user can only view their own report (PID {user_pid})",  # noqa: E501
                    }
                )

            # Else fetch status
            else:
                result = get_report_status(requested_pid)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": item["id"],
                        "content": result,
                    }
                )

    return tool_results


def chat() -> None:
    # Get patient id
    pid = input("Enter your PID: ").strip()

    messages: list[MessageParam] = []
    last_response: Message | None = None
    last_processed_response: dict = {}

    # Limit of CHAT_LIMIT messages per session
    i = 1
    while i < CHAT_LIMIT:
        # Get new user input
        if last_response is None or last_response.stop_reason == "end_turn":
            # Get the user input and handle quit
            user_input = input("> ").strip()
            if user_input.lower() in ("quit", "q"):
                break
            elif user_input == "":
                continue

            # Add user message to messages
            messages.append({"role": "user", "content": user_input})

        # Tool call
        elif last_response.stop_reason == "tool_use":
            # Get tool results
            tool_results = get_tool_results(
                last_processed_response["tool_use"],
                pid,
            )
            messages.append({"role": "user", "content": tool_results})

        # Others
        else:
            break

        # Make LLM call & print response
        last_response = call_llm(messages)
        last_processed_response = process_response(last_response)
        # Add LLM message to messages
        messages.append(
            {"role": "assistant", "content": last_response.content},
        )

        i += 1

    if i == CHAT_LIMIT:
        print(f"\n --- Session limit ({CHAT_LIMIT}) exhausted --- \n")


if __name__ == "__main__":
    print("\n --- Welcome --- \n")
    chat()
    print("\n --- Thank you --- \n")
