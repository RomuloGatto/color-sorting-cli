from harmony import convertions, core, data_access


class ColorFactory:
    """Provide methods for making colors"""

    def make_from_hexcode_with_auto_label(self, hexcode: str) -> core.Color:
        """Make a `Color` from a RGB in hexcode format with a self-generated description

        Args:
            hexcode (str): string of a RGB in hexcode format

        Returns:
            core.Color: the resulting color
        """
        return self.make_from_hexcode(
            hexcode, self.__get_description_from_hexcode(hexcode)
        )

    def __get_description_from_hexcode(self, hexcode: str) -> str:
        return data_access.ColorNamesStorage().get_color_name_by_hsl(
            self.__get_hsl_from_hexcode(hexcode)
        )

    def make_from_hexcode(self, hexcode: str, description: str) -> core.Color:
        """Make a `Color` from a RGB in hexcode format

        Args:
            hexcode (str): string of a RGB in hexcode format
            description (str): label of the color

        Returns:
            core.Color: the resulting color
        """
        return core.Color(
            rgb=core.RGBUtils.get_rgb_from_hexcode(hexcode),
            hsl=self.__get_hsl_from_hexcode(hexcode),
            hexcode=hexcode,
            original_format=core.ColorFormat.HEXCODE,
            description=description,
        )

    def __get_hsl_from_hexcode(self, hexcode: str) -> core.HSL:
        return convertions.RGBToHSLConverter().convert(
            core.RGBUtils.get_rgb_from_hexcode(hexcode)
        )

    def make_from_rgb_with_auto_label(self, rgb: core.RGB) -> core.Color:
        """Make a `Color` from a `RGB` object with a self-generated description

        Args:
            rgb (RGB): `RGB` object

        Returns:
            core.Color: the resulting color
        """
        return self.make_from_rgb(rgb, self.__get_description_from_rgb(rgb))

    def __get_description_from_rgb(self, rgb: core.RGB) -> str:
        return data_access.ColorNamesStorage().get_color_name_by_hsl(
            convertions.RGBToHSLConverter().convert(rgb)
        )

    def make_from_rgb(self, rgb: core.RGB, description: str) -> core.Color:
        """Make a `Color` from a `RGB` object

        Args:
            rgb (RGB): `RGB` object
            description (str): label of the color

        Returns:
            core.Color: the resulting color
        """
        return core.Color(
            rgb=rgb,
            hsl=convertions.RGBToHSLConverter().convert(rgb),
            hexcode=core.HexcodeUtils.get_hexcode_from_rgb(rgb),
            original_format=core.ColorFormat.RGB,
            description=description,
        )

    def make_from_hsl_with_auto_label(self, hsl: core.HSL) -> core.Color:
        """Make a `Color` from a `HSL` object with a self-generated description

        Args:
            hsl (core.HSL): `HSL` object

        Returns:
            core.Color: the resulting color
        """
        return self.make_from_hsl(
            hsl, data_access.ColorNamesStorage().get_color_name_by_hsl(hsl)
        )

    def make_from_hsl(self, hsl: core.HSL, description: str) -> core.Color:
        """Make a `Color` from a `HSL` object

        Args:
            hsl (HSL): `HSL` object
            description (str): label of the color

        Returns:
            core.Color: the resulting color
        """
        return core.Color(
            rgb=convertions.HSLToRGBConverter().convert(hsl),
            hsl=hsl,
            hexcode=self.__get_hexcode_from_hsl(hsl),
            original_format=core.ColorFormat.HSL,
            description=description,
        )

    def __get_hexcode_from_hsl(self, hsl: core.HSL) -> str:
        return core.HexcodeUtils.get_hexcode_from_rgb(
            convertions.HSLToRGBConverter().convert(hsl)
        )
