from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref


class VerticalDivider(Control):
    """
    A thin vertical line, with padding on either side.

    In the material design language, this represents a divider.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):

        page.add(
            ft.Row(
                [
                    ft.Container(
                        bgcolor=ft.colors.ORANGE_300,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                    ft.VerticalDivider(),
                    ft.Container(
                        bgcolor=ft.colors.BROWN_400,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/verticaldivider
    """

    def __init__(
        self,
        ref: Optional[Ref] = None,
        opacity: OptionalNumber = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        width: OptionalNumber = None,
        thickness: OptionalNumber = None,
        color: Optional[str] = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            opacity=opacity,
            visible=visible,
            data=data,
        )

        self.width = width
        self.thickness = thickness
        self.color = color

    def _get_control_name(self):
        return "verticaldivider"

    # width
    @property
    def width(self) -> OptionalNumber:
        return self._get_attr("width")

    @width.setter
    def width(self, value: OptionalNumber):
        self._set_attr("width", value)

    # thickness
    @property
    def thickness(self) -> OptionalNumber:
        return self._get_attr("thickness")

    @thickness.setter
    def thickness(self, value: OptionalNumber):
        self._set_attr("thickness", value)

    # color
    @property
    def color(self):
        return self._get_attr("color")

    @color.setter
    def color(self, value):
        self._set_attr("color", value)
