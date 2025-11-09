import pyttsx3
import datetime
import speech_recognition as sr
import os
import pywhatkit
import pygame
import math
import random
import sys
import time as t
import threading
import requests
from openai import OpenAI
import webbrowser

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")  # replace with your key

name = input("Enter your name: ")

def say(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 0.5)
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language='en-in')
        print("You said:", command)
        return command.lower()
    except:
        say("Sorry, I did not catch that.")
        return ""

def get_command():
    say("Do you want to speak or type your command?")
    print("\nType 'voice' to speak or 'type' to type:")
    mode = input("Mode: ").lower()
    if "voice" in mode:
        return listen()
    else:
        return input("Enter your command: ").lower()

def greet():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        say(f"Good morning {name}")
    elif 12 <= hour < 18:
        say(f"Good afternoon {name}")
    else:
        say(f"Good evening {name}")
    say("I am Jarvis, ready for your command.")
    show_options()

MEMORY_FILE = "memory.txt"

def load_memory():
    memory = {}
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            for line in file:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    memory[key.strip()] = value.strip()
    return memory

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        for key, value in memory.items():
            file.write(f"{key}: {value}\n")

memory = load_memory()

# Show all commands
def show_options():
    options = [
        "1. Play YouTube video",
        "2. Open WhatsApp Web",
        "3. Open ChatGPT",
        "4. Open Gmail",
        "5. Show current time",
        "6. Search Google",
        "7. Ask ChatGPT",
        "8. Set an alarm",
        "9. Get news",
        "10. Remember something",
        "11. Show memory",
        "12. game",
        "13. Forget something",
        "14. Exit"
    ]
    say("Here are the commands you can use:")
    for option in options:
        print(option)
        say(option)

def google_search(query):
    say(f"Searching Google for {query}")
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)

def get_news():
    api_key = "d9bb891b9c4045999ef47c0d5afad0ff"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        response = requests.get(url).json()
        articles = response["articles"][:5]
        say("Here are the latest headlines:")
        for a in articles:
            say(a["title"])
    except:
        say("Sorry, I could not fetch the news.")

def set_alarm(alarm_time):
    say(f"Alarm set for {alarm_time}")
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == alarm_time:
            say("Wake up! It's time!")
            break
        t.sleep(30)

def run_ai_enemy_game():
    pygame.init()

    # Music setup
    try:
        pygame.mixer.music.load("rider.mp3")  # Make sure the file exists
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
    except:
        print("Music file not found, continuing without music.")

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AI Enemy Game - Smart Enemies")

    WHITE = (255, 255, 255)
    RED = (255, 60, 60)
    BLUE = (50, 150, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)

    clock = pygame.time.Clock()
    FPS = 60

    player_size = 40
    player_speed = 5
    player_x, player_y = WIDTH // 2, HEIGHT // 2

    enemy_size = 50
    enemy_speed = 2
    frame_count = 0
    level = 1
    score = 0
    game_over = False

    ENEMY_TYPES = ["chaser", "zigzag", "circle", "predict"]

    def spawn_enemies(count):
        enemies = []
        for _ in range(count):
            x = random.randint(0, WIDTH - enemy_size)
            y = random.randint(0, HEIGHT - enemy_size)
            etype = random.choice(ENEMY_TYPES)
            enemies.append({"x": x, "y": y, "type": etype, "angle": 0})
        return enemies

    enemy_list = spawn_enemies(1)

    def move_enemy(enemy, player_x, player_y, speed):
        dx = player_x - enemy["x"]
        dy = player_y - enemy["y"]
        distance = math.hypot(dx, dy)
        if distance == 0:
            return
        nx, ny = dx / distance, dy / distance
        if enemy["type"] == "chaser":
            enemy["x"] += speed * nx
            enemy["y"] += speed * ny
        elif enemy["type"] == "zigzag":
            enemy["x"] += speed * nx + math.sin(pygame.time.get_ticks() * 0.005) * 3
            enemy["y"] += speed * ny + math.cos(pygame.time.get_ticks() * 0.005) * 3
        elif enemy["type"] == "circle":
            enemy["angle"] += 0.05
            enemy["x"] += speed * nx + math.cos(enemy["angle"]) * 2
            enemy["y"] += speed * ny + math.sin(enemy["angle"]) * 2
        elif enemy["type"] == "predict":
            enemy["x"] += speed * nx * 1.1
            enemy["y"] += speed * ny * 1.1

    font = pygame.font.SysFont("Arial", 30)
    
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT]:
                player_x -= player_speed
            if keys[pygame.K_RIGHT]:
                player_x += player_speed
            if keys[pygame.K_UP]:
                player_y -= player_speed
            if keys[pygame.K_DOWN]:
                player_y += player_speed

            player_x = max(0, min(WIDTH - player_size, player_x))
            player_y = max(0, min(HEIGHT - player_size, player_y))

            for enemy in enemy_list:
                move_enemy(enemy, player_x, player_y, enemy_speed)
                if abs(player_x - enemy["x"]) < player_size - 10 and abs(player_y - enemy["y"]) < player_size - 10:
                    game_over = True

            pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
            for enemy in enemy_list:
                color = RED if enemy["type"] == "chaser" else GREEN if enemy["type"] == "zigzag" else YELLOW if enemy["type"] == "circle" else (255, 100, 255)
                pygame.draw.rect(screen, color, (enemy["x"], enemy["y"], enemy_size, enemy_size))

            frame_count += 1
            score = frame_count // FPS
            if frame_count % (15 * FPS) == 0:
                level += 1
                enemy_speed += 0.3
                enemy_list.extend(spawn_enemies(len(enemy_list)))

            screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
            screen.blit(font.render(f"Level: {level}", True, YELLOW), (10, 40))
        else:
            text1 = font.render("Game Over! Press R to Restart", True, WHITE)
            text2 = font.render(f"Final Score: {score}", True, GREEN)
            screen.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//2 - 20))
            screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 + 20))

            if keys[pygame.K_r]:
                player_x, player_y = WIDTH//2, HEIGHT//2
                enemy_list = spawn_enemies(1)
                enemy_speed = 2
                frame_count = 0
                level = 1
                score = 0
                game_over = False

        pygame.display.flip()
        clock.tick(FPS)

