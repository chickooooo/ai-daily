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
    if result.value is None:
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
def extract(raw_data: str) -> tuple[dict | None, dict]:
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
        output_config={"effort": "low"},
    )

    # Collect the output
    output = {}
    if response.parsed_output:
        output["patient_name"] = response.parsed_output.patient_name
        output["results"] = []
        # Each result on new line
        for result in response.parsed_output.results:
            output["results"].append(
                {
                    "test_name": result.test_name,
                    "value": result.value,
                    "unit": result.unit,
                    "ref_low": result.ref_low,
                    "ref_high": result.ref_high,
                    "flag": flag_result(result),
                }
            )

    # Print token usage
    usage = response.usage
    usage_dict = {
        "in": usage.input_tokens,
        "out": usage.output_tokens,
        "cost": total_cost(usage.input_tokens, usage.output_tokens),
    }

    if output != {}:
        return output, usage_dict
    return None, usage_dict


# Mock extraction
def mock_extract(raw_data: str) -> tuple[dict | None, dict]:
    output = {
        "patient_name": "Mr. rahul Sharma",
        "results": [
            {
                "test_name": "haemoglobin",
                "value": 13.8,
                "unit": "g/dL",
                "ref_low": 13.0,
                "ref_high": 17.0,
                "flag": "",
            },
        ],
    }
    usage_dict = {
        "in": 0,
        "out": 0,
        "cost": 0.0,
    }

    return output, usage_dict
