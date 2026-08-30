# ==============================================================================
# SISTEMA Y PANTALLA DE SIMULACIÓN DE STREAM EN VIVO
# ==============================================================================

# Variables de estado del stream
default stream_live_chat = []
default current_streamer_expression = "neutral"
default stream_viewers_count = 1250



# INTERFAZ DE USUARIO: OVERLAY DEL STREAM
screen stream_overlay_screen(char_name):
    # Bloquear menú del juego si el guardado está deshabilitado
    if not config.save:
        key "game_menu" action NullAction()

    # Banner superior "EN VIVO"
    frame:
        xalign 0.04
        yalign 0.03
        background Solid("#cc000088")
        padding (20, 10)
        
        hbox:
            spacing 12
            text "* EN VIVO" color "#ffffff" size 24 bold True
            text " | Espectadores: [stream_viewers_count]" color "#dddddd" size 22

    # Caja del Chat del Stream
    frame:
        xalign 0.96
        yalign 0.12
        xsize 480
        ysize 600
        background Solid("#000000aa")
        padding (18, 18)

        vbox:
            spacing 10
            text "CHAT EN VIVO" color "#ffcc00" size 20 bold True
            null height 5

            viewport:
                scrollbars None
                draggable True
                mousewheel True
                yinitial 1.0

                vbox:
                    spacing 8
                    for author, msg in stream_live_chat:
                        hbox:
                            spacing 8
                            text "[author]:" color "#4da6ff" size 20 bold True
                            text "[msg]" color "#ffffff" size 20


# LÓGICA DE CONTROL DEL STREAMING (LABEL)
label iniciar_simulacion_stream(idea_stream, duracion_stream):
    $ config.save = False
    $ stream_viewers_count = random.randint(800, 2500)
    $ stream_live_chat = []
    $ prev_expression = ""
    
    "Preparando la transmisión en vivo sobre: '[idea_stream]'..."
    "Duración estimada del stream: [duracion_stream] bloques."

    # Solicitar la simulación completa en un único mensaje JSON a la API
    $ res_stream = consultar_groq(current_character_id, idea_stream, fase="simular_stream", duracion=duracion_stream)
    
    $ eventos_stream = res_stream.get("eventos", [])
    $ resultado_puntos = int(res_stream.get("resultado_stream", 0))

    # Respaldos en caso de que la respuesta venga vacía o con errores
    if not eventos_stream:
        $ eventos_stream = [
            {
                "dialogo": "¡Hola a todos! Bienvenidos al stream de hoy.",
                "expresion": "happy",
                "viewer_name": "Fan1",
                "viewer_comment": "¡Saludos!"
            },
            {
                "dialogo": "Estamos probando cosas geniales hoy.",
                "expresion": "smile",
                "viewer_name": "Anonimo",
                "viewer_comment": "<3 <3"
            },
            {
                "dialogo": "¡Muchas gracias por acompañarme!",
                "expresion": "happy",
                "viewer_name": "Mod_Zero",
                "viewer_comment": "GGWP"
            }
        ]

    # Mostrar la interfaz overlay del stream
    show screen stream_overlay_screen(current_character_name)

    # Iterar y mostrar paso a paso en formato novela visual
    $ idx = 0
    while idx < len(eventos_stream):
        $ evt = eventos_stream[idx]
        $ evt_dialogo = evt.get("dialogo", "...")
        $ evt_expresion = evt.get("expresion", "neutral")
        $ evt_vname = evt.get("viewer_name", "Viewer")
        $ evt_vcomment = evt.get("viewer_comment", "...")

        # Construir el nombre del tag de la imagen declarada
        $ image_tag_name = f"{current_character_id} {evt_expresion}"
        
        # Si la expresión recibida no está definida, usar neutral
        if not renpy.has_image(image_tag_name):
            $ evt_expresion = "neutral"
            $ image_tag_name = f"{current_character_id} neutral"

        # Mostrar la imagen a la izquierda con la transición qdissolve si cambia
        if evt_expresion != prev_expression:
            $ renpy.show(image_tag_name, at_list=[left])
            $ renpy.with_statement(qdissolve)
            $ prev_expression = evt_expresion

        # Actualizar estado de la escena y chat en vivo
        $ current_streamer_expression = evt_expresion
        $ stream_live_chat.append((evt_vname, evt_vcomment))
        
        # Mantener solo los últimos 8 mensajes en el chat
        if len(stream_live_chat) > 8:
            $ stream_live_chat.pop(0)

        # Fluctuación orgánica de espectadores
        $ stream_viewers_count += random.randint(-15, 30)

        # Usar el objeto de Character correspondiente para mantener el color configurado en characters.rpy
        $ char_obj = getattr(store, current_character_id, None)
        if char_obj:
            $ renpy.say(char_obj, evt_dialogo)
        else:
            "[current_character_name]" "[evt_dialogo]"

        $ idx += 1

    # Ocultar la personaje y la interfaz del stream al finalizar
    $ renpy.hide(current_character_id)
    $ renpy.with_statement(qdissolve)
    hide screen stream_overlay_screen

    # Aplicar variación a la variable global pts_stream (-1, 0, +1)
    if resultado_puntos > 1:
        $ resultado_puntos = 1
    elif resultado_puntos < -1:
        $ resultado_puntos = -1

    $ pts_stream += resultado_puntos

    if resultado_puntos > 0:
        "¡El stream fue un gran éxito! Ganaste +1 punto de stream."
    elif resultado_puntos < 0:
        "El stream tuvo bastantes problemas... Perdiste -1 punto de stream."
    else:
        "El stream terminó sin pena ni gloria (+0 puntos)."

    $ config.save = True
    return resultado_puntos
