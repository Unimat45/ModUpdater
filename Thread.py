from PyQt5 import QtCore
from requests import get 
import os

class Threader(QtCore.QThread):
    done = QtCore.pyqtSignal(bool)
    pbValue = QtCore.pyqtSignal(int)

    def __init__(self, pPath: str = None, pLinks = {}, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.path = pPath
        self.links = pLinks

    def downloadMods(self):
        if self.path:
            os.chdir(self.path)
            multiplyer = 1
            done = 0
            for link in self.links.keys():
                fileName = self.links[link]

                r = get(link, stream=True)
                total_length = r.headers.get('content-length')

                with open(fileName, "wb") as f:

                    if not total_length:
                        f.write(r.content)
                        
                    else:
                        dl = 0
                        total_length = int(total_length)
                        if not done % 100 and done != 0:
                                multiplyer += 1
                        for data in r.iter_content(chunk_size=4096):
                            dl += len(data)
                            f.write(data)
                            done = int((100 * multiplyer) * dl / total_length) 
                            if multiplyer != 1 and done == 0:
                                continue
                            print("{}".format(done))
                            self.pbValue.emit(done)
                            
            self.done.emit(True)
