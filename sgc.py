from random import randint
from subprocess import getoutput
from time import time, sleep
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from sys import argv


def initwindow():
    def iniciar():
        load = 0
        while load < 100:
            janela.showMessage(f"Carregando Modulos: {load}%", align, Qt.GlobalColor.white)
            sleep(0.5)
            load += randint(2, 10)
        janela.close()
        app.janelaprincipal.show()

    img = QPixmap("favicon/init.png")
    align = int(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignAbsolute)
    janela = QSplashScreen(img)
    janela.setStyleSheet(tema)
    janela.show()
    iniciar()


class SGC:
    def __init__(self):
        self.gc = QApplication(argv)

        QFontDatabase.addApplicationFont("font/copse.ttf")
        self.janelaprincipal = QMainWindow()
        self.janelaprincipal.setFixedSize(QSize(700, 550))
        self.janelaprincipal.setWindowTitle("seticongc")
        self.janelaprincipal.setWindowIcon(QIcon("favicon/seticongc-256x256.ico"))
        self.janelaprincipal.setStyleSheet(tema)
        self.ferramenta = QWidget()
        
        bg_image = QImage(f"favicon/bg.jpg")
        set_bg_image = bg_image.scaled(QSize(700, 550))  # resize Image to widget's size
        palette = QPalette()
        palette.setBrush(palette.ColorGroup.All, palette.ColorRole.Window, QBrush(set_bg_image))
        self.janelaprincipal.setPalette(palette)

        menu = QMenuBar()
        detalhes = menu.addMenu("Details")
        instr = detalhes.addAction("Instructions")
        instr.triggered.connect(self._instr)
        detalhes.addSeparator()
        _sair = lambda: self.gc.exit(0)
        sair = detalhes.addAction("Quit")
        sair.triggered.connect(_sair)
        sobre = menu.addAction("About")
        sobre.triggered.connect(self._sobre)
        self.janelaprincipal.setMenuBar(menu)

        self.mainwindow()
        self.janelaprincipal.setCentralWidget(self.ferramenta)

    def _sobre(self):
        QMessageBox.information(self.janelaprincipal, "About",
                                "<b>Info about the program</b><hr>"
                                "<p><ul><li><b>Name:</b> seticonGC</li>"
                                "<li><b>Version:</b> 0.1-122022</li>"
                                "<li><b>Maintener:</b> &copy;Nurul-GC</li>"
                                "<li><b>Publisher:</b> &trade;ArtesGC, Inc.</li></ul></p>")

    def _instr(self):
        QMessageBox.information(self.janelaprincipal, "Instructions",
                                "<b>Brief Presentation</b><hr>"
                                "<p>seticonGC is a simple way to compile C/C++ scripts with an icon"
                                "it was built with `PyQt6 + QSS + GNU GCC` frameworks allowing the user"
                                "to easily compile their C/C++ programs with three simple steps:</p>"
                                "<p>1. Search and get the location of the C/C++ script;<br>"
                                "2. Search and get the location of the costumized icon;<br>"
                                "3. Then just hit the compile button and save where to save the program;</p>"
                                "<p>The program creates an (.rc) file with the details of the icon then compile both "
                                "the script and the icon resource into one executable.</p>"
                                "<p>Thanks for your support!<br>"
                                "<b>&trade;ArtesGC, Inc.</b></p>")

    def mainwindow(self):
        def getscipt():
            filename = QFileDialog.getOpenFileName(
                self.janelaprincipal,
                caption="Choose the Cxx script",
                filter="Cxx Files (*.c *.cpp)"
            )[0]
            getcscript.setText(filename)

        def geticon():
            filename = QFileDialog.getOpenFileName(
                self.janelaprincipal,
                caption="Choose the icon file",
                filter="Icon Files (*.ico)"
            )[0]
            getcicon.setText(filename)
        
        def compilar():
            dirname = QFileDialog.getExistingDirectory(self.janelaprincipal)
            inicio = time()
            try:
                with open(f"{dirname}/icon.rc", "w+") as resource:
                    resource.write(f'MAINICON ICON "{getcicon.text()}"')
                windresslog = getoutput(f".\\src\\bin\\windres {dirname}\\icon.rc {dirname}\\icon.o")
                gcclog = getoutput(f".\\src\\bin\\gcc {dirname}\\icon.o {getcscript.text()} -o {dirname}\\setup.exe")
                log.setText(f"{windresslog}\n\n{gcclog}")
            except Exception as erro:
                QMessageBox.warning(
                    self.janelaprincipal,
                    "Erro",
                    f"Lamento, durante a execução do program ocorreu o seguinte erro:\n- {erro}"
                )
                log.setText(f"\n{'x'*30}\n- {erro}")
            finally:
                QMessageBox.information(
                    self.janelaprincipal,
                    "Operação Concluida",
                    f"A compilação do seu programa terminou apôs {int(time() - inicio)}s!"
                )
                log.setText(f"\n{'+'*30}\n- Compilação concluida apôs {int(time() - inicio)}s!")

        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        infolabel = QLabel("<p>Seja Bem-Vindo ao utilitario<h2>seticonGC</h2></p><hr>"
                           "<p>O metodo mais simples de compilar o seu programa em Cxx<br>"
                           "ja com um icone personalizado</p>")
        infolabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(infolabel)

        layoutscript = QHBoxLayout()
        getcscript = QLineEdit()
        getcscript.setReadOnly(True)
        getcscript.setPlaceholderText("Pesquise pelo script do programa em Cxx..")
        layoutscript.addWidget(getcscript)
        getcscriptbtn = QPushButton("Pesquisar Script")
        getcscriptbtn.clicked.connect(getscipt)
        layoutscript.addWidget(getcscriptbtn)
        layout.addLayout(layoutscript)

        layouticon = QHBoxLayout()
        getcicon = QLineEdit()
        getcicon.setReadOnly(True)
        getcicon.setPlaceholderText("Pesquise pelo icone para o programa..")
        layouticon.addWidget(getcicon)
        getciconbtn = QPushButton("Pesquisar Icone")
        getciconbtn.clicked.connect(geticon)
        layouticon.addWidget(getciconbtn)
        layout.addLayout(layouticon)

        compilarbtn = QPushButton("Compilar Programa")
        compilarbtn.clicked.connect(compilar)
        layout.addWidget(compilarbtn)

        log = QTextEdit()
        log.setReadOnly(True)
        log.setPlaceholderText("As informações sobre a execução do programa serão apresentadas aqui..")
        log.setStyleSheet("background-color:black; color:gray;")
        layout.addWidget(log)
        
        copylabel = QLabel("<a>&trade;ArtesGC, Inc.</a>")
        copylabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(copylabel)

        self.ferramenta.setLayout(layout)


if __name__ == "__main__":
    tema = open("theme/sgc.qss").read().strip()
    app = SGC()
    initwindow()
    app.gc.exec()
