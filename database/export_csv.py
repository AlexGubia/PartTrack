import csv
from typing import List
from models.componente import Componente


def export_components_to_csv(componentes: List[Componente], file_path: str) -> None:
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow([
            "ID", "Name", "Type", "Value", "Package", "Quantity",
            "Location", "Manufacturer", "Manufacturer Code", "Description", "Notes"
        ])

        # Write component data
        for c in componentes:
            writer.writerow([
                c.id, c.nombre, c.tipo, c.valor, c.encapsulado, c.cantidad,
                c.ubicacion, c.fabricante, c.codigo_fabricante, c.descripcion, c.notas
            ])
