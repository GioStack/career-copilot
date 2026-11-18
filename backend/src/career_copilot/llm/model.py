from pydantic_ai.exceptions import UserError
from pydantic_ai.models import Model, infer_model
from pydantic_ai.providers import infer_provider_class

from career_copilot.core.config import settings


class LLMNotConfiguredError(Exception):
    """Raised when the LLM settings are missing or incomplete."""


def get_model() -> Model:
    """Build the LLM from the settings, or raise if it is not configured (ADR 0019)."""
    if settings.llm_provider is None or settings.llm_model is None:
        raise LLMNotConfiguredError("Set LLM_PROVIDER and LLM_MODEL in .env")

    # Only the options that are set; a local Ollama needs a base URL but no key.
    options: dict[str, str] = {}
    if settings.llm_api_key is not None:
        options["api_key"] = settings.llm_api_key.get_secret_value()
    if settings.llm_base_url is not None:
        options["base_url"] = settings.llm_base_url

    # The provider's class comes from its name, so there is no code for each provider.
    # Its error names its own variable (e.g. GOOGLE_API_KEY), which this app does not read,
    # so it is replaced with one that names ours.
    try:
        provider = infer_provider_class(settings.llm_provider)(**options)
    except UserError as error:
        raise LLMNotConfiguredError(
            f"Check LLM_API_KEY and LLM_BASE_URL in .env ({error})"
        ) from error

    return infer_model(
        f"{settings.llm_provider}:{settings.llm_model}", provider_factory=lambda _name: provider
    )
