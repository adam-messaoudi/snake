import pygame  
import sys 
import random 

pygame.init()  # Initialisation de Pygame

# Paramètres du jeu
largeur, hauteur = 800, 600  # Dimensions de la fenêtre du jeu
taille_case = 50  # Taille de chaque case
fps = 7  # Taux de rafraîchissement du jeu (frames par seconde)

# Nouvelles variables pour définir la zone de jeu
zone_jeu = (700, 500)  # Dimensions de la zone de jeu
couleur_fond = (100, 100, 100)  # Couleur de fond principale de la fenêtre
couleur_fond_jeu = (150, 150, 150)  # Couleur de fond distincte pour la zone de jeu

# Couleurs utilisées pour dessiner le serpent, la pomme, le texte, etc.
couleur_serpent = (240, 240, 240)
couleur_tete_serpent = (255, 255, 255)
couleur_pomme = (0, 0, 0)
couleur_texte = (0, 0, 0)

# Calcul pour centrer la zone de jeu
x_centre_jeu = (largeur - zone_jeu[0]) // 2  # Position en X pour centrer la zone de jeu
y_centre_jeu = (hauteur - zone_jeu[1]) // 2  # Position en Y pour centrer la zone de jeu

# Initialisation de l'écran
ecran = pygame.display.set_mode((largeur, hauteur))  # Création de la fenêtre de jeu
pygame.display.set_caption("Snake game")  # Définition du titre de la fenêtre

# Ajout des variables de score et highscore
score = 0  # Variable pour stocker le score actuel du joueur
highscore = 0  # Variable pour stocker le meilleur score

