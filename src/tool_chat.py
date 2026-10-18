from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import Message, MessageParam, ToolParam

# Load environment variables
load_dotenv()


# Constants
MODEL = "claude-haiku-5-5"
# Cost per million tokens
COST_INPUT = 0.1
COST_OUTPUT = 0.5

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


def get_report_status(pid: str) -> str | None:
    """Return report status for the given PID. None if no data is present"""
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
        return None
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
    return {
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


def chat() -> None:
    messages: list[MessageParam] = [
        {
            "role": "user",
            "content": "Is the report for PID 5555 ready?",
        }
    ]

    for _ in range(2):
        # Make LLM call & print response
        response = call_llm(messages)
        processed = process_response(response)

        print("Stop Reason:", processed["stop_reason"])
        print("Thinking:", processed["thinking"])
        print("Text:", processed["text"])
        print("Tool Use:", processed["tool_use"])
        print("Usage:", processed["usage"], "\n")

        # If no tool use
        if processed["stop_reason"] != "tool_use":
            break

        # Results of tool use
        tool_results = []
        for item in processed["tool_use"]:
            if item["name"] == "get_report_status":
                pid = item["input"]["pid"]
                result = get_report_status(pid)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": item["id"],
                    "content": result
                })

        # If no tool was executed
        if len(tool_results) == 0:
            break

        messages = messages + [
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": tool_results},
        ]


if __name__ == "__main__":
    print("\n --- Welcome --- \n")
    chat()
    print("\n --- Thank you --- \n")
