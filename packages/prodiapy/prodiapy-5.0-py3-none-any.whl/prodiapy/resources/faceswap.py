from __future__ import annotations

from prodiapy.resources.engine import APIResource
from prodiapy.resources.utils import form_body


class FaceSwap(APIResource):
    def __init__(self, client) -> None:
        super().__init__(client)

    def faceswap(
            self,
            source_url: str | None = None,
            target_url: str | None = None,
            dict_parameters: dict | None = None
    ) -> dict:
        return self._post(
            "/faceswap",
            body=form_body(
                dict_parameters=dict_parameters,
                sourceUrl=source_url,
                targetUrl=target_url
            )
        )


class AsyncFaceSwap(APIResource):
    def __init__(self, client) -> None:
        super().__init__(client)

    async def faceswap(
            self,
            source_url: str | None = None,
            target_url: str | None = None,
            dict_parameters: dict | None = None
    ) -> dict:
        return await self._post(
            "/faceswap",
            body=form_body(
                dict_parameters=dict_parameters,
                sourceUrl=source_url,
                targetUrl=target_url
            )
        )

