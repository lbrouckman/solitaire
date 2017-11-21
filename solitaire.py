from random import shuffle
import time
import os
# Each player will have a state that includes their
# Board: Array of arrays of cards [] [] [] [] [] [] []
# Deck: Array of cards that is in their draw pile
# Faceup: Index of card that is face up (and available to play)
# MadeMove: Boolean for whether they made a move in the last round through their hand

# Card:
# Suit, Value (number), Name (ace, king, 10...)

# Print card in readable way
import os
countBy = 3
def clear():
	os.system('clear')

def printCard(card, forcePrint=False):
	if not card['faceDown'] or forcePrint:
		print str(card['name']) + ' ' + card['suit'],
	else:
		print '(' + str(card['name']) + ' ' + card['suit'] + ')',

# Create deck of 52 cards
def createDeck():
	deck = []
	for i in range(52):
		if i < 13:
			suit = 'hearts'
			color = 'red'
		elif i < 26:
			suit = 'clubs'
			color = 'black'
		elif i < 39:
			suit = 'spades'
			color = 'black'
		else:
			suit = 'diamonds'
			color = 'red'
		value = i % 13 + 1
		name = value
		if value == 1:
			name = 'Ace'
		elif value == 11:
			name = 'Jack'
		elif value == 12:
			name = 'Queen'
		elif value == 13:
			name = 'King'
		deck.append({'value': value, 'name': name, 'suit': suit, 'color': color, 'faceDown': True})
	return deck

# Deal out a board (7 stacks, 1 card in the first, 2 in the second... 7 in the last)
def dealDeck(deck):
	board = [[] for i in range(7)]
	start = 0
	for i in range(0, 7):
		board[i] = deck[start: start + i + 1]
		board[i][-1]['faceDown'] = False
		start = start + i + 1
	return board

# Deal out n hands, set up the deck, board, faceup, and mademove for each player
def deal():
	hands = []
	for i in range(n):
		deck = createDeck()
		shuffle(deck)
		board = dealDeck(deck)
		myDeck = deck[28:]
		hands.append({'board': board, 'deck': myDeck, 'faceup': -1, 'madeMove': True})
	return hands

# If there is an ace available on the board, move it to the center
def aceFromBoard(hand, stacks):
	foundMove = False
	for i in range(7):
		pile = hand['board'][i]
		if len(pile) == 0:
			continue
		card = pile[len(pile) - 1]
		if card['value'] == 1:
			# add a new stack to the center
			foundMove = True
			stacks.append([card])
			hand['board'][i] = hand['board'][i][:-1]
			if len(hand['board'][i]) != 0:
				hand['board'][i][-1]['faceDown'] = False
			break
	return foundMove

# If the face up card is an Ace, move it to the center
def aceFromDeck(hand, stacks):
	foundMove = False
	if hand['faceup'] >= 0:
		i = hand['faceup']
		if hand['deck'][i]['value'] == 1:
			foundMove = True
			stacks.append([hand['deck'][i]])
			del hand['deck'][i]
			hand['faceup'] = i - 1
	return foundMove

# If there is a card that can be moved from the board to the center (non-Ace), move it
def cardFromBoard(hand, stacks):
	foundMove = False
	for i in range(len(stacks)):
		stack = stacks[i]
		if foundMove:
			break
		centerCard = stack[-1]
		for j in range(7):
			pile = hand['board'][j]
			if foundMove:
				break
			if len(pile) == 0:
				continue
			handCard = pile[-1]
			if handCard['value'] == centerCard['value'] + 1 and handCard['suit'] == centerCard['suit']:
				foundMove = True
				stacks[i].append(handCard)
				del hand['board'][j][-1]
				if len(hand['board'][j]) != 0:
					hand['board'][j][-1]['faceDown'] = False
	return foundMove

# If there is a card on top of the deck that can be moved to the center, move it
def cardFromDeck(hand, stacks):
	foundMove = False
	if hand['faceup'] >= 0:
		i = hand['faceup']
		card = hand['deck'][i]
		for j in range(len(stacks)):
			stack = stacks[j]
			if card['suit'] == stack[-1]['suit'] and card['value'] == stack[-1]['value'] + 1:
				foundMove = True
				stacks[j].append(card)
				del hand['deck'][i]
				hand['faceup'] = i - 1
				break
	return foundMove

# Find a move on the board (move a stack to another stack to uncover faceDown cards)
def moveOnBoard(hand, allowEmptyMoves=False):
	foundMove = False
	for i in range(7):
		if foundMove:
			break
		pile = hand['board'][i]
		# Find the lowest index of card with faceDown = False
		if len(pile) == 0:
			continue
		pos = len(pile) - 1
		while True:
			card = pile[pos]
			if card['faceDown'] == True:
				break
			else:
				cardToMove = card
				pos = pos - 1
				if pos < 0:
					break
		if pos == -1 and not allowEmptyMoves:
			continue
		for j in range(7):
			pileToCheck = hand['board'][j]
			if len(pileToCheck) == 0:
				continue
			if cardToMove['value'] + 1 == pileToCheck[-1]['value'] and cardToMove['color'] != pileToCheck[-1]['color']:
				hand['board'][j] += hand['board'][i][pos + 1:]
				hand['board'][i] = hand['board'][i][:pos + 1]
				if len(hand['board'][i]) > 0:
					hand['board'][i][-1]['faceDown'] = False
				foundMove = True
				break
	return foundMove

