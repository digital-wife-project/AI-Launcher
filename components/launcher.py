from PyQt5.QtCore import QProcess, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication
import sys

class BatRunner(QObject):
    finished = pyqtSignal(int)  # Signal to indicate the process has finished
    output = pyqtSignal(str)  # Signal to emit console output

    def __init__(self, parent=None):
        super(BatRunner, self).__init__(parent)
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)
        self.process.readyReadStandardError.connect(self.onReadyReadStandardError)
        self.process.finished.connect(self.onFinished)

    def run_bat(self, bat_file_path, working_directory):
        """
        Run a .bat file in the specified working directory.

        :param bat_file_path: The path to the .bat file to run.
        :param working_directory: The working directory to run the .bat file in.
        """
        self.process.setWorkingDirectory(working_directory)
        self.process.start(bat_file_path)

    def onReadyReadStandardOutput(self):
        """
        Read and emit standard output from the process.
        """
        output = self.process.readAllStandardOutput().data().decode()
        self.output.emit(output)
        print(output, end='')  # Print output in real-time

    def onReadyReadStandardError(self):
        """
        Read and emit standard error from the process.
        """
        error = self.process.readAllStandardError().data().decode()
        self.output.emit(error)
        print(error, end='')  # Print error in real-time

    def onFinished(self, exit_code):
        """
        Slot to handle the process finishing.

        :param exit_code: The exit code of the process.
        """
        self.finished.emit(exit_code)

