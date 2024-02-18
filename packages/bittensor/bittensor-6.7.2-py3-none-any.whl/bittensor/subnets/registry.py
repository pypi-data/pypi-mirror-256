# The MIT License (MIT)
# Copyright © 2021 Yuma Rao
# Copyright © 2023 Opentensor Foundation
# Copyright © 2023 Opentensor Technologies Inc

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


class RegistryMeta(type):
    def __str__(cls):
        return f"APIRegistry with handlers: {list(cls._apis)}"

    def __repr__(cls):
        return f"APIRegistry with handlers: {list(cls._apis)}"


class APIRegistry(metaclass=RegistryMeta):
    _apis = {}

    @classmethod
    def register_api_handler(cls, key, handler):
        cls._apis[key] = handler

    @classmethod
    def get_api_handler(cls, key, *args, **kwargs):
        handler = cls._apis.get(key)
        if not handler:
            raise ValueError(f"No handler registered for key: {key}")
        return handler(*args, **kwargs)

    @classmethod
    def __call__(cls, *args, **kwargs):
        return cls.get_api_handler(*args, **kwargs)


def register_handler(key):
    def decorator(cls):
        APIRegistry.register_api_handler(key, cls)
        return cls

    return decorator
