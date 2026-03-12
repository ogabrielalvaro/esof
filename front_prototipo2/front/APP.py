import sys
from PySide6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout, 
    QStackedWidget
)

from main import LoginWindow
from mainWindow import MainWindow


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EstoqueAPP")
        self.resize(1000, 600)

        self.stack = QStackedWidget()

        # Criando páginas
        self.loginPage = LoginWindow(self)
        self.mainPage = MainWindow(self)

        # Adicionando ao stack
        self.stack.addWidget(self.loginPage)
        self.stack.addWidget(self.mainPage)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)

    # Navegação
    def irParaMain(self):
        self.stack.setCurrentWidget(self.mainPage)

    def voltarLogin(self):
        self.stack.setCurrentWidget(self.loginPage)



app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec())