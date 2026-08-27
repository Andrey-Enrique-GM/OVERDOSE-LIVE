# ==============================================================================
# BUCLE PRINCIPAL DE MAÑANA Y EVALUACIÓN DE STREAM
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
    
    # 1. Generar cantidad aleatoria de interacciones (entre 1 y 5)
    $ chats_manana_limite = renpy.random.randint(1, 5)
    $ chats_realizados = 0

    "Iniciando el Día [current_day] con [current_character_name]."
    "Revisas tu teléfono por la mañana..."

    # FASE CHAT DE LA MAÑANA
    while chats_realizados < chats_manana_limite:
        $ msgs_restantes = chats_manana_limite - chats_realizados
        $ input_msg = ""
        
        # Mostrar interfaz del Smartphone
        call screen phone_chat_screen(current_character_name, msgs_restantes, es_evaluacion_stream=False)
        $ user_text = _return

        if user_text.strip() != "":
            # Agregar mensaje del usuario al historial
            $ chat_history.append({"sender": "user", "text": user_text})
            
            # Petición a la API de Groq
            $ res_json = consultar_groq(current_character_id, user_text, fase="chat")
            
            $ res_dialogo = res_json.get("dialogo", "...")
            $ res_expresion = res_json.get("expresion", "neutral")
            $ delta_afecto = int(res_json.get("puntos_afecto", 0))
            
            # Actualizar puntuación de afecto
            $ pts_afecto += delta_afecto
            
            # Agregar respuesta del personaje al historial
            $ chat_history.append({"sender": "char", "text": res_dialogo, "expresion": res_expresion})
            $ chats_realizados += 1

    # FASE PREGUNTA Y EVALUACIÓN DE IDEA DE STREAM
    $ chat_history.append({"sender": "char", "text": "Y... ¿Qué idea tienes para el stream de hoy?", "expresion": "curious"})
    
    $ input_msg = ""
    call screen phone_chat_screen(current_character_name, 0, es_evaluacion_stream=True)
    $ idea_stream_user = _return

    if idea_stream_user.strip() != "":
        $ chat_history.append({"sender": "user", "text": idea_stream_user})
        
        # Evaluar idea enviando a Groq
        $ res_eval = consultar_groq(current_character_id, idea_stream_user, fase="evaluar_idea")
        
        $ res_dialogo_eval = res_eval.get("dialogo", "Entendido.")
        $ res_expresion_eval = res_eval.get("expresion", "neutral")
        $ delta_stream = int(res_eval.get("puntos_stream", 0))
        
        # Actualizar puntuación del stream
        $ pts_stream += delta_stream
        
        $ chat_history.append({"sender": "char", "text": res_dialogo_eval, "expresion": res_expresion_eval})

    # Mostrar la última reacción en pantalla antes de finalizar el prototipo
    "Resumen mañanero — Puntos Afecto: [pts_afecto] | Puntos Stream: [pts_stream]."

    # Mostrar respuesta final en la pantalla del teléfono antes de guardar el móvil
    "[current_character_name]" "[res_dialogo_eval]"

    # TRANSICIÓN E INICIO DEL STREAMING EN VIVO
    "Guardas tu teléfono. Es hora de preparar el setup de transmisión..."

    # setup de streaming
    scene stream_room with dissolve

    "Conectas la cámara y abres el software de transmisión."
    "Tema programado para hoy: '[idea_stream_user]'"

    # SIMULACIÓN DE STREAM EN VIVO
    call iniciar_simulacion_stream(idea_stream_user)

    # RESUMEN DEL DÍA Y PROGRESIÓN
    scene bedroom with dissolve

    "Termina la transmisión y apagas las luces del estudio."
    "Resumen del Día [current_day]:"
    "- Puntos de Afecto con [current_character_name]: [pts_afecto]"
    "- Puntos de Rendimiento del Stream: [pts_stream]"

    $ current_day += 1
    "Vas a descansar..."

    return