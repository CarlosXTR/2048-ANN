
from game import Game2048
from qlearning import Qlearning

if __name__ == "__main__":
    game = Game2048(4, 4)
    qlearn = Qlearning(game)
    qlearn.start()
