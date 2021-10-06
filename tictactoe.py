import itertools
import os
import random

class Game(object):

    x = 0
    o = 1
    cat = 2

    def __init__(self):
        self.xs = [0] * 9
        self.os = [0] * 9

    def key(self):
        return tuple(self.xs), tuple(self.os)

    def key_with(self, player, square):
        x = self.xs
        o = self.os
        if player == self.x:
            x = list(x)
            x[square] = 1
        elif player == self.o:
            o = list(o)
            o[square] = 1
        return tuple(x), tuple(o)

    def record_turn(self, player, square):
        if player == self.x:
            self.xs[square] = 1
        elif player == self.o:
            self.os[square] = 1

    def winner(self):
        if self._did_win(self.xs):
            return self.x
        elif self._did_win(self.os):
            return self.o
        return self.cat

    def _did_win(self, player):
        # 0 1 2
        # 3 4 5
        # 6 7 8

        if player[4] == 1:
            if player[0] == 1:
                if player[8] == 1:
                    return True
            if player[1] == 1:
                if player[7] == 1:
                    return True
            if player[2] == 1:
                if player[6] == 1:
                    return True
            if player[5] == 1:
                if player[3] == 1:
                    return True

        if player[0] == 1:
            if player[1] == 1:
                if player[2] == 1:
                    return True
            if player[3] == 1:
                if player[6] == 1:
                    return True

        if player[8] == 1:
            if player[5] == 1:
                if player[2] == 1:
                    return True
            if player[7] == 1:
                if player[6] == 1:
                    return True

        return False

    def draw(self):
        os.system('clear')

        print(self._player_at(0), end='')
        print('|', end='')
        print(self._player_at(1), end='')
        print('|', end='')
        print(self._player_at(2), end='')
        print('    0|1|2')

        print('-+-+-    -+-+-')

        print(self._player_at(3), end='')
        print('|', end='')
        print(self._player_at(4), end='')
        print('|', end='')
        print(self._player_at(5), end='')
        print('    3|4|5')

        print('-+-+-    -+-+-')

        print(self._player_at(6), end='')
        print('|', end='')
        print(self._player_at(7), end='')
        print('|', end='')
        print(self._player_at(8), end='')
        print('    6|7|8')

    def _player_at(self, square):
        if self.xs[square]:
            return 'X'
        if self.os[square]:
            return 'O'
        return ' '

class Trainer(object):

    tempfile = '/tmp/tictactoe'

    def __init__(self):
        self.data = {}

    def train(self):
        for board in itertools.permutations(range(9)):
            self.record_game(board)
        self.save()

    def record_game(self, board):
        game, turns = Game(), []
        player, other = Game.x, Game.o

        for turn in board:
            game.record_turn(player, turn)
            turns.append(game.key())
            player, other = other, player

            winner = game.winner()
            if winner != Game.cat:
                break

        for turn in turns:
            self.data.setdefault(turn, [0, 0, 0])[winner] += 1

    def save(self):
        data = {}
        for key, (x, o, cat) in self.data.items():
            total = x + o + cat
            data[key] = (x / total, o / total, cat / total)

        if os.path.isfile(self.tempfile):
            os.remove(self.tempfile)

        with open(self.tempfile, 'w') as f:
            f.write(str(data))

class Player(object):

    def __init__(self):
        self.player = random.choice((Game.x, Game.o))
        self.player_str = 'X' if self.player == Game.x else 'O'
        self.game = Game()
        with open(Trainer.tempfile, 'r') as f:
            self.data = eval(f.read())

    def play(self):
        player, other = Game.x, Game.o
        for turn in range(9):
            self.game.draw()
            if player == self.player:
                square = self._get_input_square()
            else:
                square = self._get_cpu_square(player)
            self.game.record_turn(player, square)
            player, other = other, player

            winner = self.game.winner()
            if winner != Game.cat:
                break

        self.game.draw()
        if winner == self.player:
            print('GAME OVER!  YOU WIN!')
        elif winner == Game.cat:
            print('CATS GAME!')
        else:
            print('GAME OVER!  COMPUTER WINS!')

    def _get_input_square(self):
        while True:
            try:
                square = int(input('You are player %s, choose your square:  ' %
                        self.player_str))
                assert square >= 0 and square < 9
                return square
            except KeyboardInterrupt:
                exit(1)
            except:
                print('that is not a valid square')
                continue

    def _get_cpu_square(self, player):
        available = [i for i in range(9) if not self.game.xs[i] and not
                self.game.os[i]]
        top_val, top_choices = float('-inf'), []
        for choice in available:
            val = self.data[self.game.key_with(player, choice)][player]
            if val > top_val:
                top_choices = [choice]
                top_val = val
            elif val == top_val:
                top_choices.append(choice)

        return random.choice(top_choices)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] in ('--train', '-t'):
            Trainer().train()
        else:
            print('usage: python3 tictactoe.py [-t|--train]')
            exit(1)
    else:
        Player().play()
