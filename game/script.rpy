# ==============================================================================
# INICIALIZACIÓN DE VARIABLES GLOBALES (PERSISTENTES Y DE SESIÓN)
# ==============================================================================

default persistent.unlocked_airi = True
default persistent.unlocked_ruka = False
default persistent.unlocked_kaori = False

default current_character_id = ""
default current_character_name = ""
default current_system_prompt = ""

default pts_afecto = 0
default pts_stream = 0
default current_day = 1

python early:
    import sys
    import os

    game_dir = config.gamedir
    
    libs_dir = os.path.join(game_dir, "libs")
    python_src_dir = os.path.join(game_dir, "src", "python")

    if libs_dir not in sys.path:
        sys.path.insert(0, libs_dir)
    if game_dir not in sys.path:
        sys.path.append(game_dir)
    if python_src_dir not in sys.path:
        sys.path.append(python_src_dir)

    try:
        from dotenv import load_dotenv
        env_path = os.path.join(config.basedir, ".env")
        load_dotenv(dotenv_path=env_path)
    except Exception as e:
        print(f"[ENV ERROR]: No se pudo cargar python-dotenv: {e}")

    from src.python.character_prompts import CHARACTERS
    from src.python.groq_api import consultar_groq

# Aqui se define la transicion rapida para el cambio de sprite
define qdissolve = Dissolve(0.25)



# ==============================================================================
# PUNTO DE ENTRADA AL INICIAR NUEVA PARTIDA
# ==============================================================================

label start:
    $ pts_afecto = 0
    $ pts_stream = 0
    $ current_day = 1

    call screen character_select_screen
    jump loop_principal_dia
