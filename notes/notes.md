## Notes

<br>
<br>

- Parameters:
    - `max_tokens`: Maximum number of tokens the LLM generate before stopping.
    - `system`: Used to provide context and instructions to the LLM.

<br>

- Stop reason:
    - `end_turn`: LLM naturally finished the response.
    - `max_tokens`: LLM reached the maximum output token limit.
    - `stop_sequence`: LLM encountered a user-defined stop sequence.
    - `tool_use`: LLM stopped because it wants to use a tool.
    - `refusal`: LLM refused to provide the requested content.

<br>

- Output tokens cost 5x more than input tokens.
