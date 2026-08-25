# ==============================================================================
# INICIALIZACIÓN DE VARIABLES GLOBALES (PERSISTENTES Y DE SESIÓN)
# ==============================================================================

# Control de desbloqueo de personajes (Persistente entre partidas)
default persistent.unlocked_airi = True
default persistent.unlocked_ruka = False
default persistent.unlocked_kaori = False

# Variables de la sesión actual
default current_character_id = ""
default current_character_name = ""
default current_system_prompt = ""

# Puntuaciones y métricas
default pts_afecto = 0
default pts_stream = 0
default current_day = 1

# Importación del módulo de prompts al arrancar Ren'Py
python early:
    import sys
    import os
    game_dir = os.path.join(config.gamedir)
    if game_dir not in sys.path:
        sys.path.append(game_dir)
    
    from src.python.character_prompts import CHARACTERS



# ==============================================================================
# PUNTO DE ENTRADA AL INICIAR NUEVA PARTIDA
# ==============================================================================

label start:
    # Reiniciar contadores del día
    $ pts_afecto = 0
    $ pts_stream = 0
    $ current_day = 1

    # Transición hacia la pantalla de selección de personajes
    call screen character_select_screen

    # Una vez seleccionado el personaje en la pantalla, el flujo continúa aquí
    jump loop_principal_dia



# ==============================================================================
# BUCLE PRINCIPAL Y CARGA DE DATOS DEL PERSONAJE
# ==============================================================================

label cargar_personaje(char_id):
    $ current_character_id = char_id
    $ current_character_name = CHARACTERS[char_id]["name"]
    $ current_system_prompt = CHARACTERS[char_id]["system_prompt"]
    
    # Notificación en consola de desarrollo
    $ renpy.log(f"Personaje cargado: {current_character_name}")
    return

label loop_principal_dia:
    scene bedroom with dissolve
    
    "Has seleccionado a [current_character_name]."
    "Día [current_day] - Puntos de afecto actuales: [pts_afecto]."
    
    # Fin del prototipo

    return
