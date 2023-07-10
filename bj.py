import random as rand
import time
import bj_cards


class Player:
    """A class representing a player of a game.

    === Public Attributes ===
    name: The name of the player.
    hand: the player's cards, represented as a list object.
    score: the total score of a player's hand.

    === Private Attributes ===
    _bust: A boolean object representing whether the player is Bust.
    """
    name: str
    hand: list[str]
    score: int
    _bust: bool

    def __init__(self, _id: int) -> None:
        """Create a new Player called 'Player <_id>'. Initially, the player
        has no cards in their hand, a score of 0, and is not bust.
        """
        if _id == 0:
            self.name = 'Dealer'
        else:
            self.name = 'Player ' + str(_id)
        self.hand = []
        self.score = 0
        self._bust = False

    def calculate_score(self) -> None:
        """Calculate the total score of the player's hand and update
        their 'score' attribute accordingly.
        """
        total = []
        for card in self.hand:
            total.append(bj_cards.blackjack_scores[card])

        if sum(total) > 21:
            while 11 in total:
                index = total.index(11)
                total[index] = 1

        if sum(total) > 21:
            self._bust = True

        self.score = sum(total)

    def is_bust(self) -> bool:
        """Return whether the player is Bust (has a score greater than 21).
        """
        return self._bust


