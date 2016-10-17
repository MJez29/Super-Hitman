#ADD HEADER COMMENTS

from pygame import *
from math import *
from random import *
import glob

#-------------------Functions For The Loading Screen--------------------
def fadeIn(surface,logo):
    "Screen starts black and image slowly gains colour"
    for i in range(255//4):
        surface.blit(logo,(0,0))
        layer=Surface((surface.get_width(),surface.get_height()))
        layer.set_alpha(255-i*4)
        surface.blit(layer,(0,0))
        display.flip()

def fadeOut(surface,logo):
    "Image loses colour and fades to black"
    for i in range(255//4):
        surface.blit(logo,(0,0))
        layer=Surface((surface.get_width(),surface.get_height()))
        layer.set_alpha(i*4)
        surface.blit(layer,(0,0))
        display.flip()

#---------------------VARIABLES THAT DO NOT CHANGE----------------------

resx,resy = 1280,720 #resolution size
cx,cy = resx//2,resy//2 #center coordinates, also half size of resolution
#The above actually change (ssshhhh dont tell anyone!) but they arent constantly
#changing. The only reason they are priviledged to be here is because they're
#needed in the next line :P
screen=display.set_mode((resx,resy),HWSURFACE|DOUBLEBUF|RESIZABLE)

font.init()


#---weapons---
#contains all weapon information
#(weapon image names (idle and firing), number of bullets fired per shot,rate of fire (the lower it is,
#the faster the gun shoots), damage per bullet)
weapons = [((image.load('Player\m161.png'),image.load('Player\m162.png')),1,10,10),
           ((image.load('Player\dualPistols1.png'),image.load('Player\dualPistols2.png')),2,30,20),
           ((image.load('Player\shotgun1.png'),image.load('Player\shotgun2.png')),5,60,15)]
           #((image.load("pistol1.png"),image.load("pistol2.png"),1,30,20)]
#---Creating the lists of the reloading images---

#shotgun reloading sprites:
shotgunReload=[]
for i in range(6):
    shotgunReload.append(image.load("Player\shotgunR%d.png"%(i+1)))
shotgunReload=tuple(shotgunReload) #tuples are cooler

#M16 reloading sprites:
M16Reload=[]
for i in range(6):
    M16Reload.append(image.load("Player\m16R%d.png"%(i+1)))
M16Reload=tuple(M16Reload) #tuples are cooler

"""#Pistol reloading sprites:
pistolReload=[]
for i in range(6):
    pistolReload.append(image.load("Player\pistolR%d.png"%(i+1)))
pistolReload=tuple(pistolReload) #tuples are cooler
"""

#Dual pistol reloading sprites:
DPReload=[]
for i in range(6):
    DPReload.append(image.load("Player\dualPistolsR%d.png"%(i+1)))
DPReload=tuple(DPReload) #tuples are cooler

#list of reloading lists:
reloadList=[M16Reload,DPReload,shotgunReload]
#---

meleeList = [('boomerang',image.load('Player\Boomerang.png')),
             ('grenade',[image.load('Player\grenade1.png'),image.load('Player\grenade2.png'),
                         image.load('Player\grenade3.png'),image.load('Player\grenade4.png'),
                         image.load('Player\grenadeT1.png')])] #list of secondary weapon names/sprites
sprites = []
for i in range(6):
    sprites.append(image.load('Player\knife%d.png'%i))
meleeList.append(sprites)
meleeList[2] = ('knife',meleeList[2])

explosions = glob.glob('Player\Explosion\*.png')
explosions.sort()

clip = 1000 #starting number of bullets of each clip
bLen = 20 #bullet length
bWid = 7 #bullet width
#dynamicView = True #setting for if dynamic view is turned on/off (will finish if we have time)
viewDelay = 8 #reduction of aim sensitivity
myClock = time.Clock()
peacefulSprites=[(image.load("Civilians\peaceful AI-1.png"),image.load("Civilians\peaceful AI-1-shot.png"))]
#list of images for peaceful ai sprites
maxCoinDrop=101 #the most $ that an AI can drop
minCoinDrop=1 #the least $ that an AI can drop
fadeSpeed=2 #speed at which onscreen info about pickups fade away
slowMoTime = 7 #number of seconds slow motion is active per use
minSpeed = 1 #lowest speed allowed for object/player/enemy movement in slow motion
defaultBSpeed = 20 #default bullet speed
grenadeDistPerc = 7 #percentage of wanted distance already traveled on first bounce divided by 10
grenadeSpeedCutback = 2 #grenade speed is reduce by this number on second bounce
enemySpritesPistol=[] #list on enemy sprites that carry a pistol
gunNames=["M16","Dual Pistols","Shotgun"] #names of guns
for i in range(3):
    enemySpritesPistol.append((image.load("Enemies\e%sPistols1.png"%(str(i+1))),
                                image.load("Enemies\e%sPistols2.png"%(str(i+1)))))

enemySpritesM16=[]
for i in range(3):
    enemySpritesM16.append((image.load("Enemies\e%sm161.png"%(str(i+1))),
                            image.load("Enemies\e%sm162.png"%(str(i+1)))))

enemySpritesShotgun=[]
for i in range(3):
    enemySpritesShotgun.append((image.load("Enemies\e%sshotgun1.png"%(str(i+1))),
                            image.load("Enemies\e%sshotgun2.png"%(str(i+1)))))

#---Shooter AI Constants---
ammoPistol=36
healthPistol=randint(10,300)
#for each weapon list : [number of bullets per shot,rate of fire,damage per bullet]
pistol=[1,60,20,enemySpritesPistol]
m16=[1,10,15,enemySpritesM16]
shotgun=[5,60,10,enemySpritesShotgun]
weaponsAI=[m16,pistol,shotgun]
AIammo=100
shooterHealth=100
magazine=image.load("ammo magazine.png")

#---player constants---
knifeDmg = 5 #damage X 12 used per swipe

#---HUD---
HUDimgHeight=50
shotgunHUD=image.load("Shotgun HUD.png")
shotgunHUD=transform.scale(shotgunHUD,(shotgunHUD.get_width()//shotgunHUD.get_height()*HUDimgHeight,HUDimgHeight))
M16HUD=image.load("M16 HUD.png")
M16HUD=transform.scale(M16HUD,(M16HUD.get_width()//M16HUD.get_height()*HUDimgHeight,HUDimgHeight))
pistolHUD=image.load("Pistol HUD.png")
pistolHUD=transform.scale(pistolHUD,(pistolHUD.get_width()//pistolHUD.get_height()*HUDimgHeight,HUDimgHeight))
HUDList=[M16HUD,pistolHUD,shotgunHUD]


#-------------------------VARIABLES THAT CAN CHANGE------------------------

running = True #flag for if program is running
count = 0
fps = 0
fpsList = []
playerSpeed = 5 #movement speed of player and AIs (same speed) (changes in slow motion)
grenadeSpeed = playerSpeed*11 #travelling speed of grenade
sprSpeed = 0.5 #speed of melee attacks
reloadingSpeed = 0.1 #speed of reloading
AIspeed = playerSpeed #enemy ai speed
civSpeed = 2 #civilian speed
bSpeed = 20 #bullet speed
w = 0 #selected weapon can change by changing this variable
n = 1 #selected secondary weapon can change by changing this variable
weapon = weapons[w] #selected weapon inside weapon list
bulletList = [] #list of active bullets in play in the game
shot = False #flag checking if player is currently shooting
bCol = (218,165,32) #bullet colour
bRicochet = True #flag for if bullet ricochets of walls is active
delay = 0 #counter keeping track of current frame number (0-29)
secDelay = 0 #counter for secondary weapon sprites
grenadeDelay = 0 #counter for grenade image sprites
grenadeDefDist = 300 #longest length of grenade throw
grenadeAng = 0 #angle grenade travels at
grenadeRot = 0 #grenade image default rotation
grenadeFuse = 3 #number of seconds grenade takes to blow up
explosionSpr = image.load(explosions[0]) #default explosion sprite
blastRad = 200 #grenade blast radius
impactTime = False #moment when grenade damage is applied
explosion = False
grenadeIdle = False #flag for if grenade is idle on ground
grenade2 = False #flag for second bounce of grenade
throw = False #flag for if grenade is thrown or not
grenx = 0 #default coordinates of grenade
greny = 0
grenDmg = 1.5 #max grenade damage (itself multiplied by grenade damage radius) at the centre of grenade explosion
peacefulAIList=[] #list of active civilians on screen
civHealth = 100
cur_x = 0 #default player coordinates in accordance to map
cur_y = 0
coinList=[] #the positions of dropped money by AIs and how much each is worth
money=0 #the amount of money that the player has
collectedCoinList=[] #list of coins that have been collected
#purpose is to display the amount for a little while after it has been collected
melSpr = image.load('Player\knife1.png') #default melee sprite
secondary = False #flag for if player is using secondary weapon or not
knife = False #flag for if player is knifing or not
dmgTip = (0,0) #default melee knife tip used for damage
deadList=[]
shooterAIList=[]
droppedClipList=[] #the list of ammo clips dropped by dead enemies
collectedClipList=[] #the list of ammo clips collected by the player
para = False #flag for slow motion and counter used for parabola
grenade = False #flag for if grenade is thrown for the first time or not
c = -1 #counter for bullet time

#---gun ammo---
M16ammo=37
M16clip=20
DPammo=1000
DPclip=24
shotgunammo=1000
shotgunclip=50
reloadingFrame=0
hasReloaded=True
reloading=False
ammoList=[M16ammo,DPammo,shotgunammo]
clipList=[M16clip,DPclip,shotgunclip]



#---------------------------------FONT--------------------------------------
#---money---
moneyFontHeight=50
moneyFontCol=(0,255,0)
moneyFont=font.SysFont("impact",moneyFontHeight)
#---collected coin text---
collectedCoinFontHeight=40
collectedCoinFontCol=(255,255,0)
collectedCoinFont=font.SysFont("impact",collectedCoinFontHeight)
#---text blitted when u are near enough to enter the gun store---
enterFontHeight=60
enterFontCol=(0,0,255)
enterFont=font.SysFont("impact",enterFontHeight)
enterText=enterFont.render("E to enter",True,enterFontCol)

#---blitting ammo left in clip---
ammoInClipFontHeight=50
ammoInClipFontCol=(0,0,0)
ammoInClipFont=font.SysFont("impact",ammoInClipFontHeight)
ammoInClipFontDict={"col":ammoInClipFontCol,"font":ammoInClipFont}

#---total ammo---
ammoFontHeight=30
ammoFontCol=(255,255,255)
ammoFont=font.SysFont("impact",ammoFontHeight)
ammoFontDict={"col":ammoFontCol,"font":ammoFont}

#---collected clips text---
collectedClipFontHeight=40
collectedClipFontCol=(255,255,255)
collectedClipFont=font.SysFont("impact",collectedClipFontHeight)
collectedClipFontDict={"col":collectedClipFontCol,"font":collectedClipFont}


#----------------------------------MAP--------------------------------------
#loads all map images

collide = image.load("Game Maps\Collide Check.png").convert()
horizontal = image.load("Game Maps\Horizontal Check.png").convert()
#top=image.load("Top of Map.png")
#bottom=image.load("Background of Map.png").convert_alpha()
gameMap=image.load("Game Maps\Game Map.png").convert()
#gameMapCopy=gameMap.copy()
coin=image.load("Coin.png")
#"""
gunStoreImg=image.load("Game Maps\Gun store.png").convert() #the actual gun store img
width=gunStoreImg.get_width()+screen.get_width()
height=gunStoreImg.get_height()+screen.get_height()
gunStore=Surface((width,height)) #actual surface that the player will see
#larger than actual img because if the player is in a corner, they can see outside the actual
#image
gunStore.fill((0,0,0))
gunStore.blit(gunStoreImg,(screen.get_width()//2,screen.get_height()//2))

gunStoreCollideImg=image.load("Game Maps\Gun store collide check.png").convert() #the actual gun store img
gunStoreCollide=Surface((width,height)) #will see
#larger than actual img because if the player is in a corner, they can see outside the actual
#image
gunStoreCollide.fill((0,0,0))
gunStoreCollide.blit(gunStoreCollideImg,(screen.get_width()//2,screen.get_height()//2))
#"""

#---------------------------------SOUNDS------------------------------------
mixer.init()
m16Sound="Sounds\Assault Rifle.wav" #sound filenames
shotgunSound="Sounds\Old School Shotgun.wav"
pistolSound="Sounds\Pistol.wav"
weaponSounds=[m16Sound,pistolSound,shotgunSound,pistolSound] #list of gun sounds to be used
mixer.music.load(weaponSounds[w]) #mixer.Sound doesnt work well in the setting of our game
#so we use mixer.music instead
#---------------------------------CLASSES-----------------------------------

class Player:
    '''Player keeps track of:

    x,y - current position
    ang - current angle the Player is facing in degrees
    pic1 - sprite to display when not moving
    pic2 - sprite to alternate to when firing
    fire - flag for if the player is shooting
    money - the amount of money they start off with
    '''

    def __init__(self,x,y,ang,pic1,pic2,money,reloadSpeed,reloadingSprites=None,ammo=0,clipSize=1,reloadingFrame=0,reloading=False,hasReloaded=True):

        self.x = x
        self.y = y
        self.ang = ang
        self.pic1 = pic1
        self.pic2 = pic2
        self.fire = False
        self.money=money
        self.reloadingSprites=reloadingSprites
        self.reloading=reloading
        self.reloadingFrame=reloadingFrame
        self.reloadSpeed = reloadSpeed
        self.ammo=ammo
        self.clipSize=clipSize
        self.hasReloaded=hasReloaded
        self.ammoInClip=self.ammo%self.clipSize
        #print(len(self.reloadingSprites))

    def weaponChange(self,pic1,pic2,reloadingSprites,ammo,clipSize):
        self.pic1=pic1
        self.pic2=pic2
        self.reloadingSprites=reloadingSprites
        self.reloading=False
        self.hasReloaded=True
        self.reloadingFrame=0
        self.ammo=ammo
        self.clipSize=clipSize
        self.ammoInClip=self.ammo%self.clipSize

    def rotate(self,destX,destY,hScreenX,hScreenY):
        '''Player angle changes based on mouse coordinates'''

        moveX = destX - hScreenX
        moveY = destY - hScreenY
        self.ang = degrees(atan2(-moveY, moveX))

    def collectMoney(self,coinList,coin,collectedCoinList):
        """Checks to see if the player comes in contact with any coins laying on the ground
        If he does then he picks them up (obviously)"""
        for curCoin in coinList:
            if distance((player.x,player.y),curCoin[0])<=coin.get_width()//2+40: #width and height of coin are ==
                player.money+=curCoin[1] #the players money total increases based on the coins amount
                collectedCoinList.append((curCoin[0],curCoin[1],255)) #255 is the alpha that it
                                                      #will be blitted at
        for c in collectedCoinList:
            try :
                coinList.remove((c[0],c[1])) #removes the collected coins
            except ValueError: pass #occurs if the item has already been erased

    def collectAmmo(self,droppedClipList,collectedClipList,ammoList,w):
        "Collects any ammo if the player walks over any dropped magazines"
        ammoList[w]=self.ammo #updates ammoList
        for clip in droppedClipList: #for every clip on the ground
            if distance((player.x,player.y),clip[0])<=60: #if the player is pretty close to it
                ammoList[clip[2]]+=clip[1] #bullets added to total
                collectedClipList.append((clip[0],clip[1],clip[2],255))
                self.reloading=False
                self.hasReloaded=True
                self.reloadingFrame=0

        for c in collectedClipList: #removes collected magazines
            #print(c)
            for i in range(360):
                try:
                    droppedClipList.remove((c[0],c[1],c[2],i))
                except ValueError: pass
        self.ammo=ammoList[w] #updates player's ammo info
        self.ammoInClip=self.ammo%self.clipSize
        if w==1 and self.ammo%2!=0: #if the player has dual pistols
            #and they collected an odd number of bullet
            self.ammo-=1 #makes it even

    def draw(self,surface,delay,mb,secondary,meleeDelay,secWeap,meleeSprite,mx,my,cx,cy,):
        '''Player is rotated/drawn based on angle coordinates. If he is
        shooting, the sprite drawn alternates between the idle and firing
        sprites (pic1 and pic2)'''
        #self.rotate(mx,my,cx,cy)
        #print(self.ang)
        if self.ammo%self.clipSize==0 and self.hasReloaded==False and self.ammo>0: #if a clip is empty and hasnt been reloaded yet
            self.reloading=True
        if self.ammo%self.clipSize!=0: #if it doesnt need to be reloaded
            self.hasReloaded=False
        if self.hasReloaded: #if it has been reloaded it doesnt need to reload anymore
            self.reloading=False

        if self.hasReloaded==True and self.ammoInClip==0 and self.ammo>0:
            self.ammoInClip=self.clipSize

        if self.reloading==True: #if its reloading
            newpic=transform.rotate(self.reloadingSprites[int(self.reloadingFrame)],self.ang+270)
            surface.blit(newpic,getCentre(newpic,surface.get_width()//2,surface.get_height()//2))
            self.reloadingFrame += self.reloadSpeed #slows the speed at which the reloading frames are cycled through
            if self.reloadingFrame>6:
                self.reloadingFrame=0
                self.hasReloaded=True #done reloading

        else:
            if secondary:
                if secWeap == 'knife' or secWeap == 'grenade':
                    newPic = transform.rotate(meleeSprite,self.ang+270)
            else:
                if mb[0]==1 and delay % weapon[2] == 0 or mb[0]==1 and (delay-1) % weapon[2] == 0 or mb[0]==1 and (delay-2) % weapon[2] == 0:
                    newPic = transform.rotate(self.pic2,self.ang+270)
                else:
                    newPic = transform.rotate(self.pic1,self.ang+270)
            surface.blit(newPic,getCentre(newPic,surface.get_width()//2,surface.get_height()//2))

class Bullet:
    '''Bullet keeps track of:

    ex,ey - current end position
    tx,ty - current tip position
    ang - current angle bullet is going from player when it was shot in radians
    damage - the amount of damage that a bullet deals
    '''

    def __init__(self,ex,ey,tx,ty,ang,damage):

        self.ex = ex
        self.ey = ey
        self.tx = tx
        self.ty = ty
        self.ang = ang
        self.damage=damage

    def move(self,speed,length):
        '''finds the bullet end's and tip's next coordinates by using trig and
        the set distance and length of the bullet (which can be changed easily)'''

        self.ex, self.ey = self.tx + cos(self.ang) * (speed-length), self.ty - sin(self.ang) * (speed-length)
        self.tx, self.ty = self.tx + cos(self.ang) * speed, self.ty - sin(self.ang) * speed


    def draw(self,surface,player,width,bulCol):
        '''draws bullet using it's end and tip coordinates'''
        if fitOnscreen(surface,(player.x,player.y),(self.tx,self.ty)):
            new_tx=surface.get_width()//2-(player.x-self.tx)
            new_ex=surface.get_width()//2-(player.x-self.ex)
            new_ty=surface.get_height()//2-(player.y-self.ty)
            new_ey=surface.get_height()//2-(player.y-self.ey)
            draw.line(surface,bulCol,(new_tx,new_ty),(new_ex,new_ey),width)

class peacefulAI:
    """The peaceful AI keeps track of:

    x,y - current position
    sprite - sprite of the AI
    direction - direction headed (North, East, South, West or None if stationary)
    health - current amount of health
    maxHealth - default amount of starting health
    money - the amount of money that they are carrying
    shot - whether they have just been shot
    count - serves as a count for when the ai is hit to display the shot sprite
    """

    def __init__(self,x,y,sprites,direction,health,money):
        self.x=x
        self.y=y
        self.direction=direction
        self.sprite=sprites[0] #the original sprite
        self.spriteShot=sprites[1]
        self.rotated=self.sprite #self.sprite in its rotated form
        self.rotatedShot=self.spriteShot
        self.health=health
        self.maxHealth=health #the amount of health they start off with
        self.money=money
        self.shot=False
        self.count=0


    def move(self,speed):
        """Moves the civilian
        There is a 4 in 250 chance that the AI will change directions
        the remaining chance will make the AI continue in the same direction
        """
        num=randint(1,250)
        directions = ['North','East','South','West','None']
        for i in range(5):
            if num-1 == i:
                self.direction = directions[i]

        if self.direction=="North" and collide.get_at((self.x,self.y-2))[:3]!=(0,0,0):
                self.y -= speed #moves AI in set direction if possible
        elif self.direction=="East" and collide.get_at((self.x+2,self.y))[:3]!=(0,0,0):
                self.x += speed
        elif self.direction=="South" and collide.get_at((self.x,self.y+2))[:3]!=(0,0,0):
                self.y += speed
        elif self.direction=="West" and collide.get_at((self.x-2,self.y))[:3]!=(0,0,0):
                self.x -= speed

        #---Rotation of sprite image for different directions---
        if self.direction=="South" or self.direction=="None":
            self.rotated=transform.rotate(self.sprite,0)
            self.rotatedShot=transform.rotate(self.spriteShot,0)
        elif self.direction=="East":
            self.rotated=transform.rotate(self.sprite,90)
            self.rotatedShot=transform.rotate(self.spriteShot,90)
        elif self.direction=="North":
            self.rotated=transform.rotate(self.sprite,180)
            self.rotatedShot=transform.rotate(self.spriteShot,180)
        elif self.direction=="West":
            self.rotated=transform.rotate(self.sprite,270)
            self.rotatedShot=transform.rotate(self.spriteShot,270)

    def draw(self,surface,player):
        """
        Blits the civilian onto the screen and draws health bar
        """
        sx=surface.get_width()//2-(player.x-self.x) #x-coordinate relative to the screen
        sy=surface.get_height()//2-(player.y-self.y) #y-coordinate relative to the screen
        if self.shot==True: #if he is being shot
            self.count+=0.2 #adds to the count
            if self.count==1:
                self.shot=False #if the shot sprite has been blitted for the correct
                #number of frames, then it reverts to the original state
                self.count=0
            surface.blit(self.rotatedShot,getCentre(self.rotatedShot,sx,sy))
        else :
            surface.blit(self.rotated,getCentre(self.rotated,sx,sy))

        width=int(self.rotated.get_width()/self.maxHealth*self.health) #width will be the
        #same whether it is self.rotated of self.rotatedShot
        height=10
        col=(255-int(width*2.5),5+int(width*2.5),0)
        draw.rect(surface,col,(sx-self.rotated.get_width()//2, #draws health bar
                                   sy-self.rotated.get_height()//2-10,
                                   width,height))

    def rectangle(self):
        """
        Returns the rectangular area that the sprite covers
        Used for collision detection
        """
        return Rect(self.x-self.rotated.get_width()//2,self.y-self.rotated.get_height()//2,
                    self.rotated.get_width(),self.rotated.get_height())

    def reduceHealth(self,bulDamage):
        'Reduces the AIs health based on how much damage the bullet deals'
        self.health -= bulDamage
        self.shot=True

class enemyShooter:
    """
    This is the class for the AI enemies that shoot at the player
    x - x coordinate of the enemy
    y - y coordinate of the enemy
    regSprite - sprite of the enemy when they are not shooting their gun
    shootingSprite - sprite when they are shooting their gun
    player - the class for the player
    ang - the angle they are facing in degrees
    dist - distance from the player
    weapon - the weapon that they are carrying
    rotatedReg/rotatedShoot - the rotated versions of the sprites
    shot - if they are shooting or not
    ammo - the amount of ammo they have
    """
    def __init__(self,x,y,player,ang,weapon,speed,health,ammo):
        self.x=x
        self.y=y

        self.regSprite,self.shootingSprite=choice(weapon[3])
        self.player=player
        self.rotatedReg=self.regSprite
        self.rotatedShooting=self.shootingSprite
        self.ang=ang
        self.shot=False
        self.dist=distance((self.x,self.y),(self.player.x,self.player.y))
        self.weapon=weapon
        self.ammo=weapon[2]
        self.speed=speed
        self.lastMove=(0,self.speed)
        self.delay=0
        self.prevPref=None
        self.blocked=False
        self.health=health
        self.maxHealth=health
        self.ammo=ammo
        #self.direction=
    def move(self,player,collide):
        """
        This function moves the AI
        """
        self.player=player
        self.dist=distance((self.x,self.y),(self.player.x,self.player.y))
        if blockedPath(collide,self.player,self)==True:
            self.blocked=True
            self.pathfind=Pathfind(self.player,self) #initiates the pathfinding class
            self.preferences=self.pathfind.getPreferences(self.lastMove,self.prevPref) #the preferences of the AI
            #It now runs through the preferences, doing whichever it can that is closest to the top preference
            if collide.get_at((int(self.x+self.preferences[0][0]),
                               int(self.y+self.preferences[0][1])))[:3]!=(0,0,0):
                #checks to see if it is a valid move
                self.x+=int(self.preferences[0][0]) #if it is, then it moves it
                self.y+=int(self.preferences[0][1])

            elif collide.get_at((int(self.x+self.preferences[1][0]),
                                 int(self.y+self.preferences[1][1])))[:3]!=(0,0,0):
                #2nd preference
                self.x+=int(self.preferences[1][0])
                self.y+=int(self.preferences[1][1])

            elif collide.get_at((int(self.x+self.preferences[2][0]),
                                 int(self.y+self.preferences[2][1])))[:3]!=(0,0,0):
                #3rd preference
                self.x+=int(self.preferences[2][0])
                self.y+=int(self.preferences[2][1])

            elif collide.get_at((int(self.x+self.preferences[3][0]),
                                 int(self.y+self.preferences[3][1])))[:3]!=(0,0,0):
                #4th preference
                self.x+=int(self.preferences[3][0])
                self.y+=int(self.preferences[3][1])

            self.prevPref=self.preferences
            self.ang=self.ang=degrees(atan2(-(self.player.y-self.y),self.player.x-self.x))
            #AI always faces the player, for some reason, having them face the way they are moving
            #makes it look like they are spazzing out

        else:
            self.blocked=False #since they are no longer blocked
            if self.dist>350: #If they are a decent way away from the player, they B-line towards him
                #---Code from FP Basics Eg 4.py---
                #that has been modified to fit into our program
                dist=max(self.dist,1)
                moveX=(self.player.x-self.x)*ai.speed/dist #distance along the X-axis they move
                moveY=(self.player.y-self.y)*ai.speed/dist #distance along the Y-axis they move
                self.ang=degrees(atan2(-moveY,moveX))
                if collide.get_at((int(self.x+moveX),int(self.y+moveY)))[:3]!=(0,0,0):
                    #If they arent walking into a wall, then they can go there
                    self.x+=moveX
                    self.y+=moveY
            elif self.dist<250:
                #If the player gets too close to the AI, then it backs away from him
                #Its just has them B-line away from the player
                #Its pretty simple but it makes the player have to work harder for those melee kills
                dist=max(self.dist,1)
                moveX=(self.player.x-self.x)*ai.speed/dist
                moveY=(self.player.y-self.y)*ai.speed/dist
                self.ang=degrees(atan2(-moveY,moveX))
                if collide.get_at((int(self.x-moveX),int(self.y-moveY)))[:3]!=(0,0,0):
                    self.x-=moveX
                    self.y-=moveY
            else :
                #if their in their shooting hotspot then they dont move
                self.ang=degrees(atan2(-(self.player.y-self.y),self.player.x-self.x))

    def shoot(self,bulletList,weaponsAI):
        """Class that makes the AI shoot at the player"""
        if self.dist>100 and self.dist<800 and self.delay%self.weapon[1]==0 and self.blocked==False and self.ammo>0:
            #If they are in or close to their shooting hotspot
            #and they've waited long enough to shoot again
            #and their path to the player isnt blocked
            self.shot=True
            for i in range(self.weapon[0]):
                bull=makeBullet(self.ang,weaponsAI.index(self.weapon),i,(self.x,self.y),self.weapon[2])
                bulletList.append(Bullet(bull[0],bull[1],bull[2],bull[3],bull[4],bull[5]))
                self.ammo-=1
            #adds the bullet(s) they shoot to the bullet list
        if self.delay==59:
            self.delay=0 #resets their delay
        else :
            self.delay+=1 #adds 1 to their delay each frame



    def draw(self,surface):
        sx=surface.get_width()//2-(player.x-self.x) #x-coordinate relative to the screen
        sy=surface.get_height()//2-(player.y-self.y) #y-coordinate relative to the screen
        if self.shot==True:
            #blits their shooting sprite if they are shooting
            self.rotatedShooting=transform.rotate(self.shootingSprite,self.ang-90)
            if fitOnscreen(surface,(self.player.x,self.player.y),(self.x,self.y)):
                surface.blit(self.rotatedShooting,getCentre(self.rotatedShooting,sx,sy))
            self.shot=False
        else : #blits their normal sprite otherwise
            self.rotatedReg=transform.rotate(self.regSprite,self.ang-90)
            if fitOnscreen(surface,(self.player.x,self.player.y),(self.x,self.y)):
                surface.blit(self.rotatedReg,getCentre(self.rotatedReg,sx,sy))

        #---Health Bar---
        width=int(self.regSprite.get_width()/self.maxHealth*self.health) #width will be the
        #same whether it is self.rotated of self.rotatedShot
        height=10
        col=(255-int(width*2.5),5+int(width*2.5),0)
        draw.rect(surface,col,(sx-self.regSprite.get_width()//2, #draws health bar
                                   sy-self.regSprite.get_height()//2-10,
                                   width,height))
    def rectangle(self):
        """
        Returns the rectangular area that the sprite covers
        Used for collision detection
        """
        if self.shot==True:
            return Rect(self.x-self.rotatedShooting.get_width()//2,self.y-self.rotatedShooting.get_height()//2,
                    self.rotatedShooting.get_width(),self.rotatedShooting.get_height())
        else :
            return Rect(self.x-self.rotatedReg.get_width()//2,self.y-self.rotatedReg.get_height()//2,
                    self.rotatedReg.get_width(),self.rotatedReg.get_height())
    def reduceHealth(self,bulDamage):
        'Reduces the AIs health based on how much damage the bullet deals'
        self.health -= bulDamage


class Pathfind:
    """This class finds a path to the player
    It isnt the most effective pathfinding algorithm to find the most efficient way to
    get to Point B from Point A but it was designed 100% by us and also works well in our game
    The algorithm is adaptable if the player changes location and is also fast. It doesnt chart out
    its entire path per loop, it just charts out what would be the best to worst direction to go to get
    a step closer to its objective"""
    def __init__(self,player,ai):
        """player - player class
        ai - ai class
        There is only 1 real function in this class so it would make more sense for this to be a function
        but when we were first designing the pathfinder, we werent sure how to approach so we made it into
        a class in case we would need a lot of functions in it"""
        self.player=player #player
        self.ai=ai
        self.preferences=[]
        self.allMoves=[(0,self.ai.speed),(0,-(self.ai.speed)),(self.ai.speed,0),
                       (-(self.ai.speed),0)]

    def getPreferences(self,lastMove,prevPref):
        """Lists the order of moves (from best to worse) that should be taken to approach the player
        It returns a list with 4 tuples in it. Each tuple contains the player's next move
        to take if that is the option that is best suited for their location on the map
        """
        xDist=self.ai.x-self.player.x #positive if player is to the left of ai;
        #otherwise negative if to the right
        yDist=self.ai.y-self.player.y #positive if plaayer is above ai;
        #otherwise negative if below

        #---First Preference---
        #The first preference will be to overcome the greatest distance between the player and the ai
        #If the y-dist is larger than the x-dist, it will first try to move up; and vice versa
        if abs(xDist)>=abs(yDist): #if the x-dist is >= to the y-dist between the 2
            if self.ai.x-self.player.x>0: #if player is to the left of ai
                self.preferences.append((-(self.ai.speed),0)) #adds their next move (their speed to the direction
                #that they need to go)
            else : #if player is to the right of the ai
                self.preferences.append((self.ai.speed,0))
        else : #y-dist > x-dist
            if self.ai.y-self.player.y>0: #if the player is above the ai
                self.preferences.append((0,-(self.ai.speed)))
            else : #if the player is below the ai
                self.preferences.append((0,self.ai.speed))

        #---Second Preference---
        #The 2nd preference cannot be to move the opposite direction from pref 1
        #so if the first is to move a dist horizontally, then the 2nd will be to move vertically
        if self.preferences[0][0]==0: #if pref 1 is moving vertically
            if xDist>0: #if the player is to the left of AI
                self.preferences.append((-(self.ai.speed),0))
            else : #if player to AI's right
                self.preferences.append((self.ai.speed,0))
        else : #if pref 1 is moving horizontally
            if yDist>=0: #if player is above AI
                self.preferences.append((0,-(self.ai.speed)))
            else: #if player is below AI
                self.preferences.append((0,self.ai.speed))

        #---Last Preference (last preference is needed to determine
        #second last preference)---
        #The last preference is the reverse of the move that they just did
        if (lastMove[0]*(-1),lastMove[1]*(-1)) not in self.preferences:
            self.preferences.append((lastMove[0]*(-1),lastMove[1]*(-1)))

        #---Third Preferences---
        #Third preference is just what isnt in the self.preferences list
        for move in self.allMoves:
            if move not in self.preferences:
                self.preferences.insert(2,move)

        #After analyzing self.preferences when bugs occur, the following if statements try to correct most of the bugs
        #involved in pathfinding
        #We're not 100% sure why pathfinding has some bugs but all we know is that this fixes most of them

        try:
            if (prevPref[0]==self.preferences[0] and
                prevPref[1][0]==self.preferences[1][0]*(-1) and
                prevPref[1][1]==self.preferences[1][1]*(-1) and
                prevPref[2]==self.preferences[2] and
                prevPref[3][0]==self.preferences[3][0]*(-1) and
                prevPref[3][1]==self.preferences[3][1]*(-1)):
                self.preferences=prevPref
        except TypeError: pass #error is raised the 1st time it is the function is called
        #for an AI because they dont have a previous preference so it starts at None, which will
        #raise an error

        try:
            if (prevPref[0]==self.preferences[0] and
                  prevPref[1][0]==self.preferences[1][0]*(-1) and
                  prevPref[1][1]==self.preferences[1][1]*(-1) and
                  prevPref[2][0]==self.preferences[2][0]*(-1) and
                  prevPref[2][1]==self.preferences[2][1]*(-1) and
                  prevPref[3]==self.preferences[3]):
                  self.preferences=prevPref
        except TypeError: pass #error is raised the 1st time it is the function is called
        #for an AI because they dont have a previous preference so it starts at None, which will
        #raise an error

        try:
            if (prevPref[0][0]==self.preferences[0][0]*(-1) and
                prevPref[0][1]==self.preferences[0][1]*(-1) and
                prevPref[1]==self.preferences[2] and
                prevPref[2][0]==self.preferences[2][0]*(-1) and
                prevPref[2][1]==self.preferences[2][1]*(-1) and
                prevPref[3]==self.preferences[3]):
                self.preferences=prevPref
        except TypeError: pass #error is raised the 1st time it is the function is called
        #for an AI because they dont have a previous preference so it starts at None, which will
        #raise an error

        return self.preferences #the preferences of the player at that given frame






#--------------------------------------FUNCTIONS-------------------------------------

def makePeacefulAI(screen,mainMap,collide,player,peacefulSprites,health,maxCoinDrop,minCoinDrop):
    'Makes a peaceful AI by accepting surface, map, player, different civilian sprites and starting health'
    money=randint(minCoinDrop,maxCoinDrop) #the amount of money they drop
    if money==maxCoinDrop:
        """If the maxCoinDrop is chosen, then the AI will carry a large amount of money,
        which can vary from 1-4 times the maxCoinDrop value"""
        money=maxCoinDrop*randint(1,4)
    x_pos,y_pos = 0,0
    while collide.get_at((x_pos,y_pos))==(0,0,0) or fitOnscreen(screen,(player.x,player.y),(x_pos,y_pos))==True:
        x_pos = randint(screen.get_width()//2,mainMap.get_width()-screen.get_width()//2) #A random position available
        y_pos = randint(screen.get_height()//2,mainMap.get_height()-screen.get_height()//2) #for a civilian to spawn
    direction = choice(["North","South","East","West","None"]) #on and first direction is created
    sprites = choice(peacefulSprites) #random civilian sprite is chosen for civilian
    return (x_pos,y_pos,sprites,direction,health,money)

def makeShooterAI(screen,mainMap,collide,player,weapon,health,speed,ammo):
    """Makes the AI for a enemy that can shoot at you
    Requires the screen that it will be blitted onto, the game map, the collide map
    the player class to check their position relative to him, which weapon they are to use
    their predetermined amount of health and their movement speed
    """
    x_pos,y_pos=0,0 #needs to be a position where its position on
    #the collide map will be black
    while collide.get_at((x_pos,y_pos))==(0,0,0) or fitOnscreen(screen,(player.x,player.y),(x_pos,y_pos))==True:
        #while it is spawning on a building or will be on the player's current screen
        x_pos = randint(screen.get_width()//2,mainMap.get_width()-screen.get_width()//2) #A random position available
        y_pos = randint(screen.get_height()//2,mainMap.get_height()-screen.get_height()//2) #for them to spawn offscreen
    MoveX=x_pos-player.x
    MoveY=y_pos-player.y
    ang=degrees(atan2(-MoveY,MoveX)) #the angle that they spawn facing
    return (x_pos,y_pos,player,ang,weapon,speed,health,ammo)


def distance(p1,p2):
    'Simple distance formula'
    return hypot(p2[0]-p1[0],p2[1]-p1[1])

def erase(player,peacefulAIlist,bulletList,coinList,deadList,damageTip,secondary,secWeap,knifeDamage,droppedClipList,
          weaponsAI,damageRadius,grenadeDamage,grenadex,grenadey,damageTime,reflection,collide,horizCollide):
    'Checks to see which bullets/AIs should be removed'
    bList,pList,sList = [],[],[]
    for ai in peacefulAIlist:
        for bullet in bulletList:
            if ai.rectangle().collidepoint(bullet.tx,bullet.ty):
                ai.reduceHealth(bullet.damage) #decreases ai health if shot
                bList.append(bullet)
        if secondary:
            if secWeap == 'knife':
                if ai.rectangle().collidepoint(damageTip)==True:
                    ai.reduceHealth(knifeDamage)
        if damageTime and distance((ai.x,ai.y),(grenadex,grenadey)) <= damageRadius:
            ai.reduceHealth(grenadeDamage*(damageRadius+1-distance((ai.x,ai.y),(grenadex,grenadey))))
        if ai.health<1:
            pList.append(ai)
            coinList.append(((ai.x,ai.y),ai.money))
            deadList.append(((ai.x,ai.y),ai.rotatedShot,255))
    for ai in shooterAIList:
        for bullet in bulletList:
            if ai.rectangle().collidepoint(bullet.tx,bullet.ty):
                ai.reduceHealth(bullet.damage) #decreases ai health if shot
                bList.append(bullet)
        if secondary:
            if secWeap == 'knife':
                if ai.rectangle().collidepoint(damageTip)==True:
                    ai.reduceHealth(knifeDamage)
        if damageTime and distance((ai.x,ai.y),(grenadex,grenadey)) <= damageRadius:
            ai.reduceHealth(grenadeDamage*(damageRadius+1-distance((ai.x,ai.y),(grenadex,grenadey))))
            print(ai.health)
            print(grenadeDamage*(damageRadius-distance((ai.x,ai.y),(grenadex,grenadey))))
        if ai.health<1:
            sList.append(ai)
            #droppedClipList.append(position,amount of ammo that can be picked up, which kind of ammo, angle of rotation)
            droppedClipList.append(((ai.x,ai.y),ai.ammo,weaponsAI.index(ai.weapon),randint(0,360)))
            deadList.append(((ai.x,ai.y),ai.rotatedReg,255))
            #print(droppedClipList)

    for bullet in bulletList: #checks for collisions on the map
        if int(bullet.tx)<collide.get_width() and int(bullet.ty)<collide.get_height():
            if collide.get_at((int(bullet.tx),int(bullet.ty)))[:3]==(0,0,0):
                if reflection:
                    (bullet.ex,bullet.ey,bullet.ang,bList) = projectileCollide(bullet,bullet.tx,bullet.ty,int(bullet.tx),int(bullet.ty),bullet.ang,bList,collide,horizCollide)
                    bullet.ang = radians(bullet.ang) #reflects bullets off walls
                    bullet.ex,bullet.ey = bullet.ex + cos(bullet.ang) * bSpeed * 2, bullet.ty - sin(bullet.ang) * bSpeed * 2
                    bullet.tx,bullet.ty = bullet.ex + cos(bullet.ang) * bSpeed, bullet.ty - sin(bullet.ang) * bSpeed
                else:
                    bList.append(bullet) #bullets to be deleted

    for b in bList: #removes all the bullets that collide with buildings or AIs
        try:
            bulletList.remove(b)
        except ValueError: pass #crashes if the bullet has already been erased
                                #in the erase() function
    for p in pList: #erases all of the peaceful AIs that have lost all health
        try:
            peacefulAIlist.remove(p)
        except ValueError: pass #an error occurs if an AI is hit with multiple
                                #bullets
    for s in sList:
        try:
            shooterAIList.remove(s)
        except ValueError: pass

def makeBullet(ang,wNum,shots,pos,damage):#(shooter,wNum,shots,pos,damage):
    '''Makes bullets starting in various places going in various directions
    based on the weapon chosen. After determining the specific position and
    angle of the bullet, the properties of the bullet (tip/end coordinates,
    angle) are created and added to the list of active bullets as a tuple'''
    ang=radians(ang)
    randang = randint(8*(shots-1),8*shots)
    ammoList = [(pos[0] + cos(ang) * 100, pos[1] - sin(ang) * 100, ang), #machine gun bullets
    (pos[0] + cos(ang+radians(-5+10*shots)) * 100, pos[1] -
        sin(ang+radians(-5+10*shots)) * 100, ang), #dual pistol bullets
    ((pos[0]+cos(ang)*35)+cos(ang+radians(-14+randang)) * 100,
     (pos[1]-sin(ang)*35)-sin(ang+radians(-14+randang)) * 100,
     ang+radians(-14+randang)), #shotgun bullets
                (pos[0]+cos(ang)*100,pos[1]-sin(ang)*100,ang)] #pistol
    tipX,tipY = ammoList[wNum][0], ammoList[wNum][1]
    ang = ammoList[wNum][2]
    return ((tipX,tipY,tipX,tipY,ang,damage))

def gunRun(mb,w,magazine,shot,delay,weaponsList,weapon,player,mx,my,cx,cy,cur_x,cur_y,bList,bulletSpeed,bulletLength,secondaryFire):
    'Handles bullet creating, bullet moving and player shooting sprite selection procedures'

    if mb[0] == 1 and secondaryFire == False:
        if player.ammo > 0:
            if delay % weapon[2] == 0 and player.reloading==False:
                shot = True
                player.rotate(mx,my,cx,cy)
                mixer.music.play()
                for i in range(weapon[1]):
                    bull = makeBullet(player.ang+(randint(-2,2)),weaponsList.index(weapon),i,(cur_x,cur_y),weapon[3])
                    bList.append(Bullet(bull[0],bull[1],bull[2],bull[3],bull[4],bull[5]))
                    player.ammo-=1
                player.ammoInClip=player.ammo%player.clipSize


    for i in range(len(bList)):
        bList[i].move(bulletSpeed,bulletLength)

    return(shot)

def getDelay(count,shot):
    'Calculates bullets and sees if player is still shooting or not'

    if count == 59: #counter for each frame
        count = 0 #helps calculate fire rate for each weapon
        shot = False
    if shot:
        count += 1
    return(count,shot)

def drawScene(surface,cur_pos,player,bList,delay,mb,peacefulAIList,mx,my,rx,ry,viewDel,bulletWidth,bulCol,coinList,coin,
              moneyFont,moneyFontCol,collectedCoinList,collectedCoinFont,collectedCoinFontHeight,collectedCoinFontCol,
              fadeSpeed,deadList,shooterAIList,secondary,meleeDelay,secWeap,meleeSprite,cx,cy,ammoFontDict,
              ammoInClipFontDict,droppedClipList,collectedClipList,magazine,collectedClipFontDict,gunNames,grenadeFlag,
              grenadeFlag2,grenadex,grenadey,grenadePic,rotation,grenadeOnGround,exploding,explodeSpr):
    'Draws bullets in active bullet list, civilians and the player plus the HUD'

    if grenadeFlag or grenadeFlag2 or grenadeOnGround:
        surface.blit(transform.rotate(grenadePic,rotation),(int(screen.get_width()//2-(player.x-grenadex)-20),
                                                            int(screen.get_height()//2-(player.y-grenadey)-20)))
    for b in bList:
        b.draw(surface,player,bulletWidth,bulCol)
    drawDead(surface,deadList,player)
    for ai in peacefulAIList:
        ai.draw(surface,player)
    for ai in shooterAIList:
        ai.draw(surface)
    for curCoin in coinList:
        if fitOnscreen(surface,(player.x,player.y),curCoin[0]):
            surface.blit(coin,getCentre(coin,surface.get_width()//2-(player.x-curCoin[0][0]),
                                              surface.get_height()//2-(player.y-curCoin[0][1])))

    for clip in droppedClipList:
        if fitOnscreen(surface,(player.x,player.y),clip[0]):
            img=transform.rotate(magazine,clip[3])
            surface.blit(img,getCentre(img,surface.get_width()//2-(player.x-clip[0][0]),
                                              surface.get_height()//2-(player.y-clip[0][1])))
    player.draw(surface,delay,mb,secondary,meleeDelay,secWeap,meleeSprite,mx,my,cx,cy)
    if exploding:
        explodeSpr = transform.scale(explodeSpr,(explodeSpr.get_width()*2,explodeSpr.get_height()*2))
        surface.blit(explodeSpr,(int(screen.get_width()//2-(player.x-grenadex))-explodeSpr.get_width()//2,
                                 int(screen.get_height()//2-(player.y-grenadey))-explodeSpr.get_height()//2))
    #dist = distance((cur_pos[0],cur_pos[1]),(mx,my)) #distance between player and mouse coordinates
    #screen.blit(surface.subsurface(cur_pos[0]+(dist//viewDel)*cos(player.ang)-cenx,
    #cur_pos[1]-(dist//viewDel)*sin(player.ang)-ceny,rx,ry),(0,0))
    drawCoinText(surface,collectedCoinFontCol,collectedCoinList,coin,collectedCoinFont,
                 collectedCoinFontHeight,collectedCoinFontCol,player,fadeSpeed)

    drawClipText(surface,collectedClipList,collectedClipFontDict,player,fadeSpeed,gunNames)

    surface.blit(moneyFont.render("$ %s"%player.money,True,moneyFontCol),(0,0))
    Atot=ammoFontDict["font"].render("/%s"%(str(player.ammo)),True,ammoFontDict["col"])
    AIC=ammoInClipFontDict["font"].render(str(player.ammoInClip),True,ammoInClipFontDict["col"])
    surface.blit(Atot,(surface.get_width()-Atot.get_width(),surface.get_height()-AIC.get_width()//2-Atot.get_width()//2))
    surface.blit(AIC,(surface.get_width()-Atot.get_width()-AIC.get_width(),surface.get_height()-AIC.get_height()))
    screen.blit(surface,(0,0))


def getCentre(surface,h,k):
    'returns coordinate of where to blit picture so that it is always in the centre'
    x = surface.get_width()
    y = surface.get_height()
    return h-(x//2),k-(y//2)

def drawCoinText(surface,col,collectedCoinList,coin,collectedCoinFont,
                 collectedCoinFontHeight,collectedCoinFontCol,player,fadeSpeed):
    """
    Draws the amount of money that was collected from a coin onscreen to be brief
    for every coin collected, it blits the amount onscreen and then adds it
    back into the list with its alpha slightly reduced and its position moving
    towards the top left of the screen, then it removes the old coin tuples from
    the list
    """
    length=len(collectedCoinList)
    toAdd=[] #the local variable that holds all the new coin tuples
    for c in collectedCoinList:
        if fitOnscreen(surface,(player.x,player.y),c[0])==True:
            text=collectedCoinFont.render("$ %s"%c[1],True,col)
            try:
                toBlit=surface.subsurface(surface.get_width()//2-(player.x-c[0][0]-coin.get_width()//2),
                                       surface.get_height()//2-(player.y-c[0][1]-coin.get_height()//2),
                                         text.get_width(),text.get_height()).copy()
                #since rendered font surfaces dont seem to be able to change alpha, we have to make a
                #surface of what its supposed to be blitted over, and then blit the text onto, change the
                #alpha and finally blit the new surface onto the screen
                toBlit.blit(text,(0,0))
                toBlit.set_alpha(c[2])

                surface.blit(toBlit,(surface.get_width()//2-(player.x-c[0][0]-coin.get_width()//2),
                                       surface.get_height()//2-(player.y-c[0][1]-coin.get_height()//2)))
            except ValueError: #error is raised if the text is partly onscreen and partly off
                pass
        if c[2]-5>0: #if the alpha for the next time it will be blitted is >0
            toAdd.append(((c[0][0]-2,c[0][1]-2),c[1],c[2]-fadeSpeed)) #adds the text and modifies
                                                                      #its properties slightly

    for i in range(length):
        try: #error occurs if an object is not appended to toAdd because its alpha is 0
            collectedCoinList.append(toAdd[i]) #adds the new coin info
        except IndexError: pass
        collectedCoinList.remove(collectedCoinList[0]) #removes the old coin info

def drawClipText(surface,collectedClipList,collectedClipFontDict,player,fadeSpeed,gunNames):
    """Draws the amount of ammo that the clip that the player picks up contains
    and for which gun the ammo can be used with
    very similar to the drawCoinText function"""
    length=len(collectedClipList)
    toAdd=[]
    for c in collectedClipList:
        if fitOnscreen(surface,(player.x,player.y),c[0]):
            text=collectedClipFontDict["font"].render("%s +%sbullets"%(gunNames[c[2]].upper(),c[1]),True,collectedClipFontDict["col"])
            try:
                toBlit=surface.subsurface(surface.get_width()//2-(player.x-c[0][0]),
                                       surface.get_height()//2-(player.y-c[0][1]),
                                         text.get_width(),text.get_height()).copy()
                #since rendered font surfaces dont seem to be able to change alpha, we have to make a
                #surface of what its supposed to be blitted over, and then blit the text onto, change the
                #alpha and finally blit the new surface onto the screen
                toBlit.blit(text,(0,0))
                toBlit.set_alpha(c[3])

                surface.blit(toBlit,(surface.get_width()//2-(player.x-c[0][0]),
                                       surface.get_height()//2-(player.y-c[0][1])))
            except ValueError: #error is raised if the text is partly onscreen and partly off
                pass
        if c[3]-5>0: #if the alpha for the next time it will be blitted is >0
            toAdd.append(((c[0][0]+2,c[0][1]+2),c[1],c[2],c[3]-fadeSpeed)) #adds the text and modifies
                                                                      #its properties slightly
    for i in range(length):
        try: #error occurs if an object is not appended to toAdd because its alpha is 0
            collectedClipList.append(toAdd[i]) #adds the new clip info
        except IndexError: pass
        collectedClipList.remove(collectedClipList[0]) #removes the old clip info


def fitOnscreen(surface,center,point):
    """Checks to see whether or not a certain object is in the current screen
    For an object to appear onscreen, it can be up to 50 px off of it
    in case that its diameter is large enough that a portion of it should
    be seen by the player
    center - the center of the screen (player.x,player.y)
    point - the center of the object in question
    """
    if (point[0]>=center[0]-surface.get_width()//2-50
        and point[0]<=center[0]+surface.get_width()//2+50
        and point[1]>=center[1]-surface.get_height()//2-50
        and point[1]<=center[1]+surface.get_height()//2+50):
            return True
    else : return False

def blockedPath(surface,player,ai):
    """Checks to see whether there is a wall in between the path from
    the AI to the player"""
    for i in range(int(ai.dist/ai.speed)):
        x=int(ai.x+i*ai.speed*cos(radians(ai.ang))) #some trig to check each
        y=int(ai.y-i*ai.speed*sin(radians(ai.ang))) #position that the AI will be able to move to
        #with their given speed
        if surface.get_at((x,y))[:3]==(0,0,0):
            return True
    return False


def drawDead(surface,deadList,player):
    """Draws the bodies of the dead AIs onto the screen and has them slowly fade away
    deadList - the dead bodies
    player - the player class"""
    length=len(deadList) #length of the list
    toAdd=[] #list for the new values to be added to the deadList
    for dead in deadList:
        #dead - (position, sprite, alpha)
        if fitOnscreen(surface,(player.x,player.y),dead[0]):
            try:
                img=dead[1]
                toBlit=surface.subsurface(getCentre(img,surface.get_width()//2-(player.x-dead[0][0]),
                                                    surface.get_height()//2-(player.y-dead[0][1]))[0],
                                           getCentre(img,surface.get_width()//2-(player.x-dead[0][0]),
                                                     surface.get_height()//2-(player.y-dead[0][1]))[1],
                                             img.get_width(),img.get_height()).copy()
                #sprites with transparencies cannot have an alpha set to them
                #so we have to copy the surface that they will be blitted onto
                #and the blit it onto the surface and then set the alpha to the new surface
                toBlit.blit(img,(0,0))
                toBlit.set_alpha(dead[2])
                surface.blit(toBlit,getCentre(toBlit,surface.get_width()//2-(player.x-dead[0][0]),
                                              surface.get_height()//2-(player.y-dead[0][1])))
            except ValueError: pass
            #raises an error if the body is partly on the screen and partly off
        if dead[2]-5>0:
            toAdd.append((dead[0],dead[1],dead[2]-5))
    for i in range(length):
        del deadList[0] #removes all the old values
        try:
            deadList.append(toAdd[i]) #adds all the new values
        except IndexError: pass
        #error occurs if the list goes out of range because some of the alphas are 0 so they
        #dont need to be re-added to the list because they wont be seen anyhow


def movePlayer(keys,cur_x,cur_y,collide,playerSpeed):
    '''Moves the player if the WASD keys are pressed and if it's possible (checks collisions using collision map'''
    if keys[K_a] and collide.get_at((cur_x-playerSpeed,cur_y))[:3]!=(0,0,0):
        cur_x-=playerSpeed
    if keys[K_d] and collide.get_at((cur_x+playerSpeed,cur_y))[:3]!=(0,0,0):
        cur_x+=playerSpeed
    if keys[K_w] and collide.get_at((cur_x,cur_y-playerSpeed))[:3]!=(0,0,0):
        cur_y-=playerSpeed
    if keys[K_s] and collide.get_at((cur_x,cur_y+playerSpeed))[:3]!=(0,0,0):
        cur_y+=playerSpeed
    return cur_x,cur_y

def meleeAtk(player,weapon,count,spriteSpeed):
    'Executes melee attacks and chooses melee sprites to display'
    if weapon[0] == 'knife':
        spr = weapon[1][int(min(5,count))] #uses counter to calculate correct sprite frame number
        count += spriteSpeed #returns sprites for knife animation
        if count >= 6:
            count = 0
        knifeTip = (int(player.x+50*(cos(radians((player.ang-30)+15*secDelay)))),
                    int(player.y-50*(sin(radians((player.ang-30)+(15*secDelay))))))
        return (count,spr,knifeTip)
    if weapon[0] == 'grenade':
        spr = weapon[1][int(min(3,count))]
        count += spriteSpeed/3 #frame speed is slower than knife animation so that it is more distinguishable
        if count >= 4: #returns sprites for grenade throwing animation
            count = 0
        return(count,spr)

def paraMaker(count,secTime,startSpeed,lowestSpeed):
    '''creates parabolas for different equations by accepting minimum, amount of time parabola is active
    and 2 highest points in parabola'''
    count += 1
    speed = int(((startSpeed-lowestSpeed)/(secTime*30)**2)*((count-(secTime*30))**2)+lowestSpeed)
    if count >= secTime*60:
        count = -1
    return(count,speed)

def throwGrenade(gx,gy,player,ang,count,sprList,speed,dist,totalDist,rotation,collide,horizCollide):
    '''initiates grenade roll/bounce animation'''
    if count == 0:
        count = 1
        gx,gy = player.x,player.y
        ang = player.ang
    speed = min(dist-totalDist,speed//count) #grenade moves either to the mouse position
    speed = max(1,speed) #or the max distance, whichever is smaller with a minimum distance of 1
    totalDist += speed
    destX,destY = (int(gx+speed*cos(radians(ang))),int(gy-speed*sin(radians(ang)))) #destination coordinates
    (gx,gy,ang,unusedList) = projectileCollide(None,gx,gy,destX,destY,radians(ang),None,collide,horizCollide)
    count += 1
    if totalDist >= dist:
        count = 0
    rotation += speed
    return (gx,gy,count,ang,totalDist,rotation)

def projectileCollide(projectile,x,y,destX,destY,ang,eraseList,collide,horizCollide):
    'Returns new position and angle of projectile if it is bouncing off walls'
    ang = degrees(ang)
    if collide.get_at((destX,destY))[:3]!=(0,0,0):
        x,y = destX,destY #returns the position if it doesn't hit any walls
    elif horizCollide.get_at((destX,destY))[:3]==(0,255,0):
        if ang in range(70,111) or ang in range(250,291):
            ang += 180
        elif -1 < ang < 90:
            ang -= 2*ang #makes projectile bounce off horizontal walls
        elif 89 < ang < 180:
            ang += 2*(180-ang)
        elif 179 < ang < 270:
            ang = 360-ang
        else:
            ang += 2*(360-ang)
    elif horizCollide.get_at((destX,destY))[:3]==(0,0,255):
        if ang in range(170,191) or ang in range(350,361) or ang in range(0,11):
            ang += 180
        elif -1 < ang < 90:
            ang += 2*(90-ang) #makes projectiles bounce off vertical walls
        elif 89 < ang < 180:
            ang -= 2*(ang-90)
        elif 179 < ang < 270:
            ang += 2*(270-ang)
        else:
            ang -= 2*(ang-270)
    else:
        eraseList.append(projectile) #if the projectile starts too close to the wall, it is added to the erase list
    return(x,y,ang,eraseList)

#-----Functions For When the Player is Inside the Gun Store-----

def InsideGunStore(screen,gunStore,gunStoreCollide,player,secondary,meleeDelay,secWeap,meleeSprite,cx,cy,delay):
    """The loop for when the player is inside the gun store"""
    inside=True
    in_x,in_y=screen.get_width()//2+50,gunStore.get_height()//2 #pos of the player inside the store
    origScreen=screen.copy() #the screen that is blitted the frame b4 they enter the store
    fadeOut(screen,origScreen)
    fadeIn(screen,gunStore.subsurface((in_x-screen.get_width()//2,in_y-screen.get_height()//2,
                                       screen.get_width(),screen.get_height())).copy())

    #player=player
    while inside:
        for e in event.get():
            if e.type==VIDEORESIZE: #allows the screen to be resized
                screen=display.set_mode(e.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                resx,resy = e.dict['size'] #resolution size
                cx,cy = resx//2,resy//2 #center coordinates, also half size of resolution

                """
                #---Resizing of the map according to the new screen dimensions---
                gunStoreImg=image.load("Game Maps\Gun store.png").convert() #the actual gun store img
                width=gunStoreImg.get_width()+screen.get_width()
                height=gunStoreImg.get_height()+screen.get_height()
                gunStore=Surface((width,height)) #actual surface that the player will see
                #larger than actual img because if the player is in a corner, they can see outside the actual
                #image
                gunStore.fill((0,0,0))
                gunStore.blit(gunStoreImg,(screen.get_width()//2,screen.get_height()//2))

                gunStoreCollideImg=image.load("Game Maps\Gun store collide check.png").convert() #the actual gun store img
                gunStoreCollide=Surface((width,height)) #will see
                #larger than actual img because if the player is in a corner, they can see outside the actual
                #image
                gunStoreCollide.fill((0,0,0))
                gunStoreCollide.blit(gunStoreCollideImg,(screen.get_width()//2,screen.get_height()//2))
                """

            if e.type==QUIT:
                inside=False
        #---Input from user---
        k=key.get_pressed()
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        #---

        in_x,in_y=movePlayer(k,in_x,in_y,gunStoreCollide,2) #moves player
        playerInStore=Player(in_x,in_y,0,player.pic1,player.pic1,player.money,) #class for the player while inside store
        playerInStore.rotate(mx,my,screen.get_width()//2,screen.get_height()//2)


        if gunStoreCollide.get_at((in_x,in_y))[:3]==(255,0,0): #if they walk out of store
            inside=False
        onscreen = gunStore.subsurface((in_x-screen.get_width()//2, #section of map currently viewed on screen
                                       in_y-screen.get_height()//2, screen.get_width(),screen.get_height())).copy()
        if gunStoreCollide.get_at((in_x,in_y))[:3]==(0,255,0) and k[K_e]:
            shop(screen)
            in_x-=5
        #---Drawing on screen---
        screen.blit(onscreen,(0,0))
        playerInStore.draw(screen,delay,mb,secondary,meleeDelay,secWeap,meleeSprite,mx,my,cx,cy)
        #---
        player.money-=10
        display.flip()
    #return player.money
    fadeOut(screen,onscreen) #makes for a cool transition
    fadeIn(screen,origScreen)

def shop(screen):
    shopping=True
    back=screen.copy()
    layer=Surface((screen.get_width(),screen.get_height()))
    layer.set_alpha(150)
    #back=screen.copy()
    #back.set_alpha(150)
    mainBack=image.load("shopping screen background.jpg")
    secBack=image.load("shopping screen background 2.jpg")
    while shopping:
        for e in event.get():
            if e.type==VIDEORESIZE: #allows the screen to be resized
                screen=display.set_mode(e.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                resx,resy = e.dict['size'] #resolution size
                cx,cy = resx//2,resy//2 #center coordinates, also half size of resolution
                #print(e.dict['size'])
            if e.type==QUIT:
                shopping=False
        #for i in range(3):
        #    screen.blit(transform.scale(secBack,(screen.get_width()//4,screen.get_height()//3)),(0,screen.get_height()//3*i))
        screen.blit(back,(0,0))
        screen.blit(layer,(0,0))
        display.flip()

class GoShopping:
    def __init__(screen):
        gunRect=Rect(10,screen.get_height())



while collide.get_at((cur_x,cur_y)) == (0,0,0): #chooses a random spot the player can spot
    cur_x = randint(0,gameMap.get_width())
    cur_y = randint(0,gameMap.get_height())

pic1,pic2 = weapon[0][0], weapon[0][1]
reloadingSprites=reloadList[w]
player = Player(cur_x,cur_y,0,pic1,pic2,money,reloadingSpeed,reloadList[w],ammoList[w],clipList[w],reloadingFrame,reloading,hasReloaded)
while running:
    for e in event.get():
        if e.type==MOUSEBUTTONDOWN:
            if e.button ==2:
                if throw == False:
                    n += 1
                    if n > 2:
                        n = 0
            if e.button == 3:
                secondary = True #initiates secondary attack
            if e.button == 4:
                prevWep=w
                ammoList[prevWep]=player.ammo
                w -= 1 #changes weapons when mouse is scrolled
                if w < 0:
                    w = 2
                weapon = weapons[w]
                pic1,pic2 = weapon[0][0], weapon[0][1]
                reloadingSprites=reloadList[w]
                ammo=ammoList[w]
                clipSize=clipList[w]
                player.weaponChange(pic1,pic2,reloadingSprites,ammo,clipSize)
                mixer.music.load(weaponSounds[w])
            if e.button == 5:
                prevWep=w
                ammoList[prevWep]=player.ammo
                w += 1 #changes weapons when mouse is scrolled
                if w > 2:
                    w = 0
                weapon = weapons[w]
                pic1,pic2 = weapon[0][0], weapon[0][1]
                reloadingSprites=reloadList[w]
                ammo=ammoList[w]
                clipSize=clipList[w]
                player.weaponChange(pic1,pic2,reloadingSprites,ammo,clipSize)
                mixer.music.load(weaponSounds[w])

        if e.type==VIDEORESIZE: #allows the screen to be resized
            screen=display.set_mode(e.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
            resx,resy = e.dict['size'] #resolution size
            cx,cy = resx//2,resy//2 #center coordinates, also half size of resolution
            #print(e.dict['size'])
        if e.type==QUIT:
            running=False

#--------------------------------------------CONSTANTLY CHANGING VARIABLES----------------------------------------------

    k = key.get_pressed()
    player.x,player.y = movePlayer(k,player.x,player.y,collide,playerSpeed)
    secWeapon = meleeList[n]
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()

#----------------------------------------------FUNCTIONS CONSTANTLY USED------------------------------------------------
    if throw == False:
        player.rotate(mx,my,cx,cy)

    if k[K_KP_MULTIPLY]:
        para = True
    if k[K_KP_PLUS]:
        bSpeed += 1
    if k[K_KP_MINUS]:
        bSpeed -= 1
    if para: #slows down speeds for bullet time
        c,bSpeed = paraMaker(c,slowMoTime,defaultBSpeed,minSpeed)[0], paraMaker(c,slowMoTime,defaultBSpeed,minSpeed)[1]
        playerSpeed = max(1,bSpeed//6)
        sprSpeed = min(0.5,bSpeed/60)
        reloading = min(0.1,sprSpeed/5)
    if c == -1:
        para = False

    shot = gunRun(mb,w,clip,shot,delay,weapons,weapon,player,mx,my,cx,cy,player.x,player.y,bulletList,bSpeed,bLen,secondary)
    delay,shot = getDelay(delay,shot)[0],getDelay(delay,shot)[1] #makes/moves bullets in the game

    if secondary:
        result = meleeAtk(player,secWeapon,secDelay,sprSpeed)
        if secWeapon[0] == 'knife': #activates knife animation/damage
            player.rotate(mx,my,cx,cy)
            secDelay,melSpr,dmgTip = result[0],result[1],result[2]
        elif secWeapon[0] == 'grenade' and grenade2 == False and grenadeIdle == False: #activates grenade sprites/damage
            secDelay,melSpr = result[0],result[1]
            throw = True
            if secDelay == 0:
                throw = False
                grenade = True
                grenadeTotalDist = 0 #resets total distance travelled by grenade by each throw
                grenadeRot = 0 #resets grenades rotation angle
                grenadeDist = min(grenadeDefDist,distance((cx,cy),(mx,my))) #distance of grenade throw is
#either the default throwing distance or shorter if the player wishes it to be so

    if secDelay == 0: #returns melee frame number to choose melee sprite number for the next frame
        secondary = False #and melee frame to draw for the current frame and knife tip to calculate damage

    if grenade:
        result = throwGrenade(grenx,greny,player,grenadeAng,grenadeDelay,secWeapon[1],grenadeSpeed,
                              grenadeDist//10*grenadeDistPerc,grenadeTotalDist,grenadeRot,collide,horizontal)
        grenx,greny,grenadeDelay,grenadeAng,grenadeTotalDist,grenadeRot = result[0],result[1],result[2],result[3],result[4],result[5]
        if grenadeDelay == 0:
            grenade = False #returns information to draw grenade travelling before bounce
            grenadeDelay = 1
            grenade2 = True
            grenadeTotalDist = 0

    if grenade2:
        result = throwGrenade(grenx,greny,player,grenadeAng,grenadeDelay,secWeapon[1],grenadeSpeed//grenadeSpeedCutback,
                              grenadeDist//10*(10-grenadeDistPerc),grenadeTotalDist,grenadeRot,collide,horizontal)
        grenx,greny,grenadeDelay,grenadeAng,grenadeTotalDist,grenadeRot = result[0],result[1],result[2],result[3],result[4],result[5]
        if grenadeDelay == 0: #returns information to draw grenade after bounce and ends grenade animation
            grenade2 = False
            grenadeIdle = True

    if grenadeIdle: #delay when grenade is idle on the ground
        grenadeDelay += 1
        if grenadeDelay >= grenadeFuse*60:
            grenadeIdle = False
            grenadeDelay = 0
            explosion = True
            explosionDelay = 0 #counter for explosion sprites

    if explosion: #chooses exploding images for grenade and initiates explosion
        explosionSpr = image.load(explosions[int(explosionDelay)])
        explosionDelay += 0.8
        impactTime = 11 < explosionDelay < 12
        if explosionDelay >= len(explosions):
            explosion = False
            impactTime = False

    while len(peacefulAIList)<4: #spawns 4 random civilians in 30 random positions on the city map
        ai = makePeacefulAI(screen,gameMap,collide,player,peacefulSprites,civHealth,maxCoinDrop,minCoinDrop)
        peacefulAIList.append(peacefulAI(ai[0],ai[1],ai[2],ai[3],ai[4],ai[5]))

    while len(shooterAIList)<5: #makes shooters
        ai=makeShooterAI(screen,gameMap,collide,player,choice(weaponsAI),healthPistol,AIspeed,AIammo)
        shooterAIList.append(enemyShooter(ai[0],ai[1],ai[2],ai[3],ai[4],ai[5],ai[6],ai[7]))

    for ai in peacefulAIList: #moves civilians, shooters
        ai.move(civSpeed)

    for ai in shooterAIList:
        ai.move(player,collide)

    for ai in shooterAIList: #makes enemies shoot
        ai.shoot(bulletList,weaponsAI)


    player.collectMoney(coinList,coin,collectedCoinList) #collects any money that the player happens to walk over
    player.collectAmmo(droppedClipList,collectedClipList,ammoList,w)

    erase(player,peacefulAIList,bulletList,coinList,deadList,dmgTip,secondary,secWeapon[0],knifeDmg,droppedClipList,
          weaponsAI,blastRad,grenDmg,grenx,greny,impactTime,bRicochet,collide,horizontal) #erases bullets that already
          #collided, calculates damage and civilians/enemies who've lost all health
    onscreen = gameMap.subsurface((player.x-screen.get_width()//2, #section of map currently viewed on screen
                                   player.y-screen.get_height()//2, screen.get_width(),screen.get_height())).copy()
    drawScene(onscreen,(player.x,player.y),player,bulletList,delay-1,mb,peacefulAIList,mx,my,resx,resy,viewDelay,bWid,bCol,
              coinList,coin,moneyFont,moneyFontCol,collectedCoinList,collectedCoinFont,
              collectedCoinFontHeight,collectedCoinFontCol,fadeSpeed,deadList,shooterAIList,secondary,secDelay,
              secWeapon[0],melSpr,mx,my,ammoFontDict,ammoInClipFontDict,droppedClipList,collectedClipList,
              magazine,collectedClipFontDict,gunNames,grenade,grenade2,grenx,greny,meleeList[1][1][4],grenadeRot,grenadeIdle,
              explosion,explosionSpr)
    #draws all elements on screen (E.g. background, player, AIs, bullets)


    if collide.get_at((player.x,player.y))[:3]==(0,0,255):
        screen.blit(enterText,(screen.get_width()//2-enterText.get_width()//2,screen.get_height()//3*2-enterText.get_height()//2))
        if k[K_e]:
            InsideGunStore(screen,gunStore,gunStoreCollide,player,secondary,secDelay,secWeapon[0],melSpr,cx,cy,delay)
    #money=player.money #allows the players total money to be carried over to the next loop of the game
    #reloadingFrame=player.reloadingFrame
    #hasReloaded=player.hasReloaded
    #reloading=player.reloading

    screen.blit(HUDList[w],(0,screen.get_height()-HUDList[w].get_height()))
    #new_tx=surface.get_width()//2-(player.x-self.tx)
    #new_ty=surface.get_height()//2-(player.y-self.ty)
    #draw.circle(screen,(255,0,0),(int(screen.get_width()//2-(player.x-grenx)),int(screen.get_height()//2-(player.y-greny))),5)
    #print(ammoList[w])

    count += 1
    fps += myClock.get_fps()
    fpsList.append(myClock.get_fps())
    myClock.tick(60)
    display.flip()

print(fps/count)
print(max(fpsList))
print(min(fpsList))
quit()


#--------------------------------------Notes------------------------------------
#---Screen Resizing Feature---
"""We didn't come up with the code for it all by ourselves.
There was a sample program in the pygame.com cookbook at
http://www.pygame.org/wiki/WindowResizing?parent=CookBook
where we got the code to do it which we modified and adjusted to fit into
our program"""
