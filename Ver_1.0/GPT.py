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
