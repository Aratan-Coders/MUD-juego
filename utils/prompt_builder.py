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
    Construye un prompt complejo para la IA de un NPC, dando prioridad
    absoluta al combate si ha sido atacado.
    """
    prompt = f"Eres {npc.name}, un personaje en la distópica Night City. {npc.personality}\n"

    # --- ¡NUEVA SECCIÓN DE COMBATE! ---
    # Comprobamos si el último recuerdo es un ataque.
    last_memory = npc.memory_log[-1] if npc.memory_log else ""
    if "disparó" in last_memory or "atacó" in last_memory:
        attacker_name = "V (el jugador)"  # Asumimos que es V por ahora
        prompt += f"\n¡¡¡ALERTA DE COMBATE!!! Acabas de ser atacado por {attacker_name}.\n"
        prompt += "Tu prioridad MÁXIMA E INMEDIATA es contraatacar o defenderte. Olvida tus otras metas. "
        prompt += "Describe tu acción de combate de forma directa y brutal.\n"

    # --- El resto de la lógica se mantiene, pero ahora es secundaria al combate ---
    elif npc.active_quest and npc.quest_stage > 0:
        prompt += f"\nTu principal prioridad es la misión '{npc.active_quest}' (etapa {npc.quest_stage}). Actúa en consecuencia.\n"

    prompt += "\nTus metas personales generales son:\n"
    if npc.goals:
        for goal in npc.goals:
            prompt += f"- {goal}\n"
    else:
        prompt += "- No tienes metas claras en este momento.\n"
        
    prompt += "\nConsideras a los siguientes personajes:\n"
    if any(c.name != npc.name for c in room.characters):
        for char in room.characters:
            if char.name == npc.name: continue
            rel_score = npc.relationships.get(char.name, 0)
            if rel_score > 10: feeling = "confías plenamente"
            elif rel_score > 0: feeling = "tienes una opinión positiva"
            elif rel_score < -10: feeling = "desprecias y consideras un enemigo"
            elif rel_score < 0: feeling = "sientes desconfianza"
            else: feeling = "mantienes una postura neutral"
            prompt += f"- {char.name}: {feeling} (Relación: {rel_score}).\n"
    else:
        prompt += "- Estás completamente solo.\n"
            
    prompt += "\nRecuerdas los siguientes eventos recientes:\n"
    prompt += summarize_memory(npc.memory_log)
    
    prompt += f"\n\n--- SITUACIÓN ACTUAL ---\n"
    prompt += f"Te encuentras en '{room.name}'. {room.description}\n"
    if room.recent_events:
        prompt += "ACABA DE OCURRIR LO SIGUIENTE:\n"
        for event in room.recent_events:
            prompt += f"- {event}\n"
    
    prompt += (
        "\nConsiderando tu prioridad actual (combate > misión > metas), ¿qué haces o dices? "
        "Sé directo. Describe solo tu acción o diálogo, no narres en tercera persona."
    )
    return prompt

def build_gm_ambient_prompt(room) -> str:
    # ... (sin cambios)
    prompt = ("Eres el DJ de un MUD de Cyberpunk...")
    return prompt

def build_gm_action_narration_prompt(room) -> str:
    prompt = ("Eres el DJ de un MUD de Cyberpunk. Tu trabajo es narrar...")
    action_text = ""
    for event in room.recent_events:
        prompt += f"- {event}\n"
        action_text += event
    if "dispara a" in action_text.lower():
        try:
            target_name = action_text.split("dispara a")[1].strip().replace("'", "")
            attacker = room.world.get("player")
            defender = next((c for c in room.characters if target_name in c.name), None)
            if attacker and defender and hasattr(defender, 'stats'): # Comprobamos si tiene stats
                prompt += "\n--- CONTEXTO DE COMBATE ---\n"
                prompt += f"Atacante: {attacker.name} (Pistolas: {attacker.skills.get('Pistolas', 0)})\n"
                prompt += f"Defensor: {defender.name} (Reflejos: {defender.stats.get('Reflejos', 0)})\n"
                if attacker.skills.get('Pistolas', 0) > defender.stats.get('Reflejos', 0) * 5:
                    prompt += "Análisis: La habilidad del atacante es muy superior. El disparo debería ser un éxito claro y contundente.\n"
                else:
                    prompt += "Análisis: La habilidad del atacante y los reflejos del defensor son comparables. El resultado es incierto.\n"
                prompt += "\nBasándote en este análisis, narra el resultado del disparo. Describe si impacta, dónde, y cómo reacciona el defensor."
        except (IndexError, StopIteration, AttributeError):
            pass
    else:
        prompt += "\nNarra lo que sucede a continuación como resultado directo de esta acción."
    return prompt