import abc
import asyncio
import json
import typing

from loguru import logger
from openai import AsyncOpenAI
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from config import AI_API

client = AsyncOpenAI(api_key=AI_API, base_url="https://openrouter.ai/api/v1")


class WorkerAI:
    @staticmethod
    @retry(stop=stop_after_attempt(2), wait=wait_fixed(1), retry_if_exception_type=TimeoutError)
    async def is_has_ad(text: list[str]) -> list | None:
        try:
            json_text = json.dumps(text, indent=2, ensure_ascii=False)
            system_promt = """You are a strict text classifier. Your task is to determine whether the provided text is advertising (a direct call to purchase a product/service, mention of a brand with a benefit, a promotion, or a commercial offer).
        Criteria:
        - YES — if the text contains a direct offer to buy, a discount, a call to action (order, call), mention of price, or product advantages.
        - NO — if the text is news, a fact, a personal opinion, a review without a call to action, educational content, or mentions a brand in a neutral context.
        You MUST return only a single JSON array of strings in the format ["YES", "NO"] strictly in the same order as the input list. No explanations, semicolons, or extra text.}]
        """

            user_promt = f"Text for analysis...\n\n {text}"
            logger.debug(f"trying to get response")
            response = await asyncio.wait_for(
                client.chat.completions.create(
                    model="openrouter/free",
                    messages=[
                        {"role": "system", "content": system_promt},
                        {"role": "user", "content": user_promt},
                    ],
                    temperature=0.0,
                ),
                timeout=30,
            )

            logger.debug("trying to get result")
            result = response.choices[0].message.content
            logger.warning(f"result is {result}")

            if isinstance(result, list):
                return result
            else:
                return None
        except Exception as e:
            logger.exception(f"Error in is_has_ad {e}")
