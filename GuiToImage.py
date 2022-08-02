import sys
import random
import matplotlib
matplotlib.use('Qt5Agg')
import os
import numpy as np

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getmtime)

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.subplots()


        self.update_plot()


        file=newest(r"./TmpData/buffer")
        image = np.loadtxt(file)
        self.ax.imshow(image)
        self.ax.set_axis_off()
        self.setCentralWidget(self.canvas)

        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()


    def update_plot(self):

        file=newest(r"./TmpData/buffer")
        image = np.loadtxt(file)
        self.ax.imshow(image)

        self.canvas.draw()




app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
