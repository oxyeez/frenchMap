#LIEHN Marcelin P2D Grp2
#Projet villes de France
#Bien mettre tous les fichiers suivants dans le même dossier que le fichier villes.py :
# --> villes.txt,  map_france_494x516.gif,  map_france_742x773.gif,  map_france_989x1031.gif,  map_france_1236x1289.gif
#Faire attention à ce que le fichier ville.txt n'ai pas de ligne vide à la fin, sinon l'ajout d'une nouvelle ville fera planter la programme

from tkinter import *
import random as rd
import time

def import_cities() :
	#impote toutes les villes contenues dans le document ville.txt
	global cities, cities_list

	cities = {}
	cities_list = []
	#crée un dico qui prend comme clés les villes du document villes.txt, et pour chaque clé retourne une liste : [latitude, longitude] correspondant à la ville
	with open("villes.txt", encoding = 'utf-8') as file :
	#pour chaque ligne du document ville.txt, on ajoute au dico le nom de la ville (30 premiers caractères) et ce nom de ville est associé à une liste comprenant la latitude (car 30 à 36) et la longitude (car 55 à 63)
		for line in file:		
			cities[line[0:29].rstrip()] = [float(line[30:36].rstrip()), float(line[55:63].rstrip())]
	#à partir du dico on crée une liste comprenant toutes les villes car on en aura beosin à plusieures reprises par la suite
	for city in cities :
		#on ajoute une par une chaque ville du dico
		cities_list.append(city)
	#on les trie par ordre alphabétique pour plus tard
	cities_list.sort()


def extremal_cities() :
	#défini les villes extremales et les dimensions de la carte
	global southcity, northcity, eastcity, westcity, map_height, map_width

	#on défini pour chaque extrème une longitue ou latitude pour laquelle toutes les villes de france sont plus extremales
	southcity = ['', 100, 0]
	northcity = ['', 0, 0]
	eastcity = ['', 0, 0]
	westcity = ['', 0, 0]

	#puis on effectue une boucle qui va passer en revue toutes les villes du dico afin de trouver les villes extremales
	for city in cities :
		#pour cela, chaque ville du dico va se voir comparé sa longitude ou latitude avec celles des fausses villes extremales pour voir si cette ville est plus extremale
		if cities[city][0] < southcity[1] :
			southcity = [city, cities[city][0], cities[city][1]]
		if cities[city][0] > northcity[1] :
			northcity = [city, cities[city][0], cities[city][1]]
		if cities[city][1] > eastcity[2] :
			eastcity = [city, cities[city][0], cities[city][1]]
		if cities[city][1] < westcity[2] :
			westcity = [city, cities[city][0], cities[city][1]]
	#pour obtenir les dimensions de la carte on fait la différence des longitudes ou latitudes des extremums
	map_height = northcity[1]-southcity[1]
	map_width = eastcity[2]-westcity[2]

	print('Ville la plus au sud :',southcity[0],'\nVille la plus au nord :',northcity[0],"\nVille la plus à l'est :",eastcity[0],"\nVille la plus à l'ouest :",westcity[0])


def conv_latlon_km() :
	#détermine la distance en km entre deux unités de latitude et deux unités de longitude
	global ratio_lat_km, ratio_lon_km
	
	#afin de connaitre la distance en km on prend 2 villes de latitudes égales, et deux autres de longitudes égales et on effectue des règles de trois
	ratio_lat_km = 541.186/abs(cities['Lille'][0] - cities['Clermont-Ferrand'][0])
	ratio_lon_km = 463.931/abs(cities['Pau'][1] - cities['Marseille'][1])


