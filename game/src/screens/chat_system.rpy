# ==============================================================================
# SISTEMA DE CHAT DE SMARTPHONE (MAÑANA Y NOCHE)
# ==============================================================================

default chat_history = []
default input_msg = ""
default current_chat_expression = "neutral"


screen phone_chat_screen(char_name, mensajes_restantes, es_evaluacion_stream=False, es_noche=False):
    modal True

    # Color de fondo según el momento del día
    $ frame_bg = "#0f172a" if es_noche else "#121b22"
    $ header_bg = "#1e1b4b" if es_noche else "#1f2c34"
    $ header_title = "Chat Nocturno" if es_noche else char_name

    frame:
        xalign 0.95
        yalign 0.5
        xsize 420
        ysize 680
        background Solid(frame_bg)

        vbox:
            spacing 10
            xfill True

            # Encabezado del Smartphone
            frame:
                xfill True
                ysize 60
                background Solid(header_bg)
                hbox:
                    align (0.05, 0.5)
                    spacing 10
                    text "[header_title]" size 26 bold True color "#ffffff" yalign 0.5
                    if not es_evaluacion_stream:
                        text "(Msgs: [mensajes_restantes])" size 16 color "#a6adc8" yalign 0.5
                    else:
                        text "(Idea Stream)" size 16 color "#00ffcc" yalign 0.5

            # Área de Historial de Conversación
            viewport:
                id "chat_vp"
                xfill True
                ysize 520
                draggable True
                mousewheel True
                yinitial 1.0

                vbox:
                    xfill True
                    spacing 12

                    $ history_to_show = chat_history_noche if es_noche else chat_history

                    for item in history_to_show:
                        if item["sender"] == "user":
                            frame:
                                xalign 0.95
                                xmaximum 300
                                background Solid("#005c4b" if not es_noche else "#312e81")
                                padding (12, 8)
                                text "[item['text']]" color "#ffffff" size 18
                        else:
                            frame:
                                xalign 0.05
                                xmaximum 300
                                background Solid("#202c33" if not es_noche else "#1e293b")
                                padding (12, 8)
                                text "[item['text']]" color "#e9edef" size 18

            # Área de entrada de texto
            frame:
                xfill True
                ysize 70
                background Solid(header_bg)

                hbox:
                    align (0.5, 0.5)
                    spacing 10

                    input:
                        value VariableInputValue("input_msg")
                        length 120
                        pixel_width 280
                        color "#ffffff"
                        size 18

                    textbutton "Enviar":
                        action Return(input_msg)
                        sensitive (len(input_msg.strip()) > 0)
                        text_color "#00a884"
                        text_hover_color "#02e7b5"
                        text_size 18
                        text_bold True
