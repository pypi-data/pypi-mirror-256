from dataclasses import dataclass
import json
import logging
import os
import threading
from typing import Optional
import urllib3

LAMBDA_EXTENSION_NAME = "lambda-sigterm"
LAMBDA_EXTENSION_VERSION = "2020-01-01"

http = urllib3.PoolManager()


@dataclass
class Context:
    logger: logging.Logger = None
    log_level: int = logging.ERROR
    log_level_debug_msg: int = logging.DEBUG
    log_level_info_msg: int = logging.INFO
    log_level_error_msg: int = logging.ERROR
    lambda_runtime_api_host: str = ''


def _register(ctx: Context) -> Optional[str]:
    response = http.request(
        "POST",
        f"http://{ctx.lambda_runtime_api_host}/{LAMBDA_EXTENSION_VERSION}/extension/register",
        headers={
            "Lambda-Extension-Name": LAMBDA_EXTENSION_NAME,
            "Content-Type": "application/json",
        },
        body=json.dumps({}).encode("utf-8"),
    )
    if response.status // 100 != 2:
        ctx.logger.log(
            level=ctx.log_level_error_msg,
            msg=f"could not register extension, request failed: {response.data.decode('utf-8')}",
        )
        return None
    return response.headers.get("Lambda-Extension-Identifier")


def _next(ctx: Context, id: str) -> None:
    # blocks until lambda finishes executing
    http.request(
        "GET",
        f"http://{ctx.lambda_runtime_api_host}/{LAMBDA_EXTENSION_VERSION}/extension/event/next",
        headers={
            "Lambda-Extension-Identifier": id,
        },
    )


def _run(ctx: Context) -> None:
    id = _register(ctx)
    if not id:
        ctx.logger.log(
            level=ctx.log_level_error_msg,
            msg="could not register extension, extension id not resolved",
        )
        return

    threading.Thread(target=_next, name=None, args=[ctx, id]).start()


def register(
    log_level: int = logging.INFO,
    **kwargs,
):
    ctx = Context(**kwargs)

    if ctx.logger is None:
        ctx.logger = logging.getLogger(__name__)
        ctx.logger.setLevel(log_level)

    if ctx.lambda_runtime_api_host == "":
        ctx.lambda_runtime_api_host = os.getenv("AWS_LAMBDA_RUNTIME_API", "")
        if ctx.lambda_runtime_api_host == "":
            ctx.logger.log(
                level=ctx.log_level_error_msg,
                msg="AWS_LAMBDA_RUNTIME_API env unset, returning without starting",
            )
            return

    _run(ctx)

    ctx.logger.log(
        level=ctx.log_level_info_msg,
        msg="lambda-sigterm extension started",
    )