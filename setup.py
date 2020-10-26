import sys
from cx_Freeze import setup, Executable

base = None
if (sys.platform == 'win32'):
    base = "Win32GUI"

setup(
    name = "MonProgramme",
    version = '0.1',
    description = "none",
    executables = [Executable("student interface.py", base = base)],
    options = {"build_exe": {"packages": ["tkinter","os","turtle","fitz","PIL","io","socket","threading"],
                             "include_files": ["Cours arduino + TP.pdf",
                                               "assets/PdfFiles/All in one Cours C & TD.pdf",
                                               "assets/PdfFiles/ALL IN ONE JAVA.pdf",
                                               "assets/PdfFiles/Cours arduino + TP.pdf",
                                               "assets/PdfFiles/datasheet.pdf",
                                               "assets/PdfFiles.pdf",
                                               "assets/buttons",
                                               "assets/buttons",
                                               "assets/buttons",
                                               "assets/buttons",
                                               "assets/buttons",
                                               "assets/buttons",
                                               "assets/buttons",
                                               "assets/buttons",
                                               "assets/buttons",
                                               "assets/buttons",
                                               "assets/buttons",
                                               "assets/buttons",
                                               "assets/buttons",
                                               "assets/buttons",
                                               "assets/buttons",
                                               "assets/buttons",
                                               "assets/buttons",
                                               ]}}, requires=['fitz', 'PIL']
)
