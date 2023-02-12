# Hakim AOUDIA, Victor BERNIER, Mini-Projet 2 Snake
import fltk
import doctest
from time import sleep, time
from random import randint

# dimensions du jeu
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases


def case_vers_pixel(case):
    """
    Fonction recevant les coordonnées d'une case du plateau sous la
    forme d'un couple d'entiers (ligne, colonne) et renvoyant les
    coordonnées du pixel se trouvant au centre de cette case. Ce calcul
    prend en compte la taille de chaque case, donnée par la variable
    globale taille_case.

    >>> case_vers_pixel((8,7))
    (127.5, 112.5)
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


# fonctions affichage

def HUD(points):
    """
    Affiche le score en créant un rectangle gris en bas de la fenetre
    avec écrit au centre le nombre de points gagné par le joueur.

    :param points: int
    """
    fltk.rectangle(0, taille_case * 27, taille_case * 40, taille_case * 30, "grey", "grey")
    fltk.texte(taille_case * 20, taille_case * 28, "Score : " + str(points), "black", "center")


def affiche_murs(murs):
    """
    Fonction recevant une liste murs et qui affiche chaque
    élément de la listes dans la fenêtre
    :param murs: list
    """
    for mur in murs:
        x, y = case_vers_pixel(mur)  # Place le mur

        fltk.rectangle(x - taille_case / 2, y - taille_case / 2,  # Cree le mur
                       x + taille_case / 2, y + taille_case / 2,
                       couleur='darkred', remplissage='black')


def affiche_pommes(pommes):
    """
    Fonction recevant une listes pommes et qui affiche chaque
    élément de la listes dans la fenêtre
    :param pommes: list
    """
    for pomme in pommes:
        x, y = case_vers_pixel(pomme)
        fltk.cercle(x, y, taille_case/2,  # Place la pomme
                    couleur='darkred', remplissage='red')
        # Cree la pomme
        fltk.rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
                       couleur='darkgreen', remplissage='darkgreen')


def affiche_serpent(serpent):
    """
    Fonction recevant une listes serpent et qui affiche chaque partie du corps
    de la liste serpent grâce à la fonction case_vers_pixel().

    :param serpent: list
    """
    for i in serpent:
        x, y = case_vers_pixel(i)  # Place chaque partie du serpent
        # Colorie le serpent
        fltk.cercle(x, y, taille_case/2 + 1,
                    couleur='darkgreen', remplissage='green')
        if i == serpent[-1]:  # Colorie la tete en vert foncé
            fltk.cercle(x, y, taille_case/2 + 1,
                        couleur='black', remplissage='darkgreen')


def affiche_pomme_bonus(pomme_bonus, temps_spawn_bonus):
    """
    Fonction recevant une listes pomme_bonus et qui affiche ou non
    la pomme_bonus en fonction du contenu de la liste,
    et qui affiche pomme_bonus de plusieurs tailles en fonction
    de l'écart entre le temps réel donné par time() et temps_spawn_bonus
    :param pommes: list
    :param temps_spawn_bonus: list

    """
    # Place la pomme si elle existe
    if pomme_bonus[0] is not None:
        x, y = case_vers_pixel(pomme_bonus[0])
        ecart_temps = (time() - temps_spawn_bonus) % 1

        # Fait clignoter la pomme chaque demi seconde
        if ecart_temps >= 0 and ecart_temps < 0.5:
            fltk.cercle(x, y, taille_case/2,
                        couleur='darkblue', remplissage='blue')
        else:
            fltk.cercle(x, y, taille_case/4,
                        couleur='darkblue', remplissage='blue')


def affichage_jeu(jouer, direction, serpent, pommes,
                  points, murs, nb_pommes_mange,
                  pomme_bonus, temps_spawn_bonus):
    """
    Permet de gérer la partie en cours.
    La fonction gère le score, l'image de fond,
    les murs, le serpent, les pommes,
    et la potentielle mort du serpent.

    :param jouer: bool
    :param direction: tuple
    :return: serpent: list
    :param pommes: list
    :param points: int
    :param murs: list
    :param nb_pommes_mange: int
    :param pomme_bonus: int
    :param temps_spawn_bonus: int

    :return: jouer, points

    """

    # affichage des objets
    fltk.efface_tout()
    fltk.image(taille_case * largeur_plateau/2,
               taille_case * hauteur_plateau/2, 'img/fondDeJeu.png')
    HUD(points)  # Ecrit le score
    # Génère les variables nécessaire à la partie
    points, temps_spawn, is_new_time, nb_pommes_mange,\
        temps_spawn_bonus = update(direction, serpent, pommes,
                                   points, murs, nb_pommes_mange,
                                   pomme_bonus, temps_spawn_bonus)
    affiche_murs(murs)
    affiche_pommes(pommes)
    affiche_serpent(serpent)
    affiche_pomme_bonus(pomme_bonus, temps_spawn_bonus)
    jouer = is_alive(serpent, murs)
    if jouer:
        fltk.mise_a_jour()

    return jouer, points, temps_spawn, is_new_time,\
        nb_pommes_mange, temps_spawn_bonus


# initialisation et mise a jour

def spawn_pommes(pommes, serpent, y, murs):
    """
    Génère une position aléatoire pomme avec x, y compris
    dans la fenêtre de largeur 40 et hauteur 26.
    Puis compare si cette position est égal
    à une position d'un élément de la list serpent et mur
    sinon la pomme est ajouté dans la liste pommes
    et l'élément y de pommes est éliminé.

    :param pommes: list
    :param serpent: list
    :param y: int
    :param murs: list
    """
    go = True
    while go:
        cmpt = False
        pomme = (randint(0, 39), randint(0, 26))
        # Savoir si la pomme est sur le serpent
        for i in serpent:
            if pomme == i:
                cmpt = True
        # Savoir si la pomme est sur un mur
        for j in murs:
            if pomme == j:
                cmpt = True
        # Alors la pomme apparait
        if not cmpt:
            go = False
            pommes.append(pomme)
            pommes.pop(y)
    return time()


def spawn_pomme_bonus(serpent, murs, pommes, pomme_bonus):
    """
    Génère une position aléatoire pomme avec x, y
    compris dans la fenêtre de largeur 40 et hauteur 26.
    Puis compare si cette position est égal à une position
    d'un élément de la list serpent, murs et pomme,
    si la pomme bonus n'est pas a la meme position d'un autre élément
    elle est ajouté dans la liste pomme_bonus.

    :param pommes: list
    :param serpent: list
    :param y: int
    :param murs: list
    """
    go = True
    while go:
        cmpt = False
        pomme = (randint(0, 39), randint(0, 26))
        # Savoir si la pomme est sur un mur
        for i in serpent:
            if pomme == i:
                cmpt = True
        # Savoir si la pomme est sur un mur
        for j in murs:
            if pomme == j:
                cmpt = True
        # Savoir si la pomme est sur une pomme
        for k in pommes:
            if pomme == k:
                cmpt = True
        # Alors la pomme bonus apparait
        if not cmpt:
            go = False
            pomme_bonus.pop()
            pomme_bonus.append(pomme)


def supprime_pomme_bonus(pomme_bonus):
    """
    Fonction qui supprime le dernier élément de la liste
    pomme_bonus et qui rajoute un élément vide

    :param pomme_bonus: list
    """
    pomme_bonus.pop()
    pomme_bonus.append(None)


def mursClassique(murs):
    """
    Fonction qui génère les murs et rajoute leur position dans la liste murs
    Ces murs sont utilisés seulement dans le mode de jeu classique

    :param murs: list
    """
    # Cree des murs à droite et à gauche
    for x in range(40):
        murs.append((x, 0))
        murs.append((x, 26))
    # Cree des murs en haut et en bas
    for y in range(1, 26):
        murs.append((0, y))
        murs.append((39, y))


def mursLabyrinthe(murs):
    """
    Fonction qui génère les murs et rajoute leur position dans la liste murs
    Ces murs sont utilisés seulement dans le mode de jeu labyrinthe

    :param murs: list
    """
    # Cree des murs aléatoirement sur le terrain
    y = randint(3, 5)
    for a in range(50):
        for i in range(y):
            x = randint(0, 39)
            yPos = randint(0, 26-y)
            newPos = x, i + yPos

            # Evite l'apparition des murs sur la zone de spawn du serpent
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if newPos == (20 + j, 13 + k):
                        newPos = 0
            if newPos != 0:
                murs.append(newPos)


def mursJoueur(murs):
    """
    Fonction qui génère les murs et rajoute leur position dans la liste murs
    Ces murs sont utilisés seulement dans le mode de jeu joueur contre joueur

    :param murs: list
    """
    # Cree des murs aléatoirement sur le terrain
    for i in range(50):
        x, y = randint(0, 39), randint(0, 26)
        pos = x, y

        # Evite l'apparition des murs sur la zone de spawn du serpent
        for j in range(-1, 2):
            for k in range(-1, 2):
                if pos == (20 + j, 13 + k):
                    pos = 0

        # Si les murs apparaissent sur le joueur la boucle recommence de 1 tour
        if pos == 0:
            i -= 1
        else:
            murs.append(pos)


# logique

def update(direction, serpent, pommes, points, murs,
           nb_pommes_mange, pomme_bonus, temps_spawn_bonus):
    """
    Fonction permettant de gérer les différentes fonctionnalité du
    serpent. Lorsque le serpent avance, chaque partie de son coprs suit.
    Lorsque la futur position de la tete du serpent sors de l'écran alors
    la tete va de l'autre bord de l'écran.
    Pour chaque élément de la liste pomme si la tete touche une pomme alors
    la pomme disparait une nouvelle pomme apparait dans l'arène,
    un point est ajouté et le serpent grandit.

    :param direction: tuple
    :param serpent: list
    :param pommes: list
    :param points: int
    :param murs: list

    :param nb_pommes_mange: int
    :param pomme_bonus: list
    :param temps_spawn_bonus: int


    :return: points, temps_spawn, is_new_time,
             nb_pommes_mange, temps_spawn_bonus
    """
    # Le serpent bouge tout son coprs
    x, y = serpent[-1]
    a, b = direction
    new_dir = x + a, y + b

    # Permet une arène torique
    if new_dir[0] > 39:
        new_dir = (0, new_dir[1])
    elif new_dir[0] < 0:
        new_dir = (39, new_dir[1])
    elif new_dir[1] > 26:
        new_dir = (new_dir[0], 0)
    elif new_dir[1] < 0:
        new_dir = (new_dir[0], 26)
    serpent.append(new_dir)

    is_new_time = False
    temps_spawn = 0

    # Si le serpent mange ube pomme
    for i in range(len(pommes)):
        if serpent[-1] == pommes[i]:
            temps_spawn = spawn_pommes(pommes, serpent, i, murs)
            nb_pommes_mange += 1
            is_new_time = True
            points += 1
            queue = serpent[0]
            serpent.reverse()
            serpent.append(queue)
            serpent.reverse()
    serpent.pop(0)

    # Apparition des pommes bonus
    temps_spawn_bonus, points,\
        nb_pommes_mange = gestion_pomme_bonus(serpent, murs,
                                              pommes, nb_pommes_mange,
                                              pomme_bonus, points,
                                              temps_spawn_bonus)
    return points, temps_spawn, is_new_time, nb_pommes_mange, temps_spawn_bonus


def gestion_pomme_bonus(serpent, murs, pommes, nb_pommes_mange,
                        pomme_bonus, points, temps_spawn_bonus):
    """
    Fonction permettant de créer et supprimer le contenu de pomme_bonus
    ainsi que d'ajouter des points en cas d'issue favorable pour le joueur
    en fonction de nb_pommes_mange, temps_spawn_bonus et de serpent.

    :param murs: list
    :param serpent: list
    :param pommes: list
    :param nb_pommes_mange: int
    :param pomme_bonus: list
    :param points: int
    :param temps_spawn_bonus: int
    """
    # Chaque 5 pommes une pommes bonus apparait
    if nb_pommes_mange % 5 == 0 and nb_pommes_mange > 0:
        spawn_pomme_bonus(serpent, murs, pommes, pomme_bonus)
        temps_spawn_bonus = time()
        nb_pommes_mange = 0

    # Après 10 seconde sla pomme disparait
    if (time() - temps_spawn_bonus) > 10:
        supprime_pomme_bonus(pomme_bonus)

    # Calcule du nombre de points gagner
    if pomme_bonus is not None:
        if serpent[-1] == pomme_bonus[0]:
            supprime_pomme_bonus(pomme_bonus)
            points += int(randint(0, 1) + 20 - (time()
                          - (temps_spawn_bonus))//1*2)
    return temps_spawn_bonus, points, nb_pommes_mange


def score(points):
    """
    Affiche seulement le score du joueur au centre de l'écran. Une fois qu'il y
    a un évenement du joueur la fonction se termine.

    :param points: int
    """
    fltk.efface_tout()
    fltk.texte(300, 225, "Score : " + str(points), "black", "center")
    fltk.attend_ev()


def change_direction(direction, touche):
    """
    Permet de modifier les valeurs de la direction selon les touches
    flèches que le joueur presse. Les direction opposées à la diretion actuel
    ne sont pas prises en compte.

    :param direction: tuple
    :param touche: str

    :return: la nouvelle diretion du serpent
    >>> change_direction((1, 0), 'Up')
    (0, -1)
    >>> change_direction((1, 0), 'Left')
    (1, 0)
    """
    if touche == 'Up' and direction != (0, 1):
        # flèche haut pressée
        return (0, -1)
    elif touche == 'Down' and direction != (0, -1):
        return (0, 1)
    elif touche == 'Left' and direction != (1, 0):
        return (-1, 0)
    elif touche == 'Right' and direction != (-1, 0):
        return (1, 0)
    else:
        # pas de changement !
        return direction


def is_alive(serpent, murs):
    """
    Fonction permettant de savoir si le joueur est en vie.
    La position de la tête est comparée avec chaque élément
    de la liste serpent et murs.
    Si la position de la tête est égal à un
    élément de serpent ou murs alors return False.


    :param serpent: list
    :param murs: list

    :return: retourne True si aucune des conditions est vrai sinon False

    >>> is_alive((0, 0), (0, 0))
    False
    """
    # Si le serpent se mange
    head = serpent[-1]
    for i in range(len(serpent) - 1):
        if serpent[i] == head:
            return False
    # Si le serpent touche un mur
    for i in range(len(murs)):
        if head == murs[i]:
            return False
    # sinon il est en vie
    return True


def events(jouer, direction):
    """
    Permet de savoir si le joueur interagit en appuyant sur des touches
    ou avec la souris.

    :param jouer: bool
    :param direction: tuple
    :return: joueur, direction
    """
    # gestion des événements
    ev = fltk.donne_ev()
    ty = fltk.type_ev(ev)
    if ty == 'Quitte':
        jouer = False
    elif ty == 'Touche':
        print(fltk.touche(ev))
        direction = change_direction(direction, fltk.touche(ev))
    return jouer, direction


# gestion de l'interface

def choix_fleche_mort(ty, ev, pos_fleche, choix):
    """
    Permet de choisir de recommencer ou de quitter la partie avec
    la flèche.

    :param ty: str
    :param ev: str
    :param pos_fleche: int
    :param choix: bool

    >>> choix_fleche_mort("Quitte", None, 1, True)
    (0, False)
    >>> choix_fleche_mort("ClicGauche", None, 1, True)
    (1, False)
    """
    if ty == 'Quitte':
        return 0, False
    elif ty == 'Touche':
        if fltk.touche(ev) == "Left":
            if pos_fleche > 0:
                pos_fleche -= 1
            else:
                pos_fleche = 1
        elif fltk.touche(ev) == "Right":
            if pos_fleche < 1:
                pos_fleche += 1
            else:
                pos_fleche = 0
        elif fltk.touche(ev) == 'Return':
            choix = False

    elif ty == 'ClicGauche':
        choix = False
    return pos_fleche, choix


def choix_du_jeu(pos_fleche):
    """
    Permet de choisir le mode de jeu selon la position de la flèche.
    :param pos_fleche: int

    >>> choix_du_jeu(0)
    True
    >>> choix_du_jeu(1)
    True
    >>> choix_du_jeu(2)
    True
    >>> choix_du_jeu(3)
    True
    >>> choix_du_jeu(4)
    False

    """
    # Choix mode de jeu
    if pos_fleche == 0:
        game("Classique")
        return True
    elif pos_fleche == 1:
        game("Labyrinthe")
        return True
    elif pos_fleche == 2:
        game("Joueur")
        return True
    elif pos_fleche == 3:
        credits()
        return True
    elif pos_fleche == 4:
        return False


def flecheBouge(pos_fleche):
    """
    Permet de controler la fleche à l'aide la souris.
    :param pos_fleche: int
    """
    x, y = fltk.abscisse_souris(), fltk.ordonnee_souris()
    if x < taille_case * largeur_plateau / 2 and x > 10:
        if y >= 150 and y < 200:
            pos_fleche = 0
        elif y >= 200 and y < 250:
            pos_fleche = 1
        elif y >= 250 and y < 300:
            pos_fleche = 2
        elif y >= 300 and y < 350:
            pos_fleche = 3
        elif y >= 350 and y < 400:
            pos_fleche = 4
    return pos_fleche


# crédits

def credits():
    '''
    Fonction permettant d'afficher les crédits du jeu.
    '''
    y = 225
    skip = False
    fltk.efface_tout()
    fltk.rectangle(0, 0, 600, 450, couleur="black", remplissage="black")
    fltk.image(taille_case * largeur_plateau / 2 - 271 / 2,
               225, "img/credit.png", ancrage='nw', tag='c')
    fltk.mise_a_jour()
    for i in range(100):
        if fltk.donne_ev() is None:
            sleep(0.01)
        else:
            skip = True
    while y > -600 and not skip:
        ev = fltk.donne_ev()
        ty = fltk.type_ev(ev)
        if ty is not None:
            skip = True
        else:
            sleep(0.01)
        fltk.efface('c')
        fltk.image(taille_case * largeur_plateau / 2 - 271 / 2,
                   y, "img/credit.png", ancrage='nw', tag='c')
        fltk.mise_a_jour()
        y -= 1


# fonction jeu et associé

def game(style):
    """
    Fonction principale permettant d'initialiser et finir la partie.
    La liste murs prend une valeur selon le style de la partie.
    Une la partie fini la fonction mort et score se lance.

    :param style: str
    """
    # initialisation du jeu
    framerate = 10    # taux de rafraîchissement du jeu en images/s
    direction = (0, 0)  # direction initiale du serpent
    pommes = [(0, 0)]  # liste des coordonnées des cases contenant des pommes
    pomme_bonus = [None]
    points = 0
    nb_pommes_mange = 0
    serpent = [(20, 13)]
    # liste des coordonnées de cases adjacentes décrivant le serpent

    murs = []
    temps_spawn = time()
    temps_spawn_bonus = time()
    temps_actuel = temps_spawn

    if style == "Classique":
        mursClassique(murs)
    elif style == "Labyrinthe":
        mursLabyrinthe(murs)
    elif style == "Joueur":
        mursJoueur(murs)

        fltk.efface_tout()
        fltk.texte(300, 200, "In development,", "black", "center")
        fltk.texte(300, 225, "true gamemode coming soon.", "black", "center")
        fltk.attend_ev()
    temps_spawn = spawn_pommes(pommes, serpent, 0, murs)

    # boucle principale
    jouer = True
    while jouer:
        jouer, direction = events(jouer, direction)
        if jouer:
            jouer, points, temps_test, is_new_time, nb_pommes_mange,\
                temps_spawn_bonus = affichage_jeu(jouer, direction, serpent,
                                                  pommes, points, murs,
                                                  nb_pommes_mange,
                                                  pomme_bonus,
                                                  temps_spawn_bonus)
            if is_new_time:
                temps_spawn = temps_test
            temps_actuel = time()
            if temps_actuel - temps_spawn > 20:
                temps_spawn = spawn_pommes(pommes, serpent, 0, murs)

        # attente avant rafraîchissement
        sleep(1/framerate)
    score(points)
    mort(style)


def mort(style):
    """
    Cette fonction intervient lorsque le joueur est mort.
    L'écran est effacer apparait alors 2 images,
    une du gameover et une flèche.
    On peut alors choisir de recommener une partie
    ou de quitter pour revenir au menu principal.

    :param style: str Cette variable permet de relancer le bon mode de jeu
    """
    fltk.efface_tout()
    fltk.image(taille_case * largeur_plateau/2,
               taille_case * hauteur_plateau/2, "img/gameover.png")
    pos_fleche = 0
    fltk.image(((taille_case * largeur_plateau) / 3) + 136 * pos_fleche,
               260, "img/flecheMort.png", ancrage="nw", tag='f')
    choix = True
    while choix:
        ev = fltk.donne_ev()
        ty = fltk.type_ev(ev)

        pos_fleche, choix = choix_fleche_mort(ty, ev, pos_fleche, choix)

        x, y = fltk.abscisse_souris(), fltk.ordonnee_souris()
        if y < 275 and y > 175:
            if x < 300 and x > 190:
                pos_fleche = 0
            elif x < 410 and x > 300:
                pos_fleche = 1

        fltk.efface('f')
        fltk.image(((taille_case * largeur_plateau) / 3) + 136 * pos_fleche,
                   260, "img/flecheMort.png", ancrage="nw", tag='f')
        fltk.mise_a_jour()
    if pos_fleche == 0:
        pass
    elif pos_fleche == 1:
        game(style)  # Recommence le bon mode de jeu


# programme principal

def menu_1():
    """
    Fonction qui gère l'interface du premier menu.
    Une fois un évènement réalisé par le joueur la fonction
    se termine.
    """
    fltk.cree_fenetre(taille_case * largeur_plateau,
                      taille_case * hauteur_plateau)
    fltk.image(taille_case * (largeur_plateau/2),
               taille_case * (hauteur_plateau/2), "img/fondMenu.png")
    # Fait clignoter l'image
    while True:
        fltk.texte(300, 400, "Press Start", "black",
                   "center", police='Helvetica', taille=24, tag='a')
        fltk.mise_a_jour()
        for i in range(50):
            if fltk.donne_ev() is not None:
                return
            sleep(0.01)
        fltk.efface('a')
        fltk.mise_a_jour()
        for i in range(50):
            if fltk.donne_ev() is not None:
                return
            sleep(0.01)


def menu_2():
    """
    Fonction qui gère l'interface et l'utilisation
    du menu principal avec soit les flèches
    directionnelles soit la souris.
    """
    fltk.efface_tout()
    fltk.image(taille_case * largeur_plateau/2,
               taille_case * hauteur_plateau/2, "img/fondMenu.png")
    fltk.image(125, 300, "img/menu.png")
    pos_fleche = 0
    fltk.image((taille_case * largeur_plateau) * 2 / 3,
               182 + 50 * pos_fleche, "img/flecheMenu.png", ancrage="nw", tag='f')
    choix = True
    while choix:
        ev = fltk.donne_ev()
        ty = fltk.type_ev(ev)

        if ty == 'Quitte':
            return False
        elif ty == 'Touche':
            if fltk.touche(ev) == "Up":
                if pos_fleche > 0:
                    pos_fleche -= 1
                else:
                    pos_fleche = 4
            elif fltk.touche(ev) == "Down":
                if pos_fleche < 4:
                    pos_fleche += 1
                else:
                    pos_fleche = 0
            elif fltk.touche(ev) == 'Return':
                choix = False
        elif ty == 'ClicGauche':
            choix = False

        pos_fleche = flecheBouge(pos_fleche)

        fltk.efface('f')
        fltk.image((taille_case * largeur_plateau) * 3 / 7.5,
                   182 + 50 * pos_fleche, "img/flecheMenu.png",
                   ancrage="nw", tag='f')
        fltk.mise_a_jour()

    return choix_du_jeu(pos_fleche)


if __name__ == "__main__":

    menu_1()
    play = True
    while play:
        play = menu_2()
    # fermeture et sortie
    fltk.ferme_fenetre()

doctest.testmod()
