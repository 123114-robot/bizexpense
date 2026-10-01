from app.core.config import Settings


def test_cors_origins_are_trimmed_and_empty_values_are_removed():
    settings = Settings(cors_origins="https://app.example, https://admin.example, ")

    assert settings.allowed_origins == [
        "https://app.example",
        "https://admin.example",
    ]


def test_allowed_hosts_are_trimmed():
    settings = Settings(allowed_hosts="api.example, localhost")

    assert settings.trusted_hosts == ["api.example", "localhost"]
