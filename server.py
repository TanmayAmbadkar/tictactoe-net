import socket
from func_timeout import func_timeout, FunctionTimedOut

def get_position(player):
    
    pos=player.recv(1024)
    return pos
    

def main():
    ip="127.0.0.1"
    port=8000
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((ip,port))
        s.listen()
        player1, address1 = s.accept()
        print('Player 1 connected by address',address1)
        player1.sendall("1".encode("utf-8"))
        
        s.listen()
        player2, address2  = s.accept()
        player2.sendall("2".encode("utf-8"))
        print('Player 2 connected by address', address2)
        
        while True:
            
            try:
                pos_x=func_timeout(10, get_position, args = (player1, ))
                player2.sendall(pos_x)
            
            except FunctionTimedOut:
                
                print("No input received from Player 1, Player 2 wins!")
                break
            
            try:
                pos_o=func_timeout(10, get_position, args = (player2, ))
                player1.sendall(pos_o)
            
            except FunctionTimedOut:
                
                print("No input received from Player 2, Player 1 wins!")
                break
                
            if pos_o == b'':
                break;
                # con.sendall()

if __name__ == '__main__':
    
    main()