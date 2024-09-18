import pygame
from pygame import *
import random
import time

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
res = (720, 720)
screen = pygame.display.set_mode(res)

# Charger les images
fond = pygame.image.load('overwatch2_background.png')
fond = fond.convert()
character_image = pygame.image.load('character.png')
character_image = pygame.transform.scale(character_image, (70, 70))  # Agrandir le personnage
question_image = pygame.image.load('question_mark.png')
question_image = pygame.transform.scale(question_image, (50, 50))  # Agrandir les points d'interrogation
golden_question_image = pygame.image.load('golden_question_mark.png')
golden_question_image = pygame.transform.scale(golden_question_image, (50, 50))  # Agrandir les points d'interrogation dorés
bomb_image = pygame.image.load('bomb.png')
bomb_image = pygame.transform.scale(bomb_image, (50, 50))  # Agrandir les bombes
explosion_image = pygame.image.load('explosion.png')
explosion_image = pygame.transform.scale(explosion_image, (70, 70))  # Agrandir l'explosion
bonus_time_image = pygame.image.load('bonus_timer.png')
bonus_time_image = pygame.transform.scale(bonus_time_image, (50, 50))  # Agrandir les bonus de temps
speed_boost_image = pygame.image.load('speed_boost.png')  # Charger l'image du bonus de vitesse
speed_boost_image = pygame.transform.scale(speed_boost_image, (50, 50))  # Agrandir le bonus de vitesse
boss_image = pygame.image.load('boss.png')  # Charger l'image du boss
boss_image = pygame.transform.scale(boss_image, (100, 100))  # Agrandir le boss
attack_image = pygame.image.load('attack.png')  # Charger l'image des boules d'attaque
attack_image = pygame.transform.scale(attack_image, (30, 30))  # Agrandir les boules d'attaque

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

# Configuration de la police et du texte
smallfont = pygame.font.SysFont('Corbel', 25)
play_text = smallfont.render('Jouer', True, WHITE)
quit_text = smallfont.render('Quitter', True, WHITE)
score_font = pygame.font.SysFont('Corbel', 30)
timer_font = pygame.font.SysFont('Corbel', 50)
life_font = pygame.font.SysFont('Corbel', 25)

# Dimensions et position des boutons
button_width = 260
button_height = 40
button_x = (res[0] - button_width) / 2
play_button_y = (res[1] - button_height) / 2
quit_button_y = play_button_y + button_height + 10

# Calcul des coordonnées pour centrer le texte dans les boutons
play_text_x = button_x + (button_width - play_text.get_width()) / 2
play_text_y = play_button_y + (button_height - play_text.get_height()) / 2
quit_text_x = button_x + (button_width - quit_text.get_width()) / 2
quit_text_y = quit_button_y + (button_height - quit_text.get_height()) / 2

# Position initiale et vitesse du personnage
xCoord = 360
yCoord = 360
xSpeed = 0
ySpeed = 0

# Etat du jeu
game_mode = False

# Apparition aléatoire et réinitialisation des objets (questions et bonus de temps)
object_spawn_interval = 5  # Temps en secondes avant réapparition
last_spawn_time = time.time()

# Points d'interrogation
num_questions = 10
question_positions = [(random.randint(0, res[0] - 50), random.randint(0, res[1] - 50)) for _ in range(num_questions)]

# Points d'interrogation dorés
golden_question_positions = []
golden_question_spawn_time = time.time()  # Temps au moment de la dernière apparition des questions dorées
golden_question_interval = 5  # Intervalle en secondes pour l'apparition des questions dorées

# Bombes
num_bombs = 5
bomb_positions = [(random.randint(0, res[0] - 50), random.randint(0, res[1] - 50)) for _ in range(num_bombs)]

# Bonus de temps
num_bonus_times = 3
bonus_time_positions = [(random.randint(0, res[0] - 50), random.randint(0, res[1] - 50)) for _ in range(num_bonus_times)]

# Bonus de vitesse
speed_boost_positions = []
speed_boost_spawn_time = time.time()  # Temps au moment de la dernière apparition du bonus de vitesse
speed_boost_interval = 20  # Intervalle en secondes pour l'apparition du bonus de vitesse
speed_boost_duration = 5  # Durée du boost de vitesse en secondes
speed_boost_active = False  # État du boost de vitesse
boost_start_time = 0  # Temps de début du boost de vitesse

# Compteur de points
score = 0

# Variables pour l'effet d'explosion
explosions = []  # Liste pour stocker les explosions actives
explosion_duration = 500  # Durée de l'effet d'explosion en millisecondes

