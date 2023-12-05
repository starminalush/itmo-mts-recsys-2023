import asyncio
import os
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any, Dict

import uvloop
from fastapi import FastAPI

from ..log import app_logger, setup_logging
from ..recsys_models import PopModel, TestModel, UserKnn
from ..recsys_models.model_loader import load
from ..settings import ServiceConfig
from .exception_handlers import add_exception_handlers
from .middlewares import add_middlewares
from .views import add_views

__all__ = ("create_app",)

test_model = TestModel()
user_knn = UserKnn(
    backbone_model=load(os.getenv("USER_KNN_MODEL_PATH")),
    cold_user_reco_model=PopModel(
        dataset_path=os.getenv("POP_MODEL_DATASET"), backbone_model=load(os.getenv("POP_MODEL_WEIGHTS"))
    ),
)
models = {"test_model": test_model, "userknn_tfidf": user_knn}


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

    new_app = FastAPI(debug=False)
    new_app.state.k_recs = config.k_recs
    new_app.state.models = models
    add_views(new_app)
    add_middlewares(new_app)
    add_exception_handlers(new_app)

    return new_app
