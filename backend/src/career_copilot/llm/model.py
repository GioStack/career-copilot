from pydantic_ai.models import infer_model
from pydantic_ai.providers import infer_provider_class

from career_copilot.core.config import settings


class LLMNotConfiguredError(Exception):
    """Raised when LLM_PROVIDER or LLM_MODEL is not set."""


def get_model():
    """Build the LLM from the settings, or raise if it is not configured (ADR 0019)."""
    if settings.llm_provider is None or settings is None:
        raise LLMNotConfiguredError("Set LLM_PROVIDER and LLM_MODEL in .env")

    # Only the options that are set; a local Ollama needs a base URL but no key.
    options: dict[str, str] = {}
    if settings.llm_api_key is not None:
        options["api_key"] = settings.llm_api_key.get_secret_value()
    if settings.llm_base_url is not None:
        options["base_url"] = settings.llm_base_url

    # The provider's class comes from its name, so there is no code for each provider.
    provider = infer_provider_class(settings.llm_provider)(**options)

    return infer_model(
        f"{settings.llm_provider}:{settings.llm_model}", provider_factory=lambda _name: provider
    )
