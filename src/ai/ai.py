import abc
import asyncio
import json
import typing

from loguru import logger
from openai import AsyncOpenAI
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from config import AI_API, AI_ROUTER_API, BASE_URL, OLD_BASE_URL

client = AsyncOpenAI(api_key=AI_API, base_url=BASE_URL)
router_client = AsyncOpenAI(api_key=AI_ROUTER_API, base_url=OLD_BASE_URL)


@typing.final
class WorkerAI:
    @staticmethod
    @retry(
        stop=stop_after_attempt(2),
        wait=wait_fixed(1),
    )
    # TODO: this finc has no profit. so wont use it. will delete later
    async def is_has_ad(text: list[str]) -> list | None:
        try:
            # json_text = json.dumps(text, indent=2, ensure_ascii=False)
            system_promt = """You are a strict text classifier. Your task is to determine whether the provided text is advertising (a direct call to purchase a product/service, mention of a brand with a benefit, a promotion, or a commercial offer).
        Criteria:
        - YES — if the text contains a direct offer to buy, a discount, a call to action (order, call), mention of price, or product advantages.
        - NO — if the text is news, a fact, a personal opinion, a review without a call to action, educational content, or mentions a brand in a neutral context.
        You MUST return only a single JSON array of strings in the format ["YES", "NO"] strictly in the same order as the input list. No explanations, semicolons, or extra text.}]
        """

            user_promt = f"Text for analysis...\n\n {text}"
            logger.debug("trying to get response")
            response = await asyncio.wait_for(
                client.chat.completions.create(
                    model="gemini-1.5-flash",
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
    async def say_hello() -> list | None:
        try:
            # json_text = json.dumps(text, indent=2, ensure_ascii=False)
            promt = 'you only say "hello." '

            logger.debug("trying to get response")
            response = await asyncio.wait_for(
                client.chat.completions.create(
                    model="gemini-3.5-flash-lite",
                    messages=[
                        {"role": "user", "content": promt},
                    ],
                    temperature=0.0,
                ),
                timeout=30,
            )

            result = response.choices[0].message.content
            logger.warning(f"response is {result}")
        except Exception as e:
            logger.exception("No hello for us", e)

    @staticmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
    )
    async def analyze_daily_data(data: list[list[str]]) -> typing.Any:
        try:
            system_promt = """You are a news analyst. Your task is to cluster and categorize daily Telegram news.

INPUT: Array of news items with channel name, and text.

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
   - ecology
3. Write a clear, neutral title and a 2-3 sentence summary in Russian for each cluster.
4. Rate fact_quality from 1 to 5: 5 = confirmed fact/official statement/statistic, 1 = rumor/unverified claim/opinion.
5. Skip advertising/promotional content and pure entertainment.
6. A single mention does NOT automatically mean unreliable — 
   if the fact is stated clearly and neutrally (official statement, 
   confirmed event, verifiable data), include it even from one source, 
   but reflect this in a lower fact_quality score if uncorroborated.
7. Only skip genuinely unverifiable rumors or gossip lacking any concrete 
   factual basis, regardless of source count.

Do NOT invent channel names or ids that weren't in the input.
Only include a channel in "channels" if it reports THIS SPECIFIC event, 
not just mentions related entities in passing.

IMPORTANT: The input contains news from specialized channels covering 
technology, crypto, and ecology topics specifically. Even if political 
news dominates by volume, you MUST actively look for and include distinct 
clusters from technology, crypto_fintech, and ecology categories if any 
relevant news exists in the input — do not let them get overshadowed.


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

            user_promt = f"data for analysis...\n\n {data}"
            logger.debug("trying to get response")
            response = await asyncio.wait_for(
                client.chat.completions.create(
                    model="gemini-3.5-flash-lite",
                    messages=[
                        {"role": "system", "content": system_promt},
                        {"role": "user", "content": user_promt},
                    ],
                    temperature=0.0,
                    response_format={"type": "json_object"},
                ),
                timeout=3600,
            )

            logger.debug("trying to get result")
            result = response.choices[0].message.content
            if result:
                result = json.loads(result)
            else:
                result = ""

            logger.warning(f"result is {result}")
            return result
        except Exception as e:
            logger.exception(f"Error in is_has_ad {e}")
