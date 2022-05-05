
import turtle
import random
import math
import time


## ======================= permet d'afficher la map ====================== ##
def showMap(height,width,sizeX,sizeY,world,light,light_intencity):
    '''
    affiche la map avec et sans les ombres (en fonction des arguments)
    '''

    # si on a pas de lumiere
    if light == False:
        light = [light_intencity] * len(world)

    # turtle.tracer(0,0) permet d'aller plus vite dans l'affichage de la map
    turtle.tracer(0, 0)
    
    turtle.penup()

    # turtle.speed(0) est la vitesse la plus rapide possible
    turtle.speed(0)
    
    long = len(world)-1
    turtle.pensize(math.ceil((sizeY/height)))

    # repete pour toute la hauteur du monde
    for i in range(height):

        # va tout a gauche
        turtle.goto(math.floor(-sizeX/2),math.ceil(-(i+1)*sizeY/height + sizeY/2))
        
        turtle.pendown()

        # repete pour toute la largeur
        for j in range(width):
            item = long - (i * width + j)

            # defini la couleur de chaque bloc
            turtle.colormode(255)
            if world[item] == 1:
                col = [153, 74, 0] # terre
            elif world[item] == 2:
                col = [158, 158, 158]  # pierre
            elif world[item] == 3:
                col = [42, 137, 232] # grotte
            elif world[item] == 4:
                col = [193, 207, 2]# or
            elif world[item] == 5:
                col = [116, 219, 218] # diamand
            elif world[item] == 6:
                col = [42, 137, 232] # ciel
            elif world[item] == 7:
                col = [4, 16, 194] # eau
            else:
                col = [54, 173, 3] # herbe

            # defini la luminosite du bloc
            if type(light[item]) == int:
                for h in range(3):
                    new_col = math.floor(col[h] * (int(light[item])/light_intencity))
                    if new_col > 255:
                        new_col = 255
                    if new_col < 0:
                        new_col = 0
                    col[h] = new_col
            else:
                # la luminosite n'a meme pas ete calculer : on est a 0
                col = [0,0,0]

            # affiche le bloc avec la luminosite defini
            turtle.pencolor(col)

            # va a droite pour faire le bloc suivant
            turtle.forward(math.floor(sizeX/width))
        turtle.penup()

    # affiche le tout pour aller plus vite
    turtle.update()

    # cache le tracer pour plus d'estetique
    turtle.hideturtle()







# ================ Tout est utile a partir d'ici ============= #


def generate(height,width,light_intencity,parameters='all'):
    '''
    f( int , int , int , dict/None ) -> list , list
    '''

    # defini ce que l'on va avoir
    if parameters == 'all':
        generate_type = {'dirt-stone deep':True,
                         'caves':True,
                         'deep-cave':True,
                         'sky':True,
                         'water':True,
                         'grass':True,
                         'light':True,}
    else:
        generate_type = parameters

    # fait un monde avec 1/3 de terre et le reste de pierre
    world = []

    # pierre
    for i in range(math.floor(height/3)*2):
        for j in range(width):
            world += [2]

    # terre
    for i in range(math.floor(height/3)):
        for j in range(width):
            world += [1]

    long = height * width
    while len(world) < long:
        world += [1]



    if generate_type['dirt-stone deep']:
        # genere de la pierre et de la terre en profondeur
        # max_radius, min_nb, max_nb, type, from, to
    
        # pierre
        world = generateDeeper(height,width,list(world),7,round(height*10/200),round(height*15/200),2,round(height/3)*2*width,long-1)
        # terre
        world = generateDeeper(height,width,list(world),7,round(height*10/200),round(height*15/200),1,0,round(height/3)*2*width)


    if generate_type['caves']:
        # genere des grottes
        world = generateCaves(height,width,list(world),8,round(height*10/200),round(height*15/200),20,0,long-1)
        print('grottes : OK')

    if generate_type['deep-cave']:
        # genere une grande et profonde grotte
        world,start_deep = deepBigCave(height,width,list(world),10)
    else:
        # prend une position aleatoire pour ne pas avoir d'erreur
        if random.randint(1,2) == 1:
            start_deep = long - random.randint(40,round(width/4))

        else:
            start_deep = long - random.randint(round(width/4)*3,width-40)


    if generate_type['sky']:
        # genere le ciel
        world = generateSky(height,width,list(world))
        print('ciel : OK')


    if generate_type['water']:
        # genere de l'eau
        # nb_min, nb_max, min_size, max_size
        world = generateWater(height,width,list(world),round(height*5/200),round(height*10/200),round(height*50/200),round(height*100/200),start_deep)
        print('eau : OK')

    if generate_type['grass']:
        # genere de l'herbe
        world = generateGrass(height,width,list(world))


    # genere la lumiere du soleil
    light = lightSim(height,width,list(world),light_intencity)
    print('lumiere : OK')
    
    return world,light
    


