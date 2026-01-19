import turtle
import time
import random
import pygame
import os

intro_sound = None

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Global var
delay = 0.1
score = 0
high_score = 0

def show_intro_screen():

    global intro_sound

    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_dir = os.path.join(script_dir, "Resources")

    try:
        intro_sound = pygame.mixer.Sound(os.path.join(audio_dir, "snake-kodedev-intro.ogg"))
        intro_sound.set_volume(1)
        intro_sound.play()
    except:
        print("Intro sound not found, continuing without it...")

    intro_screen = turtle.Screen()
    intro_screen.setup(650, 650)
    intro_screen.bgcolor('black')
    intro_screen.title('S N A K E - Intro')
    
    intro_text = turtle.Turtle()
    intro_text.speed(0)
    intro_text.color('yellow')
    intro_text.penup()
    intro_text.hideturtle()
    
    # Main title
    intro_text.goto(0, 280)
    intro_text.write("─────  S N A K E  ɴᴇᴏ ʀᴇᴍɪx  ─────", 
                     align="center", font=("Courier", 18, "bold"))
    
    # Intro header
    snake_art = [
        "███████╗███╗   ██╗ █████╗ ██╗  ██╗███████╗",
        "██╔════╝████╗  ██║██╔══██╗██║ ██╔╝██╔════╝", 
        "███████╗██╔██╗ ██║███████║█████╔╝ █████╗  ",
        "╚════██║██║╚██╗██║██╔══██║██╔═██╗ ██╔══╝  ",
        "███████║██║ ╚████║██║  ██║██║  ██╗███████╗",
        "╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝"
    ]
    
    y_pos = 230 
    for line in snake_art:
        intro_text.goto(0, y_pos)
        intro_text.write(line, align="center", font=("Courier", 8, "bold"))
        y_pos -= 15 
    
    # Author info
    intro_text.goto(0, 140)
    intro_text.write("Author: KodeDev | Github: KodeDevHub", align="center", font=("Courier", 12, "normal"))

    # Descr info
    intro_text.goto(0, 110)
    intro_text.write("Classic snake arcade - Eat fruit, avoid walls", 
                     align="center", font=("Courier", 10, "normal"))
    
    # Controls text
    intro_text.goto(0, 80)
    intro_text.write("↑ ↓ ← →  Move | P Pause | ESC Exit", 
                     align="center", font=("Courier", 10, "bold"))
    
    # Press ENTER text
    intro_text.goto(0, 10)
    intro_text.color('lime')
    intro_text.write("PRESS ENTER TO START", 
                     align="center", font=("Courier", 16, "bold"))


    intro_text.goto(0, -80)
    intro_text.write("Email: KodeDev@protonmail.com", align="center", font=("Courier", 12, "normal"))

    intro_text.goto(0, -110)
    intro_text.write("Special thanks to my beloved Paloma", align="center", font=("Courier", 12, "normal"))
    
    def start_game():
        if intro_sound:
            intro_sound.stop()
        intro_screen.clear()
        turtle.clearscreen() 
        main_game()
    
    intro_screen.listen()
    intro_screen.onkeypress(start_game, "Return")
    intro_screen.mainloop()

