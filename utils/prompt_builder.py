def summarize_memory(memory_log: list, max_memories: int = 5) -> str:
    """
    Toma una lista de recuerdos y devuelve un resumen de los más recientes.
    """
    if not memory_log:
        return "No tienes recuerdos recientes."
    
    recent_memories = memory_log[-max_memories:]
    return "\n".join([f"- {mem}" for mem in recent_memories])

def build_npc_prompt(npc, room) -> str:
    """
    Construye un prompt complejo para la IA de un NPC, incorporando
    personalidad, metas, relaciones, memoria y situación actual.
    """
    
    # 1. Perfil Psicológico y Personalidad
    prompt = f"Eres {npc.name}, un personaje en la distópica Night City. {npc.personality}\n"
    
    # 2. Metas y Motivaciones (Iniciativa)
    prompt += "\nTus metas personales y motivaciones actuales son:\n"
    if npc.goals:
        for goal in npc.goals:
            prompt += f"- {goal}\n"
    else:
        prompt += "- No tienes metas claras en este momento.\n"
        
    # 3. Relaciones y Sentimientos
    prompt += "\nConsideras a los siguientes personajes:\n"
    if any(c.name != npc.name for c in room.characters):
        for char in room.characters:
            if char.name == npc.name: continue
            rel_score = npc.relationships.get(char.name, 0)
            if rel_score > 10: feeling = "confías plenamente y consideras un/a aliado/a cercano/a"
            elif rel_score > 0: feeling = "tienes una opinión positiva"
            elif rel_score < -10: feeling = "desprecias y consideras un/a enemigo/a"
            elif rel_score < 0: feeling = "sientes desconfianza"
            else: feeling = "mantienes una postura neutral"
            prompt += f"- {char.name}: {feeling} (Puntuación de relación: {rel_score}).\n"
    else:
        prompt += "- Estás completamente solo.\n"
            
    # 4. Memoria Reciente (Persistencia)
    prompt += "\nRecuerdas los siguientes eventos recientes:\n"
    prompt += summarize_memory(npc.memory_log)
    
    # 5. Situación Inmediata
    prompt += f"\n\n--- SITUACIÓN ACTUAL ---\n"
    prompt += f"Te encuentras en '{room.name}'. {room.description}\n"
    if room.recent_events:
        prompt += "ACABA DE OCURRIR LO SIGUIENTE:\n"
        for event in room.recent_events:
            if "realiza la acción" in event:
                prompt += f"- ¡ACCIÓN CRÍTICA! {event}. DEBES reaccionar a esto.\n"
            else:
                prompt += f"- {event}\n"
    
    # 6. La Instrucción Final
    prompt += (
        "\nConsiderando tus metas, personalidad, recuerdos y la situación actual, "
        "¿qué haces o dices a continuación? Sé directo y proactivo. "
        "Describe solo tu acción o diálogo, no narres en tercera persona."
    )
    return prompt

def build_gm_ambient_prompt(room) -> str:
    """
    Construye un prompt para que el Director de Juego describa el ambiente
    cuando no están ocurriendo acciones importantes.
    """
    prompt = (
        "Eres el Director de Juego (DJ) de un MUD de Cyberpunk. Tu trabajo es describir el ambiente y la atmósfera de una escena cuando está en calma. "
        "NO describas las acciones de los personajes, solo el entorno físico y sensorial.\n"
    )
    prompt += f"La escena actual es en '{room.name}'. {room.description}\n"
    characters_present = [c.name for c in room.characters]
    if characters_present:
        prompt += f"Los personajes aquí son: {', '.join(characters_present)}.\n"
    
    prompt += (
        "\nDescribe brevemente la atmósfera. Menciona un detalle sensorial (un olor, un sonido, el clima, la luz de neón) "
        "que enriquezca la escena. Sé evocador y conciso, en una o dos frases."
    )
    return prompt

def build_gm_action_narration_prompt(room) -> str:
    """
    ¡NUEVO Y CRUCIAL! Construye un prompt para que el Director de Juego narre
    las consecuencias directas de una acción importante del jugador.
    """
    prompt = (
        "Eres el Director de Juego (DJ) de un MUD de Cyberpunk. Tu trabajo es narrar las consecuencias de las acciones importantes de los jugadores. "
        "Sé cinemático y descriptivo. Concéntrate en el resultado de la acción, no en la intención.\n"
    )
    prompt += f"La escena actual es en '{room.name}'.\n"
    prompt += "ACCIÓN CRÍTICA REALIZADA POR EL JUGADOR (V):\n"
    # Mostramos los eventos recientes que llevaron a esta narración
    for event in room.recent_events:
        prompt += f"- {event}\n"
    
    prompt += (
        "\nNarra lo que sucede a continuación como resultado directo de esta acción. "
        "Describe el movimiento, los sonidos, las reacciones inmediatas del entorno. "
        "Si el jugador se está moviendo a un nuevo lugar, describe brevemente la transición y cómo es la llegada. "
        "No hables como un personaje, sé el narrador omnisciente de la historia."
    )
    return prompt