# Définir les intervalles pour la réinitialisation des objets
question_interval = 5  # Intervalle en secondes pour les points d'interrogation
bomb_interval = 5  # Intervalle en secondes pour les bombes
bonus_interval = 20  # Intervalle en secondes pour les bonus de vitesse
last_question_spawn_time = time.time()
last_bomb_spawn_time = time.time()
last_bonus_spawn_time = time.time()

# Variables pour la barre de vie
max_life = 100
current_life = max_life

# Variables pour le boss
boss_appeared = False
boss_current_life = 100
boss_max_life = 100
boss_position = (0, 0)
boss_attack_positions = []
attack_spawn_time = time.time()
attack_interval = 2  # Temps entre les attaques du boss

# Minuteur
timer_duration = 60  # Durée du minuteur en secondes
start_time = time.time()  # Temps de départ du minuteur

# Boucle principale
clock = pygame.time.Clock()
done = False

while not done:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit()

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_LEFT:
                xSpeed = -3
            if ev.key == pygame.K_RIGHT:
                xSpeed = 3
            if ev.key == pygame.K_UP:
                ySpeed = -3
            if ev.key == pygame.K_DOWN:
                ySpeed = 3

        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_LEFT:
                xSpeed = 0
            if ev.key == pygame.K_RIGHT:
                xSpeed = 0
            if ev.key == pygame.K_UP:
                ySpeed = 0
            if ev.key == pygame.K_DOWN:
                ySpeed = 0

        if ev.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if not game_mode:
                if button_x <= mouse[0] <= button_x + button_width:
                    if play_button_y <= mouse[1] <= play_button_y + button_height:
                        game_mode = True
                        start_time = time.time()  # Réinitialiser le minuteur au début du jeu
                    if quit_button_y <= mouse[1] <= quit_button_y + button_height:
                        pygame.quit()
                        exit()
            else:
                pass

    if game_mode:
        # Mettre à jour la position du personnage avec la vitesse accrue si le boost est actif
        if speed_boost_active:
            xCoord += xSpeed * 2
            yCoord += ySpeed * 2
        else:
            xCoord += xSpeed
            yCoord += ySpeed

        # Empêcher le personnage de sortir de l'écran
        if xCoord >= res[0] - 70:
            xCoord = res[0] - 70
        elif xCoord <= 0:
            xCoord = 0
        if yCoord >= res[1] - 70:
            yCoord = res[1] - 70
        elif yCoord <= 0:
            yCoord = 0

        # Apparition du boss après 30 secondes
        current_time = time.time()
        if not boss_appeared and current_time - start_time > 30:
            boss_appeared = True
            boss_position = (res[0] // 2 - 50, 50)  # Position initiale du boss

        # Apparition aléatoire des points d'interrogation et bonus de temps toutes les x secondes
        if current_time - last_spawn_time > object_spawn_interval:
            question_positions = [(random.randint(0, res[0] - 50), random.randint(0, res[1] - 50)) for _ in range(num_questions)]
            bonus_time_positions = [(random.randint(0, res[0] - 50), random.randint(0, res[1] - 50)) for _ in range(num_bonus_times)]
            last_spawn_time = current_time  # Réinitialiser le temps d'apparition

        # Apparition du bonus de vitesse
        if current_time - speed_boost_spawn_time > speed_boost_interval:
            speed_boost_positions = [(random.randint(0, res[0] - 50), random.randint(0, res[1] - 50))]
            speed_boost_spawn_time = current_time  # Réinitialiser le temps d'apparition

        def reset_objects():
            global question_positions, bonus_time_positions, speed_boost_positions, last_question_spawn_time, last_bomb_spawn_time, last_bonus_spawn_time
            
            current_time = time.time()
            
            # Réinitialiser les questions si l'intervalle est écoulé
            if current_time - last_question_spawn_time > question_interval:
                question_positions = [(random.randint(0, res[0] - 50), random.randint(0, res[1] - 50)) for _ in range(num_questions)]
                last_question_spawn_time = current_time
            
            # Réinitialiser les bombes si l'intervalle est écoulé
            if current_time - last_bomb_spawn_time > bomb_interval:
                bomb_positions = [(random.randint(0, res[0] - 50), random.randint(0, res[1] - 50)) for _ in range(num_bombs)]
                last_bomb_spawn_time = current_time
            
            # Réinitialiser les bonus de vitesse si l'intervalle est écoulé
            if current_time - last_bonus_spawn_time > bonus_interval:
                speed_boost_positions = [(random.randint(0, res[0] - 50), random.randint(0, res[1] - 50))]
                last_bonus_spawn_time = current_time


        # Détecter les collisions avec les points d'interrogation
        new_question_positions = []
        for (qx, qy) in question_positions:
            if (xCoord < qx + 50 and xCoord + 70 > qx and
                yCoord < qy + 50 and yCoord + 70 > qy):
                score += 1
            else:
                new_question_positions.append((qx, qy))
        question_positions = new_question_positions

        def move_boss():
            global boss_position, boss_current_life
            # Déplace le boss à une nouvelle position aléatoire
            boss_position = (random.randint(0, res[0] - 100), random.randint(0, res[1] - 100))
            # Réduit les PV du boss de 1%
            boss_current_life = max(0, boss_current_life - boss_max_life * 0.01)
            
        def boss_action():
            current_time = time.time()
            if not boss_appeared:
                return
            
            if current_time - attack_spawn_time > attack_interval:
                # Lancer des attaques tout autour du boss
                for angle in range(0, 360, 45):  # Attaques tous les 45 degrés
                    attack_x = boss_position[0] + 50 + 100 * math.cos(math.radians(angle))
                    attack_y = boss_position[1] + 50 + 100 * math.sin(math.radians(angle))
                    boss_attack_positions.append([attack_x, attack_y])
                attack_spawn_time = current_time

            # Mise à jour des attaques
            new_boss_attack_positions = []
            for (ax, ay) in boss_attack_positions:
                ay += 5  # Déplace les attaques vers le bas
                if ay < res[1]:
                    new_boss_attack_positions.append([ax, ay])
                elif (xCoord < ax + 30 and xCoord + 70 > ax and
                    yCoord < ay + 30 and yCoord + 70 > ay):
                    current_life -= 20  # Perte de vie si le personnage touche une attaque
            boss_attack_positions = new_boss_attack_positions



        # Détecter les collisions avec les points d'interrogation dorés
        new_golden_question_positions = []
        for (gx, gy) in golden_question_positions:
            if (xCoord < gx + 50 and xCoord + 70 > gx and
                yCoord < gy + 50 and yCoord + 70 > gy):
                score += 5  # Points plus élevés pour les questions dorées
            else:
                new_golden_question_positions.append((gx, gy))
        golden_question_positions = new_golden_question_positions

        # Détecter les collisions avec les bombes
        new_bomb_positions = []
        for (bx, by) in bomb_positions:
            if (xCoord < bx + 50 and xCoord + 70 > bx and
                yCoord < by + 50 and yCoord + 70 > by):
                current_life -= 10
                explosions.append({'position': (bx, by), 'start_time': pygame.time.get_ticks()})
            else:
                new_bomb_positions.append((bx, by))
        bomb_positions = new_bomb_positions

        # Détecter les collisions avec les bonus de temps
        new_bonus_time_positions = []
        for (tx, ty) in bonus_time_positions:
            if (xCoord < tx + 50 and xCoord + 70 > tx and
                yCoord < ty + 50 and yCoord + 70 > ty):
                start_time += 5  # Gagnez 5 secondes supplémentaires
            else:
                new_bonus_time_positions.append((tx, ty))
        bonus_time_positions = new_bonus_time_positions

        # Détecter les collisions avec les bonus de vitesse
        new_speed_boost_positions = []
        for (sx, sy) in speed_boost_positions:
            if (xCoord < sx + 50 and xCoord + 70 > sx and
                yCoord < sy + 50 and yCoord + 70 > sy):
                speed_boost_active = True  # Activer le boost de vitesse
                boost_start_time = current_time
                num_questions = 20  # Augmenter le nombre de questions pendant le boost
            else:
                new_speed_boost_positions.append((sx, sy))
        speed_boost_positions = new_speed_boost_positions

        # Désactiver le boost de vitesse après la durée
        if speed_boost_active and current_time - boost_start_time > speed_boost_duration:
            speed_boost_active = False
            num_questions = 10  # Réinitialiser le nombre de questions après le boost

        # Générer les attaques du boss
        if boss_appeared and current_time - attack_spawn_time > attack_interval:
            attack_x = random.randint(boss_position[0], boss_position[0] + 100)
            attack_y = boss_position[1] + 100
            boss_attack_positions.append([attack_x, attack_y])
            attack_spawn_time = current_time

        # Mettre à jour les positions des attaques du boss
        new_boss_attack_positions = []
        for (ax, ay) in boss_attack_positions:
            ay += 5  # La vitesse des attaques du boss
            if ay < res[1]:
                new_boss_attack_positions.append([ax, ay])
            elif (xCoord < ax + 30 and xCoord + 70 > ax and
                  yCoord < ay + 30 and yCoord + 70 > ay):
                current_life -= 20  # Perdre de la vie en cas de collision avec une attaque du boss
        boss_attack_positions = new_boss_attack_positions

        # Vérifier si la vie est épuisée
        if current_life <= 0:
            print("Game Over!")
            pygame.quit()
            exit()

        # Gérer les explosions
        current_time_ms = pygame.time.get_ticks()
        explosions = [exp for exp in explosions if current_time_ms - exp['start_time'] <= explosion_duration]

        # Dessiner sur l'écran
        screen.blit(fond, (0, 0))
        screen.blit(character_image, (xCoord, yCoord))

        # Dessiner les points d'interrogation
        for (qx, qy) in question_positions:
            screen.blit(question_image, (qx, qy))

        # Dessiner les points d'interrogation dorés
        for (gx, gy) in golden_question_positions:
            screen.blit(golden_question_image, (gx, gy))

        # Dessiner les bombes
        for (bx, by) in bomb_positions:
            screen.blit(bomb_image, (bx, by))

        # Dessiner les bonus de temps
        for (tx, ty) in bonus_time_positions:
            screen.blit(bonus_time_image, (tx, ty))

        # Dessiner les bonus de vitesse
        for (sx, sy) in speed_boost_positions:
            screen.blit(speed_boost_image, (sx, sy))

        # Dessiner les explosions
        for exp in explosions:
            screen.blit(explosion_image, exp['position'])

        # Dessiner le boss
        if boss_appeared:
            screen.blit(boss_image, boss_position)

            # Dessiner la barre de vie du boss
            pygame.draw.rect(screen, RED, [boss_position[0], boss_position[1] - 20, boss_max_life, 10])
            pygame.draw.rect(screen, GREEN, [boss_position[0], boss_position[1] - 20, boss_current_life, 10])

        # Dessiner les attaques du boss
        for (ax, ay) in boss_attack_positions:
            screen.blit(attack_image, (ax, ay))

        # Afficher le score
        score_text = score_font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        # Afficher la barre de vie
        pygame.draw.rect(screen, RED, [10, 50, max_life, 20])
        pygame.draw.rect(screen, GREEN, [10, 50, current_life, 20])
        life_text = life_font.render(f'Vie: {current_life}', True, WHITE)
        screen.blit(life_text, (10, 75))

        # Afficher le minuteur
        elapsed_time = time.time() - start_time
        remaining_time = max(0, timer_duration - elapsed_time)
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        timer_text = timer_font.render(f'{minutes:02}:{seconds:02}', True, GREEN)
        timer_rect = timer_text.get_rect(topright=(res[0] - 10, 10))

        # Effet d'illumination du texte du chrono
        if remaining_time <= 5:
            flash_duration = 500  # Durée de l'effet en millisecondes
            current_time_ms = pygame.time.get_ticks()
            if (current_time_ms // flash_duration) % 2 == 0:
                timer_text = timer_font.render(f'{minutes:02}:{seconds:02}', True, RED)
                screen.blit(timer_text, timer_rect)
        else:
            screen.blit(timer_text, timer_rect)

        if remaining_time <= 0:
            print("Temps écoulé !")
            pygame.quit()
            exit()

    else:
        # Dessiner le menu
        screen.fill(BLACK)

        # Dessiner le bouton "Jouer"
        mouse = pygame.mouse.get_pos()
        if button_x <= mouse[0] <= button_x + button_width and play_button_y <= mouse[1] <= play_button_y + button_height:
            pygame.draw.rect(screen, color_light, [button_x, play_button_y, button_width, button_height])
        else:
            pygame.draw.rect(screen, color_dark, [button_x, play_button_y, button_width, button_height])
        
        # Dessiner le texte sur le bouton "Jouer"
        screen.blit(play_text, (play_text_x, play_text_y))

        # Dessiner le bouton "Quitter"
        if button_x <= mouse[0] <= button_x + button_width and quit_button_y <= mouse[1] <= quit_button_y + button_height:
            pygame.draw.rect(screen, color_light, [button_x, quit_button_y, button_width, button_height])
        else:
            pygame.draw.rect(screen, color_dark, [button_x, quit_button_y, button_width, button_height])
        
        # Dessiner le texte sur le bouton "Quitter"
        screen.blit(quit_text, (quit_text_x, quit_text_y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
