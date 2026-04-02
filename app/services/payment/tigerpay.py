from typing import Any

import aiohttp
from pydantic import BaseModel, Field, field_validator

from app.core.config import settings
from app.core.logging import logger


class TigerPayError(RuntimeError):
	pass


class TigerPayCreatePaymentRequest(BaseModel):
	partner_payment_id: str
	amount: int
	callback_url: str
	currency: str = "RUB"
	payment_type: str = "ACQ_SBP"
	back_url: str = "https://t.me/smmly_bot/app?startapp=success"
	payment_lifetime: int = Field(..., ge=1, le=30)
	payload: str | None = None


	@field_validator("partner_payment_id", "currency", "payment_type", "callback_url", "back_url")
	@classmethod
	def validate_required_strings(cls, value: str) -> str:
		value = value.strip()
		if not value:
			raise ValueError("Field must not be empty.")
		return value

	@field_validator("amount")
	@classmethod
	def validate_amount(cls, value: int) -> int:
		if value <= 0:
			raise ValueError("Amount must be greater than zero.")
		return value


class TigerPayService:
	def __init__(
		self,
		timeout: float = 30.0,
	):
		self.base_url = settings.TIGER_PAY_URL.rstrip("/")
		self.api_key = settings.TIGER_PAY_KEY.get_secret_value()
		self.timeout = timeout

	def _get_headers(self) -> dict[str, str]:
		return {
			"apikey": self.api_key,
			"Accept": "application/json",
		}

	async def _request(
		self,
		path: str,
		*,
		params: dict[str, Any] | None = None,
	) -> dict[str, Any]:
		request_params = {
			key: value
			for key, value in (params or {}).items()
			if value is not None
		}
		headers = self._get_headers()
		timeout = aiohttp.ClientTimeout(total=self.timeout)

		try:
			async with aiohttp.ClientSession(
				base_url=self.base_url,
				headers=headers,
				timeout=timeout,
			) as session:
				async with session.get(path, params=request_params or None) as response:
					response_text = await response.text()
		except aiohttp.ClientError as exc:
			logger.error(f"Tiger Pay request transport error: {exc}")
			raise TigerPayError("Tiger Pay request failed.") from exc

		if response.status >= 400:
			logger.error(
				f"Tiger Pay request failed: GET {path} "
				f"status={response.status} body={response_text}"
			)
			raise TigerPayError(
				f"Tiger Pay returned HTTP {response.status}: {response_text}"
			)

		if not response_text:
			return {}

		try:
			return await response.json()
		except ValueError as exc:
			logger.error(
				f"Tiger Pay returned a non-JSON response for GET {path}: {response_text}"
			)
			raise TigerPayError("Tiger Pay returned an invalid response body.") from exc

	async def create_payment(
		self,
		payload: TigerPayCreatePaymentRequest,
	) -> dict[str, Any]:
		request_params = {
			"PartnerPaymentId": payload.partner_payment_id,
			"Amount": payload.amount,
			"Currency": payload.currency,
			"PaymentType": payload.payment_type,
			"CallbackUrl": payload.callback_url,
			"BackUrl": payload.back_url,
			"PaymentLifeTime": str(payload.payment_lifetime),
			"Payload": payload.payload,
		}

		logger.info(f"TigerPay create params: {request_params}")
		result = await self._request("/api/v3/fiat/payments/create", params=request_params)
		logger.info(f"TigerPay response: {result}")

		return result


tiger_pay_service = TigerPayService()