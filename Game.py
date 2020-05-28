import time
import cv2
import numpy as np
from random import randrange
from environment import Env
from pynput import keyboard


HEIGHT = 3
WIDTH = 10
BLOCK_SIZE = 50
DELAY = 0.5

def animation(matrix): #animacia prostredia, volaj ju az po skonceni ucenia
    img = np.zeros((HEIGHT * BLOCK_SIZE,WIDTH * BLOCK_SIZE, 3), np.uint8)

    for i in range(HEIGHT):
        for j in range(WIDTH):
            if matrix[i, j] == 0:
                img = cv2.rectangle(img, (j * BLOCK_SIZE + 5, i * BLOCK_SIZE + 5),
                                    ((j+1) * BLOCK_SIZE - 5, (i+1) * BLOCK_SIZE - 5), (255,255,255), -1) # biela / 0
            elif matrix[i, j] == -1:
                img = cv2.rectangle(img, (j * BLOCK_SIZE + 5, i * BLOCK_SIZE + 5),
                                    ((j+1) * BLOCK_SIZE - 5, (i+1) * BLOCK_SIZE - 5), (0,0,255), -1) # cervena / -1
            elif matrix[i, j] > 0.09 and matrix[i, j] < 1.9:
                img = cv2.rectangle(img, (j * BLOCK_SIZE + 5, i * BLOCK_SIZE + 5),
                                    ((j+1) * BLOCK_SIZE - 5, (i+1) * BLOCK_SIZE - 5), (0,255,0), -1) # zelena / 1
            elif matrix[i, j] == 2:
                img = cv2.rectangle(img, (j * BLOCK_SIZE + 10, i * BLOCK_SIZE + 10),
                                    ((j+1) * BLOCK_SIZE - 10, (i+1) * BLOCK_SIZE - 10), (255,0,0), -1) # modra / 2

    cv2.imshow('game', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
    time.sleep(env.getDelay())

def on_press(key):
        if key == keyboard.Key.space:
            env.jump()
            print("space")
            time.sleep(env.getDelay() *2)
            env.jumpback()



if __name__ == '__main__':
    height = HEIGHT
    width = WIDTH
    end = 0
    env = Env(height, width)

    
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    #listener.join()  # remove if main thread is polling self.keys

    while(end == 0):
        animation(env.get_animation_matrix())
        env.step()
        #if(env.getScore() == 1):
            #env.jump()
        #if(env.getScore() == 2):
            #env.jumpback()
        env.obstacle()
        env._Env__score += 1
        print(env.getScore())
        if(env.getScore()%10 == 0):
            env.setDelay(env.getDelay() - 0.05)

        if(env.crash()):
            print("koniec hry")
            env.reset()


    cv2.destroyAllWindows()

