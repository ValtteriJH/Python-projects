"""
Poker night at TUT
Valtteri Huhdankoski 283386
TTY 22:08:19
A simple standalone graphic poker game (training) simulator with the same rules that apply at a casino. 

Tähtään skaalautuvan projektin pisteisiin. Pelin ohjeet ilmestyvät ikkunaan kun käynnistät ohjelman, ja käsien vahvuudet
selviävät kun klikkaat "Ranking of poker hands" nappia.
Pelin alkaessa pelaaja saa korttinsa näkyviin "Show cards"- näppäimellä, jonka jälkeen hän voi korttia klikkaamalla
lukita sen, ja sitten vaihtaa loput "switch"- napilla, kun pelaaja on tyytyväinen kortteihinsa (tai switchit ovat loppu)
, niin vuoroa vaihdetaan "End turn"- napilla. Kun kaikki pelaajat ovat saaneet vuoronsa, niin voittajan kortit
paljastetaan, ja muiden saama tulos kirjataan alle.

Korttien nimeämisessä käytettiin englanninkielestä tulevia nimityksiä arvojärjestyksessRä:
Spades = Padat = S
Hearts = Hertta = H
Diamonds = Ruutu = D
Clubs = Risti = C

Pelin jälkeen voi ottaa revanssin "restart"- napilla
Pelien välisiä tuloksia, tai pelaajien rahoja ei kirjata koska uhkapelaaminen on laitonta.

Peli on rakennettu 4 peruspilarin päälle:
1. Perusfunktiot ja main loop, jolla kasataan pakka, määritellään kortit, ja pyöräytetään setup,- ja peli-ikkunat käyntiin
2. Korttiolio, joka muistaa maansa, arvonsa, värinsä, kuvatiedostonsa(PIL support kielletty, joten ei tässä versiossa),
ja paikkansa pelaajien kädessä
3. Setup ikkuna, joka ottaa vastaan pelaajalta pelaajien kokonaismäärän, ja nimet, ja tarkistaa etteivät tiedot ole
solmussa keskenään
4. Itse peli, joka sisältää pelilogiikan, ja GUI:n peliin.

"""
#TODO: Fix UI elements (Grammar, and try to make the alarm windows into a dropdown menu), get the graphis working
#TODO: Finish menu items. Exit button, about button, settings for displaying rules at the start and colorful cards
#                                                                                                   and white cards

from tkinter import *
from tkinter import messagebox
import random
from time import sleep


class Probabilities:
    def __init__(self):
        pass  # TODO Win condition probabilities as separate entities?
    # Module constructed and used at the black jack sim.


class StartWindow:
    """
    Launches first when you start the program. Takes in player count, and their respective names, and then returns them
    to the main window.
    """

    def __init__(self):
        self.__start_window = Tk()
        self.__start_window.title("Initialization")
        self.__start_window.geometry("600x100")
        self.__player_count = Entry()
        self.__help_label1 = Label(text="How many players will attend? Input a single integer 1-5")
        self.__readybutton = Button(self.__start_window, text="Ready to play!", command=self.__start_window.destroy
                                    , state=DISABLED)

        self.__errorlabel = Label("")
        self.__help_label2 = Label(text="What are the names of the players? Separate with commas")
        self.__names = Entry()
        self.__ok_button = Button(self.__start_window, text="OK!", command=self.return_info)
        self.__readybutton.grid(row=3, column=0, columnspan=2)
        self.__ok_button.grid(row=3, column=3, columnspan=1)
        self.__help_label1.grid(row=0, column=1)
        self.__help_label2.grid(row=1, column=1)
        self.__names.grid(row=1, column=2, columnspan=2)
        self.__player_count.grid(row=0, column=2, columnspan=2)
        self.__errorlabel.grid(row=5, column=2, columnspan=2)

        self.__player_names = []

    def quit(self):
        self.__start_window.destroy()

    def return_info(self):
        """
        Evaluates and checks all given data, if all is good, it return's it to the main function at the bottom of the
        file
        :return: player count, and their respective names
        """
        self.__player_names = []
        try:
            self.__players = int(self.__player_count.get())
            if self.__players > 5:
                self.__errorlabel.configure(text="Too many players!")
                self.__readybutton.configure(state=DISABLED)
                return 0

            names = self.__names.get().split(",")
            for i in names:
                i = i.strip()
                self.__player_names.append(i)

                if i == "":
                    self.__errorlabel.configure(text="A player's name cant be empty!")
                    self.__readybutton.configure(state=DISABLED)
                    return 0

            if len(self.__player_names) == self.__players:
                self.__readybutton.configure(state=NORMAL)
                self.__errorlabel.configure(text="")
            else:
                self.__errorlabel.configure(text="Amount of players and names don't match up!")
                self.__readybutton.configure(state=DISABLED)
                return 0

        except ValueError:
            self.__errorlabel.configure(text="Please input a single integer as player count")
            self.__readybutton.configure(state=DISABLED)

    def start(self):
        self.__start_window.mainloop()
        try:
            return self.__players, self.__player_names
        except AttributeError:
            return 0


