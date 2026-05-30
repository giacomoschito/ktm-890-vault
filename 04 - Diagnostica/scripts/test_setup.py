"""
Test installazione librerie diagnostica KTM.
Esegui questo script PRIMA di collegare qualsiasi hardware.
"""

import sys

def check_library(import_name, pip_name=None):
    pip_name = pip_name or import_name
    try:
        __import__(import_name)
        print(f"  [OK]      {pip_name}")
        return True
    except ImportError:
        print(f"  [MANCA]   {pip_name}  →  esegui:  pip install {pip_name}")
        return False

print("=" * 45)
print("  Test Setup Diagnostica KTM 890 Duke")
print("=" * 45)
print(f"\nPython: {sys.version.split()[0]}")
print(f"Percorso: {sys.executable}\n")

print("Librerie richieste:")
results = [
    check_library("serial", "pyserial"),
    check_library("obd", "python-obd"),
    check_library("rich"),
    check_library("pandas"),
]

print()
if all(results):
    print("  Tutto OK. Pronto per il collegamento hardware.")
    print("  Quando arriva il cavo, apri: OBD2 Setup KTM.md")
else:
    missing = results.count(False)
    print(f"  {missing} libreria/e mancante/i.")
    print("  Installa quelle con MANCA e riesegui questo script.")

print("=" * 45)
