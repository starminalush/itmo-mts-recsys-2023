from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)


class LogConfig(Config):
    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="log_")
    level: str = "INFO"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"


class ServiceConfig(Config):
    model_config = SettingsConfigDict(env_file=".env", extra="forbid")
    service_name: str = "reco_service"
    k_recs: int = 10

    log_config: LogConfig

    ann_model_path: str = "weights/ann.pkl"
    pop_model_path: str = "weights/pop_model.pkl"
    user_knn_model_path: str = "weihts/user_knn.pkl"
    kion_dataset_path: str = "datasets/interactopns.csv"

    vae_recos_path: str = "offline/vae_recos.json"
    multivae_recos_path: str = "offline/multivae_user_reco.json"
    dssm_recos_path: str = "offline/dssm.json"
    two_stage_ranking: str = "offline/xgb_ranking_recos.json"
    token: str = "testtoken"


def get_config() -> ServiceConfig:
    return ServiceConfig(
        log_config=LogConfig(),
    )