# =========================== outil pour la generation ==================== #

def getWithRadius(height,width,item,radius):
    '''
    f( int , int , int , int ) -> list
    retourne une liste avec les positions des pixels dans un cercle
    plein base sur son rayon
    '''


    # 'dessine' virtuelement un carre et tourne autoure, si un pixel est
    # trop loin du centre(distance avec la formule de Pythagore) il n'est pas pris

    # retourne les positions dans un cercle fait avec le rayon
    # utilise pour faire des grottes...
    
    x_dist = 0
    y_dist = 0
    position = 1
    allowed_pos = []
    dist = width - radius -1
    long = width * height
    for i in range(radius):
        
        # pour ne pas avoir trop de lignes
        for h in range(4):
            
            # fait un cercle qui grandi et tourne autoure
            if h == 0:
                changex_dist = 1
                changey_dist = 0
                change_item = 1
            elif h == 1:
                changex_dist = 0
                changey_dist = -1
                change_item = -width
            elif h == 2:
                changex_dist = -1
                changey_dist = 0
                change_item = -1
            else:
                changex_dist = 0
                changey_dist = 1
                change_item = width
                
            for j in range(position):
                item += change_item
                x_dist += changex_dist
                y_dist += changey_dist

                
                # verifie si le point du carre est plus petit ou egal au rayon
                if round(math.sqrt(x_dist**2 + y_dist**2)) < radius:
                    
                    # verifie que cela ne passe pas de l'autre cote
                    if item%width <= dist and item%width >= radius:
                        
                        # verifie si ca n'est pas sorti du monde
                        if item >= 0 and item < long-1:
                            allowed_pos += [item]

        # tourne autoure du carre
        position += 2
        x_dist += -1
        y_dist += 1
        item += width-1

    # retourne les position dans le cercle
    return allowed_pos


def checkDir(width,direction,world,liquids,pos,check_pos):
    '''
    f( int , int , list , list , int , int ) -> str or bool
    retourne si la prochaine position d'une particule d'un liquide est valide
    ou non
    '''
    
    if direction < 0 or direction > len(world):
        # si c'est en dehors du monde
        return 'out'

    # verifie si la prochaine position est occuper dans la liste 'world'
    if world[direction] == 3:

        # verifie si il n'y a pas de particule d'eau a la prochaine position
        if not(direction in liquids):
            
            # verifie si cela ne passe pas de l'autre cote
            if math.floor(direction/width) + check_pos == math.floor(pos/width):
                
                # la prochaine position est valide
                return True

    # la prochaine position N'est PAS valide
    return False


