#python code env
#-*-coding:utf-8-*-
#

import cocos
from cocos.actions import *
import pyglet
import random


class TableLayer(cocos.layer.Layer):
    """The main game layer
    
    
    """ 
    is_event_handler = True
 

    def __init__(self, GameRange = 6, Numbers = 4, MaxLevel = 13):
        """


        """

        super(TableLayer, self).__init__()

        self.keys_pressed = set()
        
        # use the StartTimer to calculate the time passed
        self.StartTimer = 0
        self.schedule(self.Timer_Refresh)
        
        self.GameRange = GameRange
        self.Numbers = Numbers
        self.MaxLevel = MaxLevel
        self.round = 1
        self.BestRound = MaxLevel

        self.BlackChar = '▪'
        self.WhiteChar = '▫'

        # the .Result is the Numbers to be guessed, which will be generated in the Game_init()
        self.Result = []
        
        self.HighLightColor = (0, 200, 200, 255)
        self.DefaultColor = (0, 0, 0, 255)
        
        self.image = pyglet.resource.image('bg.png')
        
        # Number_Label are the labels to show the numbers 
        self.Number_Label = [cocos.text.Label('', 
            font_size = 26, 
            font_name = 'Verdana', 
            bold = True, 
            color = self.DefaultColor, 
            x = 33 + ((i) % 4) * 69, y = 628 - ((i) // 4) * 48 ) for i in range(self.MaxLevel * self.Numbers)]
        
        # show the first line with '0's
        for i in range(self.Numbers):
            self.Number_Label[i].element.text = '0'
        
        self.Number_Label[0].element.color = self.HighLightColor

        for i in range(self.MaxLevel * self.Numbers):
            self.add(self.Number_Label[i])

        self.Result_Label = [cocos.text.Label('', 
            font_size = 42, 
            font_name = 'Verdana', 
            bold = True, 
            color = self.DefaultColor,  
            x = 395 + ((i) % 4) * 69, y = 628 - ((i) // 4) * 48 ) for i in range(self.MaxLevel * self.Numbers)]
        
        for i in range(self.MaxLevel * self.Numbers):
            self.add(self.Result_Label[i])

        self.Round_Label = cocos.text.Label(str(self.round),
            font_size = 16,
            font_name = 'Verdana', 
            bold = False, 
            color = self.DefaultColor, 
            x = 105, y = 10)

        self.add(self.Round_Label)

        self.BestRound_Label = cocos.text.Label(str(self.BestRound),
            font_size = 16,
            font_name = 'Verdana', 
            bold = False, 
            color = self.DefaultColor, 
            x = 285, y = 10)

        self.add(self.BestRound_Label)

        self.TimePassed = 0
        self.BestTime = 100000 # the BestTime = 100000 here is not equal to the value showed as '99:59' 

        self.Time_Label = cocos.text.Label('00:00',
            font_size = 16,
            font_name = 'Verdana', 
            bold = False, 
            color = self.DefaultColor, 
            x = 445, y = 10)

        self.add(self.Time_Label)

        self.BestTime_Label = cocos.text.Label('99:59',
            font_size = 16,
            font_name = 'Verdana', 
            bold = False, 
            color = self.DefaultColor, 
            x = 585, y = 10)

        self.add(self.BestTime_Label)

        self.sprite_images = { 'Bingo_img':'bingo.png', 'Gameover_img':'gameover.png' }

        self.Bingo_sprite = cocos.sprite.Sprite(self.sprite_images['Bingo_img'])
        self.Bingo_sprite.position = 320, 350
        self.add(self.Bingo_sprite, z = 2)
        self.Bingo_sprite.visible = False

        self.Gameover_sprite = cocos.sprite.Sprite(self.sprite_images['Gameover_img'])
        self.Gameover_sprite.position = 320, 350
        self.add(self.Gameover_sprite, z = 2)
        self.Gameover_sprite.visible = False

        self.Game_init()


    def Timer_Refresh(self, dt):
        """A simple on_time event
        dt means the time passed after the last event
        use the StartTimer and 'dt' to set the time interval
        use the TimePassed the calculate the time passed of the game
        """
        self.StartTimer += dt
        self.TimePassed += dt
        if self.StartTimer > 1:  # timer_interval
            self.Time_Label.element.text = str(int(self.TimePassed // 60)) + ' : ' + str(int(self.TimePassed % 60)) 
            self.StartTimer = 0


    def Game_init(self):
        """Initialise the new game when:
        - game starts
        - game ends (over the MaxLevel)
        - game wins
        """

        self.GameStatus = True
        self.round = 1
        self.Number_position = 0
        self.Number_Index = 1
        self.TimePassed = 0
        
        self.Result = [random.randrange(self.GameRange) + 1 for i in range(self.Numbers)]

        self.Round_Label.element.text = str(self.round)
        self.Bingo_sprite.visible = False
        self.Gameover_sprite.visible = False

        for i in range(self.MaxLevel * self.Numbers):
            
            self.Result_Label[i].element.text = ''
            self.Number_Label[i].element.text = ''

        for i in range(self.Numbers):

            self.Number_Label[i].element.text = '0'



    def draw(self):
        """the function to draw backgroud image
        but the mechanism is unknown
        """
        self.image.blit(0,0)


    def update_text(self):
        """Upate the UI
        get keyboard input and react
        """
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        
        # the index means the current position( 0 - 3) of the numbers to be controlled 
        Now_Index = 0
        Before_Index = 0

        if 'ENTER' in key_names:
            
            if not(self.GameStatus):
                self.Game_init()
            
            #tResult stores the numbers that you guessed
            tResult = []
            for i in range(self.Numbers):
                try:
                    # Get the guessed numbers from the UI
                    tResult.append(int(self.Number_Label[(self.round - 1) * 4 + i].element.text))
                except:
                    return 0
            if 0 in tResult:
                return 0

            GuessResult = self.Guess(tResult) # temp guess result
            ResultString = ['', self.WhiteChar, self.BlackChar]
            
            for i in range(self.Numbers):
                # output the GuessResult to the UI
                self.Result_Label[(self.round - 1) * 4 + i].element.text = ResultString[GuessResult[i]] 

            if GuessResult.count(2) == 4:
                
                #the 'Bingo!' process
                self.GameStatus = False
                self.Bingo_sprite.visible = True
                if self.round < self.BestRound:
                    self.BestRound = self.round
                    self.BestRound_Label.element.text = str(self.round)

                if self.TimePassed < self.BestTime:
                    self.BestTime = self.TimePassed
                    self.BestTime_Label.element.text =str(int(self.TimePassed // 60)) + ' : ' + str(int(self.TimePassed % 60)) 
                    
                return 2
            
            if self.round == self.MaxLevel:
                
                #the 'Game End' process
                self.Gameover_sprite.visible = True
                self.GameStatus = False
                return 4

            # go to the next round
            Now_Index = (self.round - 1) * 4 + self.Number_position
            self.Number_Label[Now_Index].element.color = self.DefaultColor
            self.round += 1
            self.Number_Index = 0
            self.Number_position = 0
    
            Now_Index = (self.round - 1) * 4 + self.Number_position
            self.Number_Label[Now_Index].element.color = self.HighLightColor
            self.Round_Label.element.text = str(self.round)

            for i in range(self.Numbers):
                self.Number_Label[(self.round - 1) * 4 + i].element.text = '0'
            
            return 1

        if not(self.GameStatus):
            return 0

        if 'RIGHT' in key_names:
            
            if self.Number_position < 3:
                self.Number_position += 1
                Now_Index = (self.round - 1) * 4 + self.Number_position
                Before_Index =  Now_Index - 1
            else:
                self.Number_position = 0
                Now_Index = (self.round - 1) * 4 
                Before_Index = Now_Index + 3
        
            self.Number_Label[Now_Index].element.color = self.HighLightColor
            self.Number_Index = int(self.Number_Label[Now_Index].element.text)
            self.Number_Label[Before_Index].element.color = self.DefaultColor
            return 1

        if 'LEFT' in key_names:
            
            if self.Number_position > 0:
                self.Number_position -= 1
                Now_Index = (self.round - 1) * 4 + self.Number_position
                Before_Index =  Now_Index + 1
            else:
                self.Number_position = 3
                Now_Index = (self.round - 1) * 4 + 3 
                Before_Index =  (self.round - 1) * 4 
        
            self.Number_Label[Now_Index].element.color = self.HighLightColor
            self.Number_Label[Before_Index].element.color = self.DefaultColor
            self.Number_Index = int(self.Number_Label[Now_Index].element.text)
            return 1

        if 'UP' in key_names:

            if self.Number_Index > 1:
                self.Number_Index -= 1
            else:
                self.Number_Index = 6

            Now_Index = (self.round - 1) * 4 + self.Number_position
            self.Number_Label[Now_Index].element.text = str(self.Number_Index)
            return 1

        if 'DOWN' in key_names:

            if self.Number_Index < 6:
                self.Number_Index += 1
            else:
                self.Number_Index = 1

            Now_Index = (self.round - 1) * 4 + self.Number_position
            self.Number_Label[Now_Index].element.text = str(self.Number_Index)
            return 1


    def on_key_press(self, key, modifiers):

        self.keys_pressed.add(key)
        self.update_text()


    def on_key_release(self, key, modifiers):

        self.keys_pressed.remove(key)


    def Guess(self, GuessString = None):

        """The main Guess function
        returns a list whose len is self.Numbers: 
        [black,black,...,white,white,...,0,...,0]
        in which: black = 2, white = 1
        """
        if GuessString == None or (0 in GuessString):
            return None
        else:
            #print (GuessString, self.Result)
            i = 0
            Black = 0
            White = 0

            tLoc = [0 for i in range(self.Numbers)]
            tWLoc = [0 for i in range(self.Numbers)]
            for i in range(self.Numbers):
                if GuessString[i] == self.Result[i]:
                    Black = Black + 1
                    tLoc[i] = 1
                    tWLoc[i] = 1 

            for i in range(self.Numbers):
                if tWLoc[i] == 1:
                    continue
                for j in range(self.Numbers):

                    if (GuessString[i] == self.Result[j]) & (tLoc[j] != 1) & (i != j):
                        White = White + 1
                        tLoc[j] = 1
                        break

            tChar = []
            for i in range(Black):
                tChar.append(2)
            for i in range(White):
                tChar.append(1)
            for i in range(self.Numbers - White - Black):
                tChar.append(0)

            return tChar


if __name__ == '__main__':

    cocos.director.director.init(width = 664, height = 808, caption ='Guess Number by Crix', resizable = False)
    Game = TableLayer(6, 4, 13)
    main_scene = cocos.scene.Scene(Game)
    cocos.director.director.run(main_scene)

