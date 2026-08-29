# ==============================================================================
# BUCLE PRINCIPAL DE DÍA: MAÑANA (1/3), STREAM (2/3) Y NOCHE (3/3)
# ==============================================================================

label cargar_personaje(char_id):
    $ current_character_id = char_id
    $ current_character_name = CHARACTERS[char_id]["name"]
    $ current_system_prompt = CHARACTERS[char_id]["system_prompt"]
    $ renpy.log(f"Personaje cargado: {current_character_name}")
    return

label loop_principal_dia:
    scene bedroom with dissolve
    
    $ chat_history = []
    $ current_chat_suffix = "1" # Sprites mañana terminados en 1
    
    # Mostrar sprite neutral inicial del personaje
    call actualizar_sprite_chat(current_character_id, "neutral", suffix="1")

    $ chats_manana_limite = renpy.random.randint(1, 5)
    $ chats_realizados = 0

    "Iniciando el Día [current_day] con [current_character_name]."
    "Revisas tu teléfono por la mañana..."

    # --------------------------------------------------------------------------
    # FASE 1/3: CHAT DE LA MAÑANA
    # --------------------------------------------------------------------------
    while chats_realizados < chats_manana_limite:
        $ msgs_restantes = chats_manana_limite - chats_realizados
        $ input_msg = ""
        
        call screen phone_chat_screen(current_character_name, msgs_restantes, es_evaluacion_stream=False, es_noche=False)
        $ user_text = _return

        if user_text and user_text.strip() != "":
            $ chat_history.append({"sender": "user", "text": user_text})
            
            $ res_json = consultar_groq(current_character_id, user_text, fase="chat")
            
            $ res_dialogo = res_json.get("dialogo", "...")
            $ res_expresion = res_json.get("expresion", "neutral")
            $ delta_afecto = int(res_json.get("puntos_afecto", 0))
            
            $ pts_afecto += delta_afecto
            $ chat_history.append({"sender": "char", "text": res_dialogo, "expresion": res_expresion})
            
            call actualizar_sprite_chat(current_character_id, res_expresion, suffix="1")
            $ chats_realizados += 1

    # --------------------------------------------------------------------------
    # PREGUNTA Y EVALUACIÓN DE IDEA DE STREAM
    # --------------------------------------------------------------------------
    $ chat_history.append({"sender": "char", "text": "Y... ¿Qué idea tienes para el stream de hoy?", "expresion": "curious"})
    call actualizar_sprite_chat(current_character_id, "curious", suffix="1")

    $ input_msg = ""
    call screen phone_chat_screen(current_character_name, 0, es_evaluacion_stream=True, es_noche=False)
    $ idea_stream_user = _return

    if not idea_stream_user or idea_stream_user.strip() == "":
        $ idea_stream_user = "Charlando con la audiencia y jugando algo divertido."

    $ chat_history.append({"sender": "user", "text": idea_stream_user})
    
    $ res_eval = consultar_groq(current_character_id, idea_stream_user, fase="evaluar_idea")
    
    $ res_dialogo_eval = res_eval.get("dialogo", "¡Entendido! Vamos a preparar todo.")
    $ res_expresion_eval = res_eval.get("expresion", "neutral")
    $ delta_stream = int(res_eval.get("puntos_stream", 0))
    
    $ pts_stream += delta_stream
    $ chat_history.append({"sender": "char", "text": res_dialogo_eval, "expresion": res_expresion_eval})
    
    call actualizar_sprite_chat(current_character_id, res_expresion_eval, suffix="1")

    "Guardas tu teléfono. Es hora de preparar el setup de transmisión..."
    call ocultar_sprites_chat

    # --------------------------------------------------------------------------
    # FASE 2/3: SIMULACIÓN DE STREAM EN VIVO
    # --------------------------------------------------------------------------
    scene stream_room with dissolve

    "Conectas la cámara y abres el software de transmisión."
    "Tema programado para hoy: '[idea_stream_user]'"

    call iniciar_simulacion_stream(idea_stream_user)
    $ resultado_puntos_stream = _return

    # SÍNTESIS Y RESUMEN DEL DÍA PARA MEMORIA IA
    scene bedroom with dissolve

    "El stream ha terminado. Tomas un respiro mientras la noche empieza a caer..."

    # Generación de resumen sin dependencias externas
    $ res_resumen = consultar_groq(
        current_character_id, 
        idea_stream_user, 
        fase="generar_resumen", 
        contexto_extra=f"Puntos obtenidos en stream: {resultado_puntos_stream}"
    )
    $ resumen_dia_actual = res_resumen.get("resumen", f"Hablaron en la mañana y transmitieron sobre {idea_stream_user}.")

    # --------------------------------------------------------------------------
    # FASE 3/3: CHAT ANTES DE DORMIR (NOCHE)
    # --------------------------------------------------------------------------
    $ current_chat_suffix = "2"
    $ chat_history_noche = []
    
    call actualizar_sprite_chat(current_character_id, "neutral", suffix="2")

    $ chats_noche_limite = renpy.random.randint(1, 4)
    $ chats_noche_realizados = 0

    "Ya acostado en tu cama, ves una notificación en tu teléfono antes de dormir..."

    while chats_noche_realizados < chats_noche_limite:
        $ msgs_restantes = chats_noche_limite - chats_noche_realizados
        $ input_msg = ""
        
        call screen phone_chat_screen(current_character_name, msgs_restantes, es_evaluacion_stream=False, es_noche=True)
        $ user_text = _return

        if user_text and user_text.strip() != "":
            $ chat_history_noche.append({"sender": "user", "text": user_text})
            
            # Consulta a Groq pasando el resumen acumulado de la jornada
            $ res_json = consultar_groq(
                current_character_id, 
                user_text, 
                fase="chat_noche", 
                resumen_dia=resumen_dia_actual
            )
            
            $ res_dialogo = res_json.get("dialogo", "Buenas noches...")
            $ res_expresion = res_json.get("expresion", "neutral")
            $ delta_afecto = int(res_json.get("puntos_afecto", 0))
            
            $ pts_afecto += delta_afecto
            $ chat_history_noche.append({"sender": "char", "text": res_dialogo, "expresion": res_expresion})
            
            call actualizar_sprite_chat(current_character_id, res_expresion, suffix="2")
            $ chats_noche_realizados += 1

    # --------------------------------------------------------------------------
    # RESUMEN DEL DÍA Y PROGRESIÓN AL SIGUIENTE DÍA
    # --------------------------------------------------------------------------
    call ocultar_sprites_chat

    "Apagas la pantalla del teléfono y te acomodas para descansar."
    "Resumen del Día [current_day]:"
    "- Puntos de Afecto acumulados: [pts_afecto]"
    "- Puntos de Rendimiento del Stream: [pts_stream]"

    $ current_day += 1
    scene black with dissolve
    "Te quedas profundamente dormido..."

    jump loop_principal_dia
