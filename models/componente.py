from dataclasses import dataclass

@dataclass
class Componente:
    id: int = None
    nombre: str = ""
    tipo: str = ""
    valor: str = ""
    encapsulado: str = ""
    cantidad: int = 0
    ubicacion: str = ""
    fabricante: str = ""
    codigo_fabricante: str = ""
    descripcion: str = ""
    notas: str = ""
