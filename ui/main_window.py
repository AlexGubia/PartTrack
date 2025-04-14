from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFileDialog)
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from database.db_manager import DBManager
from database.export_csv import export_components_to_csv
from models.componente import Componente
from ui.add_component_dialog import AddComponentDialog
from ui.diff_dialog import ConfirmacionCambioDialog


class MainWindow(QMainWindow):
    def __init__(self, db: DBManager):
        super().__init__()
        self.setWindowTitle("Inventario Electrónico")
        self.resize(1000, 600)

        self.db = db

        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu("File")

        action_export_csv = QAction("Export CSV", self)
        action_export_csv.triggered.connect(self.export_to_csv)
        file_menu.addAction(action_export_csv)

        central_widget = QWidget()
        self.layout = QVBoxLayout(central_widget)

        # Avoiding lazy initialization of componentes variables
        self.componentes = []
        self.valor_anterior = ""

        self.boton_recargar = QPushButton("Recargar inventario")
        self.boton_recargar.clicked.connect(self.cargar_componentes)

        self.boton_agregar = QPushButton("Añadir componente")
        self.boton_agregar.clicked.connect(self.abrir_formulario)

        self.tabla = QTableWidget()
        self.tabla.setEditTriggers(
            QTableWidget.EditTrigger.DoubleClicked | QTableWidget.EditTrigger.SelectedClicked)

        self.layout.addWidget(self.boton_recargar)
        self.layout.addWidget(self.tabla)
        self.layout.addWidget(self.boton_agregar)

        # self.setLayout(self.layout)
        self.cargar_componentes()

        # We are adding connections here
        self.tabla.cellChanged.connect(self.actualizar_celda)
        self.tabla.cellClicked.connect(self.guardar_valor_original)

        self.setCentralWidget(central_widget)

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

    def guardar_valor_original(self, fila: int, columna: int):
        item = self.tabla.item(fila, columna)
        if item:
            self.valor_anterior = item.text()
            self.coordinates = (fila, columna)
        else:
            self.valor_anterior = None
            self.coordinates = None

    def actualizar_celda(self, fila: int, columna: int):
        # Is this the correct condition?
        if fila > len(self.componentes):
            return

        # Is this the same cell that was clicked?
        if self.coordinates != (fila, columna):
            return

        componente = self.componentes[fila]
        nuevo_valor = self.tabla.item(fila, columna).text()

        if nuevo_valor == self.valor_anterior:
            return  # Nada cambió

        # Mostrar confirmación visual con diferencias
        dialogo = ConfirmacionCambioDialog(self.valor_anterior, nuevo_valor)
        if dialogo.exec() != QDialog.DialogCode.Accepted:
            self.cargar_componentes()
            return

        campos = [
            "id", "nombre", "tipo", "valor", "encapsulado", "cantidad",
            "ubicacion", "fabricante", "codigo_fabricante", "descripcion", "notas"
        ]
        campo_modificado = campos[columna]

        if campo_modificado == "cantidad":
            try:
                nuevo_valor = int(nuevo_valor)
            except ValueError:
                QMessageBox.warning(
                    self, "Error", "La cantidad debe ser un número entero.")
                self.cargar_componentes()
                return

        setattr(componente, campo_modificado, nuevo_valor)
        self.db.actualizar_componente(componente)

    def cargar_componentes(self):
        self.coordinates = None
        self.valor_anterior = None
        self.componentes = self.db.obtener_componentes()
        self.tabla.setRowCount(len(self.componentes))
        self.tabla.setColumnCount(11)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Tipo", "Valor", "Encapsulado",
            "Cantidad", "Ubicación", "Fabricante", "Código Fab.", "Descripción", "Notas"
        ])

        for i, c in enumerate(self.componentes):
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
            self.tabla.setItem(i, 9, QTableWidgetItem(c.descripcion))
            self.tabla.setItem(i, 10, QTableWidgetItem(c.notas))

    def closeEvent(self, event):
        if hasattr(self, "db") and self.db:
            self.db.close()
        event.accept()

    def export_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Components to CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                export_components_to_csv(self.componentes, file_path)
                QMessageBox.information(
                    self, "Export Successful", f"Components exported to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed",
                                     f"An error occurred:\n{str(e)}")