def conv_latlon_pixel() :
	#convertie toutes les coordonnées gps en coordonnées pixels
	global cities_pixel
	
	cities_pixel = {}
	#on crée une nouvelle liste qui elle, pour chaque ville, renverra une liste contenant les coordonnées en pixels de chaque ville sous la forme : [x, y]
	for city in cities :
		#pour calculer les coordonnées, on fait la différence entre les coordonnées de la ville et les coordonnées de la ville extrème nord pour les longitude/x, et de la ville extrème ouest pour les latitudes/y, plus 1 pour avoir une petite marge sur les bords
		#puis on multiplie par le nombre de km que fait une unité de coordonnées gps ainsi que par le multiplicateur qui correspond à la résolution qui a été demandé (c'est le dict_sizes[dim.get()][0])
		cities_pixel[city] = [round((northcity[1]-cities[city][0]+1)*ratio_lat_km*dict_sizes[dim.get()][0]), round((cities[city][1]-westcity[2]+1)*ratio_lon_km*dict_sizes[dim.get()][0])]


def place_cities() :
	#affiche la carte
	global can, background
	#on modifie le canvas pour qu'il soit à la résolution demandée par l'utilisateur
	#les dimensions sont obtenue en prenant la hauteur de la carte en unité de coordonnées gps, plus 2 unités de coordonnées gps pour laisser une espace sur les bords
	#on multiplie par le nombre de km que fait une unité de coordonnées gps ainsi que par le multiplicateur qui correspond à la résolution qui a été demandé
	can.grid_forget()
	can = Canvas(fen, height=int((map_height+2)*ratio_lat_km*dict_sizes[dim.get()][0]), width=int((map_width+2)*ratio_lon_km*dict_sizes[dim.get()][0]))
	#on charge l'image qui correspond à la résolution demandée
	background = PhotoImage(file = 'Ressources/map_france_'+dim.get()+'.gif')
	#on affiche l'image sur le canvas
	can.create_image(0, 0, anchor = 'nw', image = background)
	can.grid(row = 1, columnspan = 2)
	#on prend une par une les coordonnées de chaque ville du dico, puis on crée un cercle de rayon en adéquation avec la résolution demandée
	#pour cela on ajoute ou on retranche aux coordonnée de chaque ville le dict_sizes[dim.get()][1], afin d'avoir un rayon égal à dict_sizes[dim.get()][1] pour le cercle représentant la ville
	for city in cities_pixel :
		can.create_oval(int(cities_pixel[city][1]-dict_sizes[dim.get()][1]),int(cities_pixel[city][0]-dict_sizes[dim.get()][1]),int(cities_pixel[city][1]+dict_sizes[dim.get()][1]),int(cities_pixel[city][0]+dict_sizes[dim.get()][1]),width=1)


def print_map(*args) :
	#fonction appelée lorsque qu'une résolution est choisie ou à tout autre moment où la carte a besoin d'être réstaurée
	#fonction dont on aurait pu se passer, mais permet de ne rentrer qu'une ligne lorsque l'on veut réstaurer la carte
	
	#on ferme toutes les applications qui seraient potentiellement ouvertes avant d'afficher/actualiser la carte
	if atlas_open == 1 :
		quit_atlas()
	if ask_open == 1 :
		quit_ask()
	conv_latlon_pixel()
	place_cities()


