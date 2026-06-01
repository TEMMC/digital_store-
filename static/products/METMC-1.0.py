import datetime
import os
import random

# =========================
# MEMORY SYSTEM
# =========================
MEMORY_FILE = "metmc_memory.txt"

def save_memory(text):
    with open(MEMORY_FILE, "a") as f:
        f.write(text + "\n")

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return f.readlines()

# =========================
# OFFLINE "AI BRAIN"
# (rule + learning hybrid system)
# =========================
def brain(command):
    command = command.lower()

    # ---- TIME / DATE ----
    if "time" in command:
        return "⏰ " + datetime.datetime.now().strftime("%H:%M:%S")

    if "date" in command:
        return "📅 " + datetime.datetime.now().strftime("%Y-%m-%d")

    # ---- MEMORY ----
    if "save note" in command:
        save_memory(command.replace("save note", "").strip())
        return "🧠 Note saved offline."

    if "show notes" in command:
        notes = load_memory()
        return "🧠 MEMORY:\n" + "".join(notes[-5:]) if notes else "No memory stored."

    # ---- SELF-LEARNING STYLE RESPONSES ----
    if "hello" in command:
        return random.choice([
            "Hello. METMC online.",
            "System active.",
            "Ready for commands."
        ])

    if "your name" in command:
        return "I am METMC, your offline AI brain."

    if "how are you" in command:
        return random.choice([
            "All systems stable.",
            "Operating within normal parameters.",
            "I am functioning efficiently."
        ])

    # ---- FILE SYSTEM ----
    if "files" in command:
        return f"📁 Files in current directory: {len(os.listdir('.'))}"

    # ---- BASIC CALC (offline intelligence) ----
    if "calculate" in command:
        try:
            expr = command.replace("calculate", "")
            return "Result: " + str(eval(expr))
        except:
            return "Invalid calculation."

    # ---- LEARNING MODE ----
    if "learn" in command:
        save_memory("LEARNED: " + command)
        return "🧠 Learning stored."

    # ---- DEFAULT RESPONSE (AI BEHAVIOR SIMULATION) ----
    return "I don't fully understand yet. Teach me using 'learn' command."
    print("METMC OFFLINE AI BRAIN ACTIVE ⚡")
print("Type 'exit' to stop\n")

while True:
    user = input("YOU ➤ ")

    if user.lower() == "exit":
        print("METMC ➤ Shutting down.")
        break

    response = brain(user)
    print("METMC ➤", response)