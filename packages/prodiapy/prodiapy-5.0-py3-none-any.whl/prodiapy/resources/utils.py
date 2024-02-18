from __future__ import annotations
from prodiapy._exceptions import *


def form_body(dict_parameters: dict | None = None, **kwargs):
    if dict_parameters:
        body = dict_parameters
    else:
        body = {}
        for kwarg in kwargs:
            if kwargs.get(kwarg) is not None:
                body[kwarg] = kwargs.get(kwarg)

    return body


def raise_exception(status, message):
    message_body = f"Prodia API returned {status}. Details: {message}"
    if status == 200:
        pass
    elif status in exception_vocab:
        raise exception_vocab[status](message_body)
    else:
        raise UnknownError(message_body)


