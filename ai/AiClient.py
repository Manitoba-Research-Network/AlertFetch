from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam, ChatCompletionDeveloperMessageParam


class AIClient:
    def __init__(self, api_key:str, base_url:str, model:str):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.model = model

    def run_completion(self, user_msg:str, dev_msg:str) -> str:
        """
        run a completion query with the give messages
        :param user_msg:  user message
        :param dev_msg: dev message
        :return: completion string
        """
        res = self.client.chat.completions.create(
            model=self.model,
            messages=[
                ChatCompletionUserMessageParam(content=user_msg,
                                               role="user"),
                ChatCompletionDeveloperMessageParam(content=dev_msg, role="developer")
            ]
        )
        return res.choices[0].message.content