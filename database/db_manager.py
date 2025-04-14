import sqlite3
from models.componente import Componente


class DBManager:
    def __init__(self, db_path='data/inventario.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_table()
        
    def close(self):
        # Another component might have closen the connection already
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS componentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT,
            valor TEXT,
            encapsulado TEXT,
            cantidad INTEGER DEFAULT 0,
            ubicacion TEXT,
            fabricante TEXT,
            codigo_fabricante TEXT,
            descripcion TEXT,
            notas TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def obtener_componentes(self) -> list[Componente]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM componentes")
        rows = cursor.fetchall()
        return [Componente(*row) for row in rows]

    def agregar_componente(self, componente: Componente):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO componentes (nombre, tipo, valor, encapsulado, cantidad, ubicacion, fabricante, codigo_fabricante, descripcion, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            componente.nombre,
            componente.tipo,
            componente.valor,
            componente.encapsulado,
            componente.cantidad,
            componente.ubicacion,
            componente.fabricante,
            componente.codigo_fabricante,
            componente.descripcion,
            componente.notas
        ))
        self.conn.commit()

    def actualizar_componente(self, componente: Componente):
        query = """
        UPDATE componentes
        SET nombre = ?, tipo = ?, valor = ?, encapsulado = ?, cantidad = ?,
            ubicacion = ?, fabricante = ?, codigo_fabricante = ?, descripcion = ?, notas = ?
        WHERE id = ?
        """
        self.conn.execute(query, (
            componente.nombre, componente.tipo, componente.valor,
            componente.encapsulado, componente.cantidad, componente.ubicacion,
            componente.fabricante, componente.codigo_fabricante,
            componente.descripcion, componente.notas, componente.id
        ))
        self.conn.commit()
