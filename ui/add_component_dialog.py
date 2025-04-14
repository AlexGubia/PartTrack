from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFormLayout, QMessageBox
)
from models.componente import Componente


class AddComponentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Añadir Componente")
        self.setMinimumWidth(400)

        self.form_layout = QFormLayout()

        self.inputs = {
            "nombre": QLineEdit(),
            "tipo": QLineEdit(),
            "valor": QLineEdit(),
            "encapsulado": QLineEdit(),
            "cantidad": QLineEdit(),
            "ubicacion": QLineEdit(),
            "fabricante": QLineEdit(),
            "codigo_fabricante": QLineEdit(),
            "descripcion": QLineEdit(),
            "notas": QLineEdit()
        }

        for label, widget in self.inputs.items():
            self.form_layout.addRow(label.capitalize(), widget)

        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addLayout(self.form_layout)
        layout.addWidget(self.boton_guardar)
        self.setLayout(layout)

    def obtener_componente(self) -> Componente:
        try:
            cantidad = int(self.inputs["cantidad"].text())
        except ValueError:
            cantidad = 0

        

        return Componente(
            nombre=self.inputs["nombre"].text(),
            tipo=self.inputs["tipo"].text(),
            valor=self.inputs["valor"].text(),
            encapsulado=self.inputs["encapsulado"].text(),
            cantidad=cantidad,
            ubicacion=self.inputs["ubicacion"].text(),
            fabricante=self.inputs["fabricante"].text(),
            codigo_fabricante=self.inputs["codigo_fabricante"].text(),
            descripcion=self.inputs["descripcion"].text(),
            notas=self.inputs["notas"].text()
        )
