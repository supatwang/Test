import arcade

from models import World, Player

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
 
class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
 
    def draw(self):
        self.sync_with_model()
        super().draw()
        
class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.world = World(width,height)
        self.player_sprite = ModelSprite('snowman.png',model=self.world.player)
        self.player2_sprite = ModelSprite('snowman.png',model=self.world.player2)
        self.player_bullet_sprite = arcade.load_texture('snowball.png')        
        self.ob_texture = arcade.load_texture('snowball.png')
        self.bg = arcade.load_texture('bg.png')
        self.obg = arcade.load_texture('obg.png')
        self.box = arcade.load_texture('box.png')
        
    def on_draw(self):
        if self.world.STATE == 0:
            arcade.start_render()
            arcade.draw_texture_rectangle(0, 0,2000,2700, self.bg)
            self.player_sprite.draw()
            self.player2_sprite.draw()
            arcade.draw_text("P2 LIFE :" + str(self.world.player2.LIFE), 800, 500, arcade.color.BLACK, 20)
            arcade.draw_text("P1 LIFE :" + str(self.world.player.LIFE), 800, 100, arcade.color.BLACK, 20)
            arcade.draw_text("P2 AMMO X :" + str(self.world.player2.ammo), 800, 600, arcade.color.BLACK, 20)            
            arcade.draw_text("P1 AMMO X :" + str(self.world.player.ammo), 800, 150, arcade.color.BLACK, 20)

            for o in self.world.packList:
                arcade.draw_texture_rectangle(o.x, o.y,50,50, self.box)

            for o in self.world.player.bulletList:
                arcade.draw_texture_rectangle(o.x, o.y,50,50, self.player_bullet_sprite)


            for o in self.world.player2.bulletList:
                arcade.draw_texture_rectangle(o.x, o.y,50,50, self.player_bullet_sprite)

            for o in self.world.obList:
                arcade.draw_texture_rectangle(o.x, o.y,50,50, self.ob_texture) 

        if self.world.STATE == 1:
            arcade.draw_texture_rectangle(480, 360,1200,700, self.obg)
            arcade.draw_text("PLAYER 1 WIN", 280, 100, arcade.color.BLACK, 50)
        if self.world.STATE == 2:
            arcade.draw_texture_rectangle(480, 360,1200,700, self.obg)
            arcade.draw_text("PLAYER 2 WIN", 280, 100, arcade.color.BLACK, 50)

    def animate(self, delta):
           self.world.animate(delta)
           

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)
        
if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()

