"""HTTP request/response DTOs. Domain models are exposed directly when they're already
serializable; thin wrappers live here when the API shape diverges from domain."""
from faraday_api.schemas.ask import AskRequest

__all__ = ["AskRequest"]
