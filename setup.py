from cx_Freeze import setup, Executable

setup(
    name="How to Train Your Dragon",
    version="1.0",
    description="Jogo de desviar do dragão",
    author="Seu Nome",
    executables=[Executable("dragon2.py")],
    options={
        "build_exe": {
            "include_files": [
                "assets/",   # inclua a pasta de imagens, sons, etc.
                "log.dat",
                "Recursos/"
            ]
        }
    }
)
