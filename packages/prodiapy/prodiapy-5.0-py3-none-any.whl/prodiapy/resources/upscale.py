from __future__ import annotations

from prodiapy.resources.engine import APIResource
from typing import Union
from prodiapy.resources.constants import *
from prodiapy.resources.utils import form_body


class Upscale(APIResource):
    def __init__(self, client) -> None:
        super().__init__(client)

    def upscale(
            self,
            image_url: str | None = None,
            image_data: str | None = None,
            resize: Union[int, Literal[2, 4]] = 2,
            dict_parameters: dict | None = None
    ) -> dict:
        return self._post(
            "/upscale",
            body=form_body(
                dict_parameters=dict_parameters,
                imageUrl=image_url,
                imageData=image_data,
                resize=resize
            )
        )


class AsyncUpscale(APIResource):
    def __init__(self, client) -> None:
        super().__init__(client)

    async def upscale(
            self,
            image_url: str | None = None,
            image_data: str | None = None,
            resize: Union[int, Literal[2, 4], None] = None,
            dict_parameters: dict | None = None
    ) -> dict:
        return await self._post(
            "/upscale",
            body=form_body(
                dict_parameters=dict_parameters,
                imageUrl=image_url,
                imageData=image_data,
                resize=resize
            )
        )

