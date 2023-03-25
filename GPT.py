import openai


def askGpt(prompt):

    openai.api_key = "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"

    # генерируем ответ
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt= str(prompt),
        max_tokens=2048,
        temperature=0.3
    )

    # выводим ответ
    return completion.choices[0].text
