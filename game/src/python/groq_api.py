import json
import os
import ssl
import urllib.error
import urllib.request
from src.python.character_prompts import CHARACTERS

URL_API_GROQ = "https://api.groq.com/openai/v1/chat/completions"


def _obtener_api_key():
    """Busca la clave de API en las variables del sistema o dentro del archivo .env"""
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        return api_key.strip()

    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )
    env_file = os.path.join(base_dir, ".env")

    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea.startswith("GROQ_API_KEY="):
                    valor = linea.split("=", 1)[1].strip()
                    return valor.strip("\"'")
    return None


def _construir_instrucciones(char_id, fase, duracion=5):
    """Construye las instrucciones (system prompt) según el personaje y la fase actual."""
    char_data = CHARACTERS[char_id]
    prompt_base = char_data["system_prompt"]

    instrucciones = f"{prompt_base}\n\n[FASE ACTUAL DE LA INTERACCIÓN: {fase}]\n"

    if fase == "chat":
        instrucciones += (
            "Responde en formato JSON estricto con las llaves: "
            "'dialogo', 'expresion', 'puntos_afecto' (-1, 0, 1)."
        )
    elif fase == "evaluar_idea":
        instrucciones += (
            "Evalúa la propuesta del stream hecha por el usuario. Responde en JSON con las llaves: "
            "'dialogo', 'expresion', 'puntos_stream' (-1, 0, 1)."
        )
    elif fase == "simular_stream":
        instrucciones += (
            f"Estás en plena transmisión EN VIVO (Stream). Genera exactamente {duracion} momentos/secuencias consecutivas del stream.\n"
            "Responde en formato JSON estricto con el siguiente esquema exacto:\n"
            "{\n"
            "  'resultado_stream': int (-1 si el stream fue un desastre/fracaso, 0 si fue regular/neutro, 1 si fue un gran éxito),\n"
            "  'eventos': [\n"
            f"    // Lista de exactamente {duracion} objetos:\n"
            "    {\n"
            "      'dialogo': 'Lo que dice la streamer en voz alta a su audiencia en este turno',\n"
            "      'expresion': 'happy | excited | neutral | pout | shocked | embarrassed',\n"
            "      'viewer_name': 'Nombre de un espectador aleatorio en el chat (ej. Anonimo777, OtakuPro, SimpLord)',\n"
            "      'viewer_comment': 'Mensaje corto enviado por ese espectador en el chat del stream'\n"
            "    }\n"
            "  ]\n"
            "}"
        )

    return instrucciones


def _enviar_solicitud_http(payload, api_key):
    """Realiza la conexión con los servidores de Groq y retorna la respuesta en formato JSON."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    datos = json.dumps(payload).encode("utf-8")
    peticion = urllib.request.Request(URL_API_GROQ, data=datos, headers=headers)
    contexto_ssl = ssl._create_unverified_context()

    with urllib.request.urlopen(peticion, context=contexto_ssl) as respuesta:
        cuerpo = json.loads(respuesta.read().decode("utf-8"))
        contenido_texto = cuerpo["choices"][0]["message"]["content"]
        return json.loads(contenido_texto)


def consultar_groq(char_id, prompt_usuario, fase, contexto_extra="", duracion=5):
    """Función principal: Valida entradas, prepara la consulta y obtiene la respuesta de Groq."""
    if char_id not in CHARACTERS:
        print(f"[ERROR GROQ]: El personaje '{char_id}' no existe.")
        return {}

    api_key = _obtener_api_key()
    if not api_key:
        print("[ERROR GROQ]: No se encontró la variable GROQ_API_KEY.")
        return {}

    instrucciones = _construir_instrucciones(char_id, fase, duracion)
    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {"role": "system", "content": instrucciones},
            {
                "role": "user",
                "content": f"{contexto_extra}\nTema/Propuesta del stream: {prompt_usuario}",
            },
        ],
        "temperature": 0.7,
        "response_format": {"type": "json_object"},
    }

    try:
        return _enviar_solicitud_http(payload, api_key)
    except urllib.error.HTTPError as error:
        cuerpo_error = error.read().decode("utf-8")
        print(f"[ERROR GROQ HTTP {error.code}]: {cuerpo_error}")
        return {}
    except Exception as error:
        print(f"[ERROR GROQ]: {error}")
        return {}
