import subprocess

subprocess.run(
    ["taskkill", "/F", "/IM", "msedge.exe"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    creationflags=subprocess.CREATE_NO_WINDOW
)