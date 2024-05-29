import pygame, sys
import random
import time
import nltk
nltk.download('words')

pygame.init()
WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Bapacu Kato')
clock = pygame.time.Clock()
fps = 60
background = pygame.image.load("layangancanva.png")
background = pygame.transform.scale(background, (200, 120))
start_ticks = pygame.time.get_ticks()



# Font and sound loading


pygame.mixer.init()

#font
font = pygame.font.Font('assets/fonts/Cheri-drog.ttf', 36)
fonthelp = pygame.font.Font('assets/fonts/Cheri-drog.ttf', 24)

#sound
smemeu = pygame.mixer.music.load('assets/sounds/backsound bapacukato.mp3')
pygame.mixer.music.set_volume(0.9)
pygame.mixer.music.play(-1)
langkahkaki = pygame.mixer.Sound('assets/sounds/wood-creak-single-v2-97096 (1).mp3')
petir = pygame.mixer.Sound('assets/sounds/suara petir.mp3')
bite = pygame.mixer.Sound('assets/sounds/Swoosh.mp3')
splash = pygame.mixer.Sound('assets/sounds/click.mp3')
kalah = pygame.mixer.Sound('assets/sounds/kalah.mp3')
awas = pygame.mixer.Sound('assets/sounds/awas asli.mp3')
lose = pygame.mixer.Sound('assets/sounds/Instrument Strum.mp3')
dorslam = pygame.mixer.Sound('assets/sounds/Door slam 🚪 (mp3cut.net).mp3')
chilplay = pygame.mixer.Sound('assets/sounds/kids-in-classroom-6187.mp3')
bite.set_volume(0.3)
dorslam.set_volume(1.2)
splash.set_volume(0.2)
kalah.set_volume(0.8)
awas.set_volume(0.2)
lose.set_volume(0.3)

# Game variables
score = 0
lives = 5
word_speed = 2
word_delay = 2
word_list = []
letters = 'abcdefghijklmnopqrstuvwxyz'
timer = 30
paused = False
selected_color = (255, 0, 0)  # Default font color
highscore = 0

#background
gambar = pygame.transform.scale(pygame.image.load("img/bg/LOGO3.png"), (WIDTH, HEIGHT))
bghelp = pygame.transform.scale(pygame.image.load("img/bg/bghelp.jpg"), (WIDTH, HEIGHT))
logo = pygame.transform.scale(pygame.image.load("img/bg/Untitled_design__2_-removebg (1).png"), (400, 200))
bg3 = pygame.transform.scale(pygame.image.load("img/bg/bg2.5.jpg"), (WIDTH, HEIGHT))
bg2 = pygame.transform.scale(pygame.image.load("img/bg/bg random.2.png"), (WIDTH, HEIGHT))
bgsetting = pygame.transform.scale(pygame.image.load("img/bg/WOIII AWASS KANAI RUMAH DENNN.jpg"), (WIDTH, HEIGHT))


# Load highscore from file
def load_highscore():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Write highscore to file
def write_highscore(score):
    with open("highscore.txt", "w") as file:
        print(score)
        file.write(str(score))

