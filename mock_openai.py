"""
Mock OpenAI client for testing out LLM wrapper functions
"""

import itertools
import random
import string
import time
import uuid
from typing import Optional

import openai


class Completions:
    class Mock:
        def __init__(self) -> None:
            self._output_mode: Optional[str] = None
            self._available_output_modes = (
                "random_chars",
                "cycle",
            )
            self._cycle_outputs: list[str] | None = None
            self._cycle: Optional[itertools.cycle] = None

        @property
        def output_mode(self) -> Optional[str]:
            return self._output_mode

        @property
        def cycle_outputs(self) -> list[str] | None:
            return self._cycle_outputs

        @output_mode.setter
        def output_mode(self, mode: str) -> None:
            if mode not in self._available_output_modes:
                raise ValueError(
                    f"mode '{mode}' does not exist - available modes are "
                    + "["
                    + ", ".join(self._available_output_modes)
                    + "]"
                )
            self._output_mode = mode

        @cycle_outputs.setter
        def cycle_outputs(self, cycle_outputs: list[str]) -> None:
            if not isinstance(cycle_outputs, list) or not all(
                isinstance(x, str) for x in cycle_outputs
            ):
                raise ValueError("`cycle_outputs` must have type list[str]")
            self._cycle_outputs = cycle_outputs
            self._cycle = itertools.cycle(self._cycle_outputs)

    def __init__(
        self,
    ):
        self.mock = self.Mock()

    def create_chat_completion(
        self,
        model: str,
        text_content: str,
    ):
        return openai.types.chat.ChatCompletion(
            id=uuid.uuid4().hex,
            choices=[
                openai.types.chat.chat_completion.Choice(
                    finish_reason="stop",
                    index=0,
                    message=openai.types.chat.chat_completion.ChatCompletionMessage(
                        role="assistant",
                        content=text_content,
                    ),
                )
            ],
            created=int(time.time()),
            model=model,
            object="chat.completion",
            usage=openai.types.completion_usage.CompletionUsage(
                completion_tokens=60, prompt_tokens=9, total_tokens=69
            ),
        )

    def create(
        self,
        model: str,
        messages: list[dict],
        **kwargs,
    ) -> openai.types.chat.ChatCompletion:
        match self.mock._output_mode:
            case "random_chars":
                return self.create_chat_completion(
                    model=model,
                    text_content="".join(
                        random.choice(string.ascii_letters) for _ in range(30)
                    ),
                )
            case "cycle":
                if not self.mock._cycle_outputs:
                    raise ValueError(
                        "Please set self.chat.completions.mock.cycle_outputs"
                    )
                return self.create_chat_completion(
                    model=model, text_content=next(self.mock._cycle)
                )

            case _:
                raise ValueError(f"Unexpected output_mode '{self.mock._output_mode}'")


class Chat:
    def __init__(
        self,
    ):
        self.completions = Completions()


class MockOpenAI:
    def __init__(self, *args, **kwargs) -> None:
        self.chat = Chat()
