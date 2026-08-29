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
default current_chat_suffix = "1" # "1" para mañana, "2" para noche
default resumen_dia_actual = ""    # Almacena el contexto generado para el chat nocturno

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


# Configuración visual e imágenes de interfaz
define gui.playtime_font = "gui/fonts/playtime.ttf" 
define qdissolve = Dissolve(0.25)


# ==============================================================================
# HELPER: ACTUALIZAR SPRITE DEL CHAT (FONDO + SPRITES INDIVIDUALES)
# ==============================================================================

label actualizar_sprite_chat(char_id, expresion, suffix=None):
    $ suffix_to_use = suffix if suffix else current_chat_suffix

    # Cargar Sprite Base usando la convención _bg (ej: airi1_bg, airi2_bg)
    $ base_tag = f"{char_id}{suffix_to_use}_bg"
    if renpy.has_image(base_tag):
        $ renpy.show(base_tag, at_list=[left], tag=f"{char_id}_chat_body")

    # Validar que la Expresión con Sufijo exista (ej: airi2_face_happy)
    $ face_tag = f"{char_id}{suffix_to_use}_face_{expresion}"
    if not renpy.has_image(face_tag):
        $ expresion = "neutral"
        $ face_tag = f"{char_id}{suffix_to_use}_face_neutral"

    # Aplicar transición de cara usando Tag único para reemplazo directo
    $ tag_cara_generica = f"{char_id}_chat_face"
    if renpy.has_image(face_tag):
        $ renpy.show(face_tag, at_list=[left], tag=tag_cara_generica)
        $ renpy.with_statement(qdissolve)

    $ current_chat_expression = expresion
    return


label ocultar_sprites_chat():
    $ body_tag = f"{current_character_id}_chat_body"
    $ face_tag = f"{current_character_id}_chat_face"
    $ renpy.hide(body_tag)
    $ renpy.hide(face_tag)
    $ renpy.with_statement(dissolve)
    return


# ==============================================================================
# PUNTO DE ENTRADA AL INICIAR NUEVA PARTIDA
# ==============================================================================

label start:
    $ pts_afecto = 0
    $ pts_stream = 0
    $ current_day = 1
    $ resumen_dia_actual = ""

    call screen character_select_screen
    jump loop_principal_dia
