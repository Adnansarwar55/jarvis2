import os
import sys
import subprocess

def ensure_package(package, import_name=None):
    """Install a package if missing."""
    try:
        __import__(import_name or package)
    except ImportError:
        print(f"[Setup] Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Essential packages for Jarvis
required_packages = [
    ("pyttsx3", None),
    ("SpeechRecognition", "speech_recognition"),
    ("pygame", None),
    ("keyboard", None),
    ("requests", None),
    ("pywhatkit", None),
    ("openai", None),
    ("psutil", None),
    ("pyautogui", None),
    ("pyjokes", None)
]

for pkg, imp in required_packages:
    ensure_package(pkg, imp)

import pygame
import pyttsx3
import psutil
import pyautogui
import pyjokes
import datetime
import speech_recognition as sr
import os
import pywhatkit
import pygame
import math
import random
import keyboard
import time
import sys
import time as t
import threading
import requests
from openai import OpenAI
import webbrowser

client = OpenAI(api_key="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")  # replace with your key

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
        "14. play music",
        "15. send message",
        "16. weather",
        "17. System Control (shutdown, restart, volume, camera)",
        "18. meaning",
        "19. tell a joke",
        "20. battery status",
        "21. take screenshort",
        "22. open apps(open)",
        "23. Recipe",
        "24. Exit"
    ]
    say("Here are the commands you can use:")
    for option in options:
        print(option)
        say(option)

def open_app(app_name):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe"
    }
    if app_name.lower() in apps:
        os.system(f"start {apps[app_name.lower()]}")
        say(f"Opening {app_name}")
    else:
        say("I don't know this app.")


def run_music_player():
    pygame.mixer.init()

    # Playlist - add your own songs here
    playlist = ["hara.mp3", "rider.mp3", "tere.mp3", "fitor.mp3"]
    volume = 0.5
    pygame.mixer.music.set_volume(volume)
    current_song = 0

    def play_song(index):
        pygame.mixer.music.load(playlist[index])
        pygame.mixer.music.play()
        say(f"Now playing: {playlist[index]}")

    play_song(current_song)

    while True:
        if keyboard.is_pressed("up"):
            volume = min(1.0, volume + 0.05)
            pygame.mixer.music.set_volume(volume)
            say(f"Volume: {int(volume * 100)}%")
            time.sleep(0.2)

        elif keyboard.is_pressed("down"):
            volume = max(0.0, volume - 0.05)
            pygame.mixer.music.set_volume(volume)
            say(f"Volume: {int(volume * 100)}%")
            time.sleep(0.2)

        elif keyboard.is_pressed("n"):  # Next song
            current_song = (current_song + 1) % len(playlist)
            play_song(current_song)
            time.sleep(0.5)

        elif keyboard.is_pressed("p"):  # Previous song
            current_song = (current_song - 1) % len(playlist)
            play_song(current_song)
            time.sleep(0.5)

        elif keyboard.is_pressed("s"):  # Stop
            say("Stopping music...")
            pygame.mixer.music.stop()
            break

        if not pygame.mixer.music.get_busy():
            current_song = (current_song + 1) % len(playlist)
            play_song(current_song)

def google_search(query):
    say(f"Searching Google for {query}")
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)

def Recipe():
    materal = input("Enter your materal: ")
    if materal == "enzyme desizing":
        print("""Recipe:-
              L:R = 1:30
              wetting agent = 2g//L
              Enzyme desizer = 3% O.w.f
              Temperature = 70c
              Time = 1 hour""")
        say("""Recipe:-
              L:R = 1:30
              wetting agent = 2g//L
              Enzyme desizer = 3% O.w.f
              Temperature = 70c
              Time = 1 hour""")
    elif materal == "scouring":
        print("""Recip:-
              L:R = 1:30
              wetting agent = 2g//L
              sequesting agent = 0.1g//L
              NaOH = 1.5% O.w.f
              soda Ash = 0.5% O.w.f
              Temp = 98-100c
              Time = 1hour""")
        say("""Recip:-
              L:R = 1:30
              wetting agent = 2g//L
              sequesting agent = 0.1g//L
              NaOH = 1.5% O.w.f
              soda Ash = 0.5% O.w.f
              Temp = 98-100c
              Time = 1hour""")
    elif materal == "Bleaching":
        print("Bleaching with H2O2")
        print("""Recipe:-
              L:R = 1:30
              wetting agent = 2g//L
              sequesting agent = 0.5g//L
              stablizer = 1.5%
              NaOH = 2%
              H2O2 = 8%
              temp 98-100c
              Time = 1hour""")
        say("H2O2 Bleach Recipe.")
        say("""Recipe:-
              L:R = 1:30
              wetting agent = 2g//L
              sequesting agent = 0.5g//L
              stablizer = 1.5%
              NaOH = 2%
              H2O2 = 8%
              temp 98-100c
              Time = 1hour""")
    elif materal == "Direct dye":
        print("""Recip:-
              L:R = 1:30
              soda Ash = 1g//L
              wetting agent = 1g//L
              sequesting agent = 1g//L
              anticreasing agent = 1g//L
              Direct dye = x%
              comman salt = 15g//L
              Temp = 90c
              Time = 1hour""")
        say("""Recip:-
              L:R = 1:30
              soda Ash = 1g//L
              wetting agent = 1g//L
              sequesting agent = 1g//L
              anticreasing agent = 1g//L
              Direct dye = x%
              comman salt = 15g//L
              Temp = 90c
              Time = 1hour""")
    elif materal == "Reactive dye":
        print("""Recipe:-
              L:R = 1:30
              wetting agent = 2g//L
              sequesting agent = 2g//L
              anticreasing agent = 2g//L
              Reactive dye = x%
              soda Ash = 20g//L
              comman salt = 60g//L
              Temp = 90c
              Time = 1hour""")
        say("""Recipe:-
              L:R = 1:30
              wetting agent = 2g//L
              sequesting agent = 2g//L
              anticreasing agent = 2g//L
              Reactive dye = x%
              soda Ash = 20g//L
              comman salt = 60g//L
              Temp = 90c
              Time = 1hour""")

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