# --- Integrate into Jarvis ---
# Add to the main command loop


def ask_chatgpt(question):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content
    except Exception as e:
        if "insufficient_quota" in str(e):
            return "Adnan, your OpenAI quota seems to have expired."
        return f"Sorry, I could not get an answer. {e}"

greet()

while True:
    command = get_command()

    if "youtube" in command:
        say("What should I play on YouTube?")
        song = input("You: ")
        say(f"Playing {song} on YouTube.")
        pywhatkit.playonyt(song)

    elif "whatsapp" in command:
        say("Opening WhatsApp Web.")
        os.system("start https://web.whatsapp.com")

    elif "chatgpt" in command:
        say("Opening ChatGPT...")
        os.system("start https://chatgpt.com")

    elif "gmail" in command:
        say("Opening Gmail...")
        os.system("start https://gmail.com")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        say(f"The time is {current_time}")

    elif "search" in command:
        say("What do you want me to search for?")
        query = input("You: ")
        google_search(query)

    elif "ask" in command or "question" in command:
        say("What do you want to ask ChatGPT?")
        question = input("You: ")
        answer = ask_chatgpt(question)
        say(answer)

    elif "set alarm" in command:
        say("At what time? (HH:MM 24h format)")
        alarm_time = input("You: ")
        threading.Thread(target=set_alarm, args=(alarm_time,), daemon=True).start()

    elif "news" in command:
        get_news()
    
    elif "play game" in command or "game" in command:
        say("Launching AI Enemy Game...")
        threading.Thread(target=run_ai_enemy_game, daemon=True).start()


    elif "remember" in command:
        say("What should I remember?")
        fact = input("You: ")
        key = fact.split()[0]
        memory[key] = fact
        save_memory(memory)
        say("Got it, I’ll remember that.")

    elif "show memory" in command or "what do you remember" in command:
        if memory:
            say("Here’s what I remember:")
            for k, v in memory.items():
                print(f"- {v}")
                say(v)
        else:
            say("I don’t remember anything yet.")

    elif "forget" in command:
        say("Do you want me to forget everything or something specific?")
        choice = input("You: ").lower()
        if "everything" in choice:
            memory.clear()
            save_memory(memory)
            say("I’ve forgotten everything.")
        else:
            word = choice.split()[-1]
            if word in memory:
                del memory[word]
                save_memory(memory)
                say(f"I forgot about {word}.")
            else:
                say("I didn’t have that in memory.")

    elif "options" in command or "commands" in command:
        show_options()

    elif "exit" in command or "stop" in command or "goodbye" in command:
        say(f"Goodbye {name}")
        break

    else:
        say("Sorry, I do not know that command yet. You can say 'commands' to see all options.")