def genLiquids(height,width,world,liquids,liquids_id):
    '''
    f( int , int , list , list , int ) -> int or str
    retourne la nouvelle position d'une particule de liquide apres avoir
    essaye les positions autoure d'elle
    '''
    pos = liquids[liquids_id]

    # verifie en dessous
    gen = checkDir(width,pos-width,world,liquids,pos,1)
    if type(gen) == bool:
        if gen:
            return pos - width
    else:
        # en dehors du monde
        return 'delet'


    # verifie a droite en bas et a gauche en bas
    # [ le faite qu'une particule puisse passer entre 2 mur n'est pas un bug,
    # cela donne des choses plus joli ]

    # utilise 'random' pour ne pas aller a chaque fois dans la meme direction
    if random.randint(1,2) == 1:
        # essaye a gauche
        direction = (pos - width) - 1
        gen = checkDir(width,direction,world,liquids,pos,1)
        if type(gen) == bool:
            if gen:
                # si la position est valide
                return direction
        else:
            # en dehors du monde
            return 'delet'

        # il ne peut pas aller a gauche donc il test a droite
        direction = (pos - width) + 1
        gen = checkDir(width,direction,world,liquids,pos,1)
    else:
        # essaye a droite
        direction = (pos - width) + 1
        gen = checkDir(width,direction,world,liquids,pos,1)
        if type(gen) == bool:
            if gen:
                # si la position est valide
                return direction
        else:
            # en dehors du monde
            return 'delet'

        # il ne peut pas aller a gauche donc il test a droite
        dirction = (pos - width) - 1
        gen = checkDir(width,direction,world,liquids,pos,1)

        
    if type(gen) == bool:
        if gen:
            # si la position est valide
            return direction
    else:
        # en dehors du monde
        return 'delet'
        
    # verifie a gauche et a droite
    if random.randint(1,2) == 1:
        # verifie a gauche
        direction = pos - 1
        gen = checkDir(width,direction,world,liquids,pos,0)
        if type(gen) == bool:
            if gen:
                # si la position est valide
                return direction
        else:
            # en dehors du monde
            return 'delet'
        
        # il ne peut pas aller a gauche donc il test a droite
        direction = pos + 1
        gen = checkDir(width,direction,world,liquids,pos,0)
    else:
        # il essaye a droite
        direction = pos + 1
        gen = checkDir(width,direction,world,liquids,pos,0)
        if type(gen) == bool:
            if gen:
                # si la position est valide
                return direction
        else:
            # en dehors du monde
            return 'delet'
        
        # il ne peut pas aller a droite donc il test a gauche
        dirction = pos - 1
        gen = checkDir(width,direction,world,liquids,pos,0)
        
    if type(gen) == bool:
        if gen:
            # si la position est valide
            return direction
    else:
        # en dehors du monde
        return 'delet'
    return pos


def findNextCave(width,height,world):
    '''
    f( int , int , list ) -> int or bool
    retourne la position d'un pixel faisant partie d'une grotte
    (il fait 200 essaie avant d'arreter)
    '''

    # recherche une grotte dans le monde
    l = len(world)
    pos = random.randint(100,l - 100)
    for i in range(200):
        if world[pos] == 3 and pos > math.floor(width*(height/3)):
            # a trouve une grotte
            return pos

        # prend une nouvelle position pour essayer
        pos = random.randint(100,l - 100)

    
    # il n'en a pas trouve apres 200 essaies
    return False










def generateDeeper(height,width,world,max_radius,min_nb,max_nb,block_type,from_pos,to_pos):
    '''
    f( int , int , list , int , int , int , int , int or str , int , int ) -> list
    retourne la liste en argument avec des 'type_block'(en argument)
    generes entre 2 positions, cela permet un paterne plus naturel
    '''
    
    # setup
    long = len(world)
    radius = random.randint(2,max_radius)

    # pour ne pa avoir d'erreur avec 'random'
    if min_nb > max_nb:
        max_nb = min_nb + 1

    # defini le nombre de taches de 'type'
    nb_block = random.randint(min_nb,max_nb)

    for i in range(nb_block):

        # defini la position de depart d'une tache de 'type'
        position = random.randint(from_pos,to_pos)

        # defini la taille de la tache
        size_block = random.randint(2,5)
        for j in range(size_block):
            if random.randint(0,1) == 1:
                
                # defini le rayon d'un point de la tache
                radius = random.randint(2,max_radius)

            # prend les position dans le cercle
            block = getWithRadius(height,width,position,radius)
            if block != []:
                for h in block:
                    world[h] = block_type

                # defini la nouvelle position d'un point de la tache
                position = block[random.randint(0,len(block)-1)]
            else:
                # defini la position d'une nouvelle tache
                position = random.randint(from_pos,to_pos)
                
    return world



