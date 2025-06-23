#!/bin/bash

# Nombre del entorno virtual
VENV_NAME=".venv"

# Nombre del archivo de entrada y salida
INPUT_FILE="requirements.in"
OUTPUT_FILE="requirements.txt"

# Verificar si el entorno virtual existe, si no, crearlo
if [ ! -d "$VENV_NAME" ]; then
    echo "Creando entorno virtual en $VENV_NAME..."
    python -m venv $VENV_NAME

    # Crear un archivo .gitignore dentro del entorno virtual
    echo "Creando .gitignore en $VENV_NAME..."
    echo "*" > $VENV_NAME/.gitignore
fi

# Activar el entorno virtual
echo "Activando el entorno virtual $VENV_NAME..."
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    # Linux o MacOS
    source $VENV_NAME/bin/activate
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash o Cygwin)
    source $VENV_NAME/Scripts/activate
else
    echo "Sistema operativo no compatible. No se pudo activar el entorno virtual."
    exit 1
fi

# Verificar si pip-tools está instalado, si no, instalarlo
if ! command -v pip-compile &> /dev/null; then
    echo "pip-tools no está instalado. Instalando..."
    pip install pip-tools
fi

# Compilar requirements.in para generar requirements.txt
echo "Generando $OUTPUT_FILE a partir de $INPUT_FILE..."
pip-compile $INPUT_FILE --output-file $OUTPUT_FILE

# Sincronizar el entorno con las dependencias actualizadas
echo "Sincronizando el entorno con $OUTPUT_FILE..."
pip-sync $OUTPUT_FILE

# Instalar solo Chromium para playwright
CHROMIUM_EXEC=$(find "$HOME/AppData/Local/ms-playwright" -type f -name headless_shell.exe 2>/dev/null | head -n 1)

if [ -f "$CHROMIUM_EXEC" ]; then
    echo "Chromium ya está instalado. ✅"
else
    echo "Instalando Chromium para Playwright..."
    python -m playwright install chromium
fi

echo "¡Proceso completado!"