def add_city() :
	global name, lat_deg, lat_min, lon_deg, lon_min, fen_add, orientation
	#on crée une nouvelle fenêtre qui va, sur la première ligne demander le nom de la ville à ajouter
	fen_add = Tk()
	fen_add.title('Ajouter une ville')
	Label(fen_add, text = 'Nom de la ville :').grid(row = 0, column = 0, sticky = 'e')
	name = Entry(fen_add, width = 20)
	name.bind()
	name.grid(row = 0, column = 1, columnspan = 5, sticky = 'w')
	#sur la deuxième ligne la latitude de la ville à ajouter
	Label(fen_add, text = 'Latitude :').grid(row = 1, column = 0, sticky = 'e')
	lat_deg = Entry(fen_add, width = 5)
	lat_deg.bind()
	lat_deg.grid(row = 1, column = 1)
	Label(fen_add, text = '°').grid(row = 1, column = 2, sticky = 'w')
	lat_min = Entry(fen_add, width = 5)
	lat_min.bind()
	lat_min.grid(row = 1, column = 3)
	Label(fen_add, text = "' N").grid(row = 1, column = 4, columnspan = 2, sticky = 'w')
	#sur la troisième ligne la longitude de la ville à ajouter
	Label(fen_add, text = 'Longitude :').grid(row = 2, column = 0, sticky = 'e')
	lon_deg = Entry(fen_add, width = 5)
	lon_deg.bind()
	lon_deg.grid(row = 2, column = 1)
	Label(fen_add, text = '°').grid(row = 2, column = 2, sticky = 'w')
	lon_min = Entry(fen_add, width = 5)
	lon_min.bind()
	lon_min.grid(row = 2, column = 3)
	Label(fen_add, text = "'").grid(row = 2, column = 4, sticky = 'w')
	#ainsi qu'un menu déroulant permettant le choix de l'orientation (ouest ou est)
	orientation = StringVar(fen)
	orientation.set(['W', 'E'][0])
	orientation_select = OptionMenu(fen_add, orientation, *['W', 'E'])
	orientation_select.grid(row = 2, column = 5, sticky = 'w')

	Label(fen_add, text = "Pensez bien à sélectionner l'orientation de la \nlongitude (W-ouest ou E-est)").grid(row = 3, columnspan = 6)
	#bouton qui appelle la fonction qui va ajouer la ville et les coordonnées au fichier ville.txt
	butt_val = Button(fen_add, text = 'Ajouter', command = eval_new_city)
	butt_val.grid(row = 4, column = 3, columnspan = 3, sticky = 'se')

	fen_add.mainloop()


def eval_new_city() :
	#crée la ligne contenant toutes les informations de la ville à ajouter et l'écrit dans le fichier texte 
	file = open("villes.txt", "a")
	#la ligne est crée sous la forme d'une seule chaine de caractère composée de :
	#un bloc de 30 caractères qui prend, au début, le nom de la ville à ajouter
	#suivi d'un bloc de 10 caractères qui prend, au début, la latitude une fois convertie en décimale et arrondie à la 3e décimale
	#suivi d'un bloc de 2 caractères qui va prendre, à la fin, la valeur entrée pour le nombre de degrés de la latitude, suivi du signe °
	#suivi d'un bloc de 3 caractères qui va prendre, à la fin, la valeur entrée pour le nombre de minutes de la latitude, suivi de ' N
	#puis à la suite, on fait sensiblement la même chose pour la longitude, an ajoutant un signe - lors du calcul de la longitude en décimale si elle est orienté vers l'ouest
	if orientation.get() == 'E' :
		line = '\n'+'{:<30}'.format(name.get())+'{:<10}'.format(str("%.3f" %(int(lat_deg.get())+int(lat_min.get())/60)))+'{:>2}'.format(lat_deg.get())+'°'+'{:>3}'.format(lat_min.get())+"'N"+'{:>13}'.format(str("%.3f" %(int(lon_deg.get())+int(lon_min.get())/60)))+'{:>7}'.format(lon_deg.get())+'°'+'{:>3}'.format(lon_min.get())+"'E"
	if orientation.get() == 'W' :
		line = '\n'+'{:<30}'.format(name.get())+'{:<10}'.format(str("%.3f" %(int(lat_deg.get())+int(lat_min.get())/60)))+'{:>2}'.format(lat_deg.get())+'°'+'{:>3}'.format(lat_min.get())+"'N"+'{:>13}'.format(str('-'+"%.3f" %(int(lon_deg.get())+int(lon_min.get())/60)))+'{:>7}'.format(lon_deg.get())+'°'+'{:>3}'.format(lon_min.get())+"'W"
	
	# /!\ /!\ (faire attention à ce que le fichier text n'ait pas de ligne vide à la fin) /!\ /!\
	file.write(line)
	file.close()
	fen_add.destroy()
	#on réinporte les villes afin d'actuéliser le dico et la liste et, seulement si une résolution est séléctionnée, on réaffiche la carte afin de l'actualiser
	import_cities()
	if dim.get() != 'Dimensions' :
		print_map()


