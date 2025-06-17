import sys
from cx_Freeze import setup, Executable

# Dependências extras
build_exe_options = {
    "packages": ["pygame", "tkinter", "random", "json", "threading", "speech_recognition", "pyttsx3", "datetime"],
    "include_files": [
        "assets",         # pasta com imagens e músicas
        "recursos",       # pasta com frase_motivacional
        "log.dat",        # arquivo de pontuação
    ],
    "include_msvcr": True,
}

# Alvo principal
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # para não abrir console junto

setup(
    name="How to Train Your Dragon",
    version="1.0",
    description="Para fãs de como treinar seu dragão",
    options={"build_exe": build_exe_options},
    executables=[Executable("flying.py", base=base)]
)
