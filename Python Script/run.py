'''
    File name: run.py
    Authors: Muhammad Shiraz Ahmad and Sabieh Anwar
    Date created: 6/22/2019
    Date last modified: 6/22/2019
    Python Version: 3.7.3
'''

from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QMessageBox, QFileDialog, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
import func
import AirTrack
import os
import webbrowser
import sys

ACC=[]
MASS_RATIO=[19,9.50,6.33,4.75,3.80]
class about_gui(QWidget):

    def __init__(self):
        super().__init__()
    #    self.title = ''
    #    self.left = 1
    #    self.top = 1
    #    self.width = 1
    #    self.height = 1
        self.setWindowIcon(QtGui.QIcon('ico.ico'))
        self.initUI()

    def initUI(self):
        message = "<p><strong>Linear Air Track Analyzer<br /></strong>Version: 1.0 (June 21 2019)</p><p><strong>Created by:</strong> <a href='mailto:shiraz.phy@gmail.com'>Muhammad Shiraz Ahmad</a> and <a href='mailto:sabieh@gmail.com'>Muhammad Sabieh Anwar</a></p><p><strong>Important Links: </strong><a href='https://www.physlab.org/experiment/experiments-with-a-linear-air-track/'>PhysLab.org</a>, <a href='https://www.qosain.pk/physics/lab-experiments/air-track-6-feet-with-photogates-and-physlogger-2'>Qosain.pk</a></p><p><strong>License:</strong> <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU General Public License v3.0</a></p><p>Copyright &copy; 2018, all rights reserved.</p>"
        buttonReply = QMessageBox.question(self, 'About', message,
                                           QMessageBox.Ok, QMessageBox.Ok)
        self.show()


class Ui_Form(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)


    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 400)

        self.main_Layout = QtWidgets.QVBoxLayout(Form)
        self.main_Layout.setObjectName("main_Layout")

        #Add b utton
        self.button = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.button.setFont(font)
        self.button.setObjectName("saveDefault")
        self.main_Layout.addWidget(self.button)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


class Plot_Window(QDialog):
    def __init__(self, parent=None):
        super(Plot_Window, self).__init__(parent)
        f_name = [line.rstrip() for line in open('filesavename')]
        # a figure instance to plot on
        self.figure = plt.figure()
        self.setWindowTitle("File loaded: " + f_name[0])
        self.setWindowIcon(QtGui.QIcon('ico.ico'))
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        #self.button = QPushButton('Plot')
        #self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        f_name = [line.rstrip() for line in open('filesavename')]
        data = np.loadtxt(f_name[0])
        acc = data[:,1]
        acc = 1 / acc
        y = acc

        acc_Unc = data[:,2]
        acc_Unc = acc_Unc * (acc ** 2)
        mass_rat = data[:,0]
        x = mass_rat

        yerr = acc_Unc

        plt.xlabel('m/M')
        plt.ylabel('1/a (s²/cm)')
        plt.title("Verification of Newton's second law")
        ax = self.figure.add_subplot(111)

        ax.grid(alpha=0.5, linestyle=':')
        slope, intercept, r_value, p_value, stderr = linregress(x, y)
        Equation = 'y = '+str(np.round(slope,7))+'x + '+str(np.round(intercept,7))

        line, caps, bars = plt.errorbar(
            x,  # X
            y,  # Y
            yerr=yerr,  # Y-errors
            fmt="ro--",  # format line like for plot()
            linewidth=2,  # width of plot line
            elinewidth=0.6,  # width of error bar line
            ecolor='k',  # color of error bar
            capsize=5,  # cap length for error bar
            capthick=1,  # cap thickness for error bar
            label='Error bar',
        )
        props = dict(facecolor='wheat', alpha=0.5)
        ax.text(0.05, 0.95, Equation, transform=ax.transAxes, fontsize=11,
                verticalalignment='top')

        # refresh canvas
        self.canvas.draw()


class save_file_prompt(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.saveFileDialog()
        self.show()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Output File", "",
                                                  "Text Files (*.txt)", options=options)
        if fileName:
            outF = open("filesavename", "w")
            outF.write(str(fileName))
            outF.close()




class pick_file_to_append(QWidget):


    def __init__(self):
        super().__init__()
        self.title = "Please Pick multiple Physlogger' exported files"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.openFileNamesDialog()
        self.show()

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontConfirmOverwrite
        files, _ = QFileDialog.getOpenFileNames(self, "Pick Variables File", "A",
                                                "Text Files (*.txt);;All Files (*)", options=options)
        if files:
            outF = open("filesavename", "w")
            for line in files:
                # write line to output file
                outF.write(line)
                outF.write("\n")
            outF.close()




class GUI_App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Please Pick multiple Physlogger' exported files"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon('ico.ico'))
        self.openFileNamesDialog()
        self.show()

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Pick  Multiple Files", "",
                                                "Text Files (*.txt)", options=options)
        if files:
            outF = open("lst_paths", "w")
            for line in files:
                # write line to output file
                outF.write(line)
                outF.write("\n")
            outF.close()


            outF = open("lst_names", "w")
            files_names_list = func.name_list(files)
            for line in files_names_list:
                # write line to output file
                outF.write(line)
                outF.write("\n")
            outF.close()


            lst_acc = AirTrack.acc(files)
            lst_acc_Unc = lst_acc[1]
            lst_acc = lst_acc[0]
            outF = open("lst_acc", "w")
            for line in lst_acc:
                outF.write(str(line))
                outF.write("\n")
            outF.close()
            outF = open("lst_acc_Unc", "w")
            for line in lst_acc_Unc:
                outF.write(str(line))
                outF.write("\n")
            outF.close()





