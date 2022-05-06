from Base import Base

import os
import random
from src.analysis import Analysis

random.seed(42)

def loadFolderFiles(dirName) -> list:
    listOfFile = os.listdir(dirName)
    allFiles = []
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + loadFolderFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

class Classification(Base):
    def loadAudioLibrary(self, path):
        self.libary_dir = path
        self.labels = os.listdir(path)
        for dir in self.labels:
            # print(f'Loading Folder {dir}:')
            self.loadFolder(dir)
    
    def loadFolder(self, label):
        self.library[label] = []
        self.database[label] = []
        self.library[label] = loadFolderFiles(os.path.join(self.libary_dir, label))
        self.loadDataFrameFile()
        if self.validateFolder(label):
            progress_bar = self.loadProgressBar(label, init=self.getCountInsideDataFrame('label', label))
            # max_files = len(self.library[label])
            while self.tracks * self.segments != self.getCountInsideDataFrame('label', label):
                file_path = self.selectRandomFile(label)
                filename = os.path.basename(file_path).replace(' ', '_')
                if self.validateFile(file_path, filename):
                    # print(f'    Loading file: {file_path}')
                    if results := self.loadFile(file_path, progress_bar):
                        for i, result in enumerate(results):
                            result['filename'] = self.getFilename(filename, i)
                            self.database[label].append(results)
                        self.updateDataFrame()
                        self.saveDataFrame()
                    else:
                        print(f'Error loading file: {file_path}')
            progress_bar.close()
            
    def loadFile(self, file_path, progress_bar):
        alyis = Analysis(audio_path=file_path, options=self, _bar = progress_bar)
        if(alyis.failed == True):
            return False
        return alyis.calculate()
    
    def selectRandomFile(self, label):
        random.shuffle(self.library[label])
        return self.library[label].pop().replace('\\', '/')
