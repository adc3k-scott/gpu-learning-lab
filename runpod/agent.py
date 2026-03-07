import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
model = os.getenv("ANTHROPIC_MODEL")

if not api_key:
    raise RuntimeError("Missing ANTHROPIC_API_KEY in .env")
if not model:
    raise RuntimeError("Missing ANTHROPIC_MODEL in .env")

client = Anthropic(api_key=api_key)

print("Cloud agent node is live.")
print("Type a task and press Enter. Type 'exit' to quit.\n")

history = []

while True:
    task = input("Task> ").strip()
    
    if task.lower() in {"exit", "quit"}:
        break
    if not task:
        continue

    history.append({"role": "user", "content": task})
    history = history[-10:]  # Keep last 10 messages (5 turns)

    try:
        response = client.messages.create(
            model=model,
            max_tokens=800,
            messages=history,
        )

        parts = [
            block.text
            for block in (response.content or [])
            if hasattr(block, "text") and block.text
        ]
        answer = "\n".join(parts).strip() or "[No text returned]"

        print(f"\nAgent:\n{answer}\n")
        history.append({"role": "assistant", "content": answer})

    except Exception as e:
        print(f"\nERROR: {e}\n")

