from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QTextDocument
from PyQt6.QtCore import Qt
import difflib


class ConfirmacionCambioDialog(QDialog):
    def __init__(self, texto_anterior: str, texto_nuevo: str):
        super().__init__()
        self.setWindowTitle("Confirmar cambio")
        self.setModal(True)
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        label = QLabel("¿Quieres guardar este cambio?")
        layout.addWidget(label)

        html_diff = self.generar_html_diff(texto_anterior, texto_nuevo)
        diff_label = QLabel()
        diff_label.setTextFormat(Qt.TextFormat.RichText)
        diff_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse)
        diff_label.setWordWrap(True)
        diff_label.setText(html_diff)
        layout.addWidget(diff_label)

        botones = QHBoxLayout()
        aceptar = QPushButton("Aceptar")
        cancelar = QPushButton("Cancelar")

        aceptar.clicked.connect(self.accept)
        cancelar.clicked.connect(self.reject)

        botones.addWidget(aceptar)
        botones.addWidget(cancelar)
        layout.addLayout(botones)

        self.setLayout(layout)

    def generar_html_diff(self, texto_antiguo: str, texto_nuevo: str) -> str:
        d = difflib.Differ()
        resultado = list(d.compare(texto_antiguo, texto_nuevo))
        html = ""
        for linea in resultado:
            if linea.startswith("  "):
                html += linea[2:]
            elif linea.startswith("- "):
                html += f'<span style="background-color:#fbb;">{linea[2:]}</span>'
            elif linea.startswith("+ "):
                html += f'<span style="background-color:#bfb;">{linea[2:]}</span>'
        return html