class PokerGame:

    def __init__(self, player_count, player_names, player_hands, card_ranks, rest_of_the_deck, restarted):
        self.__main_window = Tk()
        self.__main_window.title("Poker night at the TUT")
        self.__player_count = player_count
        self.__player_names = player_names
        self.__player_cards = player_hands
        self.__deck = rest_of_the_deck
        self.__card_ranks = card_ranks
        if not restarted:
            self.rules()
        if self.__player_count <= 3:  # Switch limiter
            self.__maximum_switches = 2
        else:
            self.__maximum_switches = 1

        self.__current_switches = 0
        self.__cards_visible = 1
        # self.__player_color = ["purple", "yellow", "blue", "green", "white"]    # Players' color-coding for easier interpretation
        self.__player_color = ["white", "white", "white", "white", "white"]
        self.__turn = 0
        self.__selections = []
        self.__reset_button = Button()
        self.__explanation_box = Label()

        self.__card_buttons = []
        self.__lock_labels = []
        self.__start_turn_button = Button(self.__main_window, text="Show cards", command=self.flip_cards)
        self.__quit_button = Button(self.__main_window, text="Quit", command=self.quit)
        self.__swap_cards_button = Button(self.__main_window, text="switch", command=self.swap_cards)
        self.__end_turn_button = Button(self.__main_window, text="End turn", command=self.end_turn)

        self.__legend = Button(self.__main_window, text="Ranking of poker hands", command=legend)
        self.__legend.grid(row=0, column=99)

        self.__start_turn_button.grid(row=1, column=99)
        self.__quit_button.grid(row=5, column=99)
        self.__swap_cards_button.grid(row=2, column=99)
        self.__end_turn_button.grid(row=3, column=99)

        menubar = Menu(self.__main_window)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.quit)
        filemenu.add_command(label="Open", command=self.quit)
        filemenu.add_command(label="Save", command=self.quit)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.__main_window.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Rules", command=self.rules)
        helpmenu.add_command(label="Card combination rankings", command=legend)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.__main_window.config(menu=menubar)
 

        self.turn()

    def turn(self):
        """
        This function is what draws up players' turn in its entirety. It changes the buttons according to the current
        player's hand and colour
        """
        current_player_cards = []

        self.__card_buttons = []
        self.__lock_labels = []

        self.__selections = [False] * 5
        hand = self.__player_cards[self.__turn]
        self.__namelabel = Label(text="   {}'s turn   ".format(self.__player_names[self.__turn]))
        self.__namelabel.grid(row=0, column=0, columnspan=4)

        for card, position in zip(hand, range(5)):
            current_player_cards.append("{}".format(card))
            new_card = Button(self.__main_window, text="{}{}".format(card.my_suit(), card.my_value()),
                              foreground="{}".format(card.my_color()), font=("Helvetica", 40)
                              , command=lambda my_pos=position: self.lock_me(my_pos))  # Lambda'ing the locking mechanic

            # Picture cards attempt
            # new_card = Button(self.__main_window, image=PhotoImage(file=card.my_face()), highlightthickness=0, bd=0
            #          , command=lambda my_pos=card.my_pos(): self.lock_me(my_pos))

            new_lock_label = Label(text="Swap")
            new_lock_label.grid(row=1, column=position)
            new_card.configure(width=3, height=2, borderwidth=5)
            new_card.grid(row=2, column=position)

            self.__card_buttons.append(new_card)
            self.__lock_labels.append(new_lock_label)
            self.flip_cards()
            if self.__cards_visible == 1:
                self.flip_cards()
        self.buttons_update()
        if self.__player_names[self.__turn].lower() == "ai":
            for i in range(self.__maximum_switches):  # Loops ai for the amount of switches
                self.ai()
            self.end_turn()

    def end_turn(self):
        self.__turn += 1
        if self.__turn >= self.__player_count:
            self.win_conditions()
            return 0

        self.turn()
        self.buttons_update()

    def were_the_same(self, list):
        """
        Takes a player's hand's value list, and returns a 5 long list of how many similar cards were given.
        :param list:  valuelist
        """

        similarities = []
        counter = 0

        for i in list:
            for j in list:
                if i == j:
                    counter += 1
            similarities.append(counter)
            counter = 0
        return similarities

    def in_range(self, values):
        current_count = 0
        in_my_range = []
        for i in values:
            L = i
            for counter in range(L, L + 4):
                for suspect in values:
                    if counter == suspect:
                        current_count += 1
            in_my_range.append(current_count)
            current_count = 0
        return in_my_range

    def ai(self):
        """
        Computer player, starts up by typing ai in player name screen.
        :return: 0
        """
        self.buttons_update()
        cards = self.__player_cards[self.__turn]
        values = []
        suits = []
        for i in cards:
            values.append(i.my_value())
        for i in cards:
            suits.append(i.my_suit())
        self.__swap_cards_button.configure(state=DISABLED)
        for i, card in zip(self.__card_buttons, self.__player_cards[self.__turn]):
            i.config(text="@", foreground="{}".format("purple"), font=("Helvetica", 40),
                     state=DISABLED)

        same_values = self.were_the_same(values)
        same_suits = self.were_the_same(suits)
        in_my_range = self.in_range(values)

        if 4 in same_suits:
            for i, runner in zip(same_suits, range(5)):
                if i == 4:
                    self.lock_me(runner)
            sleep(0.5)
            self.buttons_update()
            self.__main_window.update_idletasks()
        elif sum(same_values) > 5:
            for i, runner in zip(same_values, range(5)):
                if i >= 2:
                    self.lock_me(runner)
                    values[runner] = 0  # Removing the selected values in case they are the highest so far
                    sleep(0.12)
                    self.buttons_update()
                    self.__main_window.update_idletasks()
            if sorted(same_values) != [1, 1, 1, 1, 0]:
                self.lock_me(values.index(int(max(values))))
                sleep(0.3)
                self.buttons_update()
                self.__main_window.update_idletasks()
        elif 4 in in_my_range:
            for i, runner in zip(in_my_range, range(4)):
                if i == 4:
                    self.lock_me(runner)
            sleep(0.5)
            self.buttons_update()
            self.__main_window.update_idletasks()
        else:
            self.lock_me(values.index(max(values)))
        sleep(0.3)
        self.buttons_update()
        self.__main_window.update_idletasks()
        self.swap_cards()
        self.__selections = [False] * 5
        self.__swap_cards_button.configure(state=NORMAL)   # Making sure nobody messes with the robot

    def win_conditions(self):
        """
        Scores players' hands bu giving initial points by their combination. If a tie occurs, the score is concluded by
        the combined strength of the cards.
        
        Scoring system:
                high up to 14
                pair 15
                two pairs 16
                three of a kind 17
                straight 18
                flush = 19
                full house = 20
                four of a kind = 21
                straight flush 22
        Checks who won, sets up the winning screen, and launches it.
        """
        all_scores = []
        final_hands = []

        for hand in self.__player_cards:
            player_scores = []
            suits = []
            values = []
            score = 0

            for card in hand:
                suits.append(card.my_suit())
                values.append(card.my_value())
                score += card.my_rank()
            test_list = []
            test_list.append(self.in_range(values))

            player_scores.append(score)
            if suits[1:] == suits[:-1] and sorted(values) == list(range(sorted(values)[0], sorted(values)[4] + 1)):
                player_scores.append(22)
                final_hands.append("STRAIGHT FLUSH")

            elif 4 in self.were_the_same(values):
                final_hands.append("Four of a kind!")
                player_scores.append(21)

            elif 3 in self.were_the_same(values) and 2 in self.were_the_same(values):
                final_hands.append("Full house")
                player_scores.append(20)

            elif suits[1:] == suits[:-1]:
                final_hands.append("Flush")
                player_scores.append(19)

            elif sorted(values) == list(range(sorted(values)[0], sorted(values)[4] + 1)):
                final_hands.append("Straight")
                player_scores.append(18)

            elif 3 in self.were_the_same(values):
                final_hands.append("Three of a kind")
                player_scores.append(17)

            elif [1, 2, 2, 2, 2] == sorted(self.were_the_same(values)):
                final_hands.append("Two pairs")
                player_scores.append(16)

            elif 2 in self.were_the_same(values):
                final_hands.append("Pair")
                player_scores.append(15)

            else:
                player_scores.append(sorted(values)[4])
                final_hands.append("High {}".format(sorted(values)[4]))

            all_scores.append(player_scores)

        self.__turn = 0
        self.buttons_update()
        self.__swap_cards_button.configure(state=DISABLED)
        self.finale(all_scores, final_hands)

    def finale(self, all_scores, hands):
        """
        Displays the winning hand, in the corresponding player's colour, and articulates all hands, enables reset button
        :param all_scores: list in a list, first each player's cards' combined value, then hand strength
        :param hands: each player's final hand
        """
        cur_highest = 0
        win_index = 0
        for scores, index in zip(all_scores, range(self.__player_count)):
            if scores[1] > cur_highest:
                cur_highest = scores[1]
                win_index = index
            elif scores[1] == cur_highest:
                if all_scores[win_index][0] < scores[0]:
                    win_index = index

        winner = self.__player_names[win_index]
        self.__turn = win_index
        self.buttons_update()
        self.flip_cards()

        if self.__cards_visible == 0:
            self.flip_cards()

        for i in self.__lock_labels:
            i.configure(text="            ")  # Empties out the top labels

        self.__swap_cards_button.configure(state=DISABLED)
        self.__end_turn_button.configure(state=DISABLED)
        self.__namelabel.configure(text="  {} has won with {}!  ".format(winner, hands[win_index]))
        self.__namelabel.grid(row=0, column=0, columnspan=4)
        self.__reset_button.configure(text="Restart", command=self.restart)
        self.__reset_button.grid(row=5, column=4)
        explanation_phrase = []

        for name, hand in zip(self.__player_names, hands):
            explanation_phrase.append("{} got {}".format(name, hand))
            explanation_phrase.append(",  ")
        explanation_phrase.pop(self.__player_count * 2 - 1)
        explanation_text = "".join(explanation_phrase)
        self.__explanation_box.configure(text="{}".format(explanation_text))
        self.__explanation_box.grid(row=3, column=0, columnspan=7)

    def restart(self):
        """
        Restarts the game with new deck and new hands for each player, keeps the names same.
        """
        self.__main_window.destroy()
        deck, card_ranks = decker()
        player_hands = []

        for i in range(self.__player_count):
            player_hands.append(player_hand(deck, card_ranks))

        poker_time = PokerGame(self.__player_count, self.__player_names, player_hands, card_ranks, deck, True)
        poker_time.start()

    def flip_cards(self):
        """
        Flips cards to be visible, or hidden, while simultaneously updating their colours, and turning them off/on them
        """
        if self.__cards_visible == 1:
            for i in self.__card_buttons:
                i.configure(disabledforeground="{}".format(self.__player_color[self.__turn]),
                            background="{}".format(self.__player_color[self.__turn]), state=DISABLED)
            self.__cards_visible = 0
        else:
            self.__cards_visible = 1
            for i in self.__card_buttons:
                i.configure(background="{}".format(self.__player_color[self.__turn]), state=NORMAL)

    def swap_cards(self):
        current_hand = self.__player_cards[self.__turn]
        runner = -1

        for locked, card in zip(self.__selections, current_hand):
            runner += 1
            if not locked:
                self.__player_cards[self.__turn][runner] = pick_a_card(self.__deck, self.__card_ranks)
                self.__player_cards[self.__turn][runner].my_pos_set(runner)

        self.buttons_update()
        self.__current_switches += 1

        if self.__current_switches == self.__maximum_switches:
            self.__swap_cards_button.configure(state=DISABLED)
            self.__current_switches = 0

    def buttons_update(self):
        """
        Updates the UI
        """
        path = "C:/Users/Vallu/OneDrive/Codes/01_Python_course/Finalé/PNG/"
        # PhotoImage(file="{}{}".format(path, "bomb.gif"))
        # self.__bomb_picture = PhotoImage(file="bomb.gif")

        for i, card in zip(self.__card_buttons, self.__player_cards[self.__turn]):
            i.config(text="{}{}".format(card.my_suit(), card.my_value()),
                              foreground="{}".format(card.my_color()), font=("Helvetica", 40)
                              , command=lambda my_pos=card.my_pos(): self.lock_me(my_pos))

            # Card picture attempt
            # i.config(image=PhotoImage(file=card.my_face()), highlightthickness=0, bd=0
            #          , command=lambda my_pos=card.my_pos(): self.lock_me(my_pos))

            # i.config(image=PhotoImage(self.__bomb_picture), highlightthickness=0, bd=0
            #          , command=lambda my_pos=card.my_pos(): self.lock_me(my_pos))

        for text, selected in zip(self.__lock_labels, self.__selections):
            if not selected:
                text.configure(text="   Swap   ", fg="black")
            else:
                text.configure(text="   Locked   ", fg="green")

    def lock_me(self, position):
        """
        Locks individual clicked cards
        :param position: position of the card to be locked
        :return:
        """
        if self.__selections[position]:
            self.__lock_labels[position].configure(text="   Swap   ", fg="black")
            self.__selections[position] = False

        else:
            self.__lock_labels[position].configure(text="   Locked   ", fg="green")
            self.__selections[position] = True

    def rules(self):
        self.__info_box = messagebox.showinfo("Game has started!", "Everyone has been dealt 5 cards, "
        "player 1 starts, 1-2 swaps per player, depening if there are more than 3 players. Best hand wins.\n\n"
        "You can click any card you like to lock it. You will swap the rest to see your final hand.\n\n"
        "Press start turn to flip your cards over, and end turn when you're done. "
        "After everyone has played, the best hand will be revealed with the winner's name.")

    def start(self):
        self.__main_window.mainloop()

    def quit(self):
        self.__main_window.destroy()