# See if there is a kind on  the board (with cards under it) that could be moved to empty space
def kingOnBoard(hand):
	foundMove = False
	for i in range(7):
		if foundMove:
			break
		pile = hand['board'][i]
		# Find the lowest index of card with faceDown = False
		if len(pile) == 0:
			continue
		pos = len(pile) - 1
		while True:
			card = pile[pos]
			if card['faceDown'] == True:
				break
			else:
				cardToMove = card
				pos = pos - 1
				if pos < 0:
					break
		if pos != -1 and cardToMove['value'] == 13:
			for j in range(7):
				pileToCheck = hand['board'][j]
				# found an empty pile for the king to go to
				if len(pileToCheck) == 0:
					hand['board'][j] += hand['board'][i][pos + 1:]
					hand['board'][i] = hand['board'][i][:pos + 1]
					if len(hand['board'][i]) > 0:
						hand['board'][i][-1]['faceDown'] = False
					foundMove = True
					break
	return foundMove

# Move a card from the deck out onto the board
def moveFromDeck(hand):
	foundMove = False
	pos = hand['faceup']
	if pos < 0 or len(hand['deck']) == 0:
		return False
	card = hand['deck'][pos]
	for i in range(7):
		pile = hand['board'][i]
		# move king to empty slot
		if card['value'] == 13 and len(pile) == 0:
			card['faceDown'] = False
			hand['board'][i].append(card)
			del hand['deck'][pos]
			hand['faceup'] = pos - 1
			foundMove = True
			break
		# See if the card can be moved out
		if len(pile) == 0:
			continue
		if card['value'] == pile[-1]['value'] - 1 and card['color'] != pile[-1]['color']:
			card['faceDown'] = False
			hand['board'][i].append(card)
			del hand['deck'][pos]
			hand['faceup'] = pos - 1
			foundMove = True
			break
	return foundMove

def flipHand(hand):
	pos = hand['faceup']
	if pos == len(hand['deck']) - 1:
		pos = -1
	elif pos + countBy >= len(hand['deck']):
		pos = len(hand['deck']) - 1
	else:
		pos = pos + countBy
	hand['faceup'] = pos

# Function to determine if there is a king available to play 
# Either in the deck or on the board
def existsKingToPlay(hand):
	if hand['faceup'] >= 0 and len(hand['deck']) > 0:
		if hand['deck'][hand['faceup']]['value'] == 13:
			return True
	for pile in hand['board']:
		for card in pile:
			if card['value'] == 13 and card['faceDown'] == False:
				return True
	return False

# Look for a move, first look if something can be moved to the center 
# then look for something that can be moved within the hand
def findMove(hand, stacks):
	# Look for any aces that could be put out
	foundMove = aceFromBoard(hand, stacks)
	if not foundMove:
		foundMove = aceFromDeck(hand, stacks)
	if not foundMove:
		foundMove = cardFromBoard(hand, stacks)
	if not foundMove:
		foundMove = cardFromDeck(hand, stacks)
	if not foundMove:
		foundMove = moveOnBoard(hand)
	if not foundMove and existsKingToPlay(hand):
		# IF there is a king on the board, make a move, allowing for empty moves
		foundMove = moveOnBoard(hand, True)
	if not foundMove:
		foundMove = kingOnBoard(hand)
	if not foundMove:
		foundMove = moveFromDeck(hand)
	if not foundMove:
		flipHand(hand)

	return foundMove

def printBoard(hand, stacks):
	for s in stacks:
		for card in s:
			printCard(card, True)
		print '\n'
	print 'BOARD IS '
	for h in hand['board']:
		for card in h:
			printCard(card)
		print '\n'
	print 'DECK:'
	if hand['faceup'] < 0:
		print 'X'
	else:
		c = hand['deck'][hand['faceup']]
		print str(c['name']) + ' ' + c['suit']
	print '(' + str(len(hand['deck'])) + ')'
	print '_____________________________________________________________________________'

def printDeck(hand):
	print 'Deck length: ' + str(len(hand['deck']))
	for i in range(len(hand['deck'])):
		if i == hand['faceup']:
			c = hand['deck'][i]
			print ' *' + str(c['name']) + ' ' + c['suit'] + '* ',
		else:
			print ' X ',

def wonGame(stacks):
	stackSum = 0
	for stack in stacks:
		stackSum += len(stack)
	if stackSum == 52 * n:
		return True
	return False
# Actually play the game. Each player takes a turn and does a single move
def playGame(hands):
	# For each player, if there is a move available do it, otherwise move faceup forwards 3
	stacks = [] # Stacks are arrays of cards that represent the center of the game 
	for _ in range(n * 300):
		for player in range(n):
			hand = hands[player]
			foundMove = findMove(hand, stacks)
		if wonGame(stacks):
			break
			# printBoard(hands[0], stacks)
	# for i in range(n):
	# 	printBoard(hands[i], stacks)
	return stacks

x = input('Up to how many players are there? ')
numGames = input('How many games are you playing? ')
for n in range(1, x + 1):
	wins = 0
	for _ in range(numGames):
		hands = deal()
		stacks = playGame(hands)
		if wonGame(stacks):
			wins += 1
	print 'With ' + str(n) +' players: Won ' + str(wins) + ' games out of ' + str(numGames)