def random_fact():
    facts = [
        "Honey never spoils.",
        "Bananas are berries but strawberries are not.",
        "Octopuses have three hearts."
    ]
    say(random.choice(facts))

def get_weather(city="Karachi"):
    try:
        api_key = "c6817883270c22407d42319bf52b36b7"  # get from openweathermap.org
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        data = requests.get(url).json()
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            say(f"The temperature in {city} is {temp} degrees Celsius with {desc}.")
        else:
            say("Sorry, I couldn't find that city.")
    except Exception as e:
        say(f"Error fetching weather: {e}")

def system_control(action):
    if "shutdown" in action:
        say("Shutting down the system.")
        os.system("shutdown /s /t 5")
    elif "restart" in action:
        say("Restarting the system.")
        os.system("shutdown /r /t 5")
    elif "volume up" in action:
        keyboard.press_and_release("volume up")
        say("Volume increased.")
    elif "volume down" in action:
        keyboard.press_and_release("volume down")
        say("Volume decreased.")
    elif "camera" in action:
        say("Opening camera.")
        os.system("start microsoft.windows.camera:")

def get_meaning(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        res = requests.get(url).json()
        meaning = res[0]["meanings"][0]["definitions"][0]["definition"]
        say(f"The meaning of {word} is: {meaning}")
    except:
        say("Sorry, I couldn't find that word.")

def tell_joke():
    joke = pyjokes.get_joke()
    say(joke)

def battery_status():
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        plugged = "plugged in" if battery.power_plugged else "not plugged in"
        say(f"Battery is at {percent} percent and it is {plugged}.")
    else:
        say("Battery status not available.")

def take_screenshot():
    say("Taking a screenshot.")
    file_name = f"screenshot_{int(time.time())}.png"
    pyautogui.screenshot(file_name)
    say(f"Screenshot saved as {file_name}.")

def open_website(name):
    websites = {
        "youtube": "https://youtube.com",
        "facebook": "https://facebook.com",
        "instagram": "https://instagram.com",
        "twitter": "https://twitter.com",
        "github": "https://github.com",
        "google": "https://google.com"
    }
    if name in websites:
        say(f"Opening {name}")
        webbrowser.open(websites[name])
    else:
        say("Website not found in my list.")

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

    elif "open" in command:
        say("Which application?")
        app = input("You: ")
        open_app(app)

    elif "fact" in command:
        random_fact()
    
    elif "weather" in command:
        say("Which city's weather do you want to know?")
        city = input("City: ")
        get_weather(city)

    elif "shutdown" in command or "restart" in command or "volume" in command or "camera" in command:
        system_control(command)

    elif "meaning" in command:
        say("Which word should I define?")
        word = input("Word: ")
        get_meaning(word)

    elif "joke" in command:
        tell_joke()

    elif "battery" in command:
        battery_status()

    elif "screenshot" in command:
        take_screenshot()

    elif "website" in command:
        say("Which website do you want to open?")
        name = input("Website name: ").lower()
        open_website(name)

    elif "send whatsapp message" in command or "send message" in command:
        say("Please enter the phone number with country code, for example +923211234567")
        phone = input("Phone number: ")
        say("What message should I send?")
        message = input("Message: ")

        say(f"Sending your message to {phone}")
        try:
            pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=10, tab_close=True)
            say("Message sent successfully.")
        except Exception as e:
            say(f"Sorry, I couldn't send the message. Error: {e}")

    elif "play music" in command or "music" in command:
        say("Launching music player...")
        threading.Thread(target=run_music_player, daemon=True).start()
    
    elif "Recipe" in command:
        say("Enter your Recipes.")

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
