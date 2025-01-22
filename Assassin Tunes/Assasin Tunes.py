import sys
from tkinter import filedialog
import tkinter as tk
import pygame
from pynput.keyboard import Key
from pynput.keyboard import Listener
import os

pygame.init()

stop_flag = False
pause_flag = False
current_index = 0  # Index to track the current playing song

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Assassin Tunes")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 139)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 24)


# Store song name
current_song = ""
selected_files = []


# Access Files
def browse_file():
    global stop_flag, pause_flag, current_song, selected_files, current_index
    root = tk.Tk()
    root.withdraw()
    filenames = filedialog.askopenfilenames(filetypes=[("MP3 Files", ".mp3")])
    if filenames:
        selected_files = filenames
        current_index = 0  # Reset to the first song
        current_song = selected_files[current_index].split("/")[-1]
        print(f"Selected files: {selected_files}")


# Stop music
def stop_music():
    global stop_flag, pause_flag
    if stop_flag:
        pygame.mixer.music.stop()
        stop_flag = False
        pause_flag = False
        print("Stopped")


# Play music or resume if paused
def play_button_clicked(key):
    global stop_flag, pause_flag, current_song
    if selected_files:
        if not stop_flag:
            pygame.mixer.music.load(selected_files[current_index])
            pygame.mixer.music.play()
            current_song = selected_files[current_index].split("/")[-1]
            stop_flag = True
            print(f"Playing: {current_song}")
        elif pause_flag:
            pygame.mixer.music.unpause()
            print("Resumed")
        pause_flag = False

# Preload songs from a specific folder
def preload_songs(folder_path):
    global selected_files, current_song, current_index
    if os.path.exists(folder_path):
        selected_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.mp3')]
        if selected_files:
            current_index = 0  # Reset to the first song
            current_song = selected_files[current_index].split("/")[-1]
            print(f"Preloaded files: {selected_files}")
        else:
            print(f"No .mp3 files found in {folder_path}")
    else:
        print(f"Folder path {folder_path} does not exist.")


# Pause music
def pause_button_clicked(key):
    global pause_flag
    if not pause_flag and stop_flag:
        pygame.mixer.music.pause()
        pause_flag = True
        print("Paused")


# Play the next song
def next_button_clicked():
    global current_index, current_song, stop_flag
    if selected_files and current_index < len(selected_files) - 1:
        current_index += 1
        pygame.mixer.music.load(selected_files[current_index])
        pygame.mixer.music.play()
        current_song = selected_files[current_index].split("/")[-1]
        stop_flag = True
        print(f"Playing: {current_song}")


# Play the previous song
def previous_button_clicked():
    global current_index, current_song, stop_flag
    if selected_files and current_index > 0:
        current_index -= 1
        pygame.mixer.music.load(selected_files[current_index])
        pygame.mixer.music.play()
        current_song = selected_files[current_index].split("/")[-1]
        stop_flag = True
        print(f"Playing: {current_song}")

#Preload songs
preload_songs("C://Users//Fajr//Downloads//parental control//MusicAPP//music")

# Buttons setup
button_color = BLUE
button_hover_color = DARK_BLUE
button_width = 75
button_height = 30

# Adjust positions for centering
song_display_rect = pygame.Rect((SCREEN_WIDTH - 600) // 2, 50, 600, 50)
file_list_rect = pygame.Rect((SCREEN_WIDTH - 600) // 2, 120, 600, 250)

# Button positions horizontally under the playlist box
button_x_start = (SCREEN_WIDTH - (button_width * 6 + 50)) // 2
button_file_rect = pygame.Rect(button_x_start, 400, button_width, button_height)
button_stop_rect = pygame.Rect(button_x_start + button_width + 10, 400, button_width, button_height)
button_play_rect = pygame.Rect(button_x_start + 2 * (button_width + 10), 400, button_width, button_height)
button_pause_rect = pygame.Rect(button_x_start + 3 * (button_width + 10), 400, button_width, button_height)
button_next_rect = pygame.Rect(button_x_start + 4 * (button_width + 10), 400, button_width, button_height)
button_previous_rect = pygame.Rect(button_x_start + 5 * (button_width + 10), 400, button_width, button_height)

button_file_text = "FILE"
button_stop_text = "STOP"
button_play_text = "PLAY"
button_pause_text = "PAUSE"
button_next_text = "NEXT"
button_previous_text = "PREV"


# Function to render a button
def render_button(screen, rect, color, text):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2,
                               rect.y + (rect.height - text_surface.get_height()) // 2))


# Function to render song name display
def render_song_name(screen, song_name):
    pygame.draw.rect(screen, BLACK, song_display_rect, border_radius=10)
    song_text_surface = small_font.render(f"Now Playing: {song_name}", True, WHITE)
    screen.blit(song_text_surface, (song_display_rect.x + (song_display_rect.width - song_text_surface.get_width()) // 2,
                                    song_display_rect.y + (song_display_rect.height - song_text_surface.get_height()) // 2))


# Function to render the selected files list
def render_selected_files(screen, files):
    pygame.draw.rect(screen, BLACK, file_list_rect, border_radius=10)
    y_offset = 10
    for file in files:
        file_text_surface = small_font.render(file.split("/")[-1], True, WHITE)
        screen.blit(file_text_surface, (file_list_rect.x + 10, file_list_rect.y + y_offset))
        y_offset += 30



preload_songs("C://Users//Fajr//Downloads//parental control//MusicAPP//music")
# Main loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_file_rect.collidepoint(event.pos):
                browse_file()
            elif button_stop_rect.collidepoint(event.pos):
                stop_music()
            elif button_play_rect.collidepoint(event.pos):
                play_button_clicked(None)
            elif button_pause_rect.collidepoint(event.pos):
                pause_button_clicked(None)
            elif button_next_rect.collidepoint(event.pos):
                next_button_clicked()
            elif button_previous_rect.collidepoint(event.pos):
                previous_button_clicked()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pause_flag:
                    play_button_clicked(None)  # Resume playing
                else:
                    pause_button_clicked(None)  # Pause music

    # Mouse hover detection
    mouse_pos = pygame.mouse.get_pos()
    button_file_color = button_hover_color if button_file_rect.collidepoint(mouse_pos) else button_color
    button_stop_color = button_hover_color if button_stop_rect.collidepoint(mouse_pos) else button_color
    button_play_color = button_hover_color if button_play_rect.collidepoint(mouse_pos) else button_color
    button_pause_color = button_hover_color if button_pause_rect.collidepoint(mouse_pos) else button_color
    button_next_color = button_hover_color if button_next_rect.collidepoint(mouse_pos) else button_color
    button_previous_color = button_hover_color if button_previous_rect.collidepoint(mouse_pos) else button_color

    # Drawing
    screen.fill("light blue")
    render_button(screen, button_file_rect, button_file_color, button_file_text)
    render_button(screen, button_stop_rect, button_stop_color, button_stop_text)
    render_button(screen, button_play_rect, button_play_color, button_play_text)
    render_button(screen, button_pause_rect, button_pause_color, button_pause_text)
    render_button(screen, button_next_rect, button_next_color, button_next_text)
    render_button(screen, button_previous_rect, button_previous_color, button_previous_text)

    # Render song name display
    render_song_name(screen, current_song if current_song else "No song playing")

    # Render selected files list
    render_selected_files(screen, selected_files)

    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()

