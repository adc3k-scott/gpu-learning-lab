from anthropic import Anthropic
from typing import Callable


def create_orchestrator(
    client: Anthropic,
    model: str,
    system_context: str,
    max_tokens: int = 2048,
) -> Callable[[str], str]:
    """
    Return a stateful send() function that maintains conversation history
    and calls Claude with the given system context on every turn.
    """
    history: list[dict] = []

    def send(user_message: str) -> str:
        history.append({"role": "user", "content": user_message})

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_context,
            messages=history,
        )

        text_parts = [
            block.text
            for block in response.content
            if hasattr(block, "text")
        ]
        answer = "\n".join(text_parts).strip() or "[No response returned]"

        history.append({"role": "assistant", "content": answer})
        return answer

    return send
