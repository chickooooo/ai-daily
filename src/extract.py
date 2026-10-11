from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel

# Load environment variables
load_dotenv()


# Constants
MODEL = "claude-haiku-5-5"
# Cost per million tokens
COST_INPUT = 0.1
COST_OUTPUT = 0.5

# System Prompt
SYSTEM_PROMPT = "Extract given lab result. If `value` or `unit` is not present, mark them as None."  # noqa: E501

# Input data
DATA = "Pt: Mr. Rahul Sharma | Haemoglobin 13.8 g/dL (ref 13-17)"
DATA_MISSING = "Rahul Sharma | Haemoglobin"
DATA_MISSING_UNIT = "Iskrov the great II | Lipid profile 4455"

ALL_DATA = [DATA, DATA_MISSING, DATA_MISSING_UNIT]

# Create anthropic client
# Key is taken from .env 'ANTHROPIC_API_KEY'
client = Anthropic()


# Structured output definition
class LabResult(BaseModel):
    patient_name: str
    test_name: str
    value: float | None
    unit: str | None


# Calculate total token cost
# Round to 6 digits
def total_cost(in_tokens: int, out_tokens: int) -> float:
    input_cost = (in_tokens / 1_000_000) * COST_INPUT
    output_cost = (out_tokens / 1_000_000) * COST_OUTPUT
    return round(input_cost + output_cost, 6)


# Extract structured output from raw data
def extract(raw_data: str):
    # Make LLM call
    response = client.messages.parse(
        model=MODEL,
        max_tokens=1000,
        messages=[{"role": "user", "content": raw_data}],
        system=SYSTEM_PROMPT,
        thinking={
            "type": "adaptive",
            "display": "summarized",
        },
        output_format=LabResult,
    )

    # Thinking
    resp_thinking = ""
    for block in response.content:
        if block.type == "thinking":
            resp_thinking += block.thinking

    # Print the parsed output
    print("Input:", raw_data, "\n")
    print("Thinking:", resp_thinking)
    print("Output:", response.parsed_output)
    if (
        response.parsed_output is not None
        and response.parsed_output.value is not None  # noqa: E501
    ):  # noqa: E501
        print("Value + 1:", response.parsed_output.value + 1)

    # Print token usage
    usage = response.usage
    print(
        "\n"
        f"tokens in={usage.input_tokens} "
        f"out={usage.output_tokens} "
        f"cost=${total_cost(usage.input_tokens, usage.output_tokens):.6f}"
        "\n"
    )


# 2 runs per data
for raw_data in ALL_DATA:
    for i in range(2):
        print(f" - - - ATTEMPT {i+1} - - - ")
        extract(raw_data)
        print("")
    print("\n")
