from nicegui.element import Element


class Placeholder(Element, component="placeholder.js"):
    def __init__(self) -> None:
        """ """
        super().__init__()
        # self._props["name"] = name
        self._props["id"] = None
        self._props["props"] = None
        self.style("display:none")


placeholder = Placeholder
