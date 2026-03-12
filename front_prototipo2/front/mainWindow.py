import sys
import os
import resources_rc
from PySide6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QLabel, 
    QPushButton, 
    QFrame,
    QScrollArea, 
    QLineEdit,

)
from PySide6.QtCore import Qt,QSize
from PySide6.QtGui import QFont, QIcon, QColor, QPixmap, QPainter
from PySide6.QtWidgets import QGraphicsDropShadowEffect



class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("MeuEstoque")
        self.resize(1000, 600)

        # Lista que guarda os itens cadastrados
        self.itens = []

        self.setObjectName("mainWindow")
        self.setStyleSheet("""
            #mainWindow {
                background-color: #E0E3E8;
            }

            QScrollArea {
                border: none;
                background: transparent;
            }

            QScrollArea > QWidget > QWidget {
                background-color: rgba(255,255,255,0.75);
                border-radius: 14px;
                border: 1px solid rgba(0,0,0,0.05);
            }
                           QScrollBar:vertical {
                background: transparent;
                width: 10px;
                margin: 4px 0 4px 0;
            }

            QScrollBar::handle:vertical {
                background: rgba(0, 0, 0, 0.25);
                border-radius: 5px;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background: rgba(0, 0, 0, 0.40);
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)

        mainLayout = QHBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0) 
        mainLayout.setSpacing(0)  

        # ===============================
        # MENU LATERAL
        # ===============================
        sideMenu = QFrame()
        sideMenu.setFixedWidth(200)
        sideMenu.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0,
                    x2:0, y2:1,
                    stop:0 #1E3A8A,
                    stop:1 #1BB5D1
                );
            }
            QPushButton {
                background: transparent;
                color: white;
                border: none;
                padding: 10px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.2);
            }
            QPushButton:pressed {
                background-color: rgba(0,0,0,0.2);
    }
        """)

        sideLayout = QVBoxLayout(sideMenu)
        sideLayout.setContentsMargins(15, 0, 15, 0)
        sideLayout.setSpacing(15)


        btnEntrada = QPushButton(" Entrada Produto")
        btnEntrada.setIcon(self.criarIconeBranco(":/icons/entrada.png"))

        btnAdicionar = QPushButton(" Adição")
        btnAdicionar.setIcon(self.criarIconeBranco(":/icons/adicao.png"))

        btnSaida = QPushButton(" Saída Produto")
        btnSaida.setIcon(self.criarIconeBranco(":/icons/saida.png"))

        btnRetirada = QPushButton(" Retirada")
        btnRetirada.setIcon(self.criarIconeBranco(":/icons/retirada.png"))

        btnListagem = QPushButton(" Listagem")
        btnListagem.setIcon(self.criarIconeBranco(":/icons/listagem.png"))

        btnInicio = QPushButton("Início")
        btnInicio.setIcon(self.criarIconeBranco(":/icons/inicio.png"))
        btnInicio.clicked.connect(self.voltarPagina)

        btnEntrada.setIconSize(QSize(18, 18))
        btnAdicionar.setIconSize(QSize(18, 18))
        btnSaida.setIconSize(QSize(18, 18))
        btnRetirada.setIconSize(QSize(18, 18))
        btnListagem.setIconSize(QSize(18, 18))
        btnInicio.setIconSize(QSize(18, 18))
        btnInicio.clicked.connect(self.voltarPagina)

        # -------- TAMANHO DOS ÍCONES --------

        for btn in [
            btnEntrada,
            btnAdicionar,
            btnSaida,
            btnRetirada,
            btnListagem,
            btnInicio
        ]:
            btn.setIconSize(QSize(18, 18))

        # -------- CENTRALIZAR MENU --------

        sideLayout.addStretch()

        sideLayout.addWidget(btnEntrada)
        sideLayout.addWidget(btnAdicionar)
        sideLayout.addWidget(btnSaida)
        sideLayout.addWidget(btnRetirada)
        sideLayout.addWidget(btnListagem)

        sideLayout.addStretch()

        sideLayout.addWidget(btnInicio)

        mainLayout.addWidget(sideMenu)

        # ===============================
        # AREA CENTRAL
        # ===============================
        centralWidget = QWidget()
        centralLayout = QVBoxLayout(centralWidget)
        centralLayout.setContentsMargins(20, 20, 20, 20)

        titulo = QLabel("MeuEstoque")
        titulo.setAlignment(Qt.AlignCenter)

        fonte = QFont("Arial", 40, QFont.Bold)
        fonte.setItalic(True)

        titulo.setFont(fonte)
        titulo.setStyleSheet("color: #0A2A66;")


        # Área scrollável para os blocos

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)

        self.container = QWidget()
        self.containerLayout = QVBoxLayout(self.container)
        self.containerLayout.setContentsMargins(20, 20, 20, 20)

        self.scroll.setWidget(self.container)
        # ===============================
        # Sombra no container scroll
        # ===============================
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.scroll.setGraphicsEffect(shadow)

        centralLayout.addWidget(self.scroll)


        self.scroll.setStyleSheet("""
            QScrollArea {
                background-color: rgba(255, 255, 255, 0.6); 
                border-radius: 14px;
                border: 1px solid rgba(0, 0, 0, 0.05);
                
            }
        """)

        mainLayout.addWidget(centralWidget)

        # Exemplo: botão adicionar cria item
        btnAdicionar.clicked.connect(self.adicionarItem)

    # ===================================
    # FUNÇÃO PARA ADICIONAR ITEM
    # ===================================
    def adicionarItem(self):

        # Exemplo de item fictício
        item = {
            "codigo": "001",
            "quantidade": "10",
            "custo": "50.00"
        }

        self.itens.append(item)
        self.atualizarTela()

    # ===================================
    # Voltar aba função
    # ===================================
    def voltarPagina(self):
        self.window().voltarLogin()
    # ===================================
    # ATUALIZA TELA
    # ===================================
    def atualizarTela(self):

        # Limpa layout antes de recriar
        for i in reversed(range(self.containerLayout.count())):
            widget = self.containerLayout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Só cria blocos se existir item
        if len(self.itens) == 0:
            return

        for item in self.itens:

            card = QFrame()
            card.setStyleSheet("""
            QFrame {
                background-color: #F8F9FB;
                border-radius: 14px;
                padding: 18px;
                border: 1px solid rgba(0,0,0,0.05);
            }
            """)

            cardLayout = QVBoxLayout(card)

            topLayout = QHBoxLayout()
            topLayout.setContentsMargins(0, 0, 0, 0)
            topLayout.setSpacing(0)

            # Bolinha preta (ícone)
            bolinha = QLabel()
            pixmap = QPixmap(":/icons/circulo.png")
            pixmap = pixmap.scaled(8, 8, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            bolinha.setPixmap(pixmap)

            bolinha.setContentsMargins(0,0,0,0)

            topLayout.addWidget(bolinha, alignment=Qt.AlignTop | Qt.AlignLeft)
            topLayout.addStretch()

            cardLayout.addLayout(topLayout)
            
            info = QLabel(
                f"Código: {item['codigo']}    "
                f"Quantidade: {item['quantidade']}    "
                f"Custo: {item['custo']}"
            )

            botoesLayout = QHBoxLayout()

            btnAdd = QPushButton("Adição")
            btnAdd.setStyleSheet("""
            QPushButton{
                background-color: #22C55E;
                color: white;
                border-radius: 8px;
                padding: 6px;
                font-weight: bold;
            }
            QPushButton:hover{
                background-color: #16A34A;
            }
            """)

            btnRet = QPushButton("Retirada")
            btnRet.setStyleSheet("""
            QPushButton{
                background-color: #F59E0B;
                color: white;
                border-radius: 8px;
                padding: 6px;
                font-weight: bold;
            }
            QPushButton:hover{
                background-color: #D97706;
            }
            """)
            btnSai = QPushButton("Saída")
            btnSai.setStyleSheet("""
            QPushButton{
                background-color: #EF4444;
                color: white;
                border-radius: 8px;
                padding: 6px;
                font-weight: bold;
            }
            QPushButton:hover{
                background-color: #DC2626;
            }
            """)

            botoesLayout.addWidget(btnAdd)
            botoesLayout.addWidget(btnRet)
            botoesLayout.addWidget(btnSai)

            cardLayout.addWidget(info)
            cardLayout.addLayout(botoesLayout)

            self.containerLayout.addWidget(card)

        self.containerLayout.addStretch()

    def criarIconeBranco(self, caminho):
        pixmap = QPixmap(caminho)

        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), Qt.white)
        painter.end()

        return QIcon(pixmap)