class Card:
    """
    Each card in itself is an object, so they always remember all their current states, and are easier to track
    """

    def __init__(self, suit, value, rank):
        self.__locked = False
        self.__suit = suit
        self.__value = value
        self.__my_position = 0
        self.__rank = rank
        self.__name = "{}{}".format(self.__suit, self.__value)
        self.__face = "PNG/{}{}_giftest.gif".format(self.__value, self.__suit)

    def __str__(self):
        return "{}{}".format(self.__suit, self.__value)

    def my_color(self):
        if self.__suit == "S" or self.__suit == "C":
            return "black"
        else:
            return "red"

    def my_pos_set(self, position):
        self.__my_position = position

    def my_pos(self):
        return self.__my_position

    def my_suit(self):
        return self.__suit

    def my_value(self):
        return self.__value

    def my_rank(self):
        return self.__rank

    def my_face(self):
        return self.__face

    def lock_state(self):
        if self.__locked:
            self.__locked = False
        else:
            self.__locked = True
        return


def legend():
    messagebox.showinfo("Hands' strengths in order and what do they mean",
                        "Straight Flush, all cards are of the same suit, and their values are next to each other\n"
                        "\nFour of a kind, four cards of the same value\n\n"
                        "Full House, three cards of the same value, and two cards of the same value\n\n"
                        "Flush, all cards are of the same suit\n\n"
                        "Straight, all cards' values are next to each other\n\n"
                        "Three of a Kind, three cards are of the same value\n\n"
                        "Two Pairs, two sets of cards wield the same value\n\n"
                        "Pair, two cards are of the same value\n\n"
                        "High, if all else fails, your highest card is your value, Aces high\n\n")


