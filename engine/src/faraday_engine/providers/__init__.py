"""External integrations — LLM, vector store, instruments, chemistry APIs.

Each provider category has:
    base.py     — abstract base class + decorator registry
    *_provider.py — concrete impls, each self-registers via @Registry.register

To wire up a new provider: drop a file, add @Registry.register("name", config=ConfigClass).
No edits to the factory needed.
"""