def atlas() :
	#ouvre le mode atlas
	global liste, city_choice, atlas_open
	#on met la variable qui indique si l'atlas est ouvert ou non sur 1
	atlas_open = 1
	#on vérifie que l'outil d'affichage de nom de ville n'est pas ouvert, si il l'est on le ferme
	if ask_open == 1 :
		quit_ask()
	#efface le bouton "atlas"
	butt_atlas.grid_forget()
	#crée un menu déroulant contenant toutes les villes présentes dans la liste des villes
	liste = StringVar(fen)
	liste.set('Ville')
	#appel la fonction print_city à chaque sélection d'une des ville du menu déroulant
	liste.trace("w", print_city)
	city_choice = OptionMenu(fen, liste, *cities_list)
	city_choice.grid(row = 3, columnspan = 2)


def print_city(*args) :
	global city_placed
	#affiche sur la carte la ville qui aura été séléctionnée dans le menu déroulant
	#on commence par supprimer le rond de la ville précédement affichée si il y en a un
	can.delete(city_placed)
	#on place la ville sélectionnée sur le même principe que pour placer toutes les villes de la carte
	city_placed = can.create_oval(int(cities_pixel[liste.get()][1]-3),int(cities_pixel[liste.get()][0]-3),int(cities_pixel[liste.get()][1]+3),int(cities_pixel[liste.get()][0]+3),width=1, outline = 'red', fill = 'red')


def quit_atlas() :
	global atlas_open
	#fonction fermant l'atlas
	#supprime le menu déroulant et replace le bouton permettant d'afficher l'atlas
	city_choice.grid_forget()
	butt_atlas.grid(row = 3, columnspan = 2)
	#supprime le rond rouge de la ville qui était affichée
	can.delete(city_placed)
	#on remet la variable qui indique si l'atlas est ouvert ou non sur 0
	atlas_open = 0


def ask() :
	global text_city_asked, ask_open
	#on met la variable qui indique si l'outil d'affichage de nom de ville est ouvert ou non sur 1
	ask_open = 1
	#on vérifie que l'atlas n'est pas ouvert, si il l'est on le ferme
	if atlas_open == 1 :
		quit_atlas()
	#on supprime le bouton qui permet de lancer ce programme
	butt_ask.grid_forget()
	#on affiche une consigne
	text_city_asked = Label(fen, text = 'Cliquez sur une ville pour connaitre son nom')
	text_city_asked.grid(row = 4, columnspan = 2)
	#à chaque clique sur la carte, on lance la fonction clic_ask()
	can.bind("<Button-1>", clic_ask)


def clic_ask(event) :
	#passage en revu des coordonnées de chaque ville du dico pour trouver celle qui est le centre d'un carré de dimension 2 x dict_sizes[dim.get()][1] contenant les coordonnées du clic de la souris
	for city in cities :
		if int(cities_pixel[city][1]-dict_sizes[dim.get()][1]) < event.x <	int(cities_pixel[city][1]+dict_sizes[dim.get()][1]) and int(cities_pixel[city][0]-dict_sizes[dim.get()][1]) < event.y < int(cities_pixel[city][0]+dict_sizes[dim.get()][1]) :
			#une fois la ville trouvée, on affiche son nom et on met fin à la boucle avec break
			text_city_asked.configure(text = "Cette ville est "+city)
			break

	
def quit_ask() :
	global ask_open
	#fonction fermant l'outil qui donne le nom d'une ville
	#supprime le texte où est donné le nom de la ville sélectionnée et replace le bouton permettant d'afficher l'outil
	text_city_asked.grid_forget()
	butt_ask.grid(row = 4, columnspan = 2)
	#on remet la variable qui indique si l'outil permettant d'afficher le nom d'une ville est ouvert ou non sur 0
	ask_open = 0


