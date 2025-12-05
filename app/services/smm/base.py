from soc_proof import SocProofAPI

from app.core.config import settings

smm_api = SocProofAPI(
    token=settings.SOC_PROOF_API_KEY.get_secret_value()
)