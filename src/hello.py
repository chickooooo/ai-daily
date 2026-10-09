from dotenv import load_dotenv
from anthropic import Anthropic

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


# Make LLM call
response = client.messages.create(
    model=MODEL,
    max_tokens=1000,
    system=(
        "You are the receptionist at a pathology lab. "
        "Reply in one short, friendly sentence."
    ),
    messages=[
        {
            "role": "user",
            "content": "When will my CBC report be ready?",
        },
    ],
)

# Print content of text block
for block in response.content:
    if block.type == "text":
        print(block.text)

# Print token usage
usage = response.usage
print(
    "\n"
    f"tokens in={usage.input_tokens} "
    f"out={usage.output_tokens} "
    f"cost=${total_cost(usage.input_tokens, usage.output_tokens):.6f}"
    "\n"
)
