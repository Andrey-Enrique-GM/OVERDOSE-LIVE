# ==============================================================================
# ANIMACIONES Y TRANSFORMS
# ==============================================================================

transform carta:
    on idle:
        easein 0.15 zoom 1.0
    on hover:
        easein 0.15 zoom 1.05



# ==============================================================================
# PANTALLA DE SELECCIÓN DE PERSONAJES
# ==============================================================================

screen character_select_screen():
    tag menu
    modal True

    # Fondo de la pantalla
    add "bgs/vignette.png"

    # Variable local para detectar sobre qué personaje está el cursor
    default char_hover = None

    text "SELECCIONA UN PERSONAJE" xalign 0.5 ypos 60 size 40 color "#c319e9" bold True
    text "Desbloquea nuevos personajes consiguiendo todos los finales" xalign 0.5 ypos 110 size 20 color "#cccccc"

    # Grid de tarjetas de personaje
    hbox:
        align (0.5, 0.55)
        spacing 40

        # TARJETA 1: AIRI SHIRAYUKI
        button:
            at carta
            xysize (460, 600)
            padding (20, 20)
            background Solid("#1e1e24")
            hover_background Solid("#2b2b36")

            hovered [Play("sound", "audio/UI/Retro7.wav"), SetScreenVariable("char_hover", "airi")]
            unhovered SetScreenVariable("char_hover", None)
            
            if persistent.unlocked_airi:
                action [
                    Function(renpy.call, "cargar_personaje", "airi"),
                    Return()
                ]
            else:
                action None # Desactivado si está bloqueado

            vbox:
                align (0.5, 0.5)
                spacing 15

                # Imagen de retrato
                add "images/portraits/airi_portrait.png" xalign 0.5 xysize (400, 400)

                text "Airi Shirayuki" xalign 0.5 bold True size 28 idle_color "#FFFFFF" hover_color "#7febfc"
                text "Idol & Streamer" xalign 0.5 size 16 idle_color "#a6adc8"

                null height 15

                if persistent.unlocked_airi:
                    textbutton "SELECCIONAR":
                        xalign 0.5
                        action [
                            Function(renpy.call, "cargar_personaje", "airi"),
                            Return()
                        ]
                else:
                    text "BLOQUEADO" size 18 color "#6c7086" xalign 0.5

        # TARJETA 2: RUKA KUROGANE
        button:
            at carta
            xysize (460, 600)
            padding (20, 20)
            background Solid("#1e1e24")
            hover_background Solid("#2b2b36")

            hovered [Play("sound", "audio/UI/Retro7.wav"), SetScreenVariable("char_hover", "ruka")]
            unhovered SetScreenVariable("char_hover", None)

            if persistent.unlocked_ruka:
                action [
                    Function(renpy.call, "cargar_personaje", "ruka"),
                    Return()
                ]
            else:
                action None

            vbox:
                align (0.5, 0.5)
                spacing 15

                # Imagen de retrato
                add "images/portraits/ruka_portrait.png" xalign 0.5 xysize (400, 400)

                text "Ruka Kurogane" xalign 0.5 bold True size 28 idle_color "#FFFFFF" hover_color "#c551f3"
                text "Gamer Streamer" xalign 0.5 size 16 idle_color "#a6adc8"

                null height 15

                if persistent.unlocked_ruka:
                    textbutton "SELECCIONAR":
                        xalign 0.5
                        action [
                            Function(renpy.call, "cargar_personaje", "ruka"),
                            Return()
                        ]
                else:
                    text "BLOQUEADO" size 18 color "#6c7086" xalign 0.5

        # TARJETA 3: KAORI SUMIZOME
        button:
            at carta
            xysize (460, 600)
            padding (20, 20)
            background Solid("#1e1e24")
            hover_background Solid("#2b2b36")

            hovered [Play("sound", "audio/UI/Retro7.wav"), SetScreenVariable("char_hover", "kaori")]
            unhovered SetScreenVariable("char_hover", None)

            if persistent.unlocked_kaori:
                action [
                    Function(renpy.call, "cargar_personaje", "kaori"),
                    Return()
                ]
            else:
                action None

            vbox:
                align (0.5, 0.5)
                spacing 15

                # Imagen de retrato
                add "images/portraits/kaori_portrait.png" xalign 0.5 xysize (400, 400)

                text "Kaori Sumizome" xalign 0.5 bold True size 28 idle_color "#FFFFFF" hover_color "#b34343"
                text "Streamer Compositora" xalign 0.5 size 16 idle_color "#a6adc8"

                null height 15

                if persistent.unlocked_kaori:
                    textbutton "SELECCIONAR":
                        xalign 0.5
                        action [
                            Function(renpy.call, "cargar_personaje", "kaori"),
                            Return()
                        ]
                else:
                    text "BLOQUEADO" size 18 color "#6c7086" xalign 0.5
