from openpyxl import Workbook
from typing import List
from models.componente import Componente


def export_components_to_excel(componentes: List[Componente], file_path: str) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Components"

    # Write header
    headers = [
        "ID", "Name", "Type", "Value", "Package", "Quantity",
        "Location", "Manufacturer", "Manufacturer Code", "Description", "Notes"
    ]
    sheet.append(headers)

    # Write component data
    for c in componentes:
        row = [
            c.id, c.nombre, c.tipo, c.valor, c.encapsulado, c.cantidad,
            c.ubicacion, c.fabricante, c.codigo_fabricante, c.descripcion, c.notas
        ]
        sheet.append(row)

    # Auto-width adjustment (optional)
    for column_cells in sheet.columns:
        length = max(len(str(cell.value))
                     if cell.value is not None else 0 for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = length + 2

    workbook.save(file_path)
