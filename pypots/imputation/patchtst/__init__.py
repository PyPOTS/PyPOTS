"""
The package of the partially-observed time-series imputation model PatchTST.

Refer to the paper
`Yuqi Nie, Nam H Nguyen, Phanwadee Sinthong, and Jayant Kalagnanam.
A time series is worth 64 words: Long-term forecasting with transformers.
In ICLR, 2023.
<https://openreview.net/pdf?id=Jbdc0vTOcol>`_

"""

# Created by Wenjie Du <wenjay.du@gmail.com>
# License: BSD-3-Clause


from .model import PatchTST

__all__ = [
    "PatchTST",
]
