from __future__ import annotations
from typing import Callable, Dict, Optional, TypeVar, Generic
from typing_extensions import Self
from nicegui.element import Element
from nicegui import ui
from .utils import DeferredTask
from .teleport import teleport
from dataclasses import dataclass

_TTeleportKey = TypeVar("_TTeleportKey")
_TBuildFnArgs = TypeVar("_TBuildFnArgs")


class EasySlot(Element, Generic[_TTeleportKey, _TBuildFnArgs], component="easySlot.js"):
    def __init__(
        self,
        element: Element,
        slot_name: str,
        *,
        template: Callable[[Self], str],
        build_fn_args: Callable[[Self, Dict], _TBuildFnArgs],
        teleport_key: Callable[[Self, Dict], _TTeleportKey],
        teleport_class: Callable[[Self, _TBuildFnArgs], str],
    ) -> None:
        super().__init__()

        self.slot_name = slot_name
        self.teleport_class = teleport_class
        self.__deferred_tasks = DeferredTask()

        self.element = element
        self.element.add_slot(slot_name, template(self))

        self._slot_build_fn: Optional[Callable[[_TBuildFnArgs], teleport]] = None
        self._teleport_slots_cache: Dict[_TTeleportKey, teleport] = {}

        def on_notify(e):
            key = teleport_key(self, e.args)
            tp = self._teleport_slots_cache.get(key, None)
            if tp:
                tp.forceUpdate()
                return

            if self._slot_build_fn:
                tp = self._slot_build_fn(build_fn_args(self, e.args))
                self._teleport_slots_cache[key] = tp

        self.on("notify", on_notify)

    def __call__(self, build_fn: Callable[[_TBuildFnArgs], None]):
        id = f"c{self.element.id}"

        def fn(args: _TBuildFnArgs):
            class_name = self.teleport_class(self, args)
            with teleport(f"#{id} .{class_name}") as tp:
                build_fn(args)

            return tp

        self._slot_build_fn = fn

        @self.__deferred_tasks.register
        def _():
            self.run_method("triggerNotifyTasks")
            self.run_method("setLoaded")


@dataclass
class TableCellSlotProps:
    row_index: int
    field: str


def table_cell_slot(table: ui.table, field: str):
    slot_name = f"body-cell-{field}"

    def template(slot: EasySlot):
        return rf"""
        <q-td key="name" :props="props" >
            <nicegui-placeholder :id="{slot.id}" :props="props" :class="`easy-slot-{slot.slot_name}-${{props.rowIndex}}`"></nicegui-placeholder>
        </q-td>
    """

    def get_teleport_class(slot: EasySlot, args: TableCellSlotProps):
        return f"easy-slot-{slot.slot_name}-{args.row_index}"

    def build_fn_args(slot: EasySlot, args: Dict):
        return TableCellSlotProps(row_index=args["rowIndex"], field=field)

    def get_teleport_key(slot: EasySlot, args: Dict) -> int:
        return args["rowIndex"]

    return EasySlot(
        table,
        slot_name,
        template=template,
        teleport_class=get_teleport_class,
        build_fn_args=build_fn_args,
        teleport_key=get_teleport_key,
    )


@dataclass
class TableBodySlotProps:
    row_index: int

    def row(self):
        pass


def table_body_slot(table: ui.table):
    slot_name = f"body"

    def template(slot: EasySlot):
        return rf"""
        <q-tr key="name" :props="props" >

            <q-td :key="col" :props="props" v-for="[col,colObj] in Object.entries(props.colsMap)">
                <nicegui-placeholder :id="{slot.id}" :props="props" :class="`easy-slot-{slot.slot_name}-${{col}}-${{props.rowIndex}}`"></nicegui-placeholder>
            </q-td>

        </q-tr>
    """

    def get_teleport_class(slot: EasySlot, args: TableBodySlotProps):
        return f"easy-slot-{slot.slot_name}-{args.row_index}"

    def build_fn_args(slot: EasySlot, args: Dict):
        return TableBodySlotProps(row_index=args["rowIndex"])

    def get_teleport_key(slot: EasySlot, args: Dict) -> int:
        return args["rowIndex"]

    return EasySlot(
        table,
        slot_name,
        template=template,
        teleport_class=get_teleport_class,
        build_fn_args=build_fn_args,
        teleport_key=get_teleport_key,
    )


@dataclass
class SelectOptionSlotProps:
    index: int


def select_option_slot(select: ui.select):
    slot_name = f"option"

    def template(slot: EasySlot):
        return rf"""
        <nicegui-placeholder :id="{slot.id}" :props="props" :class="`easy-slot-{slot.slot_name}-${{props.index}}`"></nicegui-placeholder>
    """

    def get_teleport_class(slot: EasySlot, args: SelectOptionSlotProps):
        return f"easy-slot-{slot.slot_name}-{args.index}"

    def build_fn_args(slot: EasySlot, args: Dict):
        return SelectOptionSlotProps(index=args["index"])

    def get_teleport_key(slot: EasySlot, args: Dict) -> int:
        return args["index"]

    return EasySlot(
        select,
        slot_name,
        template=template,
        teleport_class=get_teleport_class,
        build_fn_args=build_fn_args,
        teleport_key=get_teleport_key,
    )
