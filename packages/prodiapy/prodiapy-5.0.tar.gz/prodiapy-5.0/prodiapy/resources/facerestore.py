from __future__ import annotations

from prodiapy.resources.engine import APIResource
from prodiapy.resources.utils import form_body


class FaceRestore(APIResource):
    def __init__(self, client) -> None:
        super().__init__(client)

    def facerestore(
            self,
            image_url: str | None = None,
            image_data: str | None = None,
            dict_parameters: dict | None = None
    ) -> dict:
        return self._post(
            "/facerestore",
            body=form_body(
                dict_parameters=dict_parameters,
                imageUrl=image_url,
                imageData=image_data
            )
        )


class AsyncFaceRestore(APIResource):
    def __init__(self, client) -> None:
        super().__init__(client)

    async def facerestore(
            self,
            image_url: str | None = None,
            image_data: str | None = None,
            dict_parameters: dict | None = None
    ) -> dict:
        return await self._post(
            "/facerestore",
            body=form_body(
                dict_parameters=dict_parameters,
                imageUrl=image_url,
                imageData=image_data
            )
        )

