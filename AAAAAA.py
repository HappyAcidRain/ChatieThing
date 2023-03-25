
import openai
openai.api_key = "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"

completion = openai.Completion.create(
  model="text-davinci-003",
  prompt="кто такой пушкин",
  max_tokens=2048,
  temperature=0.5
)

print(completion.choices[0].text)
