 
## Archivo: `README.md` (Guía para instalar paquetes)


Este proyecto utiliza `pip-tools` para gestionar dependencias. Sigue estos pasos para configurar el entorno e instalar los paquetes necesarios.

---

## Requisitos previos

- **Python 3.8 o superior**: [Descargar Python](https://www.python.org/downloads/)
- **pip**: Gestor de paquetes de Python (viene incluido con Python 3.4+).

---

## Pasos para instalar paquetes

1. **Clona el repositorio** (si no lo has hecho ya):

   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
   ```

2. **Ejecuta el script de configuración**:

   El proyecto incluye un script llamado `setup_env.sh` que automatiza la instalación de dependencias. Ejecuta el siguiente comando:

   ```bash
   ./setup_env.sh
   ```

   Este script hará lo siguiente:
   - Creará un entorno virtual en `.venv`.
   - Instalará `pip-tools` si no está instalado.
   - Generará el archivo `requirements.txt` a partir de `requirements.in`.
   - Instalará las dependencias listadas en `requirements.txt`.
   - Sincronizará el entorno con las dependencias actualizadas.

3. **Activa el entorno virtual manualmente (opcional)**:

   Si necesitas activar el entorno virtual manualmente, usa uno de los siguientes comandos dependiendo de tu sistema operativo:

   - **Linux/MacOS**:

     ```bash
     source .venv/bin/activate
     ```

   - **Windows (Git Bash o WSL)**:

     ```bash
     source .venv/Scripts/activate
     ```

   - **Windows (CMD)**:

     ```bash
     .\.venv\Scripts\activate
     ```

---

## Actualizar dependencias

Si agregas o modificas dependencias en `requirements.in`, sigue estos pasos para actualizar el entorno:

1. Edita el archivo `requirements.in` y agrega/elimina las dependencias necesarias.
2. Ejecuta el script de configuración nuevamente:

   ```bash
   ./setup_env.sh
   ```

   Esto regenerará `requirements.txt` y sincronizará el entorno con las nuevas dependencias.

   **Nota**: `pip-sync` (usado en el script) desinstalará automáticamente los paquetes que ya no están en `requirements.txt`.

---

## Estructura del proyecto

Aquí hay una breve descripción de los archivos relevantes:

```
tu-repositorio/
├── .venv/                  # Entorno virtual (ignorado por Git)
├── requirements.in         # Dependencias principales
├── requirements.txt        # Dependencias generadas (no editar manualmente)
├── setup_env.sh            # Script para configurar el entorno
└── README.md               # Este archivo
```
---
 $env:PYTHONPATH = "./src"; watchfiles 'uvicorn src.main:app'