# ========================== generation des grottes ======================= #

def generateCaves(height,width,world,max_radius,cave_size,min_nb,max_nb,from_pos,to_pos):
    '''
    f( int , int , list , int , int , int , int , int , int ) -> list
    retourne la liste en argument avec des grottes generes a l'interieur
    '''

    # setup
    long = len(world)
    radius = random.randint(3,max_radius)

    # evite une erreur de 'random'
    if min_nb > max_nb:
        max_nb = min_nb + 1

    # defini le nombre de grottes
    nb_caves = random.randint(min_nb,max_nb)

    for i in range(nb_caves):

        # defini le point de depart de la grotte
        position = random.randint(from_pos,to_pos)

        # defini la taille de la grotte
        size_cave = random.randint(3,cave_size)
        for j in range(size_cave):
            if random.randint(0,2) < 2:
                # redefini la taille du crecle pour 'dessiner' la grotte
                radius = random.randint(3,max_radius)

            # prend les position du cercle
            caves = getWithRadius(height,width,position,radius)
            if caves != []:
                for h in caves:
                    # set cave
                    world[h] = 3
                position = caves[random.randint(0,len(caves)-1)]
            else:

                # fait une nouvelle grotte
                position = random.randint(from_pos,to_pos)

    return world


def deepBigCave(height,width,world,max_radius):
    '''
    f( int , int , list , int ) -> list , int
    retourne le nouveau monde avec une grotte tres profonde pour avoir un
    paterne de jeu video
    '''

    # setup
    long = len(world)

    # defini une position de depart et la direction de la grotte
    if random.randint(1,2) == 1:
        position = long - random.randint(40,round(width/4))
        # va se diriger vers la droite
        direction= 1
    else:
        position = long - random.randint(round(width/4)*3,width-40)
        # va se diriger vers la gauche
        direction = -1
    start_pos = position

    
    # defini jusqu'ou la grotte ira en profondeur
    max_deep = (round(height/3)*2) * width -( random.randint(10,50) * width )

    # defini la taille du tracer
    radius = random.randint(4,max_radius)

    # repete tant que l'on a pas atteind la profondeur voulu
    while position > max_deep:
        if random.randint(0,3) < 3:

            # change la taille du tracer
            radius = random.randint(4,max_radius)

        # prend les position du cercle fait avec son rayon
        circle = getWithRadius(height,width,position,radius)

        if circle == []:
            # on a atteind le bord : on s'arrete
            break
        else:
            # on ajoute ce que l'on a calculer dans le monde
            for h in circle:
                # set cave
                world[h] = 3


            # avance dans la direction voulu
            allowed_pos = []
            for i in range(radius):
                for j in range(radius):
                    # fabrique toutes les positions en bas et dans la direction voulut
                    pos_test = position - (i*width + (j*direction))
                    if pos_test < long:
                        if pos_test > 0:
                            allowed_pos += [pos_test]

            position = allowed_pos[random.randint(0,len(allowed_pos)-1)]

    return world,position


# =========================== generation du ciel ========================== #

def generateSky(height,width,world):
    '''
    f( int , int , list )
    retourne la liste en argument avec un ciel fait a partir des courbes
    cos() et sin()
    '''

    # prend des paramettres aleatoires
    random_sky = 0
    while random_sky == 0:
        random_sky = random.randint(-2,2)/2

    random_biome = 0
    while random_biome**2 <= 0.2 or random_biome < random_sky*2:
        random_biome = random.randint(-200,200)/100

    random_biome = random_biome ** 2


    long = len(world)
    for i in range(width):

        # permet d'avoir des montagnes(i/10) ou des pleines (i/100)
        # en fonction du diviseur
        shape = i/10

        y = 0
        y += (-abs(random_sky) *math.cos(shape * random_sky))
        y += (random_sky * math.sin(shape * 2))
        #y += (2 * cos(i * -0.25))
        #y += (random_sky * sin(i * -1))

        # utilise la valeur du biome (aleatoire)
        y *= random_biome

        y = round(y)

        # prend la position dans la liste et 'dessine' le ciel
        # au dessus de la position
        pos = long - ((width*y + i) + width*20)
        while pos > 0 and pos < long:
            world[pos] = 3
            pos += width
        #print(pos)
        #world[pos] = 6


    return world