# Background images
backgrounds = [
    pygame.transform.scale(pygame.image.load("img/bg/1.jpg"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("img/bg/2.jpg"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("img/bg/3.jpg"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("img/bg/4.jpg"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("img/bg/5.jpg"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("img/bg/6.jpg"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("img/bg/7.5.jpg"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("img/bg/7.jpg"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("img/bg/8.jpg"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("img/bg/9.jpg"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("img/bg/11.5.jpg"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("img/bg/10.jpg"), (WIDTH, HEIGHT)),
    # Add more background images as needed
]
#lives heart
lives1 = pygame.transform.scale(pygame.image.load("img/hati/1hati-removebg-preview.png"), (180, 55))
lives2 = pygame.transform.scale(pygame.image.load("img/hati/2hati-removebg-preview.png"), (180, 55))
lives3 = pygame.transform.scale(pygame.image.load("img/hati/3hati-removebg-preview.png"), (180, 55))
lives4 = pygame.transform.scale(pygame.image.load("img/hati/4hati-removebg-preview.png"), (180, 55))
lives5 = pygame.transform.scale(pygame.image.load("img/hati/5hati-removebg-preview.png"), (180, 55))
current_background = 0

#perubahan marah
marah = pygame.transform.scale(pygame.image.load("marah.png"), (100, 100))
ngintip = pygame.transform.scale(pygame.image.load("ngintip.png"), (38, 38))

# Function to draw background
def draw_background(index):
    screen.blit(backgrounds[index], (0, 0))

# Class definitions

class GameObject:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._color = color

    def draw(self):
        pass  # Abstract method

    def update(self):
        pass  # Abstract method

class Word(GameObject): #turunan gameobject
    def __init__(self, text, speed, x, y):
        super().__init__(x, y, 50, 50, 'black')  # Use appropriate width and height based on font size
        self.text = text
        self.speed = speed

    def draw(self):
        screen.blit(background, (self.x-60, self.y-30))
        screen.blit(fonthelp.render(self.text, True, selected_color), (self.x, self.y))
        act_len = len(game.active_string)
        if game.active_string == self.text[:act_len]:
            screen.blit(fonthelp.render(game.active_string, True, 'green'), (self.x, self.y))

    def update(self):
        if not paused:
            self.x -= self.speed

class BapacuKato:
    def __init__(self):
        self.active_string = ''
        self.score = 0
        self.lives = 5
        self.word_speed = 1
        self.word_delay = 3
        self.word_timer = 0
        self.random_number = random.randint(0, 100)
        self.salah = False

    def generate_word(self):
        word_text = random.choice([word.lower() for word in nltk.corpus.words.words() if len(word) <= 6])
        word_speed = self.word_speed + self.score // 5
        word_y = random.randint(70, HEIGHT - 200)
        word = Word(word_text, word_speed, WIDTH, word_y)
        word_list.append(word)

    def handle_input(self, event):
        global selected_color,highscore
        if event.type == pygame.KEYDOWN:

            if not paused:
                splash.play()
                if event.key == pygame.K_BACKSPACE:
                    self.active_string = self.active_string[:-1]
                elif event.key == pygame.K_RETURN:
                    for word in word_list:
                        if self.active_string == word.text:
                            word_list.remove(word)
                            self.active_string = ''
                            self.score += 1
                            if self.score > highscore:
                                scorebaru = self.score
                                write_highscore(scorebaru)
                            bite.play()
                            return
                    # Clear input when Enter is pressed
                    self.active_string = ''
                elif event.unicode.isalpha():
                    self.active_string += event.unicode
            if event.key == pygame.K_SPACE:
                toggle_pause()
        elif event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if 0 <= event.pos[0] <= WIDTH and 0 <= event.pos[1] <= WIDTH:  # Change color button
                    selected_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self):
        global start_ticks
        if not paused:
            if self.word_timer <= 0:
                self.generate_word()
                self.word_timer = self.word_delay * fps
            else:
                self.word_timer -= 1

            for word in word_list:
                word.update()
                if word.x + word.width < 0:
                    word_list.remove(word)
                    self.lives -= 1
                    start_ticks = 0
                    self.salah = True
                    start_ticks = pygame.time.get_ticks()
                    lose.play()
                    dorslam.play()
                    if self.lives <= 0:
                        kalah.play()  # Stop game when lives reach 0 or less
                        game_over()

    def draw(self):
        global lives1, lives2, lives3, lives4, lives5, start_ticks
        elapsed_ticks = pygame.time.get_ticks() - start_ticks# Stop game when
        pygame.mixer.music.set_volume(0.3)
        if self.random_number % 2 == 0:
            screen.blit(bg3, (0, 0))
        else:
            screen.blit(bg2, (0, 0))
        pygame.draw.rect(screen, "azure3", [250, HEIGHT-70, WIDTH, 70], 0)
        pygame.draw.rect(screen, 'white', [0, 0, WIDTH, HEIGHT], 5)
        pygame.draw.line(screen, 'white', (250, HEIGHT - 70), (WIDTH, HEIGHT - 70), 2)
        pygame.draw.rect(screen, 'black', [0, 0, WIDTH, HEIGHT], 2)
        for word in word_list:
            word.draw()
        score_text = fonthelp.render("Score: " + str(self.score), True, (210, 180, 140))
        screen.blit(score_text, (882, 50))
        lives_text = font.render("", True, (0, 0, 0))
        screen.blit(lives_text, (20, 10))
        input_text = font.render("Input: " + self.active_string, True, (0, 0, 0))
        screen.blit(input_text, (270,545))
        highscore_text = fonthelp.render("Highscore: " + str(highscore), True, (210, 180, 140))
        screen.blit(highscore_text, (830, 10))
        if self.salah == False:
            screen.blit(ngintip, (192,538))
        else:
            screen.blit(marah, (127, 500))
            if elapsed_ticks > 1500:
                self.salah = False
            

        if self.lives == 5:
            screen.blit(lives5, (15, 13))
        if self.lives == 4:
            screen.blit(lives4, (15, 13))
        if self.lives == 3:
            screen.blit(lives3, (15, 13))
        if self.lives == 2:
            screen.blit(lives2, (15, 13))
        if self.lives == 1:
            screen.blit(lives1, (15, 13))
        if paused:
            pause_text = font.render("Paused", True, (255, 0, 0))
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
            pygame.draw.rect(screen, selected_color, (372.5, 360, 250, 50))  # Change color button
            change_color_text = font.render("ganti warna", True, (0, 0, 0))
            screen.blit(change_color_text, (445 + (100 - change_color_text.get_width()) // 2, 380 + (20 - change_color_text.get_height()) // 2))
        
    def run(self):
        global paused
        running = True
        while running:
            clock.tick(fps)
            for event in pygame.event.get():
                self.handle_input(event)

            self.update()
            self.draw()

            pygame.display.flip()

            # Check if the game should stop
            if self.lives <= 0:
                running = False

def game_over():
    global running, word_list, score, lives, highscore  # Menyimpan highscore baru ke file teks

    word_list = []  # Mengosongkan daftar kata
    running = False 
    
    # Memeriksa jika skor saat ini melebihi highscore yang tersimpan
    score = 0  # Mereset nilai skor
    lives = 3  # Mereset jumlah nyawa


def toggle_pause():
    global paused
    paused = not paused

def main_menu():
    
    menu_font = pygame.font.Font('assets/fonts/GamepauseddemoRegular-RpmY6.otf', 36)
    menu_items = ['Start Game', 'Settings', 'Help', 'Quit']  # Tambahkan 'Settings' di sini
    selected = 0
    pygame.mixer.music.set_volume(0.9)

    while True:
        screen.blit(gambar, (0,0))

        for i, item in enumerate(menu_items):
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            text = menu_font.render(item, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 250 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        return 'start'
                    elif selected == 1:  # Jika 'Settings' dipilih, return 'settings'
                        return 'settings'
                    elif selected == 2:
                        show_help()
                    elif selected == 3:
                        pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Penanganan event untuk klik mouse
                if event.button == 1:  # Left mouse button
                    if 300 <= event.pos[0] <= 500 and 300 <= event.pos[1] <= 350:  # Start button
                        return 'start'
                    elif 300 <= event.pos[0] <= 500 and 350 <= event.pos[1] <= 400:  # Settings button
                        return 'settings'
                    elif 300 <= event.pos[0] <= 500 and 400 <= event.pos[1] <= 450:  # Help button
                        show_help()
                    elif 300 <= event.pos[0] <= 500 and 450 <= event.pos[1] <= 500:  # Quit button
                        pygame.quit()

def show_settings():
    running = True
    selected_option = 0
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    volume_button_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    volume_text_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    while running:
        screen.blit(bgsetting, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:  # Back to menu
                    return
                elif event.key == pygame.K_UP:
                    selected_option = 0
                elif event.key == pygame.K_DOWN:
                    selected_option = 0
                elif event.key == pygame.K_LEFT and selected_option == 0:  # Volume option
                    pygame.mixer.music.set_volume(max(0, pygame.mixer.music.get_volume() - 0.1))
                elif event.key == pygame.K_RIGHT and selected_option == 0:  # Volume option
                    pygame.mixer.music.set_volume(min(1, pygame.mixer.music.get_volume() + 0.1))
                elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    selected_option = (selected_option + 1) % 2

        # Draw Setting text
        setting_text = font.render("Setting", True, BLACK)
        jumlahvolum = font.render("" + str(int(pygame.mixer.music.get_volume()*100)) , True, BLACK)
        text_rect = jumlahvolum.get_rect(center=((WIDTH // 2)-13,270))
        screen.blit(jumlahvolum, text_rect)

        # Draw volume options
        volume_text = font.render("Volume", True, volume_text_color)
        volume_text_width = volume_text.get_width()
        volume_text_height = volume_text.get_height()
        volume_button_width = 200
        volume_button_height = 50
        volume_button_x = WIDTH // 2 - volume_button_width // 2
        volume_button_y = 250

        pygame.display.flip()
        clock.tick(60)

def show_help():
    screen.blit(bghelp, (0,0))
    help_text = [
        "HELP",
        " ",
        "Panduan Permainan",
        " "]
    panduan_text =[
        "1. Ketika layang-layang berisi kata muncul di layar,","   perhatikan kata-kata yang terdapat di dalamnya.",
        "2. Ketika layang-layang berisi kata muncul di layar,","   perhatikan kata-kata yang terdapat di dalamnya.",
        "3. Tekan tombol Enter setelah mengetik sebuah kata","   untuk mengirimkannya.",
        "4. Gunakan tombol Backspace ","   untuk memperbaiki kesalahan saat mengetik",
        "5. Anda akan kehilangan satu nyawa ","   jika sebuah kata mencapai sisi kiri layar.",
        "6. Permainan berakhir saat nyawa Anda habis.",
        "7. Tekan tombol apa pun untuk","   kembali ke menu utama."   ]

    while True:
        #screen.fill((255, 255, 255))
        #for i, line in enumerate(help_text):
        #   text = fonthelp.render(line, True, (0, 0, 0))
        #   text_rect = text.get_rect(center=(WIDTH // 2, 50 + i * 30))
        #   screen.blit(text, text_rect)
        
        #for i, line in enumerate(panduan_text):
        #    text = fonthelp.render(line, True, (0, 0, 0))
        #   text_rect = (200, 50 + (i+4) * 30)
        #    screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                return

if __name__ == "__main__":
    while True:
        
        pygame.draw.rect(screen, 'white', [0, 0, WIDTH, HEIGHT], 5)
        pygame.draw.line(screen, 'white', (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)
        pygame.draw.rect(screen, 'black', [0, 0, WIDTH, HEIGHT], 2)
        if current_background < len(backgrounds):
            draw_background(current_background)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if current_background < 5:
                            langkahkaki.play()
                        if current_background == 7:
                            petir.play()
                        if current_background == 8:
                            chilplay.play()
                        if current_background == 10:
                            awas.play()

                        current_background += 1
            pygame.display.flip() # Delay between background changes
        else:
            highscore = load_highscore()
            choice = main_menu()
            if choice == 'start':
                game = BapacuKato()
                game.run()
            elif choice == 'settings':  # Tambahkan penanganan pilihan 'settings'
                show_settings()
            else:
                break
