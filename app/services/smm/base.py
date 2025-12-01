from soc_proof import SocProofAPI
from soc_proof.cache import DataCache

from app.core.config import settings

cache = DataCache()

smm_api = SocProofAPI(
    api_key=settings.SOC_PROOF_API_KEY.get_secret_value(),
    cache=cache
)