def play() :
	#lance le jeu
	global game_open, tries, score, rand_city, text_city, text_tries, text_score, butt_surrender
	
	game_open = 1
	#si l'atlas est ouvert, on le ferme pour éviter la triche
	if atlas_open == 1 :
		quit_atlas()
	#pareil pour l'outil d'affichage de nom de ville
	if ask_open == 1 :
		quit_ask()
	#on défini le nombre d'essai sur 20, et le score initial de 0
	tries = 20
	score = 0
	#on supprime les boutons du menu principal
	butt_add.grid_forget()
	butt_atlas.grid_forget()
	butt_ask.grid_forget()
	butt_game.grid_forget()
	#on tire au hasard une ville de la liste des villes
	rand_city = cities_list[rd.randint(0, len(cities_list)-1)]
	#on affiche un message disant quelle ville trouver
	text_city = Label(fen, text = 'Situez '+rand_city+' sur la carte')
	text_city.grid(row = 2, columnspan = 2)
	#on affiche le nombre de villes restantes à trouver
	text_tries = Label(fen, text = 'Villes restantes : '+str(tries))
	text_tries.grid(row = 3, columnspan = 2)
	#on affiche le score
	text_score = Label(fen, text = 'Score : '+str(score))
	text_score.grid(row = 4, columnspan = 2)
	#on crée un bouton qui permet de quitter le jeu avant la fin
	butt_surrender = Button(fen, text = 'Abandonner', command = surrender_game)
	butt_surrender.grid(row = 5, columnspan = 2)
	#on fait en sorte que la fonction clic soit appelée à chaque clic de souris sur le canvas
	can.bind("<Button-1>", clic)


def clic(event) :
	global score, tries, rand_city, text_score_end, text_percent, butt_replay, butt_quit_game
	#fonction if qui vérifie si les coordonnées de la souris au moment du clic sont comprises dans un carré de centre : les coordonnées de la ville à trouver,
	#et de coté : 2 x dict_sizes[dim.get()][1]pixels auquel on rajoute deux pixels de chaque coté afin d'avoir une petite marge si l'utilisateur n'est pas assez précis
	if int(cities_pixel[rand_city][1]-dict_sizes[dim.get()][1]-2) < event.x < int(cities_pixel[rand_city][1]+dict_sizes[dim.get()][1]+2) and int(cities_pixel[rand_city][0]-dict_sizes[dim.get()][1]-2) < event.y < int(cities_pixel[rand_city][0]+dict_sizes[dim.get()][1]+2) and tries > 0 :
		#si le clic est bien dans le carré autour de la ville à trouver,  on ajoute 1 au score et on actualise le texte qui affiche le score
		score += 1
		text_score.configure(text = 'Score : '+str(score))
	#que la ville ait été trouvée ou non, on retranche 1 au nombre de villes restantes à trouver et on actualise le texte qui affiche ce nombre
	tries -= 1
	text_tries.configure(text = 'Coups restants : '+str(tries))
	#on tire au hasard une nouvelle ville à trouver dans la liste des villes, et on actualise le texte qui indiue la ville à trouver
	rand_city = cities_list[rd.randint(0, len(cities_list)-1)]
	text_city.configure(text = 'Situez '+rand_city+' sur la carte')
	
	if tries == 0 :
		#dans le cas où le nombre de coups à été épuisé, on efface toute l'interface du jeu
		text_city.grid_forget()
		text_tries.grid_forget()
		text_score.grid_forget()
		butt_surrender.grid_forget()
		#on affiche le nombre de villes trouvées, ainsi que le pourcentage de villes trouvées
		text_score_end = Label(fen, text = 'Vous avez trouvé '+str(score)+' villes sur 20', fg = 'blue')
		text_score_end.grid(row = 2, columnspan = 2)
		text_percent = Label(fen, text = 'Cela correspond à '+str(int(score/20*100))+' %'+' de réussite', fg = 'blue')
		text_percent.grid(row = 3, columnspan = 2)
		#on affiche deux boutons qui permettent de rejouer ou de quitter le jeu
		butt_replay = Button(fen, text = 'Rejouer', command = replay)
		butt_replay.grid(row = 4, column = 0, sticky = 'e')
		butt_quit_game = Button(fen, text = 'Quitter le jeu', command = quit_game)
		butt_quit_game.grid(row = 4, column = 1, sticky = 'w')


