import openai

openai.api_key = "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"

prompt = str(input("Введите запрос: "))

# генерируем ответ
completion = openai.Completion.create(
    model="text-davinci-003",
    prompt= prompt,
    max_tokens=2048,
    temperature=0.3
)

print("ChatGPT: " + completion.choices[0].text)
