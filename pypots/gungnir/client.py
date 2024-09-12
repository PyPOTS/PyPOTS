# coding=utf-8

"""

"""

# Created by Wenjie Du <wenjay.du@gmail.com>
# License: BSD-3-Clause

from ..utils.logging import logger

logger.info(
    """\u001b[34m
████████╗██╗███╗   ███╗███████╗    ███████╗███████╗██████╗ ██╗███████╗███████╗    █████╗ ██╗
╚══██╔══╝██║████╗ ████║██╔════╝    ██╔════╝██╔════╝██╔══██╗██║██╔════╝██╔════╝   ██╔══██╗██║
   ██║   ██║██╔████╔██║█████╗█████╗███████╗█████╗  ██████╔╝██║█████╗  ███████╗   ███████║██║
   ██║   ██║██║╚██╔╝██║██╔══╝╚════╝╚════██║██╔══╝  ██╔══██╗██║██╔══╝  ╚════██║   ██╔══██║██║
   ██║   ██║██║ ╚═╝ ██║███████╗    ███████║███████╗██║  ██║██║███████╗███████║██╗██║  ██║██║
   ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═╝╚═╝

v{0.1} - building AI for unified time-series analysis, https://time-series.ai
\u001b[0m
"""
)

from ai4ts.client import TimeSeriesAI


class Gungnir(TimeSeriesAI):
    def __init__(self):
        super().__init__()
        logger.info(
            "The functionalities of client Gungnir have not been implemented yet,\n"
            "which will be updated later 2024 once our close beta test is ready.\n"
            "AI for real-world time series is coming. 🚀 Stay tuned please! https://time-series.ai"
        )