def main_game():
    global score, high_score  # Modify global var

    current_delay = 0.1
    
    # Audio config
    pygame.mixer.set_num_channels(16)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_dir = os.path.join(script_dir, "Resources")

    pygame.mixer.music.load(os.path.join(audio_dir, "snake-kodedev-8-bit.ogg"))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    move_sound = pygame.mixer.Sound(os.path.join(audio_dir, "Move.wav"))
    eat_sound = pygame.mixer.Sound(os.path.join(audio_dir, "Eat.wav"))
    kick_sound = pygame.mixer.Sound(os.path.join(audio_dir, "Kick.wav"))

    # Restart score
    score = 0

    # Screen config
    s = turtle.Screen()
    s.setup(650, 650)
    s.bgcolor('black')
    s.title('S N A K E  ɴᴇᴏ ʀᴇᴍɪx')

    # Game status   
    game_paused = False
    game_running = True

    # Border config
    border = turtle.Turtle()
    border.speed(0)
    border.color('yellow')
    border.penup()
    border.goto(-250, 250)
    border.pendown()
    border.pensize(3)

    for _ in range(4):
        border.forward(500)
        border.right(90)

    border.hideturtle()

    # Markdown config
    text = turtle.Turtle()
    text.speed(0)
    text.color('yellow')
    text.penup()
    text.hideturtle()
    text.goto(0, 260)
    text.write(f"Score: {score} | High score: {high_score}", 
               align="center", font=("verdana", 24, "normal"))

    # Snake config
    snake = turtle.Turtle()
    snake.speed(1)
    snake.shape('square')
    snake.penup()
    snake.goto(0, 0)
    snake.direction = 'stop'
    snake.color('green')

    # Meal config
    meal = turtle.Turtle()
    meal.shape('circle')
    meal.color('orange')
    meal.penup()
    meal.goto(0, 100)
    meal.speed(0)

    # Movement functions
    def move_up():
        if snake.direction != 'down':  # Prevents reverse movement
            snake.direction = 'up'

    def move_down():
        if snake.direction != 'up':
            snake.direction = 'down'

    def move_right():
        if snake.direction != 'left':
            snake.direction = 'right'

    def move_left():
        if snake.direction != 'right':
            snake.direction = 'left'

    def movement():
        if snake.direction != 'stop':
            move_sound.play()
        if snake.direction == 'up':
            y = snake.ycor()
            snake.sety(y + 20)
        if snake.direction == 'down':
            y = snake.ycor()
            snake.sety(y - 20)
        if snake.direction == 'right':
            x = snake.xcor()
            snake.setx(x + 20)
        if snake.direction == 'left':
            x = snake.xcor()
            snake.setx(x - 20)

    def toggle_pause():
        nonlocal game_paused
        game_paused = not game_paused
        if game_paused:
            pygame.mixer.music.pause()
            # Pause text
            if not hasattr(toggle_pause, 'pause_text'):
                pause_text = turtle.Turtle()
                pause_text.speed(0)
                pause_text.color('red')
                pause_text.penup()
                pause_text.hideturtle()
                toggle_pause.pause_text = pause_text
            toggle_pause.pause_text.goto(0, 0)
            toggle_pause.pause_text.write("PAUSED\nPress P to resume", 
                        align="center", font=("Arial", 24, "bold"))
        else:
            pygame.mixer.music.unpause()
            # Clean pause text
            if hasattr(toggle_pause, 'pause_text'):
                toggle_pause.pause_text.clear()
    
    def exit_game():
        nonlocal game_running
        game_running = False
        # Try to close any open turtle screens
        try:
            turtle.bye()
        except:
            pass
        try:
            s.bye()
        except:
            pass

    # Keyboard config
    s.listen()
    s.onkeypress(move_up, "Up")
    s.onkeypress(move_down, "Down")
    s.onkeypress(move_right, "Right")
    s.onkeypress(move_left, "Left")
    s.onkeypress(toggle_pause, "p")
    s.onkeypress(toggle_pause, "P")
    s.onkeypress(exit_game, "Escape")
    
    body = []

    # Main game logic
    while game_running:
        s.update()
        if not game_paused:
            movement()
            time.sleep(current_delay)

            # Eat meal
            if snake.distance(meal) < 20:
                x = random.randint(-230, 230)
                y = random.randint(-230, 230)
                eat_sound.play()
                meal.goto(x, y)

                new_part = turtle.Turtle()
                new_part.shape('square')
                new_part.color('green')
                new_part.penup()
                new_part.goto(0, 0)
                new_part.speed(0)
                body.append(new_part)

                score += 10
                text.clear()

                if score > high_score:
                    high_score = score
                text.write(f"Score: {score} | High score: {high_score}", 
                        align="center", font=("verdana", 24, "normal"))
                
                if score >= 100: #Difficulty speed increase
                    speed_boost = min(0.03, (score // 200) * 0.01)  # Every 200 points
                    current_delay = max(0.06, 0.1 - speed_boost)  # Min 0.06
                    
                    # Anim
                    anim_speed = min(6, 1 + (score // 500))  # Every 500 points
                    snake.speed(anim_speed)

                if score >= 5000:  # 5,000 points to win
                    win_game()
                    return

            # Move snake's body
            total_body = len(body)

            for i in range(total_body - 1, 0, -1):
                x = body[i-1].xcor()
                y = body[i-1].ycor()
                body[i].goto(x, y)
                
            if total_body > 0:
                x = snake.xcor()
                y = snake.ycor()
                body[0].goto(x, y)

            # Border collide
            game_area_top = 250
            game_area_bottom = -250
            game_area_left = -250
            game_area_right = 250
            offset = 10
            
            if (snake.xcor() > game_area_right - offset or 
                snake.xcor() < game_area_left + offset or 
                snake.ycor() > game_area_top - offset or 
                snake.ycor() < game_area_bottom + offset):
                
                kick_sound.play()
                score = 0
                text.clear()
                text.write(f"Score: {score} | High score: {high_score}", 
                        align="center", font=("verdana", 24, "normal"))
                time.sleep(2)
                
                for segment in body:
                    segment.hideturtle()
                snake.goto(0, 0)
                snake.direction = 'stop'
                body.clear()

            # Self collision logic
            for i in range(1, len(body)):
                if body[i].distance(snake) < 20:
                    kick_sound.play()
                    score = 0
                    text.clear()
                    text.write(f"Score: {score} | High score: {high_score}", 
                            align="center", font=("verdana", 24, "normal"))
                    time.sleep(2)
                    
                    for segment in body:
                        segment.hideturtle()
                    snake.goto(0, 0)
                    snake.direction = 'stop'
                    body.clear()
                    break
        else:
            # Pause
            time.sleep(0.1)
    # game_running False
    pygame.mixer.music.stop()
    turtle.bye()

#Win logic
def win_game():

    pygame.mixer.music.stop()
        
    # New win screeen
    win_screen = turtle.Screen()
    win_screen.setup(650, 650)
    win_screen.bgcolor('black')
    win_screen.title('S N A K E - Victory!')
        
    # Victory text
    win_text = turtle.Turtle()
    win_text.speed(0)
    win_text.color('gold')
    win_text.penup()
    win_text.hideturtle()
        
    # Main Msj
    win_text.goto(0, 100)
    win_text.write("YOU WIN!", align="center", font=("Arial", 72, "bold"))
        
    # Score
    win_text.goto(0, 0)
    win_text.write(f"Score: {score}", align="center", font=("Arial", 36, "normal"))
        
    # High score
    win_text.goto(0, -50)
    win_text.write(f"High Score: {high_score}", align="center", font=("Arial", 28, "normal"))
        
    # Instructions
    win_text.goto(0, -150)
    win_text.color('lime')
    win_text.write("Press ENTER to continue", align="center", font=("Arial", 24, "bold"))
        
    # Continue
    def continue_to_menu():
        win_screen.clear()
        turtle.clearscreen()
        show_intro_screen()
        
    # Control config
    win_screen.listen()
    win_screen.onkeypress(continue_to_menu, "Return")
        
    # Keep window open
    win_screen.mainloop()

if __name__ == "__main__":
    show_intro_screen()