# ========================== Simulation d'un liquide ===================== #

def generateWater(height,width,world,min_lac,max_lac,min_size,max_size,start_deep):
    '''
    f( int , int , list , int , int , int , int , int ) -> list
    retourne le monde apres avoir genere de l'eau dans les grottes
    '''
    
    long = len(world)

    # fait un lac (en surface)
    gen_lac = random.randint(1,2)
    if gen_lac == 1:
        # a 1 chance sur 2 de faire un lac

        # va a l'opposee de la grottes tres profonde
        if start_deep > long - width:
            # prend la position d'ou l'eau va etre lachee
            gen_lac = long - random.randint(50,round(width/2)-25)
        else:
            # prend la position d'ou l'eau va etre lachee
            gen_lac = long - random.randint(round(width/2)+25,width-50)

        # defini la quantite de liquide a genere
        liquids = [gen_lac] * random.randint(min_size,max_size)
        print('lac at : ' + str(gen_lac))

        # defini le nombre de generation a faire pour que ce soit un lac
        # assez naturel
        rep = len(liquids) + 500
        for h in range(rep):
            
            delet = []
            for j in range(len(liquids)):
                # simule chaque particule l'une apres l'autre
                next_pos = genLiquids(height,width,world,liquids,j)
                if type(next_pos) == int:
                    liquids[j] = next_pos
                else:
                    delet += [j]

            # enleve les particules qui tombes ou qui ne sont plus valide
            # il tri la liste puis l'inverse pour ne pas avoir des
            # particules qui soit enleves alors quelle ne devrait pas
            delet.sort()
            delet.reverse()
            for j in delet:
                liquids.pop(j)

        # avoir une surface plane
        liquids = checkAroundLiquids(height,width,world,liquids)

        for j in liquids:
            world[j] = 7
    
    nb_lac = random.randint(min_lac,max_lac)
    for i in range(nb_lac):

        # cherche une grotte ou mettre de l'eau
        next_cave = findNextCave(width,height,world)
        if not(next_cave):
            
            # n'a pas trouver de grotte apres 200 essais
            print('lost')
            next_cave = findNextCave(widht,height,world)
            if not(next_cave):
                
                # n'en a toujours pas trouve donc il abandonne
                return world

        # defini la quantite de liquide
        liquids = [next_cave] * random.randint(min_size,max_size)

        # defini le nombre de simultion pour avoir un resultat satisfaisant
        rep = len(liquids) + 500
        for  h in range(rep):
            
            delet = []
            for j in range(len(liquids)):
                next_pos = genLiquids(height,width,world,liquids,j)
                if type(next_pos) == int:
                    liquids[j] = next_pos
                else:
                    delet += [j]

            # permet de supprimer une particule facilement
            delet.sort()
            delet.reverse()
            for j in delet:
                liquids.pop(j)

        # avoir une surface plane
        liquids = checkAroundLiquids(height,width,world,liquids)
        

                    
        for j in liquids:
            world[j] = 7
    print('number : ' + str(nb_lac))


    return world


