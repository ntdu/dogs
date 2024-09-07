
import httpx
import logging
from typing import Literal

logger = logging.getLogger(__name__)

async def send_external_api_request(
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
    url: str,
    base_url: str = "",
    headers: dict | None = None,
    data: dict = None,
    json: dict | None = None,
    params: dict | None = None,
) -> httpx.Response:
    async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=150) as client:
        response = await client.request(
            method=method, url=url, json=json, params=params, data=data
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            logger.warning(
                f"Error encountered while sending {method} Request to {url=} => {response.text}"
            )
            raise
        return response
