import abc
import asyncio
import json
import typing

from loguru import logger
from openai import AsyncOpenAI
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from config import AI_API, BASE_URL

client = AsyncOpenAI(api_key=AI_API, base_url=BASE_URL)


@typing.final
class WorkerAI:
    @staticmethod
    @retry(
        stop=stop_after_attempt(2),
        wait=wait_fixed(1),
    )
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

    @staticmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
    )
    async def analyze_daily_data(data: list[list[str]]) -> typing.Any:
        try:
            json_text = json.dumps(text, indent=2, ensure_ascii=False)

            system_promt = """You are a news analyst. Your task is to cluster and categorize daily Telegram news.

INPUT: Array of news items with id, channel name, and text.

YOUR TASKS:
1. Group news items that describe the same event into clusters, even if phrased differently across channels.
2. Assign each cluster to exactly one category:
   - politics (Russia and world)
   - economy
   - technology (IT, science, AI)
   - society (laws, social sphere)
   - crypto_fintech
   - emergencies
   - culture_lifestyle
3. Write a clear, neutral title and a 2-3 sentence summary in Russian for each cluster.
4. Rate fact_quality from 1 to 5: 5 = confirmed fact/official statement/statistic, 1 = rumor/unverified claim/opinion.
5. Skip pure entertainment, clickbait without substance, and single-source unverifiable gossip.
6. List the ids of all source news items that belong to this cluster.

Do NOT invent channel names or ids that weren't in the input.

OUTPUT: Return ONLY a valid JSON object, no markdown fences, no explanation text.

EXAMPLE OUTPUT:
{
  "clusters": [
    {
      "category": "politics",
      "title": "Заголовок на русском",
      "summary": "Краткое описание на русском, 2-3 предложения",
      "fact_quality": 4,
      "channels": ["ria_novosti", "readovka", "shot"]
    }
  ]
}

If no significant clusters exist for a category, simply don't include entries for it."""

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
                    response_format={"type": "json_object"},
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
