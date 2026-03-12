import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QBoxLayout,
    QVBoxLayout, 
    QLabel,
    QLineEdit, 
    QPushButton, 
    QFrame,
    QGraphicsDropShadowEffect,
    QStackedWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor


class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowTitle("EstoqueAPP")
        # self.showMaximized() # Tela cheia
        self.resize(1000, 600)  # Tela menor para editar
        
        self.setObjectName("loginWindow")
        self.setStyleSheet("""
            #loginWindow {
                background: qlineargradient(
                    spread:pad,
                    x1:0, y1:0,
                    x2:0, y2:1,
                    stop:0 #1E3A8A,
                    stop:0.5 #1E3A8A,
                    stop:1 #1BB5D1
                );
            }

            QLineEdit {
                background-color: #F5F5F5;
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                padding: 6px;
            }

            QLineEdit:focus {
                border: 2px solid #1E3A8A;
                background-color: #FFFFFF;
            }
        """)
        #===========================
        # Titulo grande no meio
        #===========================
        titleLabel = QLabel("MeuEstoque")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        titleFont = QFont("Arial", 75, QFont.Bold, italic=True)
        titleLabel.setFont(titleFont)
        
        #===========================
        # Card branco
        #===========================
        cardFrame = QFrame()
        cardFrame.setFixedWidth(400)
        cardFrame.setStyleSheet("""
            QFrame {
                background-color: #EDEDED;
                border-radius: 10px     
            } 
        """)

        cardLayout = QVBoxLayout(cardFrame)
        cardLayout.setContentsMargins(30, 30, 30, 30)
        cardLayout.setSpacing(15)

        mainLayout = QVBoxLayout(self)

        #===========================
        # Container central
        #===========================
        centerContainer = QWidget()
        centerContainer.setStyleSheet("background: transparent;")
        centerLayout = QVBoxLayout(centerContainer)
        centerLayout.addStretch()
        centerLayout.addWidget(titleLabel, alignment=Qt.AlignCenter)
        centerLayout.addSpacing(40)
        centerLayout.addWidget(cardFrame, alignment=Qt.AlignCenter)
        centerLayout.addStretch()

        # Centraliza o container na tela
        mainLayout.addWidget(centerContainer)

        #===========================
        # Usuário
        #===========================
        userLabel = QLabel("Usuário")
        userInput = QLineEdit()
        userInput.setPlaceholderText("Digite seu usuário")

        # Senha
        passLabel = QLabel("Senha")
        passInput = QLineEdit()
        passInput.setPlaceholderText("Digite sua senha")
        passInput.setEchoMode(QLineEdit.Password)

        # Botão
        loginButton = QPushButton("Entrar")
        loginButton.setFixedHeight(40)
        loginButton.setStyleSheet("""
            QPushButton {
                background-color: #0A2A66;
                color: white;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #133A85;
            }
            QPushButton:pressed {
                background-color: #08214F;
                padding-top: 3px;   
                padding-left: 1px;
            }
        """)

        # Botão entrar como funcionário
        employeeButton = QPushButton("Entrar como funcionário")
        employeeButton.setFixedHeight(40)
        employeeButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #0A2A66;
                border: 2px solid #0A2A66;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0A2A66;
                color: white;
            }
            QPushButton:pressed {
                background-color: #08214F;
                border: 2px solid #08214F;
                color: white;
                padding-top: 3px;   
                padding-left: 1px;
            }
        """)
        employeeButton.clicked.connect(self.abrirMainWindow) #Click em entrar como funcionario
        
        # Sombra no botão
        loginShadow = QGraphicsDropShadowEffect()
        loginShadow.setBlurRadius(15)
        loginShadow.setOffset(0, 5)
        loginShadow.setColor(QColor(0, 0, 0, 120))
        loginButton.setGraphicsEffect(loginShadow)

        # Sombra no botão funcionário
        employeeShadow = QGraphicsDropShadowEffect()
        employeeShadow.setBlurRadius(15)
        employeeShadow.setOffset(0, 5)
        employeeShadow.setColor(QColor(0, 0, 0, 120))
        employeeButton.setGraphicsEffect(employeeShadow)
        employeeButton.clicked.connect(self.abrirMainWindow)

        # Link
        forgotLabel = QLabel("<a href='#'>Esqueceu sua senha?</a>")
        forgotLabel.setTextFormat(Qt.RichText)
        forgotLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        forgotLabel.setAlignment(Qt.AlignLeft)

        # Adicionando ao card
        cardLayout.addWidget(userLabel)
        cardLayout.addWidget(userInput)
        cardLayout.addWidget(passLabel)
        cardLayout.addWidget(passInput)
        cardLayout.addSpacing(10)
        cardLayout.addWidget(loginButton)
        cardLayout.addSpacing(5)
        cardLayout.addWidget(employeeButton)
        cardLayout.addWidget(forgotLabel)

        # Exemplo de ação do botão
        loginButton.clicked.connect(lambda: print("Samuell lixo"))

    #Abrir proxima pagina com entrar como funcionario
    def abrirMainWindow(self):
        self.window().irParaMain()
    

