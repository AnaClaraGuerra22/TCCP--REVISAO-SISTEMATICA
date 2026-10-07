import ollama


MODEL = "qwen3:8b"


response = ollama.chat(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": (
                "This is an infrastructure test. "
                "Reply only with TESTE_OK."
            ),
        }
    ],
    options={
        "temperature": 0,
    },
    think=False,
)


answer = response["message"]["content"].strip()


print()
print("OLLAMA INFRASTRUCTURE TEST")
print("-------------------------")
print(f"Model: {MODEL}")
print(f"Response: {answer}")
print()


if answer != "TESTE_OK":
    raise ValueError(
        "O modelo respondeu, mas não retornou exatamente TESTE_OK."
    )


print("Status: OK")