def decker():
    """
    Creates a new deck and returns it. Also returns the values of each card in the deck
    """
    pack = {}
    rank = 0
    suits = ["S", "H", "D", "C"]
    for value in range(2, 15):
        for suit in suits:
            pack["{}{}".format(suit, value)] = Card(suit, value, rank)
            rank = rank + 1

    card_ranks = list(pack)

    return pack, card_ranks


def pick_a_card(deck, card_ranks):
    """
    Picks a single random card from the deck (while also removing it from the deck) and returns it
    :param deck:
    :param card_ranks:
    :return: a single card object
    """
    the_card = random.choice(card_ranks)
    while the_card not in deck:
        the_card = random.choice(card_ranks)
    pick = deck[the_card]
    del deck[the_card]
    return pick


def player_hand(pack, card_ranks):
    """
    Picks 5 random cards into a hand and returns it
    :param pack:
    :param card_ranks:
    :return: Player's hand
    """
    hand = []
    for i in range(5):
        selection = pick_a_card(pack, card_ranks)
        selection.my_pos_set(i)
        hand.append(selection)
    return hand


def main():
    """
    Starts up by creating a ranking system for the cards, a new deck, and the setup window.
    After that it creates all starting hands of the players, and then returns it, with the rest of the deck to the main
    game.
    :return: 0
    """
    deck, card_ranks = decker()
    game = StartWindow()
    try:
        player_count, player_names = game.start()
    except TypeError:
        return 0
    player_hands = []
    for i in range(player_count):
        player_hands.append(player_hand(deck, card_ranks))
    poker_time = PokerGame(player_count, player_names, player_hands, card_ranks, deck, False)
    poker_time.start()


main()
