# ==============================================================================
# SISTEMA DE CHAT DE SMARTPHONE (MAÑANA Y NOCHE)
# ==============================================================================

default chat_history = []
default chat_history_noche = []
default input_msg = ""
default current_chat_expression = "neutral"


screen phone_chat_screen(char_name, mensajes_restantes, es_evaluacion_stream=False, es_noche=False):
    modal True

    # Bloquear menú del juego si el guardado está deshabilitado
    if not config.save:
        key "game_menu" action NullAction()

    # Atajo de teclado: Enviar mensaje al presionar Enter
    if len(input_msg.strip()) > 0:
        key "K_RETURN" action Return(input_msg)
        key "K_KP_ENTER" action Return(input_msg)

    # Color de fondo según el momento del día
    $ frame_bg = "#0f172a" if es_noche else "#121b22"
    $ header_bg = "#1e1b4b" if es_noche else "#1f2c34"
    $ input_box_bg = "#090d16" if es_noche else "#0b141a"
    $ header_title = char_name  # Siempre muestra el nombre del personaje

    frame:
        xalign 0.96
        yalign 0.5
        xsize 520
        ysize 820
        background Solid(frame_bg)

        vbox:
            spacing 12
            xfill True

            # Encabezado del Smartphone
            frame:
                xfill True
                ysize 75
                background Solid(header_bg)
                
                hbox:
                    align (0.04, 0.5)
                    spacing 12
                    text "[header_title]" size 28 bold True color "#ffffff" yalign 0.5
                    if not es_evaluacion_stream:
                        text "(Msgs: [mensajes_restantes])" size 20 color "#a6adc8" yalign 0.5
                    else:
                        text "(Idea Stream)" size 20 color "#00ffcc" yalign 0.5

            # Área de Historial de Conversación
            viewport:
                id "chat_vp"
                xfill True
                ysize 620
                draggable True
                mousewheel True
                yinitial 1.0

                vbox:
                    xfill True
                    spacing 14

                    $ history_to_show = chat_history_noche if es_noche else chat_history

                    for item in history_to_show:
                        if item["sender"] == "user":
                            frame:
                                xalign 0.95
                                xmaximum 380
                                background Solid("#005c4b" if not es_noche else "#312e81")
                                padding (14, 10)
                                text "[item['text']]" color "#ffffff" size 22
                        else:
                            frame:
                                xalign 0.05
                                xmaximum 380
                                background Solid("#202c33" if not es_noche else "#1e293b")
                                padding (14, 10)
                                text "[item['text']]" color "#e9edef" size 22

            # Área de entrada de texto (Fija y Estática)
            frame:
                xfill True
                ysize 80
                background Solid(header_bg)
                padding (10, 10)

                hbox:
                    yalign 0.5
                    xfill True
                    spacing 10

                    # Campo visual contenedor del texto ingresado
                    frame:
                        xsize 380
                        ysize 55
                        background Solid(input_box_bg)
                        padding (12, 12)
                        yalign 0.5

                        input:
                            value VariableInputValue("input_msg")
                            length 150
                            pixel_width 355
                            color "#ffffff"
                            size 22
                            yalign 0.5

                    # Botón de Enviar (Posición fija a la derecha)
                    frame:
                        xsize 90
                        ysize 55
                        background None
                        yalign 0.5

                        textbutton "Enviar":
                            align (0.5, 0.5)
                            action Return(input_msg)
                            sensitive (len(input_msg.strip()) > 0)
                            text_color "#00a884"
                            text_hover_color "#02e7b5"
                            text_insensitive_color "#4a5568"
                            text_size 20
                            text_bold True
                            