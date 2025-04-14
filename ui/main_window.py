from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt
from database.db_manager import DBManager
from models.componente import Componente
from ui.add_component_dialog import AddComponentDialog



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventario Electrónico")
        self.resize(1000, 600)

        self.db = DBManager()
        self.layout = QVBoxLayout()
        
        # Avoiding lazy initialization of componentes variables
        self.componentes = []

        self.boton_recargar = QPushButton("Recargar inventario")
        self.boton_recargar.clicked.connect(self.cargar_componentes)
        
        self.boton_agregar = QPushButton("Añadir componente")
        self.boton_agregar.clicked.connect(self.abrir_formulario)
        
        self.tabla = QTableWidget()
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked | QTableWidget.EditTrigger.SelectedClicked)


        self.layout.addWidget(self.boton_recargar)
        self.layout.addWidget(self.tabla)
        self.layout.addWidget(self.boton_agregar)

        self.setLayout(self.layout)
        self.cargar_componentes()

        # We are adding connections here
        self.tabla.cellChanged.connect(self.actualizar_celda)

    def abrir_formulario(self):
        dialogo = AddComponentDialog()
        if dialogo.exec():
            nuevo_componente = dialogo.obtener_componente()
            if nuevo_componente.nombre:
                self.db.agregar_componente(nuevo_componente)
                self.cargar_componentes()
            else:
                QMessageBox.warning(self, "Faltan datos",
                                    "El campo 'Nombre' es obligatorio.")

    def actualizar_celda(self, fila: int, columna: int):
        if fila >= len(self.componentes):
            return

        componente = self.componentes[fila]
        nuevo_valor = self.tabla.item(fila, columna).text()

        campos = [
            "id", "nombre", "tipo", "valor", "encapsulado", "cantidad",
            "ubicacion", "fabricante", "codigo_fabricante", "descripcion", "notas"
        ]

        campo_modificado = campos[columna]

        # Validación opcional para cantidad
        if campo_modificado == "cantidad":
            try:
                nuevo_valor = int(nuevo_valor)
            except ValueError:
                QMessageBox.warning(
                    self, "Error", "La cantidad debe ser un número entero.")
                self.cargar_componentes()
                return

        # Actualizar el valor en el objeto
        setattr(componente, campo_modificado, nuevo_valor)

        # Actualizar en base de datos
        self.db.actualizar_componente(componente)

    def cargar_componentes(self):
        componentes = self.db.obtener_componentes()
        self.tabla.setRowCount(len(componentes))
        self.tabla.setColumnCount(10)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Tipo", "Valor", "Encapsulado",
            "Cantidad", "Ubicación", "Fabricante", "Código Fab.", "Descripción", "Notas"
        ])

        # Customization of columns
        

        for i, c in enumerate(componentes):
            item_id = QTableWidgetItem(str(c.id))
            item_id.setFlags(item_id.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tabla.setItem(i, 0, item_id)
            self.tabla.setItem(i, 1, QTableWidgetItem(c.nombre))
            self.tabla.setItem(i, 2, QTableWidgetItem(c.tipo))
            self.tabla.setItem(i, 3, QTableWidgetItem(c.valor))
            self.tabla.setItem(i, 4, QTableWidgetItem(c.encapsulado))
            self.tabla.setItem(i, 5, QTableWidgetItem(str(c.cantidad)))
            self.tabla.setItem(i, 6, QTableWidgetItem(c.ubicacion))
            self.tabla.setItem(i, 7, QTableWidgetItem(c.fabricante))
            self.tabla.setItem(i, 8, QTableWidgetItem(c.codigo_fabricante))
            self.tabla.setItem(i, 8, QTableWidgetItem(c.descripcion))
            self.tabla.setItem(i, 9, QTableWidgetItem(c.notas))
