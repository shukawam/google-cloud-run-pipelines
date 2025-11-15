import os
from typing import Dict, List

import openai
from openai import Stream
from openai.types.responses import ResponseStreamEvent

DEFAULT_SYSTEM_CONTENT = """
ワークスペースのユーザーは、何かを書く手助けや、特定のトピックについてより良く考える手助けをあなたに求めます。
あなたはそれらの質問にプロフェッショナルな方法かつゴリラのユーモアを効かせて応答します。
マークダウンテキストを含める場合、それらをSlack互換のものに変換します。
プロンプトに<@USER_ID>や<#CHANNEL_ID>のようなSlackの特別な構文が含まれている場合、あなたはそれらをそのまま応答に残さなければなりません。
"""


def call_llm(
    messages_in_thread: List[Dict[str, str]],
    system_content: str = DEFAULT_SYSTEM_CONTENT,
) -> Stream[ResponseStreamEvent]:
    openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages = [{"role": "system", "content": system_content}]
    messages.extend(messages_in_thread)
    response = openai_client.responses.create(
        model="gpt-4o-mini", input=messages, stream=True
    )
    return response
