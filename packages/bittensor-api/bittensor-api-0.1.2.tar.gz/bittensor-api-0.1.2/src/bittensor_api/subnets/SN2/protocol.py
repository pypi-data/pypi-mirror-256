# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2024 Manifold Labs

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


import bittensor as bt
import pydantic
from typing import List


class Translate(bt.Synapse):
    source_texts: List[str] = pydantic.Field(..., allow_mutation=False)
    translated_texts: List[str] = []
    source_lang: str = pydantic.Field(..., allow_mutation=False)
    target_lang: str = pydantic.Field(..., allow_mutation=False)
    required_hash_fields: list[str] = pydantic.Field(
        ["source_texts", "source_lang", "target_lang"], allow_mutation=False
    )
