import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any, Dict

import uvloop
from fastapi import FastAPI

from service.utils.unpickler import load

from ..log import app_logger, setup_logging
from ..recsys_models.offline_reco import OfflineReco
from ..recsys_models.popular_model import PopModel
from ..settings import ServiceConfig
from .exception_handlers import add_exception_handlers
from .middlewares import add_middlewares
from .views import add_views

__all__ = ("create_app",)


def setup_asyncio(thread_name_prefix: str) -> None:
    uvloop.install()

    loop = asyncio.get_event_loop()

    executor = ThreadPoolExecutor(thread_name_prefix=thread_name_prefix)
    loop.set_default_executor(executor)

    def handler(_, context: Dict[str, Any]) -> None:
        message = "Caught asyncio exception: {message}".format_map(context)
        app_logger.warning(message)

    loop.set_exception_handler(handler)


def create_app(config: ServiceConfig) -> FastAPI:
    setup_logging(config)
    setup_asyncio(thread_name_prefix=config.service_name)

    models = {
        "vae_reco_offline": OfflineReco(
            recos_path=config.vae_recos_path,
            popular_model=PopModel(dataset_path=config.kion_dataset_path, backbone_model=load(config.pop_model_path)),
        ),
        "multivae": OfflineReco(
            recos_path=config.multivae_recos_path,
            popular_model=PopModel(dataset_path=config.kion_dataset_path, backbone_model=load(config.pop_model_path)),
        ),
        "dssm": OfflineReco(
            recos_path=config.dssm_recos_path,
            popular_model=PopModel(dataset_path=config.kion_dataset_path, backbone_model=load(config.pop_model_path)),
        ),
    }

    new_app = FastAPI(debug=False)
    new_app.state.k_recs = config.k_recs
    new_app.state.models = models
    add_views(new_app)
    add_middlewares(new_app)
    add_exception_handlers(new_app)

    return new_app