class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(749, 574)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(749, 574))
        MainWindow.setMaximumSize(QtCore.QSize(749, 574))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_SrNo = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_SrNo.setGeometry(QtCore.QRect(57, 280, 41, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_SrNo.setFont(font)
        self.groupBox_SrNo.setObjectName("groupBox_SrNo")
        self.Sr_1 = QtWidgets.QLabel(self.groupBox_SrNo)
        self.Sr_1.setGeometry(QtCore.QRect(10, 30, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Sr_1.setFont(font)
        self.Sr_1.setObjectName("Sr_1")
        self.Sr_2 = QtWidgets.QLabel(self.groupBox_SrNo)
        self.Sr_2.setGeometry(QtCore.QRect(10, 50, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Sr_2.setFont(font)
        self.Sr_2.setObjectName("Sr_2")
        self.Sr_3 = QtWidgets.QLabel(self.groupBox_SrNo)
        self.Sr_3.setGeometry(QtCore.QRect(10, 70, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Sr_3.setFont(font)
        self.Sr_3.setObjectName("Sr_3")
        self.Sr_4 = QtWidgets.QLabel(self.groupBox_SrNo)
        self.Sr_4.setGeometry(QtCore.QRect(10, 90, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Sr_4.setFont(font)
        self.Sr_4.setObjectName("Sr_4")
        self.Sr_5 = QtWidgets.QLabel(self.groupBox_SrNo)
        self.Sr_5.setGeometry(QtCore.QRect(10, 110, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Sr_5.setFont(font)
        self.Sr_5.setObjectName("Sr_5")
        self.Sr_10 = QtWidgets.QLabel(self.groupBox_SrNo)
        self.Sr_10.setGeometry(QtCore.QRect(10, 210, 21, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Sr_10.setFont(font)
        self.Sr_10.setObjectName("Sr_10")
        self.Sr_7 = QtWidgets.QLabel(self.groupBox_SrNo)
        self.Sr_7.setGeometry(QtCore.QRect(10, 150, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Sr_7.setFont(font)
        self.Sr_7.setObjectName("Sr_7")
        self.Sr_6 = QtWidgets.QLabel(self.groupBox_SrNo)
        self.Sr_6.setGeometry(QtCore.QRect(10, 130, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Sr_6.setFont(font)
        self.Sr_6.setObjectName("Sr_6")
        self.Sr_9 = QtWidgets.QLabel(self.groupBox_SrNo)
        self.Sr_9.setGeometry(QtCore.QRect(10, 190, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Sr_9.setFont(font)
        self.Sr_9.setObjectName("Sr_9")
        self.Sr_8 = QtWidgets.QLabel(self.groupBox_SrNo)
        self.Sr_8.setGeometry(QtCore.QRect(10, 170, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Sr_8.setFont(font)
        self.Sr_8.setObjectName("Sr_8")
        self.groupBox_M = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_M.setGeometry(QtCore.QRect(360, 280, 71, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_M.setFont(font)
        self.groupBox_M.setObjectName("groupBox_M")
        self.M_1 = QtWidgets.QLineEdit(self.groupBox_M)
        self.M_1.setGeometry(QtCore.QRect(10, 30, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.M_1.setFont(font)
        self.M_1.setAutoFillBackground(False)
        self.M_1.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.M_1.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.M_1.setText("")
        self.M_1.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.M_1.setClearButtonEnabled(False)
        self.M_1.setObjectName("M_1")
        self.M_2 = QtWidgets.QLineEdit(self.groupBox_M)
        self.M_2.setGeometry(QtCore.QRect(10, 50, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.M_2.setFont(font)
        self.M_2.setAutoFillBackground(False)
        self.M_2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.M_2.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.M_2.setText("")
        self.M_2.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.M_2.setClearButtonEnabled(False)
        self.M_2.setObjectName("M_2")
        self.M_3 = QtWidgets.QLineEdit(self.groupBox_M)
        self.M_3.setGeometry(QtCore.QRect(10, 70, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.M_3.setFont(font)
        self.M_3.setAutoFillBackground(False)
        self.M_3.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.M_3.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.M_3.setText("")
        self.M_3.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.M_3.setClearButtonEnabled(False)
        self.M_3.setObjectName("M_3")
        self.M_4 = QtWidgets.QLineEdit(self.groupBox_M)
        self.M_4.setGeometry(QtCore.QRect(10, 90, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.M_4.setFont(font)
        self.M_4.setAutoFillBackground(False)
        self.M_4.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.M_4.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.M_4.setText("")
        self.M_4.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.M_4.setClearButtonEnabled(False)
        self.M_4.setObjectName("M_4")
        self.M_5 = QtWidgets.QLineEdit(self.groupBox_M)
        self.M_5.setGeometry(QtCore.QRect(10, 110, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.M_5.setFont(font)
        self.M_5.setAutoFillBackground(False)
        self.M_5.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.M_5.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.M_5.setText("")
        self.M_5.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.M_5.setClearButtonEnabled(False)
        self.M_5.setObjectName("M_5")
        self.M_6 = QtWidgets.QLineEdit(self.groupBox_M)
        self.M_6.setGeometry(QtCore.QRect(10, 130, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.M_6.setFont(font)
        self.M_6.setAutoFillBackground(False)
        self.M_6.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.M_6.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.M_6.setText("")
        self.M_6.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.M_6.setClearButtonEnabled(False)
        self.M_6.setObjectName("M_6")
        self.M_7 = QtWidgets.QLineEdit(self.groupBox_M)
        self.M_7.setGeometry(QtCore.QRect(10, 150, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.M_7.setFont(font)
        self.M_7.setAutoFillBackground(False)
        self.M_7.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.M_7.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.M_7.setText("")
        self.M_7.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.M_7.setClearButtonEnabled(False)
        self.M_7.setObjectName("M_7")
        self.M_8 = QtWidgets.QLineEdit(self.groupBox_M)
        self.M_8.setGeometry(QtCore.QRect(10, 170, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.M_8.setFont(font)
        self.M_8.setAutoFillBackground(False)
        self.M_8.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.M_8.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.M_8.setText("")
        self.M_8.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.M_8.setClearButtonEnabled(False)
        self.M_8.setObjectName("M_8")
        self.M_9 = QtWidgets.QLineEdit(self.groupBox_M)
        self.M_9.setGeometry(QtCore.QRect(10, 190, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.M_9.setFont(font)
        self.M_9.setAutoFillBackground(False)
        self.M_9.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.M_9.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.M_9.setText("")
        self.M_9.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.M_9.setClearButtonEnabled(False)
        self.M_9.setObjectName("M_9")
        self.M_10 = QtWidgets.QLineEdit(self.groupBox_M)
        self.M_10.setGeometry(QtCore.QRect(10, 210, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.M_10.setFont(font)
        self.M_10.setAutoFillBackground(False)
        self.M_10.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.M_10.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.M_10.setText("")
        self.M_10.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.M_10.setClearButtonEnabled(False)
        self.M_10.setObjectName("M_10")
        self.groupBox_Files_Load = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Files_Load.setGeometry(QtCore.QRect(120, 280, 111, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_Files_Load.setFont(font)
        self.groupBox_Files_Load.setObjectName("groupBox_Files_Load")
        self.Fl_1 = QtWidgets.QLabel(self.groupBox_Files_Load)
        self.Fl_1.setGeometry(QtCore.QRect(10, 30, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Fl_1.setFont(font)
        self.Fl_1.setObjectName("Fl_1")
        self.Fl_2 = QtWidgets.QLabel(self.groupBox_Files_Load)
        self.Fl_2.setGeometry(QtCore.QRect(10, 50, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Fl_2.setFont(font)
        self.Fl_2.setObjectName("Fl_2")
        self.Fl_3 = QtWidgets.QLabel(self.groupBox_Files_Load)
        self.Fl_3.setGeometry(QtCore.QRect(10, 70, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Fl_3.setFont(font)
        self.Fl_3.setObjectName("Fl_3")
        self.Fl_4 = QtWidgets.QLabel(self.groupBox_Files_Load)
        self.Fl_4.setGeometry(QtCore.QRect(10, 90, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Fl_4.setFont(font)
        self.Fl_4.setObjectName("Fl_4")
        self.Fl_5 = QtWidgets.QLabel(self.groupBox_Files_Load)
        self.Fl_5.setGeometry(QtCore.QRect(10, 110, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Fl_5.setFont(font)
        self.Fl_5.setObjectName("Fl_5")
        self.Fl_6 = QtWidgets.QLabel(self.groupBox_Files_Load)
        self.Fl_6.setGeometry(QtCore.QRect(10, 130, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Fl_6.setFont(font)
        self.Fl_6.setObjectName("Fl_6")
        self.Fl_7 = QtWidgets.QLabel(self.groupBox_Files_Load)
        self.Fl_7.setGeometry(QtCore.QRect(10, 150, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Fl_7.setFont(font)
        self.Fl_7.setObjectName("Fl_7")
        self.Fl_8 = QtWidgets.QLabel(self.groupBox_Files_Load)
        self.Fl_8.setGeometry(QtCore.QRect(10, 170, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Fl_8.setFont(font)
        self.Fl_8.setObjectName("Fl_8")
        self.Fl_9 = QtWidgets.QLabel(self.groupBox_Files_Load)
        self.Fl_9.setGeometry(QtCore.QRect(10, 190, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Fl_9.setFont(font)
        self.Fl_9.setObjectName("Fl_9")
        self.Fl_10 = QtWidgets.QLabel(self.groupBox_Files_Load)
        self.Fl_10.setGeometry(QtCore.QRect(10, 210, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Fl_10.setFont(font)
        self.Fl_10.setObjectName("Fl_10")
        self.pushButton_PickFile = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_PickFile.setGeometry(QtCore.QRect(120, 160, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_PickFile.setFont(font)
        self.pushButton_PickFile.setCheckable(False)
        self.pushButton_PickFile.setObjectName("pushButton_PickFile")
        self.groupBox_M_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_M_5.setGeometry(QtCore.QRect(460, 280, 81, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_M_5.setFont(font)
        self.groupBox_M_5.setObjectName("groupBox_M_5")
        self.mM_1 = QtWidgets.QLabel(self.groupBox_M_5)
        self.mM_1.setGeometry(QtCore.QRect(10, 30, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.mM_1.setFont(font)
        self.mM_1.setObjectName("mM_1")
        self.mM_2 = QtWidgets.QLabel(self.groupBox_M_5)
        self.mM_2.setGeometry(QtCore.QRect(10, 50, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.mM_2.setFont(font)
        self.mM_2.setObjectName("mM_2")
        self.mM_3 = QtWidgets.QLabel(self.groupBox_M_5)
        self.mM_3.setGeometry(QtCore.QRect(10, 70, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.mM_3.setFont(font)
        self.mM_3.setObjectName("mM_3")
        self.mM_4 = QtWidgets.QLabel(self.groupBox_M_5)
        self.mM_4.setGeometry(QtCore.QRect(10, 90, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.mM_4.setFont(font)
        self.mM_4.setObjectName("mM_4")
        self.mM_5 = QtWidgets.QLabel(self.groupBox_M_5)
        self.mM_5.setGeometry(QtCore.QRect(10, 110, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.mM_5.setFont(font)
        self.mM_5.setObjectName("mM_5")
        self.mM_8 = QtWidgets.QLabel(self.groupBox_M_5)
        self.mM_8.setGeometry(QtCore.QRect(10, 170, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.mM_8.setFont(font)
        self.mM_8.setObjectName("mM_8")
        self.mM_6 = QtWidgets.QLabel(self.groupBox_M_5)
        self.mM_6.setGeometry(QtCore.QRect(10, 130, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.mM_6.setFont(font)
        self.mM_6.setObjectName("mM_6")
        self.mM_10 = QtWidgets.QLabel(self.groupBox_M_5)
        self.mM_10.setGeometry(QtCore.QRect(10, 210, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.mM_10.setFont(font)
        self.mM_10.setObjectName("mM_10")
        self.mM_7 = QtWidgets.QLabel(self.groupBox_M_5)
        self.mM_7.setGeometry(QtCore.QRect(10, 150, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.mM_7.setFont(font)
        self.mM_7.setObjectName("mM_7")
        self.mM_9 = QtWidgets.QLabel(self.groupBox_M_5)
        self.mM_9.setGeometry(QtCore.QRect(10, 190, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.mM_9.setFont(font)
        self.mM_9.setObjectName("mM_9")
        self.groupBox_Acc = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Acc.setGeometry(QtCore.QRect(570, 280, 121, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_Acc.setFont(font)
        self.groupBox_Acc.setObjectName("groupBox_Acc")
        self.Acc_1 = QtWidgets.QLabel(self.groupBox_Acc)
        self.Acc_1.setGeometry(QtCore.QRect(10, 30, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Acc_1.setFont(font)
        self.Acc_1.setObjectName("Acc_1")
        self.Acc_2 = QtWidgets.QLabel(self.groupBox_Acc)
        self.Acc_2.setGeometry(QtCore.QRect(10, 50, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Acc_2.setFont(font)
        self.Acc_2.setObjectName("Acc_2")
        self.Acc_3 = QtWidgets.QLabel(self.groupBox_Acc)
        self.Acc_3.setGeometry(QtCore.QRect(10, 70, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Acc_3.setFont(font)
        self.Acc_3.setObjectName("Acc_3")
        self.Acc_4 = QtWidgets.QLabel(self.groupBox_Acc)
        self.Acc_4.setGeometry(QtCore.QRect(10, 90, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Acc_4.setFont(font)
        self.Acc_4.setObjectName("Acc_4")
        self.Acc_5 = QtWidgets.QLabel(self.groupBox_Acc)
        self.Acc_5.setGeometry(QtCore.QRect(10, 110, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Acc_5.setFont(font)
        self.Acc_5.setObjectName("Acc_5")
        self.Acc_7 = QtWidgets.QLabel(self.groupBox_Acc)
        self.Acc_7.setGeometry(QtCore.QRect(10, 150, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Acc_7.setFont(font)
        self.Acc_7.setObjectName("Acc_7")
        self.Acc_10 = QtWidgets.QLabel(self.groupBox_Acc)
        self.Acc_10.setGeometry(QtCore.QRect(10, 210, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Acc_10.setFont(font)
        self.Acc_10.setObjectName("Acc_10")
        self.Acc_6 = QtWidgets.QLabel(self.groupBox_Acc)
        self.Acc_6.setGeometry(QtCore.QRect(10, 130, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Acc_6.setFont(font)
        self.Acc_6.setObjectName("Acc_6")
        self.Acc_9 = QtWidgets.QLabel(self.groupBox_Acc)
        self.Acc_9.setGeometry(QtCore.QRect(10, 190, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Acc_9.setFont(font)
        self.Acc_9.setObjectName("Acc_9")
        self.Acc_8 = QtWidgets.QLabel(self.groupBox_Acc)
        self.Acc_8.setGeometry(QtCore.QRect(10, 170, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Acc_8.setFont(font)
        self.Acc_8.setObjectName("Acc_8")
        self.groupBox_m = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_m.setGeometry(QtCore.QRect(260, 280, 71, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_m.setFont(font)
        self.groupBox_m.setObjectName("groupBox_m")
        self.m_1 = QtWidgets.QLineEdit(self.groupBox_m)
        self.m_1.setGeometry(QtCore.QRect(10, 30, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.m_1.setFont(font)
        self.m_1.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.m_1.setAutoFillBackground(False)
        self.m_1.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.m_1.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.m_1.setText("")
        self.m_1.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.m_1.setClearButtonEnabled(False)
        self.m_1.setObjectName("m_1")
        self.m_2 = QtWidgets.QLineEdit(self.groupBox_m)
        self.m_2.setGeometry(QtCore.QRect(10, 50, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.m_2.setFont(font)
        self.m_2.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.m_2.setAutoFillBackground(False)
        self.m_2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.m_2.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.m_2.setText("")
        self.m_2.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.m_2.setClearButtonEnabled(False)
        self.m_2.setObjectName("m_2")
        self.m_3 = QtWidgets.QLineEdit(self.groupBox_m)
        self.m_3.setGeometry(QtCore.QRect(10, 70, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.m_3.setFont(font)
        self.m_3.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.m_3.setAutoFillBackground(False)
        self.m_3.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.m_3.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.m_3.setText("")
        self.m_3.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.m_3.setClearButtonEnabled(False)
        self.m_3.setObjectName("m_3")
        self.m_4 = QtWidgets.QLineEdit(self.groupBox_m)
        self.m_4.setGeometry(QtCore.QRect(10, 90, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.m_4.setFont(font)
        self.m_4.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.m_4.setAutoFillBackground(False)
        self.m_4.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.m_4.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.m_4.setText("")
        self.m_4.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.m_4.setClearButtonEnabled(False)
        self.m_4.setObjectName("m_4")
        self.m_5 = QtWidgets.QLineEdit(self.groupBox_m)
        self.m_5.setGeometry(QtCore.QRect(10, 110, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.m_5.setFont(font)
        self.m_5.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.m_5.setAutoFillBackground(False)
        self.m_5.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.m_5.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.m_5.setText("")
        self.m_5.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.m_5.setClearButtonEnabled(False)
        self.m_5.setObjectName("m_5")
        self.m_9 = QtWidgets.QLineEdit(self.groupBox_m)
        self.m_9.setGeometry(QtCore.QRect(10, 190, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.m_9.setFont(font)
        self.m_9.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.m_9.setAutoFillBackground(False)
        self.m_9.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.m_9.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.m_9.setText("")
        self.m_9.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.m_9.setClearButtonEnabled(False)
        self.m_9.setObjectName("m_9")
        self.m_6 = QtWidgets.QLineEdit(self.groupBox_m)
        self.m_6.setGeometry(QtCore.QRect(10, 130, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.m_6.setFont(font)
        self.m_6.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.m_6.setAutoFillBackground(False)
        self.m_6.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.m_6.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.m_6.setText("")
        self.m_6.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.m_6.setClearButtonEnabled(False)
        self.m_6.setObjectName("m_6")
        self.m_7 = QtWidgets.QLineEdit(self.groupBox_m)
        self.m_7.setGeometry(QtCore.QRect(10, 150, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.m_7.setFont(font)
        self.m_7.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.m_7.setAutoFillBackground(False)
        self.m_7.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.m_7.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.m_7.setText("")
        self.m_7.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.m_7.setClearButtonEnabled(False)
        self.m_7.setObjectName("m_7")
        self.m_10 = QtWidgets.QLineEdit(self.groupBox_m)
        self.m_10.setGeometry(QtCore.QRect(10, 210, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.m_10.setFont(font)
        self.m_10.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.m_10.setAutoFillBackground(False)
        self.m_10.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.m_10.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.m_10.setText("")
        self.m_10.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.m_10.setClearButtonEnabled(False)
        self.m_10.setObjectName("m_10")
        self.m_8 = QtWidgets.QLineEdit(self.groupBox_m)
        self.m_8.setGeometry(QtCore.QRect(10, 170, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.m_8.setFont(font)
        self.m_8.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.m_8.setAutoFillBackground(False)
        self.m_8.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Pakistan))
        self.m_8.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.m_8.setText("")
        self.m_8.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.m_8.setClearButtonEnabled(False)
        self.m_8.setObjectName("m_8")
        self.pushButton_GeneratePlot = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_GeneratePlot.setGeometry(QtCore.QRect(520, 160, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_GeneratePlot.setFont(font)
        self.pushButton_GeneratePlot.setObjectName("pushButton_GeneratePlot")
        self.Qosain_Label = QtWidgets.QLabel(self.centralwidget)
        self.Qosain_Label.setGeometry(QtCore.QRect(240, 10, 321, 131))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.Qosain_Label.setFont(font)
        self.Qosain_Label.setStyleSheet("")
        self.Qosain_Label.setText("")
        self.Qosain_Label.setPixmap(QtGui.QPixmap("QOSAINL.PNG"))
        self.Qosain_Label.setScaledContents(True)
        self.Qosain_Label.setWordWrap(False)
        self.Qosain_Label.setObjectName("Qosain_Label")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(310, 150, 151, 71))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.checkBoxAppend = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxAppend.setGeometry(QtCore.QRect(10, 40, 141, 31))
        self.checkBoxAppend.setObjectName("checkBoxAppend")
        self.checkBoxAppend.stateChanged.connect(self.checkBox_state)
        self.pushButton_GenerateTable = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_GenerateTable.setGeometry(QtCore.QRect(10, 10, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_GenerateTable.setFont(font)
        self.pushButton_GenerateTable.setObjectName("pushButton_GenerateTable")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(60, 230, 369, 41))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.BaseFolder = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.BaseFolder.setFont(font)
        self.BaseFolder.setObjectName("BaseFolder")
        self.horizontalLayout.addWidget(self.BaseFolder)

        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textBrowser.setFont(font)
        self.textBrowser.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser.setTabChangesFocus(False)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout.addWidget(self.textBrowser)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(440, 230, 251, 41))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.VariablesFile = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.VariablesFile.setFont(font)
        self.VariablesFile.setObjectName("VariablesFile")
        self.horizontalLayout_2.addWidget(self.VariablesFile)
        self.textBrowser_VariablesFile = QtWidgets.QTextBrowser(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textBrowser_VariablesFile.setFont(font)
        self.textBrowser_VariablesFile.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.textBrowser_VariablesFile.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_VariablesFile.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_VariablesFile.setTabChangesFocus(False)
        self.textBrowser_VariablesFile.setObjectName("textBrowser_VariablesFile")
        self.horizontalLayout_2.addWidget(self.textBrowser_VariablesFile)
        self.groupBox_2.raise_()
        self.groupBox.raise_()
        self.groupBox_SrNo.raise_()
        self.groupBox_M.raise_()
        self.groupBox_Files_Load.raise_()
        self.pushButton_PickFile.raise_()
        self.groupBox_M_5.raise_()
        self.groupBox_Acc.raise_()
        self.groupBox_m.raise_()
        self.pushButton_GeneratePlot.raise_()
        self.Qosain_Label.raise_()
        self.groupBox_3.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 749, 21))
        self.menubar.setObjectName("menubar")
#        self.menuFile = QtWidgets.QMenu(self.menubar)
#        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
    #    self.actionExport_Table = QtWidgets.QAction(MainWindow)
    #    self.actionExport_Table.setObjectName("actionExport_Table")
    #    self.actionExport_Plot = QtWidgets.QAction(MainWindow)
    #    self.actionExport_Plot.setObjectName("actionExport_Plot")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.triggered.connect(self.about_gui_command)


        self.actionHome_Page = QtWidgets.QAction(MainWindow)
        self.actionHome_Page.setObjectName("actionHome_Page")
        self.actionHome_Page.triggered.connect(self.open_home_page)

    #    self.menuFile.addAction(self.actionExport_Table)
    #    self.menuFile.addAction(self.actionExport_Plot)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionHome_Page)
     #   self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButton_PickFile, self.pushButton_GenerateTable)
        MainWindow.setTabOrder(self.pushButton_GenerateTable, self.checkBoxAppend)
        MainWindow.setTabOrder(self.checkBoxAppend, self.pushButton_GeneratePlot)
        MainWindow.setTabOrder(self.pushButton_GeneratePlot, self.M_1)
        MainWindow.setTabOrder(self.M_1, self.M_2)
        MainWindow.setTabOrder(self.M_2, self.M_3)
        MainWindow.setTabOrder(self.M_3, self.M_4)
        MainWindow.setTabOrder(self.M_4, self.M_5)
        MainWindow.setTabOrder(self.M_5, self.M_6)
        MainWindow.setTabOrder(self.M_6, self.M_7)
        MainWindow.setTabOrder(self.M_7, self.M_8)
        MainWindow.setTabOrder(self.M_8, self.M_9)
        MainWindow.setTabOrder(self.M_9, self.M_10)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Linear Air Track Analyzer"))
        self.groupBox_SrNo.setTitle(_translate("MainWindow", "Sr #"))
        self.Sr_1.setText(_translate("MainWindow", "1."))
        self.Sr_2.setText(_translate("MainWindow", "2."))
        self.Sr_3.setText(_translate("MainWindow", "3."))
        self.Sr_4.setText(_translate("MainWindow", "4."))
        self.Sr_5.setText(_translate("MainWindow", "5."))
        self.Sr_10.setText(_translate("MainWindow", "10."))
        self.Sr_7.setText(_translate("MainWindow", "7."))
        self.Sr_6.setText(_translate("MainWindow", "6."))
        self.Sr_9.setText(_translate("MainWindow", "9."))
        self.Sr_8.setText(_translate("MainWindow", "8."))
        self.groupBox_M.setTitle(_translate("MainWindow", "M (g)"))
        self.groupBox_Files_Load.setTitle(_translate("MainWindow", "Files loaded"))
        self.Fl_1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_8.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_9.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_10.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.pushButton_PickFile.setText(_translate("MainWindow", "1. Pick Files"))
        self.pushButton_PickFile.clicked.connect(self.pick_file)


        self.groupBox_M_5.setTitle(_translate("MainWindow", "m/M"))
        self.mM_1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_8.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_10.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_9.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.groupBox_Acc.setTitle(_translate("MainWindow", "Acc (cm/s²)"))
        self.Acc_1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_10.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_9.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_8.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.groupBox_m.setTitle(_translate("MainWindow", "m (g)"))
        self.pushButton_GeneratePlot.setText(_translate("MainWindow", "3. Generate Plot"))
        self.pushButton_GeneratePlot.clicked.connect(self.generate_plot)
        self.checkBoxAppend.setText(_translate("MainWindow", "Append to Variables File"))
        self.pushButton_GenerateTable.setText(_translate("MainWindow", "2. Analyze data"))
        self.pushButton_GenerateTable.clicked.connect(self.generate_table)
        self.BaseFolder.setText(_translate("MainWindow", "Base Folder:"))


        self.VariablesFile.setText(_translate("MainWindow", "Variables File:"))

    #    self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
    #    self.actionExport_Table.setText(_translate("MainWindow", "Export Table"))
    #    self.actionExport_Plot.setText(_translate("MainWindow", "Export Plot"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

        self.actionHome_Page.setText(_translate("MainWindow", "Home Page"))

    def filesname_set_text(self):

        _translate = QtCore.QCoreApplication.translate
        f_name = [line.rstrip() for line in open('filesavename')]
        f_name = func.name_list(f_name)
        #self.textBrowser_VariablesFile.setText(_translate("MainWindow", "Base Folder:"))
        self.textBrowser_VariablesFile.setText(_translate("MainWindow", f_name[0]))
    def retranslateUi_label(self, MainWindow): #os.path.dirname(lst_paths)

        _translate = QtCore.QCoreApplication.translate
        files_loaded_number = sum(1 for line in open("lst_paths"))
        lst_names = [line.rstrip() for line in open('lst_names')]
        lst_paths = [line.rstrip() for line in open('lst_paths')]
        lst_paths = lst_paths[0]

        self.textBrowser.setText(os.path.dirname(lst_paths))
        if files_loaded_number >= 1:
            self.Fl_1.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">"+lst_names[0]+"</span></p></body></html>"))
        if files_loaded_number >= 2:
            self.Fl_2.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">"+lst_names[1]+"</span></p></body></html>"))
        if files_loaded_number >= 3:
            self.Fl_3.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">"+lst_names[2]+"</span></p></body></html>"))
        if files_loaded_number >= 4:
            self.Fl_4.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">"+lst_names[3]+"</span></p></body></html>"))
        if files_loaded_number >= 5:
            self.Fl_5.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">"+lst_names[4]+"</span></p></body></html>"))
        if files_loaded_number >= 6:
            self.Fl_6.setText(_translate("MainWindow",
                                     "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">" + lst_names[0] + "</span></p></body></html>"))
        if files_loaded_number >= 7:
            self.Fl_7.setText(_translate("MainWindow",
                                     "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">" + lst_names[1] + "</span></p></body></html>"))
        if files_loaded_number >= 8:
            self.Fl_8.setText(_translate("MainWindow",
                                     "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">" + lst_names[2] + "</span></p></body></html>"))
        if files_loaded_number >= 9:
            self.Fl_9.setText(_translate("MainWindow",
                                     "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">" + lst_names[3] + "</span></p></body></html>"))
        if files_loaded_number >= 10:
            self.Fl_10.setText(_translate("MainWindow",
                                     "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">" + lst_names[4] + "</span></p></body></html>"))

    def acc_label(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        files_loaded_number = sum(1 for line in open("lst_paths"))
        lst_acc = [line.rstrip() for line in open('lst_acc')]
        lst_acc_Unc = [line.rstrip() for line in open('lst_acc_Unc')]
        if files_loaded_number >= 1:
            self.Acc_1.setText(_translate("MainWindow",
                                           "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:300;\">"+" "+str(int(np.round(np.array(lst_acc[0],dtype=float),0)))+ " ± " +str(int(np.round(np.array(lst_acc_Unc[0],dtype=float),0)))+"</span></p></body></html>"))
        if files_loaded_number >= 2:
            self.Acc_2.setText(_translate("MainWindow",
                                           "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:300;\">"+" "+str(int(np.round(np.array(lst_acc[1],dtype=float),0)))+ " ± " +str(int(np.round(np.array(lst_acc_Unc[1],dtype=float),0)))+"</span></p></body></html>"))
        if files_loaded_number >= 3:
            self.Acc_3.setText(_translate("MainWindow",
                                           "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:300;\">"+" "+str(int(np.round(np.array(lst_acc[2],dtype=float),0)))+ " ± " +str(int(np.round(np.array(lst_acc_Unc[2],dtype=float),0)))+"</span></p></body></html>"))
        if files_loaded_number >= 4:
            self.Acc_4.setText(_translate("MainWindow",
                                           "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:300;\">"+" "+str(int(np.round(np.array(lst_acc[3],dtype=float),0)))+ " ± " +str(int(np.round(np.array(lst_acc_Unc[3],dtype=float),0)))+"</span></p></body></html>"))
        if files_loaded_number >= 5:
            self.Acc_5.setText(_translate("MainWindow",
                                           "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:300;\">"+" "+str(int(np.round(np.array(lst_acc[4],dtype=float),0)))+ " ± " +str(int(np.round(np.array(lst_acc_Unc[4],dtype=float),0)))+"</span></p></body></html>"))
        if files_loaded_number >= 6:
            self.Acc_6.setText(_translate("MainWindow",
                                           "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:300;\">"+" "+str(int(np.round(np.array(lst_acc[0],dtype=float),0)))+ " ± " +str(int(np.round(np.array(lst_acc_Unc[0],dtype=float),0)))+"</span></p></body></html>"))
        if files_loaded_number >= 7:
            self.Acc_7.setText(_translate("MainWindow",
                                           "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:300;\">"+" "+str(int(np.round(np.array(lst_acc[1],dtype=float),0)))+ " ± " +str(int(np.round(np.array(lst_acc_Unc[1],dtype=float),0)))+"</span></p></body></html>"))
        if files_loaded_number >= 8:
            self.Acc_8.setText(_translate("MainWindow",
                                           "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:300;\">"+" "+str(int(np.round(np.array(lst_acc[2],dtype=float),0)))+ " ± " +str(int(np.round(np.array(lst_acc_Unc[2],dtype=float),0)))+"</span></p></body></html>"))
        if files_loaded_number >= 9:
            self.Acc_9.setText(_translate("MainWindow",
                                           "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:300;\">"+" "+str(int(np.round(np.array(lst_acc[3],dtype=float),0)))+ " ± " +str(int(np.round(np.array(lst_acc_Unc[3],dtype=float),0)))+"</span></p></body></html>"))
        if files_loaded_number >= 10:
            self.Acc_10.setText(_translate("MainWindow",
                                           "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:300;\">"+" "+str(int(np.round(np.array(lst_acc[4],dtype=float),0)))+ " ± " +str(int(np.round(np.array(lst_acc_Unc[4],dtype=float),0)))+"</span></p></body></html>"))
    def masses_ratios(self, MainWindow):
        files_loaded_number = sum(1 for line in open("lst_paths"))
        massratio = []
        if files_loaded_number >= 1:
            massratio.append(np.round(np.array(self.m_1.text(),dtype=float), 3) / np.round(np.array(self.M_1.text(),dtype=float), 3))
        if files_loaded_number >= 2:
            massratio.append(np.round(np.array(self.m_2.text(),dtype=float), 3) / np.round(np.array(self.M_2.text(),dtype=float), 3))
        if files_loaded_number >= 3:
            massratio.append(np.round(np.array(self.m_3.text(),dtype=float), 3) / np.round(np.array(self.M_3.text(),dtype=float), 3))
        if files_loaded_number >= 4:
            massratio.append(np.round(np.array(self.m_4.text(),dtype=float), 3) / np.round(np.array(self.M_4.text(),dtype=float), 3))
        if files_loaded_number >= 5:
            massratio.append(np.round(np.array(self.m_5.text(),dtype=float), 3) / np.round(np.array(self.M_5.text(),dtype=float), 3))
        if files_loaded_number >= 6:
            massratio.append(np.round(np.array(self.m_6.text(),dtype=float), 3) / np.round(np.array(self.M_6.text(),dtype=float), 3))
        if files_loaded_number >= 7:
            massratio.append(np.round(np.array(self.m_7.text(),dtype=float), 3) / np.round(np.array(self.M_7.text(),dtype=float), 3))
        if files_loaded_number >= 8:
            massratio.append(np.round(np.array(self.m_8.text(),dtype=float), 3) / np.round(np.array(self.M_8.text(),dtype=float), 3))
        if files_loaded_number >= 9:
            massratio.append(np.round(np.array(self.m_9.text(),dtype=float), 3) / np.round(np.array(self.M_9.text(),dtype=float), 3))
        if files_loaded_number >= 10:
            massratio.append(np.round(np.array(self.m_10.text(),dtype=float), 3) / np.round(np.array(self.M_10.text(),dtype=float), 3))

        mass_rat=np.round(massratio,3)
        outF = open("mass_ratios", "w")
        for line in mass_rat:
            outF.write(str(line))
            outF.write("\n")
        outF.close()

    def clear_label(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.Fl_1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_8.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_9.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Fl_10.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_8.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_10.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.mM_9.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_10.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_9.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.Acc_8.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">_________</p></body></html>"))
        self.m_1.setText("")
        self.m_2.setText("")
        self.m_3.setText("")
        self.m_4.setText("")
        self.m_5.setText("")
        self.m_6.setText("")
        self.m_7.setText("")
        self.m_8.setText("")
        self.m_9.setText("")
        self.m_10.setText("")
        self.M_1.setText("")
        self.M_2.setText("")
        self.M_3.setText("")
        self.M_4.setText("")
        self.M_5.setText("")
        self.M_6.setText("")
        self.M_7.setText("")
        self.M_8.setText("")
        self.M_9.setText("")
        self.M_10.setText("")
    def mass_ratios_label(self,MainWindow):
        files_loaded_number = sum(1 for line in open("lst_paths"))
        _translate = QtCore.QCoreApplication.translate
        mass_ratios = [line.rstrip() for line in open('mass_ratios')]

        if files_loaded_number >= 1:
            self.mM_1.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">" + " " + str(
                                              mass_ratios[0]) + "</span></p></body></html>"))
        if files_loaded_number >= 2:
            self.mM_2.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">" + " " + str(
                                              mass_ratios[1]) + "</span></p></body></html>"))
        if files_loaded_number >= 3:
            self.mM_3.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">" + " " + str(
                                              mass_ratios[2])+ "</span></p></body></html>"))
        if files_loaded_number >= 4:
            self.mM_4.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">" + " " + str(
                                              mass_ratios[3]) + "</span></p></body></html>"))
        if files_loaded_number >= 5:
            self.mM_5.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">" + " " + str(
                                              mass_ratios[4])+ "</span></p></body></html>"))
        if files_loaded_number >= 6:
            self.mM_6.setText(_translate("MainWindow",
                                    "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">" + " " + str(
                                            mass_ratios[0]) + "</span></p></body></html>"))
        if files_loaded_number >= 7:
            self.mM_7.setText(_translate("MainWindow",
                                    "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">" + " " + str(
                                            mass_ratios[1]) + "</span></p></body></html>"))
        if files_loaded_number >= 8:
            self.mM_8.setText(_translate("MainWindow",
                                    "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">" + " " + str(
                                            mass_ratios[2]) + "</span></p></body></html>"))
        if files_loaded_number >= 9:
            self.mM_9.setText(_translate("MainWindow",
                                    "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">" + " " + str(
                                            mass_ratios[3]) + "</span></p></body></html>"))
        if files_loaded_number >= 10:
            self.mM_10.setText(_translate("MainWindow",
                                    "<html><head/><body><p align=\"center\"><span style=\" font-weight:300;\">" + " " + str(
                                            mass_ratios[4]) + "</span></p></body></html>"))

    def about_gui_command(self):
        about_gui()

    def open_home_page(self):

        webbrowser.open('https://www.physlab.org/experiment/experiments-with-a-linear-air-track/', new=2)
    def checkBox_state(self,state):
        if state == QtCore.Qt.Checked:
            outF = open("chbx", "w")
            outF.write(str('1'))
            outF.close()

            if os.path.exists('filesavename') == False:
                pick_file_to_append().show()
                if os.path.exists('filesavename') == True:
                    self.filesname_set_text()
                else:
                    pass
        else:
            outF = open("chbx", "w")
            outF.write(str('0'))
            outF.close()


    def save_table(self):

        table_acc = np.single([line.rstrip() for line in open('lst_acc')])
        table_acc_unc = np.single([line.rstrip() for line in open('lst_acc_Unc')])
        table_mass_ratios = np.single([line.rstrip() for line in open('mass_ratios')])
        f_name = [line.rstrip() for line in open('filesavename')]
        np.savetxt('table_out', np.around(np.column_stack((table_mass_ratios,table_acc, table_acc_unc)), decimals=3), delimiter='\t',
                   fmt='%.3f')
        if int(open('chbx').read()) == 1:
            with open("table_out") as f:
                with open(f_name[0], "a") as f1:
                    for line in f:
                        f1.write(line)
        if int(open('chbx').read()) == 0:
            with open("table_out") as f:
                with open(f_name[0], "w") as f1:
                    for line in f:
                        f1.write(line)
    def pick_file(self):
        try:
            GUI_App().show()
            self.clear_label(MainWindow)
            self.retranslateUi_label(self)
        except:
            #print(ex)
            pass
    def generate_plot(self):
        try:
            Plot_Window().show()
        except:
            # print(ex)
            pass
    def generate_table(self):
        try:
            if os.path.exists('lst_acc') and os.path.exists('lst_acc_Unc'):
                if os.path.exists('chbx') == False:
                    outF = open("chbx", "w")
                    outF.write(str('0'))
                    outF.close()
                if int(open('chbx').read()) == 0:
                    save_file_prompt().show()
                    self.filesname_set_text()
                self.masses_ratios(MainWindow)
                self.mass_ratios_label(MainWindow)
                self.acc_label(MainWindow)
                self.save_table()
        except:
           # print("Wrong")
            pass



#import qosain_label_rc


if __name__ == "__main__":
    if os.path.exists('lst_acc'):
        os.remove('lst_acc')
    if os.path.exists('lst_acc_Unc'):
        os.remove('lst_acc_Unc')
    if os.path.exists('mass_ratios'):
        os.remove('mass_ratios')
    if os.path.exists('lst_names'):
        os.remove('lst_names')
    if os.path.exists('lst_paths'):
        os.remove('lst_paths')
    if os.path.exists('filesavename'):
        os.remove('filesavename')
    if os.path.exists('chbx'):
        os.remove('chbx')
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowIcon(QtGui.QIcon('ico.ico'))
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
