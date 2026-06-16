"""Faraday business layer.

Pure, framework-agnostic. Apps depend on engine; engine never depends on apps.

Layout:
    domain/         entities (Pydantic data)
    services/       class.verb business logic
    repositories/   data access (ABC + SQLAlchemy impls)
    providers/      external integrations + registries
    factories/      construct wired services
"""