class Game:
    """A class representing a single game of Blackjack.

    === Public Attributes ===
    deck: The deck of cards being used for the game. Represented as a
        dictionary, with keys being ints ranging from 1 to 52 and values
        being strings of their respective card names.
    dealer: The dealer of the game that every player is playing against.
    players: A list of players playing this game.
    """
    deck: dict[int, str]
    dealer: Player
    players: list[Player]

    def __init__(self, number_players: int) -> None:
        """Create a new instance of this game with <num_players> number of
        players. Initially, the deck being used is a full deck, and only
        the dealer is dealt immediately.
        """
        self.deck = bj_cards.fresh_deck_of_cards.copy()
        self.dealer = Player(0)
        self.deal(self.dealer)
        self.dealer.calculate_score()
        self.players = []
        for n in range(number_players):
            new_player = Player(n+1)
            self.players.append(new_player)

    def start(self) -> None:
        """Deal each player and print out their name and hand.
        """
        print('\n')
        for player in self.players:
            time.sleep(0.5)
            self.deal(player)
            player.calculate_score()
            print(f"{player.name}'s hand: {player.hand}")

    def deal(self, player: Player) -> None:
        """Give player 2 cards from the deck.
        """
        card1, card2 = _pull_card(self.deck), _pull_card(self.deck)
        player.hand.append(card1)
        player.hand.append(card2)

    def display_turn(self, player: Player) -> None:
        """Show player their hand and score, and give them the option
        to hit or stand iff they do not have a score of 21.
        """
        dealers_hand = ['*****', self.dealer.hand[1]]

        players_hand = player.hand
        players_score = player.score

        time.sleep(0.5)
        print('\n')
        print(f"Dealer's Hand: {dealers_hand}")
        print(f"{player.name}'s Hand: {players_hand}, Score: {players_score}")
        # print(f"{player.name}'s Score: {players_score}")
        if players_score == 21:
            time.sleep(0.5)
            print('Blackjack!!!')

            ans = input('Press [c] to celebrate!')
            while ans != 'c':
                ans = input('Press [c] to celebrate!')
        else:
            time.sleep(0.5)
            ans = input("Hit or Stand? [h] or [s] ")
            while ans != 'h' and ans != 's':
                print('Please enter [h] or [s] ')
                ans = input("Hit or Stand? [h] or [s] ")

        if ans == 'h':
            self._hit(player)

        elif ans == 's':
            self._pass(player)

        elif ans == 'c':
            print('WOOOOOOO!!!!')

    def _hit(self, player: Player):
        """Give the player another card. If the players score with this
        new hand is still less than 21, give them the option to hit or
        stand again.
        """
        print('\n')
        card = _pull_card(self.deck)
        time.sleep(0.5)
        print(f"{player.name}'s card is the {card}.")
        player.hand.append(card)
        player.calculate_score()
        if player.score == 21:
            time.sleep(0.5)
            print(f"{player.name}'s score is {player.score}. Blackjack!!!")
        elif not player.is_bust():
            if player is self.dealer:
                self.display_dealer_turn()
            else:
                self.display_turn(player)
        else:
            print(f"{player.name}'s score is {player.score}. Bust!")

    def display_dealer_turn(self) -> None:
        """First, show the dealer's hand and score. If at least one player
        is not Bust yet and the dealer has a score less than 17, the dealer
        hits. Otherwise, the dealer stands.
        """
        time.sleep(0.5)
        print('\n')
        print(f"Dealer's Hand: {self.dealer.hand}")
        print(f"Dealer's Score: {self.dealer.score}")
        time.sleep(0.5)

        everyone_bust = True
        for player in self.players:
            if not player.is_bust():
                everyone_bust = False
                break
        if everyone_bust:
            self._pass(self.dealer)
        elif self.dealer.score == 21:
            print('Dealer has Blackjack!')
        elif self.dealer.score >= 17:
            self._pass(self.dealer)
        else:
            print('Dealer Hits')
            self._hit(self.dealer)

    def display_winners(self) -> None:
        """Show the winners of this game. The winners are calculated
         as follows:
            - if any players bust, they lose.
            - if the dealer busts, every player who is not bust yet wins.
            - if the dealer does not bust, every player who has a score
                greater than the dealer wins. If no player has a score greater
                than the dealer, the dealer wins.
        """
        print('\n')
        scores = []
        for player in self.players:
            if not player.is_bust():
                scores.append(player.score)
            else:
                scores.append(0)

        winners = ""
        max_score = max(max(scores), self.dealer.score)

        if self.dealer.is_bust():
            for n in range(len(scores)):
                if scores[n] != 0:
                    winners = winners + "Player " + f"{n+1}" + ", "
            print("Congratulations " + winners + "you win!")

        elif self.dealer.score == max_score:
            for n in range(len(scores)):
                if scores[n] == max_score:
                    winners = winners + "Player " + f"{n+1}" + ", "
            if winners == '':
                print('The dealer wins. Better luck next time!')
            else:
                print("Bravo " + winners + "you tie the dealer. Push!")
        else:
            ties = ''
            for n in range(len(scores)):
                if scores[n] > self.dealer.score:
                    winners = winners + "Player " + f"{n+1}" + ", "
                elif scores[n] == self.dealer.score:
                    ties = ties + "Player " + f"{n+1}" + ", "
            print("Congratulations " + winners + "you win!")
            time.sleep(0.5)
            if ties != '':
                print("Bravo " + ties + "you tie the dealer. Push!")

    def _pass(self, player: Player):
        """Do not give the player a new card and move on to the next
        player's turn.
        """
        print('\n')
        print(f'{player.name} Stands.')


def _pull_card(deck: dict) -> str:
    """Pull a card from the given deck and change its value in the
    deck to 'pulled' to signal that the card can no longer be selected.
    If the card you select has already been pulled, pull a new card.
    """
    card_key = rand.randint(1, 52)
    while deck[card_key] == 'pulled':
        card_key = rand.randint(1, 52)
    card = deck[card_key]
    deck[card_key] = 'pulled'

    return card


if __name__ == '__main__':
    print('Welcome to Blackjack!')
    time.sleep(0.5)
    num_players = input('How many players are playing? ')
    while not num_players.isdigit() or int(num_players) < 1 or int(num_players) > 6:
        print('Please enter a valid number between 1 and 6.')
        num_players = input('How many players are playing? ')

    num_players = int(num_players)
    new_game = Game(num_players)
    new_game.start()
    for i in range(num_players):
        new_game.display_turn(new_game.players[i])
    new_game.display_dealer_turn()
    new_game.display_winners()
    time.sleep(0.5)