def checkAroundLiquids(height,width,world,liquids):
    '''
    f( int , int , list , list ) -> list
    retourne le liquide apres lui avoir fait une surfave plane
    '''

    # fait que le liquide a une surface plane
    delet = [1]
    loop = 0

    # supprime toutes les particules en qui sont au meme endroit
    #liquids = list(dict.fromkeys(liquids))
    liquids_ = []
    for i in liquids:
        if i not in liquids_:
            liquids_ += [i]

    liquids = list(liquids_)
    del liquids_





    
    while len(delet) > 0 and loop < 200:
        delet = []
        for h in range(len(liquids)):

            # verifie a droite et a gauche si il y a un mur ou une particule
            # pour supprimer les surfaces pas plane
            liquid_pos = liquids[h]
            if math.floor(liquid_pos/width) == math.floor((liquid_pos+1)/width):
                if world[liquid_pos+1] == 3:
                    if not(liquid_pos+1 in liquids):
                        delet += [h]

            if math.floor(liquid_pos/width) == math.floor((liquid_pos-1)/width):
                if world[liquid_pos-1] == 3:
                    if not(liquid_pos-1 in liquids):
                        # verifie que l'on ne le prend pas 2 fois
                        if not(h in delet):
                            delet += [h]


        # permet de supprimer une particule facilement
        delet.sort()
        delet.reverse()
        for h in delet:
            liquids.pop(h)

        # pour ne pas avoir une boucle infini
        loop += 1
    return liquids


# ========================== generation de l'herbe ======================= #

def generateGrass(height,width,world):
    '''
    f( int , int , list ) -> list
    retourne le monde apres avoir genere de l'herbe sur le sol
    '''

    # setup
    long = len(world)
    replace_block = [6,3,7]

    
    for i in range(width):
        pos = (long-1) - i
        done = False
        # repete jusqu'a trouver le sol ( mais pas un block seul ) <- important !!
        while not(done):
            # repete justqu'a trouver le sol ou la fin du monde
            while pos-width > -1 and (world[pos] == 3):
                pos -= width
                if world[pos] == 3:
                    world[pos] = 3

            # supprime les blocks qui flotent SEUL
            if pos-width > -1:
                # verifie a gauche, droite et gauche
                # comme on vient du dessus pas besoin de verifier le dessus

                if not(world[pos] in replace_block):
                    if world[pos-width] in replace_block:
                        if world[pos+1] in replace_block:
                            if world[pos-1] in replace_block:
                                world[pos] = 3                              
                            else:
                                done = True
                        else:
                            done = True
                    else:
                        done = True
                else:
                    done = True

                if done:
                    if world[pos] == 1:
                        # si le block est seul
                        world[pos] = 8
    return world




# =========================== simulation de la lumiere =================== #

def lightSim(height,width,world,intencity):
    '''
    f( int , int , list , int ) -> list
    retourne une liste avec des intencites lumineuses bases sur l'intencite
    en argument
    '''

    # met une liste avec les resistances a la lumiere de chaque bloc
    light = []
    long = len(world)
    for i in range(long):
        if world[i] == 3: # le ciel
            light += [10]
        elif world[i] == 7: # l'eau
            light += [50]
        else: # tout le reste, c'est a dire le sol
            light += [100]

    for i in range(width):
        # regarde tout les blocs en de haut en bas et de gauche a droite
        pos = long - (i+1)
        light[pos] = intencity

        pos = long - (i+1) - width
        for j in range(height - 1):
            # recupere les intencites des block autoure
            val = []
            if (pos < long-width):
                # au dessus
                val += [light[pos+width]]


            if (pos%width != height-1):
                # a gauche
                val += [light[pos+1]]

            maxi = 0
            # prend la plus grande valeur
            for k in val:
                if k > maxi:
                    maxi = k

            # soustrait la resistance du block ou l'on est
            maxi = maxi - light[pos]
            light[pos] = maxi
                
            # continue en dessous
            pos -= width

            
    return light





# ======================== Pour l'interface avec turtle =================== #
def showLight():
    '''
    reaffiche la map avec la lumiere
    '''
    # quand l'utilisateur appui sur 's'
    global world_glob, light_glob
    turtle.goto(0,0)
    turtle.color('white')
    turtle.write(f'Attendez un petit peu svp (temps estimer: {draw_time}s)',align='center')
    showMap(height_glob,width_glob,600,600,world_glob,light_glob,2000)

def hideLight():
    '''
    reaffiche la map sans la lumiere
    '''
    # quand l'utilisateur appui sur 'h'
    global world_glob,height_glob,width_glob
    turtle.goto(0,0)
    turtle.color('white')
    turtle.write(f'Attendez un petit peu svp (temps estimer: {draw_time}s)',align='center')
    showMap(height_glob,width_glob,600,600,world_glob,False,2000)


