from pathlib import Path

from self_healing_sre_agent.config import load_settings


def test_load_settings_reads_env_file(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "SERVICE_NAME=test-agent",
                "LOG_LEVEL=DEBUG",
                "MAX_ITERATIONS=3",
                "ALLOW_LIVE_REMEDIATION=true",
            ]
        ),
        encoding="utf-8",
    )

    settings = load_settings(env_file)

    assert settings.service_name == "test-agent"
    assert settings.log_level == "DEBUG"
    assert settings.max_iterations == 3
    assert settings.allow_live_remediation is True
