"""
#
# Carium Chart Themes
#
# Copyright(c) 2021, Carium, Inc. All rights reserved.
#
"""

from brewmaster.apis.base import Endpoint


class ColorScheme(Endpoint):
    _categorylight9 = [
        "#00B0BD",
        "#FB5D8C",
        "#FBC772",
        "#66D0D7",
        "#FDDDAA",
        "#BB52A8",
        "#47DD99",
        "#FDBE59",
        "#FD9EBA",
    ]

    _categorydark9 = [
        "#00B0BD",
        "#00393D",
        "#5A7475",
        "#00818A",
        "#AFDADD",
        "#4EA0A6",
        "#93B1B4",
        "#1C585C",
        "#66D0D7",
    ]

    _category20 = [
        "#00B0BD",
        "#FB5D8C",
        "#FBC772",
        "#66D0D7",
        "#FDDDAA",
        "#9C763A",
        "#47DD99",
        "#FDBE59",
        "#C74A6F",
        "#AFDADD",
        "#00A35A",
        "#CCB289",
        "#9C5690",
        "#00393D",
        "#D7BBD2",
        "#7A2D44",
        "#C74A6F",
        "#93B1B4",
        "#50B587",
        "#00818A",
    ]

    def category_light_9(self) -> list:
        """9 Carium themed light colors

        Returns:
            A list of 9 color codes to be used in altair
        """
        return self._categorylight9

    def category_dark_9(self) -> list:
        """9 Carium themed dark colors

        Returns:
            A list of 9 color codes to be used in altair
        """
        return self._categorydark9

    def category_20(self) -> list:
        """20 Carium themed colors

        Returns:
            A list of 20 color codes to be used in altair
        """
        return self._category20