def generateMap():
    '''
    demande la hauteur et largeur pour regenerer la map
    '''
    # importe les variables globales necessaires
    global world_glob,light_glob,height_glob,width_glob,draw_time

    inp = input('Etes vous sûr de vouloir regénérer la map \n(vous perdrez celle précédement générer) [oui/non]\n')
    if inp.lower() not in ['yes','y','oui','o']:
        return None
    
    correct = True

    # repete tant que l'enter n'est pas bonne
    while correct:
        # prend la largeur
        width = input(f'entez la largeur de la map (200 - 1000) (laissez vide pour garder : {width_glob}) :\n')

        # prend la hauteur
        height = input(f'entez la hauteur de la map (200 - 1000) (laissez vide pour garder : {height_glob}) :\n')

        # verifi si on ne garde pas les memes valeurs
        if width == '':
            width = width_glob
        if height == '':
            height = height_glob

        # verifie que l'entre est correct (un entier entre 200 et 1000)
        try:
            height = int(height)
            width = int(width)
            if height < 1001 and height > 199:
                if width < 1001 and width > 199:
                    # les valeurs sont correct
                    correct = False
        except:
            # les valeurs ne sont pas correct
            print('les valeurs que vous avez entrez ne sont pas valide')
            correct = True



    parametre = {'dirt-stone deep':True,
                         'caves':True,
                         'deep-cave':True,
                         'sky':True,
                         'water':True,
                         'grass':True,
                         'light':True}
    
    inp = input('Voulez vous des paramètres supplémentaires ? [oui/non]\n')
    if inp.lower() in ['yes','y','oui','o']:
        # permet d'avoir des parametres supplementaire
        
        inp = input('Voulez vous des grottes (par default : oui)? [oui/non]\n')
        if inp.lower() not in ['yes','y','oui','o']:
            parametre['caves'] = False
            parametre['deep-cave'] = False

        inp = input("Voulez vous de l'eau (par default : oui)? [oui/non]\n")
        if inp.lower() not in ['yes','y','oui','o']:
            parametre['water'] = False

        inp = input("Voulez vous de l'herbe (par default : oui)? [oui/non]\n")
        if inp.lower() not in ['yes','y','oui','o']:
            parametre['grass'] = False


    # affiche a l'ecran
    print('génération en cours - Merci de patienter -')
    height_glob = height
    width_glob = width
    turtle.goto(0,0)
    turtle.color('white')
    turtle.write(f'Veuillez patienter svp',align='center')
    turtle.goto(0,-20)
    turtle.color('white')
    turtle.write('génération en cours...',align='center')

    # genere le monde
    world_glob,light_glob = generate(height_glob,width_glob,2000,parametre)
    t = time.time()
    
    # dessine le monde
    showMap(height_glob,width_glob,600,600,world_glob,light_glob,2000)
    draw_time = round(time.time() - t)
    

if __name__ == '__main__':

    width_glob = 200
    height_glob = 200

    t = time.time()
    
    print('génération en cours...')
    # genere la map et la lumiere
    world_glob,light_glob = generate(height_glob,width_glob,2000)
    t_g = time.time()
    
    print('génération : OK')
    print('en train de dessiner...')# dessine la map avec la lumiere
    showMap(height_glob,width_glob,600,600,world_glob,light_glob,2000)
    print('dessin : OK')
    draw_time = round(time.time() - t_g)

    # affiche des infos
    print(f'temps de génération : {round(t_g - t)}s temps a dessiner : {draw_time}s (total : {round(t_g - t) + draw_time}s)')
    print(" -i- Appuyez sur [h] pour enlever la lumiere et sur [s] pour l'afficher -i-")
    print(" -i- avec [r] vous pouvez regénérer une map -i-")


    # regarde si l'utilisateur appui sur 's', 'h' ou 'r'
    turtle.listen()
    
    turtle.onkey(showLight,'s')
    turtle.onkey(hideLight,'h')
    turtle.onkey(generateMap,'r')
    turtle.mainloop()
    