def replay() :
	#sert à relancer le jeu
	#on supprime tous les résultats du jeu et les boutons de la fin du jeu, et on relance le jeu en appelant la fonction play()	
	text_score_end.grid_forget()
	text_percent.grid_forget()
	butt_replay.grid_forget()
	butt_quit_game.grid_forget()
	play()


def quit_game() :
	#sert à quitter le jeu
	global game_open
	#on remet la variable qui indique si le jeu est ouvert ou non sur 0, on efface toute l'interface des résultats du jeu, et on réaffiche les boutons du menu principal
	game_open = 0
	text_score_end.grid_forget()
	text_percent.grid_forget()
	butt_replay.grid_forget()
	butt_quit_game.grid_forget()

	butt_add.grid(row = 2, columnspan = 2)
	butt_atlas.grid(row = 3, columnspan = 2)
	butt_ask.grid(row = 4, columnspan = 2)
	butt_game.grid(row = 5, columnspan = 2)


def surrender_game() :
	#sert à abandonner la partie avant la fin
	global game_open
	#on remet la variable qui indique si le jeu est ouvert ou non sur 0, on efface toute l'interface des résultats du jeu, et on réaffiche les boutons du menu principal
	game_open = 0
	text_city.grid_forget()
	text_tries.grid_forget()
	text_score.grid_forget()
	butt_surrender.grid_forget()

	butt_add.grid(row = 2, columnspan = 2)
	butt_atlas.grid(row = 3, columnspan = 2)
	butt_ask.grid(row = 4, columnspan = 2)
	butt_game.grid(row = 5, columnspan = 2)


#dico contenant les différentes résolutions proposées, et chaque dimension renvoi à une liste contenant :
# - le ratio utilisé pour passer de coordonnées en km à des coordonnées en pixels
# - le rayon des cercles qui représentent les villes
dict_sizes = {'494x516' : [0.4, 2], '742x773' : [0.6, 3], '989x1031' : [0.8, 4], '1236x1289' : [1, 5]}
#définition de variables dont on aura l'utilité plus tard mais qui devaient absolument être définies à l'avance
#atlas_open, game_open et ask_open permettent respectivement de savoir si l'atlas, le jeu, et la fonction qui affiche le nom de la ville délectionnée sont ouverts (= 1), ou fermés (= 0)
background, text_nop, city_placed, atlas_open, game_open, ask_open = None, None, None, 0, 0, 0

#appel des fonctions qui n'ont pas besoin d'être réappelée par la suite, ou rarement
import_cities()
extremal_cities()
conv_latlon_km()

#affichage de base de la fenêtre
fen = Tk()
fen.title('Villes de France')
#création du menu déroulant permettant de choisir la résolution de la fenêtre
dim = StringVar(fen)
dim.set('Dimensions')
dim.trace("w", print_map)
menu = OptionMenu(fen, dim, *dict_sizes)
menu.grid(columnspan = 2)
#affiche un petit rappel afin que l'utilisateur pense bien à choisir la résolution avant de faire autre choses
can = Label(fen, text = " Avant tout, choisissez une dimension pour la fenêtre ")
can.grid(row = 1, columnspan = 2)
#place les différents boutons qui vont permettre d'effectuer les actions du programme
butt_add = Button(fen, text = 'Ajouter une ville', command = add_city)
butt_add.grid(row = 2, columnspan = 2)
butt_atlas = Button(fen, text = 'Atlas', command = atlas)
butt_atlas.grid(row = 3, columnspan = 2)
butt_ask = Button(fen, text = 'Afficher le nom', command = ask)
butt_ask.grid(row = 4, columnspan = 2)
butt_game = Button(fen, text = 'Jouer', command = play)
butt_game.grid(row = 5, columnspan = 2)
butt_quit = Button(fen, text = 'Quitter', command = fen.quit)
butt_quit.grid(row = 6, columnspan = 2, sticky = 'e')


fen.mainloop()	# démarrage du réceptionnaire d’événements
fen.destroy()	# destruction (fermeture) de la fenêtre
