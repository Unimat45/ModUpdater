import sys
from interface import *
from imports import *

class Main(QtWidgets.QMainWindow, Ui_MainWindow):


    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.rbtnAuto.setChecked(True)
        self.setFixedSize(self.size())
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)
        NbrLinks = len(get('https://pfk.ddns.net/mods/minecraft.json').json())
        self.progressBar.setRange(0, NbrLinks * 100)
        self.btnExit.clicked.connect(self.close)
        self.btnInstall.clicked.connect(self.on_btnInstall_clicked)

    def on_btnInstall_clicked(self):
        if self.rbtnAuto.isChecked():
            self.auto()

        if self.rbtnOnce.isChecked():
            self.noAuto()

        if self.rbtnRem.isChecked():
            self.uninstall()

    def noAuto(self):
        link = get('https://pfk.ddns.net/mods/minecraft.json').json()

        if system() == "Windows":
            path = os.path.join("C:\\", "Users", user(), "AppData", "Roaming", ".minecraft", "mods")

        elif system() == "Darwin":
            path = os.path.join("/Users", user(), "Library", "Application Support", "minecraft", "mods")

        elif system() == "Linux":
            path = os.path.join("/home", user(), ".minecraft", "mods")

        if path:
            if not os.path.isdir(path):
                os.makedirs(path)

            worker = Threader(path, link)
            worker.pbValue.connect(lambda value: self.progressBar.setValue(value))
            worker.done.connect(self.DoneDl)
            Thread(target=worker.downloadMods, daemon=True).start()

    def DoneDl(self, Done):
        if Done:
            QtWidgets.QMessageBox.about(self, "Success!", "Mods have been downloaded successfully!")
            self.progressBar.setValue(0)

    def auto(self):

        if system() == "Windows":
            path = os.path.join("C:\\", "Users", user(), "AppData", "Roaming", "ModsUpdater")

            if not os.path.isdir(path):
                os.mkdir(path)

            url = "https://pfk.ddns.net/mods/ModsUpdater.exe"
            url(url, "ModsUpdater.exe")

            command = "schtasks /create /F /sc hourly /tn ModsUpdater " 
            args = f'/tr \"C:\\Users\\{user()}\\AppData\\Roaming\\ModsUpdater\\ModsUpdater.exe\" /it > NUL'
            run(command + args, shell=True)

            run("schtasks /run /tn \"ModsUpdater\"", shell=True)
            return

        if system() == "Linux":
            path = os.path.join("/home", user(), ".ModsUpdater")

            if not os.path.isdir(path):
                os.mkdir(path)

            url = "https://pfk.ddns.net/mods/ModsUpdater.linux"
            url(url, "ModsUpdater")

            cron = CronTab(user=user())

            crons = [jobs for jobs in cron]

            job = "{}".format(os.path.join("/home", user(), ".ModsUpdater", "ModsUpdater"))

            if job not in crons:
                job = cron.new(command=job, comment="ModsUpdater")
                job.minute.on(0)
                cron.write()
            return

        if system() == "Darwin":

            if not os.path.isdir(os.path.join("/Users", user(), "Library", "Application Support", ".ModsUpdater")):
                os.mkdir(os.path.join("/Users", user(), "Library", "Application Support", ".ModsUpdater"))

            url = "https://pfk.ddns.net/mods/ModUpdater.mac"
            url(url, "ModsUpdater")

            cron = CronTab(user=user())

            crons = [jobs for jobs in cron]

            job = ''.format(os.path.join("/Users", user(), "Library", "Application Support", ".ModsUpdater","ModsUpdater"))

            if job not in crons:
                job = cron.new(command=job, comment="ModsUpdater")
                job.minute.on(0)
                cron.write()
            return

    def uninstall(self):

        if system() == "Windows":
            run("schtasks /delete /tn \"ModsUpdater\" /F > Nul", shell=True)
            return rmtree(os.path.join("C:\\", "Users", user(), "AppData", "Roaming", "ModsUpdater"))

        if system() == "Linux":
            
            cron = CronTab(user=user())

            command = ''.format(os.path.join("/Users", user(), "Library", "Application Support", ".ModsUpdater","ModsUpdater"))

            jobs = [job for job in cron if job.comment == "ModsUpdater"]

            if len(jobs) > 0:
                for job in jobs:
                    cron.remove(job)
                cron.write()

            return rmtree(os.path.join("/home", user(), ".ModsUpdater"))

        if system() == "Darwin":

            cron = CronTab(user=user())

            command = ''.format(os.path.join("/Users", user(), "Library", "Application Support", ".ModsUpdater","ModsUpdater"))

            jobs = [job for job in cron if job.comment == "ModsUpdater"]

            if len(jobs) > 0:
                for job in jobs:
                    cron.remove(job)
                cron.write()

            return rmtree(os.path.join("/Users", user(), "Library", "Application Support", ".ModsUpdater"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) 
    form = Main()
    form.show()
    app.exec()