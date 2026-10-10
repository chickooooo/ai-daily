## Notes

<br>
<br>
<br>

### Message API

- `client.messages.create()`:
    - Returns a plain text response.
    - Parameters:
        - `model`: LLM model used to generate the response.
        - `max_tokens`: Maximum number of tokens the LLM generate before stopping.
        - `messages`: List of user and assistant messages.
        - `system`: Used to provide context and instructions to the LLM.
        - `thinking`: Configuration for extended thinking.
        - `tools`: Defines tools Claude can use, such as custom functions.
        - `stop_sequences`: Specifies sequences that stop generation.
        - `output_config["effort"]`: How much efforts the model takes.

<br>

- `client.messages.parse()`:
    - Returns a structured response.
    - Generally, a Pydantic model is used to define the structure.
    - Parameters:
        - All of the parameters supported by `.create()`.
        - `output_format`: Defines the expected output structure, typically a Pydantic model.

<br>

---

<br>

- Stop reason:
    - `end_turn`: LLM naturally finished the response.
    - `max_tokens`: LLM reached the maximum output token limit.
    - `stop_sequence`: LLM encountered a user-defined stop sequence.
    - `tool_use`: LLM stopped because it wants to use a tool.
    - `refusal`: LLM refused to provide the requested content.

<br>

- Thinking:
    - Before answering, the LLM reasons privately in a thinking block.
    - Thinking tokens are billed as output tokens and counted towards `max_tokens`.
    - `type`: `adaptive | disabled | enabled | between_tools`. Default: `adaptive`.
    - `display`: `omitted | summarized | updates`. Default: `omitted`.
    - `effort`: `low | medium | high | xhigh | max`. Default: `medium`.

<br>

- Output tokens cost 5x more than input tokens.
