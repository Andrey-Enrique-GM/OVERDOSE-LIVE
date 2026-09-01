# ==============================================================================
# BUCLE PRINCIPAL DE DÍA: CHAT 1, STREAM Y CHAT 2 (NOCHE)
# ==============================================================================

label loop_principal_dia:
    scene bedroom with dissolve
    $ config.save = True
    $ renpy.take_screenshot()
    $ renpy.save("1-1")
    $ renpy.notify("Autoguardado en Slot 1 completado")
    
    $ chat_history = []
    $ current_chat_suffix = "1"
    
    call actualizar_sprite_chat(current_character_id, "neutral", suffix="1")

    # CHAT 1: Cantidad aleatoria entre 1 y 5 turnos
    $ chats_manana_limite = random.randint(1, 5)
    $ chats_realizados = 0

    "Iniciando el Día [current_day] con [current_character_name]."
    "Revisas tu teléfono por la mañana..."

    # --------------------------------------------------------------------------
    # FASE 1/3: CHAT 1 (MAÑANA)
    # --------------------------------------------------------------------------
    $ config.save = False
    while chats_realizados < chats_manana_limite:
        $ msgs_restantes = chats_manana_limite - chats_realizados
        $ input_msg = ""
        
        call screen phone_chat_screen(current_character_name, msgs_restantes, es_evaluacion_stream=False, es_noche=False)
        $ user_text = _return

        if user_text and user_text.strip() != "":
            # Consultar pasándole el historial previo para no perder el hilo
            $ res_json = consultar_groq(
                current_character_id, 
                user_text, 
                fase="chat", 
                historial=chat_history
            )
            
            $ res_dialogo = res_json.get("dialogo", "...")
            $ res_expresion = res_json.get("expresion", "neutral")
            $ delta_afecto = int(res_json.get("puntos_afecto", 0))
            
            # Sumar/Restar Puntos de Afecto según la IA
            $ pts_afecto += delta_afecto
            
            # Guardar en el historial de la sesión
            $ chat_history.append({"sender": "user", "text": user_text})
            $ chat_history.append({"sender": "char", "text": res_dialogo, "expresion": res_expresion})
            
            call actualizar_sprite_chat(current_character_id, res_expresion, suffix="1")
            $ chats_realizados += 1

    $ config.save = True

    # --------------------------------------------------------------------------
    # PREGUNTA Y EVALUACIÓN DE IDEA DE STREAM
    # --------------------------------------------------------------------------
    $ chat_history.append({"sender": "char", "text": "Y... ¿Qué idea tienes para el stream de hoy?", "expresion": "curious"})
    call actualizar_sprite_chat(current_character_id, "curious", suffix="1")

    $ input_msg = ""
    $ config.save = False
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
    $ config.save = True

    "Guardas tu teléfono. Es hora de preparar el setup de transmisión..."
    call ocultar_sprites_chat

    # --------------------------------------------------------------------------
    # FASE 2/3: SIMULACIÓN DE STREAM EN VIVO (3 a 10 Bloques)
    # --------------------------------------------------------------------------
    scene stream_room with dissolve

    "Conectas la cámara y abres el software de transmisión."
    "Tema programado para hoy: '[idea_stream_user]'"

    # Genera aleatoriamente entre 3 y 10 bloques para el stream en una sola llamada a la API
    $ duracion_stream = random.randint(3, 10)
    call iniciar_simulacion_stream(idea_stream_user, duracion_stream)
    $ resultado_puntos_stream = _return

    # SÍNTESIS Y RESUMEN DEL DÍA (CHAT 1 + STREAM)
    scene bedroom with dissolve

    "El stream ha terminado. Tomas un respiro mientras la noche empieza a caer..."

    $ res_resumen = consultar_groq(
        current_character_id, 
        idea_stream_user, 
        fase="generar_resumen", 
        contexto_extra=f"Charlas de la mañana: {json.dumps(chat_history)}. Puntos stream: {resultado_puntos_stream}"
    )
    $ resumen_current_day = res_resumen.get("resumen", f"Hablaron en la mañana y transmitieron sobre {idea_stream_user}.")

    # --------------------------------------------------------------------------
    # FASE 3/3: CHAT 2 (NOCHE: 1 a 5 turnos)
    # --------------------------------------------------------------------------
    $ current_chat_suffix = "2"
    $ chat_history_noche = []
    
    call actualizar_sprite_chat(current_character_id, "neutral", suffix="2")

    # Chat 2: Cantidad aleatoria entre 1 y 5 turnos
    $ chats_noche_limite = random.randint(1, 5)
    $ chats_noche_realizados = 0

    "Ya acostado en tu cama, ves una notificación en tu teléfono antes de dormir..."

    $ config.save = False
    while chats_noche_realizados < chats_noche_limite:
        $ msgs_restantes = chats_noche_limite - chats_noche_realizados
        $ input_msg = ""
        
        call screen phone_chat_screen(current_character_name, msgs_restantes, es_evaluacion_stream=False, es_noche=True)
        $ user_text = _return

        if user_text and user_text.strip() != "":
            # Consultar enviando el resumen del día Y el historial propio del Chat 2
            $ res_json = consultar_groq(
                current_character_id, 
                user_text, 
                fase="chat_noche", 
                resumen_dia=resumen_current_day,
                historial=chat_history_noche
            )
            
            $ res_dialogo = res_json.get("dialogo", "Buenas noches...")
            $ res_expresion = res_json.get("expresion", "neutral")
            $ delta_afecto = int(res_json.get("puntos_afecto", 0))
            
            # Sumar/Restar Puntos de Afecto también en el Chat 2
            $ pts_afecto += delta_afecto
            
            # Guardar hilo conversacional del Chat 2
            $ chat_history_noche.append({"sender": "user", "text": user_text})
            $ chat_history_noche.append({"sender": "char", "text": res_dialogo, "expresion": res_expresion})
            
            call actualizar_sprite_chat(current_character_id, res_expresion, suffix="2")
            $ chats_noche_realizados += 1

    $ config.save = True

    # --------------------------------------------------------------------------
    # RESUMEN Y FINALIZACIÓN DEL DÍA
    # --------------------------------------------------------------------------
    call ocultar_sprites_chat

    "Apagas la pantalla del teléfono y te acomodas para descansar."
    "Resumen del Día [current_day]:"
    "- Puntos de Afecto acumulados: [pts_afecto]"
    "- Puntos de Rendimiento del Stream: [pts_stream]"

    $ current_day += 1
    
    if current_day > 5:
        jump evaluar_final

    scene black with dissolve
    "Te quedas profundamente dormido..."

    jump loop_principal_dia
