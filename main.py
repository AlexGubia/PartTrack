import sys
import traceback
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from database.db_manager import DBManager


def main():
    app = QApplication(sys.argv)
    app.setStyle('windowsvista')

    db = DBManager(db_path='data/inventario.db')
    ventana = MainWindow(db)

    try:
        ventana.show()
        sys.exit(app.exec())
    except Exception as e:
        print("Error inesperado:", e)
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()
