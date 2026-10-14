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
SYSTEM_PROMPT = "Extract given lab result. If `value` or `unit` is not present, mark them as None. Also extract the reference range `ref_low` and `ref_high` if present."  # noqa: E501

# Input data
DATA = "Pt: Mr. Rahul Sharma | Haemoglobin 13.8 g/dL (ref 13-17)"
DATA_MISSING = "Rahul Sharma | Haemoglobin"
DATA_MISSING_UNIT = "Iskrov the great II | Lipid profile 4455"
DATA_MULTI_REPORTS = """Patient: Mrs. Anita Desai    Sample No: 4455
LIPID PROFILE
Total Cholesterol   212  mg/dL   (<200)
HDL Cholesterol      48  mg/dL   (>40)
LDL Cholesterol     138  mg/dL   (<100)
Triglycerides       130  mg/dL   (<150)"""

ALL_DATA = [DATA_MULTI_REPORTS]


# Create anthropic client
# Key is taken from .env 'ANTHROPIC_API_KEY'
client = Anthropic()


# Structured output definition
class LabResult(BaseModel):
    test_name: str
    value: float | None
    unit: str | None
    ref_low: float | None
    ref_high: float | None


# Lab report of a patient
class LabReport(BaseModel):
    patient_name: str
    results: list[LabResult]


# Calculate total token cost
# Round to 6 digits
def total_cost(in_tokens: int, out_tokens: int) -> float:
    input_cost = (in_tokens / 1_000_000) * COST_INPUT
    output_cost = (out_tokens / 1_000_000) * COST_OUTPUT
    return round(input_cost + output_cost, 6)


# Flag a result
def flag_result(result: LabResult) -> str:
    # If value not present
    if not result.value:
        return ""
    # if invalid ref range
    if (
        result.ref_low is not None
        and result.ref_high is not None
        and result.ref_high < result.ref_low
    ):
        return ""

    # If value is less that low ref
    if result.ref_low is not None and result.value < result.ref_low:
        return "L"
    # If value is more that high ref
    if result.ref_high is not None and result.value > result.ref_high:
        return "H"

    # value in range or both ref absent
    return ""


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
        output_format=LabReport,
    )

    # Thinking
    resp_thinking = ""
    for block in response.content:
        if block.type == "thinking":
            resp_thinking += block.thinking

    # Print the input and thinking
    print("Input:", raw_data, "\n")
    print("Thinking:", resp_thinking)

    # Print the output.
    print("Output:")
    if response.parsed_output:
        print("\t", "Patient name:", response.parsed_output.patient_name)
        # Each result on new line
        for result in response.parsed_output.results:
            print("\t\t", "Test name:", result.test_name)
            print("\t\t", "Value:", result.value)
            print("\t\t", "Unit:", result.unit)
            print("\t\t", "Ref low:", result.ref_low)
            print("\t\t", "Ref high:", result.ref_high)
            print("\t\t", "Flag:", flag_result(result))
            print("")

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