# Fonction pour placer une nouvelle pomme
def placer_pomme(serpent):
    while True:
        # Génération de coordonnées aléatoires pour une nouvelle pomme
        x_pomme = random.randint(x_centre_jeu // taille_case, (x_centre_jeu + zone_jeu[0] - taille_case) // taille_case) * taille_case
        y_pomme = random.randint(y_centre_jeu // taille_case, (y_centre_jeu + zone_jeu[1] - taille_case) // taille_case) * taille_case
        pomme = (x_pomme, y_pomme)  # Position de la nouvelle pomme
        if pomme not in serpent:  # Vérification que la pomme n'est pas sur le serpent
            return pomme  # Retourne la position de la nouvelle pomme

# Fonction principale du jeu
def jeu_serpent():
    global score, highscore  # Déclaration des variables score et highscore en tant que variables globales
    serpent = [(x_centre_jeu, y_centre_jeu)]  # Création du serpent avec une seule case au départ
    direction = (1, 0)  # Direction initiale du serpent (vers la droite)
    pomme = placer_pomme(serpent)  # Placement initial de la pomme sur le terrain

    while True:  # Boucle principale du jeu
        for event in pygame.event.get():  # Gestion des événements Pygame
            if event.type == pygame.QUIT:  # Si l'événement est de quitter la fenêtre
                pygame.quit()  # Arrêt de Pygame
                sys.exit()  # Fermeture du programme

            elif event.type == pygame.KEYDOWN:  # Si l'événement est une pression de touche
                if event.key == pygame.K_LEFT and direction != (1, 0):  # Si la touche gauche est pressée et le serpent ne va pas à droite
                    direction = (-1, 0)  # Changer la direction vers la gauche
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):  # Si la touche droite est pressée et le serpent ne va pas à gauche
                    direction = (1, 0)  # Changer la direction vers la droite
                elif event.key == pygame.K_UP and direction != (0, 1):  # Si la touche haut est pressée et le serpent ne va pas vers le bas
                    direction = (0, -1)  # Changer la direction vers le haut
                elif event.key == pygame.K_DOWN and direction != (0, -1):  # Si la touche bas est pressée et le serpent ne va pas vers le haut
                    direction = (0, 1)  # Changer la direction vers le bas

        # Déplacement du serpent
        serpent.insert(0, (serpent[0][0] + direction[0] * taille_case, serpent[0][1] + direction[1] * taille_case))

        # Vérification de la collision avec la pomme
        if (
            x_centre_jeu <= serpent[0][0] < x_centre_jeu + zone_jeu[0] and
            y_centre_jeu <= serpent[0][1] < y_centre_jeu + zone_jeu[1] and
            serpent[0] == pomme
        ):
            pomme = placer_pomme(serpent)  # Placer une nouvelle pomme
            score += 1  # Augmenter le score
            if score > highscore:  # Mettre à jour le highscore si nécessaire
                highscore = score
        else:
            serpent.pop()  # Si le serpent n'a pas mangé de pomme, retirer sa dernière case

        # Vérification de la collision avec les bords de la zone de jeu
        if (
            serpent[0][0] < x_centre_jeu or
            serpent[0][0] >= x_centre_jeu + zone_jeu[0] or
            serpent[0][1] < y_centre_jeu or
            serpent[0][1] >= y_centre_jeu + zone_jeu[1]
        ):
            game_over()  # Si le serpent sort de la zone de jeu, fin de la partie

        # Vérification de la collision avec le corps du serpent
        if serpent[0] in serpent[1:]:
            game_over()  # Si le serpent se mord la queue, fin de la partie

        afficher(serpent, pomme, score, highscore)  # Afficher la mise à jour du jeu
        pygame.time.Clock().tick(fps)  # Contrôle de la vitesse du jeu

# Fonction pour afficher le serpent et la pomme
def afficher(serpent, pomme, score, highscore):
    ecran.fill(couleur_fond)  # Remplir l'écran avec la couleur de fond principale
    pygame.draw.rect(ecran, couleur_fond_jeu, (x_centre_jeu, y_centre_jeu, zone_jeu[0], zone_jeu[1]))  # Zone de jeu avec une couleur
    pygame.draw.rect(ecran, couleur_pomme, (*pomme, taille_case, taille_case))  # Dessiner la pomme sur l'écran

    # Dessiner le serpent sur l'écran
    for i, partie in enumerate(serpent):
        if i == 0:
            pygame.draw.rect(ecran, couleur_tete_serpent, (*partie, taille_case, taille_case))  # Dessiner la tête du serpent
        else:
            pygame.draw.rect(ecran, couleur_serpent, (*partie, taille_case, taille_case))  # Dessiner le corps du serpent

    # Affichage du score et du highscore
    font = pygame.font.Font(None, 40)  # Définition de la police et de la taille du texte
    texte_score = font.render(f"Score: {score}  Highscore: {highscore}", True, couleur_texte)  # Création du texte du score

    # Calcul pour centrer le texte en haut
    rect_score = texte_score.get_rect(center=(largeur / 2, 30))  # Position du texte du score

    ecran.blit(texte_score, rect_score)  # Affichage du texte du score à sa position

    pygame.display.flip()  # Rafraîchir l'écran pour afficher les changements

# Fonction pour afficher l'écran de fin de partie
def game_over():
    global score  # Déclaration de la variable score en tant que variable globale
    font = pygame.font.Font(None, 36)  # Définition de la police et de la taille du texte pour l'écran de fin
    texte = font.render(f"Game Over/Score: {score} - Appuyez Q pour quitter ou P pour rejouer", True, couleur_texte)  # Texte de fin de partie
    rect = texte.get_rect(center=(largeur / 2, hauteur / 2))  # Position du texte de fin de partie

    while True:  # Boucle d'affichage de l'écran de fin de partie
        for event in pygame.event.get():  # Gestion des événements Pygame
            if event.type == pygame.QUIT:  # Si l'événement est de quitter la fenêtre
                pygame.quit()  # Arrêt de Pygame
                sys.exit()  # Fermeture du programme
            elif event.type == pygame.KEYDOWN:  # Si l'événement est une pression de touche
                if event.key == pygame.K_q:  # Si la touche Q est pressée
                    pygame.quit()  # Arrêt de Pygame
                    sys.exit()  # Fermeture du programme
                elif event.key == pygame.K_p:  # Si la touche P est pressée
                    score = 0  # Réinitialisation du score
                    jeu_serpent()  # Redémarrage du jeu

        ecran.fill(couleur_fond)  # Remplir l'écran avec la couleur de fond principale
        ecran.blit(texte, rect)  # Affichage du texte de fin de partie à sa position
        pygame.display.flip()  # Rafraîchir l'écran pour afficher les changements
        pygame.time.Clock().tick(5)  # Contrôle de la vitesse du jeu

# Lancer le jeu
jeu_serpent()  # Appel de la fonction principale pour démarrer le jeu
