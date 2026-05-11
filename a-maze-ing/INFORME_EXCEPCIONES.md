# Informe de flujo de excepciones y jerarquía de responsabilidades

## 1. Jerarquía de excepciones (actualizada)
- **MazeConfigError**
  - **ImposibleMazeError**
- **DisplayMazeError**
- **MazeGenerationError**
  - **MazeIOError**
- **DependencyError**

## 2. Flujo de excepciones por capa
1. **Configuración (`config/parser.py`, `config/validator.py`)**
   - `parse_config` y `parse_coord` validan formato y valores.
   - Se levantan **MazeConfigError** (o **ImposibleMazeError** en reglas
     imposibles) y no se llama a `exit()` dentro del módulo.
2. **Generación (`mazegen/maze_generator.py`)**
   - `solve` puede lanzar **MazeGenerationError** si no existe salida.
   - `save_to_file` lanza **MazeIOError** ante fallos de escritura.
3. **UI (`ui/display.py`)**
   - `check_display_size` y `animation` lanzan **DisplayMazeError** si no se
     puede renderizar con seguridad.
4. **Controlador (`controller/core.py`)**
   - Orquesta el flujo y no termina el programa.
   - `run_visuals` carga `readchar` y levanta **DependencyError** si falta.
5. **CLI (`a_maze_ing.py`)**
   - Es el único punto que imprime el mensaje final y decide terminar
     el proceso, centralizando la gestión de errores.

## 3. Refactorización aplicada
- Eliminación de salidas tempranas (`exit`/`sys.exit`) en `config/parser.py`
  y `controller/core.py` para permitir propagación controlada.
- Normalización de `ValueError` a **MazeConfigError** en parsing.
- Propagación de **DisplayMazeError** y **MazeGenerationError** hasta el CLI.
- Nueva excepción **DependencyError** para dependencias faltantes.
- Nueva excepción **MazeIOError** para errores de escritura.

## 4. Propuestas adicionales (opcional)
- Crear una excepción base `AppError` para agrupar todos los errores de la
  aplicación y simplificar el manejo en el CLI.
- Reemplazar `print` directos en la UI por excepciones (`DisplayMazeError`)
  o logging estructurado para trazabilidad.
- Usar `warnings.warn` para mensajes no críticos (por ejemplo, patrón 42).
