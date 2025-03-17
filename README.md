# Mock-OpenAI-python

To make unit testing easier, I made a simple mock of the [OpenAI python library](https://github.com/openai/openai-python) chat completions API.

I'll keep adding functionality as I require it.

Example usage:

```python
>>> from mock_openai import MockOpenAI
>>> llm_client = MockOpenAI()
>>> llm_client.chat.completions.mock.output_mode = "random_chars"
>>> response = llm_client.chat.completions.create(
...   model="gpt-4o",
...   messages=[
...     {"role": "user", "content": "model will ignore this :'("}
...   ],
... )
>>> response.choices[0].message.content
'wBgffmjwbggMdUyTceOBTibRhakwXi'
>>> llm_client.chat.completions.mock.output_mode = "cycle"
>>> llm_client.chat.completions.mock.cycle_outputs = ["first response", "second response"]
>>> for _ in range(3):
...   response = llm_client.chat.completions.create(
...   model="gpt-4o",
...   messages=[
...     {"role": "user", "content": "model will ignore this :'("}
...   ],
... )
>>> print(response.choices[0].message.content)
first response
second response
first response
```
