import arcade.key
from random import randint

GRAVITY = -1
JUMP_VY = 20

class Player():
    def __init__(self,world,x,y,floor):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.LIFE = 7
        self.floor = floor
        self.is_jump = False
        self.bulletList = []
        self.ammo = 0
        
    def jump(self):
        if not self.is_jump:
            self.is_jump = True
            self.vy = JUMP_VY

    def animate(self, delta):
        self.x += self.vx

        if self.vx > 12:
            self.vx = 12
            
        if self.vx < -12:
            self.vx = -12
            
        if self.x > self.world.width:
            self.x = 0

        if self.x < 0:
            self.x = self.world.width
            
        if self.is_jump:
            self.y += self.vy
            self.vy += GRAVITY

        if self.y < self.floor:
            self.y = self.floor
            self.is_jump = False

    def shoot(self):
        if not self.ammo == 0:
            x = Bullet(self.x,self.y)
            self.bulletList.append(x)
            self.ammo -= 1
    
    def hit(self,ob):
        return ((abs(self.x - ob.x) < 15) and
                (abs(self.y - ob.y) < 15))

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_out = False
        if y < 499:
            self.i = 1
        if y > 499:
            self.i = 2
            
    def animate(self, delta):
        if self.i == 1:
            self.y += 10
        if self.i == 2:
            self.y -= 10

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
 
        self.player = Player(self, 100, 100, 100)
        self.player2 = Player(self, 500, 500, 500)

        self.obList = []
        self.STATE = 0
        self.packList = []

    def animate(self, delta):
        if self.player.LIFE == 0:
            self.STATE = 2
        if self.player2.LIFE == 0:
            self.STATE = 1
        
        self.player.animate(delta)
        self.player2.animate(delta)
        self.gen_ob()
        self.gen_pack()
        self.update_pack(delta,self.packList)
        self.update_ob(delta)
        self.update_bullet(delta,self.player2.bulletList)
        self.update_bullet(delta,self.player.bulletList)
        
    def update_pack(self,delta,pList):
        for n in pList:
            n.animate(delta)
            if self.check_out(n):
                pList.remove(n)
            if self.player.hit(n):
                if n.i == 1:
                    self.player.ammo += 1
                    pList.remove(n)
            if self.player2.hit(n):
                if n.i == 2:
                    self.player2.ammo += 1
                    pList.remove(n)
                        
    def update_bullet(self,delta,bList):
        for n in bList:
            n.animate(delta)
            if self.check_out(n):
                bList.remove(n)
            if self.player.hit(n):
                if n.i == 2:
                    self.player.LIFE -= 1
                    bList.remove(n)
            if self.player2.hit(n):
                if n.i == 1:
                    self.player2.LIFE -= 1
                    bList.remove(n)
            
    
    def update_ob(self,delta):       
        for n in self.obList:
            n.animate(delta)
            if self.player.hit(n):
                self.player.LIFE -= 1
                #print(self.player.LIFE)
                n.is_out = True
            if self.player2.hit(n):
                self.player2.LIFE -= 1
                #print(self.player2.LIFE)
                n.is_out = True
                
            if self.check_out(n):
                n.is_out = True

            if n.is_out == True:
                self.obList.remove(n)            

    def check_out(self,n):
        if n.x < 10 or n.y > 1000 or n.y < 0:
            return True

    def gen_ob(self):
        if randint(0,100) > 99:
            x = Obstructor(self,900,500)
            self.obList.append(x)
        if randint(0,100) > 99:
            x = Obstructor(self,900,100)
            self.obList.append(x)

    def gen_pack(self):
        if randint(0,100) > 99:
            x = SnowPack(self,900,500)
            self.packList.append(x)
        if randint(0,100) > 99:
            x = SnowPack(self,900,100)
            self.packList.append(x)
    
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.player.jump()
        if key == arcade.key.ENTER:
            self.player.shoot()
        if key == arcade.key.LEFT:
            self.player.vx -= 3
        if key == arcade.key.RIGHT:
            self.player.vx += 3

        if key == arcade.key.W:
            self.player2.jump()
        if key == arcade.key.A:
            self.player2.vx -= 3
        if key == arcade.key.D:
            self.player2.vx += 3
        if key == arcade.key.F:
            self.player2.shoot()
            
class Obstructor:

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.is_out = False

    def animate(self, delta):
        self.x -= 10

class SnowPack:

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.is_out = False
        if y < 499:
            self.i = 1
        if y > 499:
            self.i = 2

    def animate(self, delta):
        self.x -= 10
    
