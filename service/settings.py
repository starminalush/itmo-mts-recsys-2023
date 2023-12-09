from os import getenv as env

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)


class LogConfig(Config):
    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="log_")
    level: str = "INFO"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"


class ServiceConfig(Config):
    service_name: str = "reco_service"
    k_recs: int = 10

    log_config: LogConfig

    ann_model_path: str = env("ANN_MODEL_PATH", "/usr/src/app/weights/ann_lightfm.pkl")
    popular_model_path: str = env("POP_MODEL_PATH", "/usr/src/app/weights/pop_model.pkl")
    kion_dataset_path: str = env("KION_DATASET", "datasets/kion_interactions.csv")


def get_config() -> ServiceConfig:
    return ServiceConfig(
        log_config=LogConfig(),
    )
