## Notes

<br>
<br>

- Parameters:
    - `max_tokens`: Maximum number of tokens the LLM generate before stopping.
    - `system`: Used to provide context and instructions to the LLM.
    - `thinking`: Configuration for extended thinking.
    - `output_config["effort"]`: How much efforts the model takes.

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
