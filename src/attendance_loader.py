from singleton import Singleton
from datetime import datetime
class Attendance_Loader(Singleton):
    _initialized = False
    _already_attended = []
    def __init__(self, name):
        if not Attendance_Loader._initialized:
            self._attendance_file = open("data/attendance_sheet/attendance_sheet.csv", "w")
            Attendance_Loader._initialized = True
        
        self._attendance_file = open("data/attendance_sheet/attendance_sheet.csv", "a")
        self._name = name
        self._write_content(name, self._attendance_file)
    def _write_content(self, name, file):
        
        if name not in self._already_attended:
            file.write(f'{name},{datetime.now().strftime("%H:%M:%S")}\n')
            Attendance_Loader._already_attended.append(name)
        else:
            pass
