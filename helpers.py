def task_helper(task_type, context):
    task_type = task_type.lower()
    context = context.strip()

    if task_type == "emotional support":
        return "I'm here for you. Feel free to share what's on your mind, and I'll listen."
    elif task_type == "stress relief techniques":
        return "Try deep breathing, short walks, or listening to calming music to reduce stress."
    elif task_type == "motivational advice":
        return "Remember, every step forward, no matter how small, is progress. Keep going!"
    elif task_type == "time management":
        return "Break tasks into small chunks and prioritize what matters most each day."
    elif task_type == "conflict resolution":
        return "Try to listen actively, communicate calmly, and find common ground."
    elif task_type == "self-care tips":
        return "Make sure to get enough rest, eat well, and take breaks when you need them."
    elif task_type == "communication skills":
        return "Practice clear and honest expression, and be mindful of non-verbal cues."
    else:
        return None  # Let GPT handle unknown tasks
