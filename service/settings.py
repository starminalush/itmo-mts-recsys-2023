from os import getenv as env

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)


class LogConfig(Config):
    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="log_")
    level: str = "INFO"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"


class ServiceConfig(Config):
    model_config = SettingsConfigDict(env_file=".env")
    service_name: str = "reco_service"
    k_recs: int = 10

    log_config: LogConfig

    ann_model_path: str
    pop_model_path: str
    kion_dataset_path: str

    vae_recos_path: str
    multivae_recos_path: str


def get_config() -> ServiceConfig:
    return ServiceConfig(
        log_config=LogConfig(),
    )
