import pygame as pg 
import sys 
import time 
from pygame.locals import *
import socket


class GameGen():

    def __init__(self):
        
        self.current_player = 'x'
        self.winner = None
        self.draw = None
        self.width, self.height = 400, 400
        self.white = (255, 255, 255)
        self.line_color = (0, 0, 0)
        self.board = [[None]*3, [None]*3, [None]*3] 
        pg.init() 
        self.fps = 60
        self.CLOCK = pg.time.Clock() 
        self.screen = pg.display.set_mode((self.width, self.height + 100), 0, 32) 
       
        self.port=8000
        self.ip="127.0.0.1"
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.player_no = None
        self.connect()
        pg.display.set_caption(f"Tic Tac Toe: Player {self.player_no}") 
        initiating_window = pg.image.load("cover-start.jpg") 
        x_img = pg.image.load("X_modified.png") 
        y_img = pg.image.load("o_modified.png") 
        
        self.initiating_window = pg.transform.scale(initiating_window, (self.width, self.height + 100)) 
        self.x_img = pg.transform.scale(x_img, (85, 85)) 
        self.o_img = pg.transform.scale(y_img, (85, 85))
        
       
    
    def initialize(self):
        self.screen.blit(self.initiating_window, (0, 0)) 
      
        # updating the display 
        pg.display.update() 
        time.sleep(2)                     
        self.screen.fill(self.white) 
       
        # drawing vertical lines 
        pg.draw.line(self.screen, self.line_color, (self.width / 3, 0), (self.width / 3, self.height), 7) 
        pg.draw.line(self.screen, self.line_color, (self.width / 3 * 2, 0), (self.width / 3 * 2, self.height), 7) 
       
        # drawing horizontal lines 
        pg.draw.line(self.screen, self.line_color, (0, self.height / 3), (self.width, self.height / 3), 7) 
        pg.draw.line(self.screen, self.line_color, (0, self.height / 3 * 2), (self.width, self.height / 3 * 2), 7)
        
        self.draw_status()
        #self.s.sendall(f"Player {self.player_no} ready!".encode("utf-8"))
    
    def draw_status(self):
        
        if self.winner is None:
            
            if self.player_no == '1' and self.current_player == 'x' or self.player_no == '2' and self.current_player == 'o':
                message = "Your turn"
            else:
                message = f"{self.current_player}\'s turn"    
        
        else:
            message = f"{self.winner.upper()} won!"
        
        if self.draw:
            message = "Draw!"
        
        font = pg.font.Font('mont.otf', 30) 
        text = font.render(message, 1, (255, 255, 255)) 
        self.screen.fill ((0, 0, 0), (0, 400, 500, 100)) 
        text_rect = text.get_rect(center =(self.width / 2, 500-50)) 
        self.screen.blit(text, text_rect) 
        pg.display.update() 
    
    def check_win(self):
        
        for row in range(0, 3): 
            if((self.board[row][0] == self.board[row][1] == self.board[row][2]) and (self.board [row][0] is not None)): 
                self.winner = self.board[row][0] 
                pg.draw.line(self.screen, (250, 0, 0), 
                             (0, (row + 1)*self.height / 3 -self.height / 6), 
                             (self.width, (row + 1)*self.height / 3 - self.height / 6 ), 
                             4) 
                break
       
        # checking for winning columns 
        for col in range(0, 3): 
            if((self.board[0][col] == self.board[1][col] == self.board[2][col]) and (self.board[0][col] is not None)): 
                self.winner = self.board[0][col] 
                pg.draw.line (self.screen, (250, 0, 0), ((col + 1)* self.width / 3 - self.width / 6, 0), 
                              ((col + 1)* self.width / 3 - self.width / 6, self.height), 4) 
                break
        
        
        if (self.board[0][0] == self.board[1][1] == self.board[2][2]) and (self.board[0][0] is not None): 
          
            self.winner = self.board[0][0] 
            pg.draw.line (self.screen, (250, 70, 70), (50, 50), (350, 350), 4) 
              
        if (self.board[0][2] == self.board[1][1] == self.board[2][0]) and (self.board[0][2] is not None): 
              
            # game won diagonally right to left 
            self.winner = self.board[0][2] 
            pg.draw.line (self.screen, (250, 70, 70), (350, 50), (50, 350), 4) 
       
        if(all([all(row) for row in self.board]) and self.winner is None ): 
            self.draw = True
           
        self.draw_status() 
    
    def drawXO(self, row, col):
          
        
        if row == 1: 
            posx = 30
              
        # of 30 from the game line      
        if row == 2:       
            posx = self.width / 3 + 30
            
        if row == 3: 
            posx = self.width / 3 * 2 + 30
       
        if col == 1: 
            posy = 30
              
        if col == 2: 
            posy = self.height / 3 + 30
          
        if col == 3: 
            posy = self.height / 3 * 2 + 30
              
        # setting up the required board  
        # value to display 
        self.board[row-1][col-1] = self.current_player 
          
        if(self.current_player == 'x'): 
              
            # pasting x_img over the screen  
            # at a coordinate position of 
            # (pos_y, posx) defined in the 
            # above code 
            self.screen.blit(self.x_img, (posy, posx)) 
            self.current_player = 'o'
          
        else: 
            self.screen.blit(self.o_img, (posy, posx)) 
            self.current_player = 'x'
        pg.display.update() 
   
    def user_click(self, counter): 
        x, y = pg.mouse.get_pos() 
        
        if(x < self.width / 3): 
            col = 1
          
        elif (x < self.width / 3 * 2): 
            col = 2
          
        elif(x < self.width): 
            col = 3
          
        else: 
            col = None
         
        if(y<self.height / 3): 
            row = 1
          
        elif (y<self.height / 3 * 2): 
            row = 2
          
        elif(y<self.height): 
            row = 3
          
        else: 
            row = None
            
        if(row and col and self.board[row-1][col-1] is None): 
            self.drawXO(row, col) 
            
            self.s.sendall(f"{row} {col} {counter}".encode("utf-8"))
            self.check_win()
            
            
        
    
    def reset_game(self): 
        time.sleep(3) 
        self.current_player = 'x'
        self.draw = False
        self.initialize() 
        self.winner = None
        self.board = [[None]*3, [None]*3, [None]*3]
    
    def draw_timeout(self):
    
        if self.player_no == 1:
            message = f"2 has timed out!"
        
        else:
            message = f"1 has timed out!"
        
        font = pg.font.Font('mont.otf', 30) 
        text = font.render(message, 1, (255, 255, 255)) 
        self.screen.fill ((0, 0, 0), (0, 400, 500, 100)) 
        text_rect = text.get_rect(center =(self.width / 2, 500-50)) 
        self.screen.blit(text, text_rect) 
        pg.display.update() 
    
    def draw_timedout(self):
    
        message = f"You have timed out!"
        
        
        font = pg.font.Font('mont.otf', 30) 
        text = font.render(message, 1, (255, 255, 255)) 
        self.screen.fill ((0, 0, 0), (0, 400, 500, 100)) 
        text_rect = text.get_rect(center =(self.width / 2, 500-50)) 
        self.screen.blit(text, text_rect) 
        pg.display.update()
        
        time.sleep(5)
        
        
    def start(self):
        
        self.initialize() 
        pos = None
        status = True

        counter, text = 30,'30'
        pg.time.set_timer(pg.USEREVENT, 1000)
        
        while(status):
            for event in pg.event.get():
                
                if counter == 0:
                    self.draw_timedout()
                    time.sleep(5)
                    pg.quit() 
                    sys.exit()
                    
                
                if counter > 30:
                    counter-=1
                    text = '30'
                    break
                
                if event.type == pg.QUIT: 
                    pg.quit() 
                    sys.exit()
                
                if self.player_no == '2':
                    if pos is None:
                        
                        pos = self.s.recv(1024).decode("utf-8")
                        print(pos)
                        try:
                            row, col, counter_new = int(pos.split()[0]), int(pos.split()[1]), int(pos.split()[2])
                            self.drawXO(row, col) 
                            self.check_win()
                            counter = 60 - counter_new
                            text = str(counter)
                        except:
                            status = False
                            self.draw_timeout()
                            pg.quit() 
                            sys.exit()

                    elif event.type is MOUSEBUTTONDOWN:
                        self.user_click(counter)
                        pos = None
                
                
                if event.type is MOUSEBUTTONDOWN and self.player_no == '1' and self.current_player == 'x':
                
                    self.user_click(counter)
                    
                    if(self.winner or self.draw):
        
                        time.sleep(5)
                        pg.quit() 
                        sys.exit()
                        
                    pos = self.s.recv(1024).decode("utf-8")
                    print(pos)
                    try:
                        row, col, counter_new = int(pos.split()[0]), int(pos.split()[1]), int(pos.split()[2])
                        self.drawXO(row, col) 
                        self.check_win()
                        counter =  60 - counter_new
                        text = str(counter)
                    
                    except:
                        status = False
                        self.draw_timeout()
                        time.sleep(5)
                        pg.quit() 
                        sys.exit()
                
                if event.type == pg.USEREVENT:
                    
                    if self.player_no == '1' and self.current_player == 'x':
                        counter -= 1
                        text = str(counter) if counter > 0 else 'boom!'
                        #print(counter)
                        
                    elif self.player_no == '2' and self.current_player == 'o':
                        counter -= 1
                        text = str(counter) if counter > 0 else 'boom!'
                        #print(counter)
                    
                    else:
                        
                        counter+=1
                        
                        
                if self.winner or self.draw:
                
                    time.sleep(5)
                    pg.quit() 
                    sys.exit()  
            
            else:
                
                pg.display.set_caption(f"Tic Tac Toe: Player {self.player_no} time remaining: {text}") 
                self.CLOCK.tick(self.fps) 
  
    def connect(self):
        
        self.s.connect((self.ip,self.port))
        self.player_no = self.s.recv(1024).decode("utf-8")
        print(self.player_no)
        

if __name__ == '__main__':
    
    game = GameGen()
    game.start()