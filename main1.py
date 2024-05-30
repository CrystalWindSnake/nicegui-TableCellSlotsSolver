from nicegui import events, ui
from src.placeholder import placeholder
from src.easySlot import (
    table_cell_slot,
    TableCellSlotProps,
)

# Since this component is used within string slots of table components,
# instantiating a placeholder component is necessary for NiceGUI to register the component properly.
placeholder()

columns = [
    {"name": "name", "label": "Name", "field": "name"},
    {"name": "age", "label": "Age", "field": "age"},
]
rows = [
    {"id": 0, "name": "Alice", "age": 18},
    {"id": 1, "name": "Bob", "age": 21},
    {"id": 2, "name": "Carol"},
]
name_options = ["Alice", "Bob", "Carol"]


def rename(e: events.ValueChangeEventArguments, index: int) -> None:
    print(f"Renamed row {index} to {e.value}")
    row = rows[index]
    row["name"] = e.value
    ui.notify(f"Table.rows is now: {table.rows}")


table = ui.table(columns=columns, rows=rows, pagination=2).classes("w-full")


@table_cell_slot(table, "name")
def _(args: TableCellSlotProps):
    # This function is invoked when the cell is being rendered
    index = args.row_index
    ui.select(
        name_options,
        value=rows[index]["name"],
        on_change=lambda e: rename(e, index),
    )


ui.run()
