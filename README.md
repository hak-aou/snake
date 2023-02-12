# Rapport de projet : Snake en Python
#### *Auteur : Hakim AOUDIA, Victor BERNIER*
#### *Langage : Python*
#### *Date : 2020*
#### *Niveau : L1*

<div style="text-align:center;">
  <img src="https://user-images.githubusercontent.com/106891439/218287330-35ab6744-2b25-450d-be5d-9c4535b7ec63.png" width="50%" height="50%">
</div>

## Introduction

Le projet consiste à développer un jeu de Snake en utilisant le langage de programmation Python. Le jeu est conçu pour être joué à partir d'un ordinateur en utilisant un clavier.
On a utilisé la bibliothèque graphique de l'université fltk.

## Menu principal

Lorsque le jeu démarre, un premier menu apparaît et attend une action du joueur. Dans ce menu, le joueur peut choisir le mode de jeu souhaité en utilisant les flèches directionnelles ou en utilisant la souris et en validant en faisant un clique gauche ou en appuyant sur Entrée. Il ya le mode classique et le mode labyrinthe avec des murs partout sur le terrain.

## Jeu

Une fois le mode de jeu choisi, le joueur peut contrôler le serpent en utilisant les touches directionnelles du clavier. Le but du jeu est de manger les pommes sans toucher les murs ni toucher son propre corps, sinon la partie est perdu et un message de "game over" apparaît.
<img src="https://user-images.githubusercontent.com/106891439/218287357-7e585ff1-5ed9-4c8d-8656-a96cb4d3cbf7.png" width="50%" height="50%" style="float:left;">
<img src="https://user-images.githubusercontent.com/106891439/218287367-214db6b2-dc8e-4a32-a99b-08378efe52c0.png" width="50%" height="50%" style="float:left;">


## Fin de partie

A la fin de la partie, le joueur a le choix soit de quitter le jeu en sélectionnant "Quit" soit de recommencer la partie avec le boutton "Retry".
