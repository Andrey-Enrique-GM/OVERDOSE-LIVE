# ==============================================================================
# SISTEMA DE CHAT DE SMARTPHONE
# ==============================================================================

# Variables de estado del chat
default chat_history = []
default input_msg = ""
default current_chat_expression = "neutral"


# ------------------------------------------------------------------------------
# INTERFAZ DE USUARIO: PANTALLA DE CHAT SMARTPHONE
# ------------------------------------------------------------------------------
screen phone_chat_screen(char_name, mensajes_restantes, es_evaluacion_stream=False):
    modal True

    # Marco del Teléfono en el lado derecho de la pantalla
    frame:
        xalign 0.95
        yalign 0.5
        xsize 420
        ysize 680
        background Solid("#121b22")

        vbox:
            spacing 10
            xfill True

            # Encabezado del Smartphone
            frame:
                xfill True
                ysize 60
                background Solid("#1f2c34")
                hbox:
                    align (0.05, 0.5)
                    spacing 10
                    text "[char_name]" size 30 bold True color "#ffffff" yalign 0.5
                    if not es_evaluacion_stream:
                        text "(Mensajes: [mensajes_restantes])" size 18 color "#a6adc8" yalign 0.5
                    else:
                        text "(Propuesta de Stream)" size 18 color "#00ffcc" yalign 0.5

            # Área de Historial de Conversación (Scrollable)
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

                    for item in chat_history:
                        if item["sender"] == "user":
                            frame:
                                xalign 0.95
                                xmaximum 300
                                background Solid("#005c4b")
                                padding (10, 8)
                                text item["text"] size 16 color "#ffffff"
                        else:
                            frame:
                                xalign 0.05
                                xmaximum 300
                                background Solid("#202c33")
                                padding (10, 8)
                                vbox:
                                    text item["text"] size 16 color "#ffffff"
                                    text "Expresión: " + str(item.get("expresion", "neutral")) size 12 color "#8596a0"

            # Área de Input de Texto y Envío
            hbox:
                xfill True
                ysize 60
                spacing 5
                
                input:
                    value VariableInputValue("input_msg")
                    length 100
                    xfill True
                    ysize 40
                    copypaste True
                    style "input_phone_style"

                textbutton "Enviar":
                    ysize 40
                    if input_msg.strip() != "":
                        action Return(input_msg)
                    else:
                        action None

style input_phone_style:
    color "#ffffff"
    background Solid("#2a3942")
    padding (8, 8)
