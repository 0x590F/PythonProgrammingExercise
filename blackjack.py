import random

# 定义全局变量
suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
decks = 6  # 牌堆数量

# 定义类
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + self.suit

class Deck:
    def __init__(self):
        self.cards = []
        self.create()

    def create(self):
        for _ in range(decks):
            for suit in suits:
                for rank in ranks:
                    self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'A':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:
    def __init__(self):
        self.total = 1000
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def stand(deck, hand):
    global playing
    playing = False

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("请输入下注金额："))
        except ValueError:
            print("请输入有效的数字！")
        else:
            if chips.bet > chips.total:
                print("下注金额不能超过您的现有金额！")
            else:
                break

def hit(deck, hand):
    card = deck.deal_card()
    hand.add_card(card)
    hand.adjust_for_ace()

def hit_or_stand(deck, hand, playing):
    choice = input("是否要牌？（输入'Y'继续要牌，输入'N'停牌）：")
    if choice.lower() == 'y':
        hit(deck, hand)
        if hand.value > 21:
            playing = False
    elif choice.lower() == 'n':
        playing = False
    else:
        print("请输入有效的选择！")
    return playing

def show_some(player, dealer):
    print("\n庄家的手牌：")
    print("<隐藏牌>")
    print(dealer.cards[0])  # 显示庄家的第一张牌
    print("\n您的手牌：")
    for card in player.cards:
        print(card)

def show_all(player, dealer):
    print("\n庄家的手牌：")
    for card in dealer.cards:
        print(card)
    print("\n您的手牌：")
    for card in player.cards:
        print(card)

def player_busts(chips):
    print("您的点数超过了21点，您输了！")
    chips.lose_bet()

def player_wins(chips):
    print("恭喜！您获得了二十一点，您赢了！")
    chips.win_bet()

def dealer_busts(chips):
    print("庄家的点数超过了21点，您赢了！")
    chips.win_bet()

def dealer_wins(chips):
    print("庄家的点数更高，您输了！")
    chips.lose_bet()

def push():
    print("平局")

def double_down(deck, chips, player_hand):
    if chips.bet <= chips.total:
        chips.bet += chips.bet
        hit(deck, player_hand)
        if player_hand.value <= 21:
            stand(deck, player_hand)
    else:
        print("您的下注金额超过了您的现有金额！无法使用双倍下注。")

def split(deck, player_hand, hands):
    if len(player_hand.cards) == 2 and player_hand.cards[0].rank == player_hand.cards[1].rank:
        hand1 = Hand()
        hand2 = Hand()
        hand1.add_card(player_hand.cards[0])
        hand2.add_card(player_hand.cards[1])
        hands.append(hand1)
        hands.append(hand2)
        hit(deck, hand1)
        hit(deck, hand2)
        player_hand.cards.remove(player_hand.cards[1])
    else:
        print("无法分牌！")

def count_cards(cards):
    count = 0
    for card in cards:
        if card.rank in ['2', '3', '4', '5', '6']:
            count += 1
        elif card.rank in ['10', 'J', 'Q', 'K', 'A']:
            count -= 1
    return count

def play_game():
    while True:
        print("\n欢迎来到二十一点游戏！")
        deck = Deck()
        deck.shuffle()
        player_chips = Chips()

        while True:
            player_hand = Hand()
            dealer_hand = Hand()
            hands = [player_hand]
            take_bet(player_chips)

            for _ in range(2):
                for hand in hands:
                    hand.add_card(deck.deal_card())



            # 将庄家的第一张牌设置为隐藏状态
            dealer_hand.add_card(deck.deal_card())
            dealer_hand.cards[0].hidden = True

            show_some(player_hand, dealer_hand)  # 显示一开始的手牌

            playing = True
            while playing:
                playing = hit_or_stand(deck, player_hand, playing)
                show_some(player_hand, dealer_hand)

                if player_hand.value > 21:
                    player_busts(player_chips)
                    break

            if player_hand.value <= 21:
                while dealer_hand.value < 17:
                    hit(deck, dealer_hand)

                # 将庄家的第一张牌设置为非隐藏状态
                dealer_hand.cards[0].hidden = False

                show_all(player_hand, dealer_hand)

                if dealer_hand.value > 21:
                    dealer_busts(player_chips)
                elif dealer_hand.value > player_hand.value:
                    dealer_wins(player_chips)
                elif dealer_hand.value < player_hand.value:
                    player_wins(player_chips)
                else:
                    push()

            print(f"\n您的现有金额为：{player_chips.total}")

            if player_chips.total <= 0:
                print("您的金额已经用完，游戏结束！")
                break

            play_again = input("是否继续游戏？（输入'Y'继续，输入'N'退出）：")
            if play_again.lower() == 'n':
                print("感谢您的参与，游戏结束！")
                break

play_game()