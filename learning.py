import matplotlib.pyplot as plt
import math
import random


global s
global k
global h
global player2
global strategy
global results 
global total_deck 
global hits_used
global total_used
global tot_hands

def new_deck():
	del total_deck[:]
	one_suit= [2,3,4,5,6,7,8,9,10,"J","Q","K","A"]
	q=0
	while q < 24:
		for i in one_suit:
			total_deck.append(i)
		q +=1
	random.shuffle(total_deck)

def  init_hit (hand):
	card= [total_deck.pop(0)]
	hand.append(card[0])

def game():
    global s
    global k
    global h
    global player2
    global strategy 
    global bust 
    global total_used
    global hits_used
    global tot_hands

    k  = False				# Stay counter
    s = False				# Split  counter
    h = False
    bust  =  False			# Bust  counter
    firstbust = False 		# First hand has been busted
    secondbust = False      	# Second hand has been busted
    points = 0
    player = []
    player2 = []
    dealer = []
    strategy = []

    init_hit(player) 		#  hits players 1st card
    init_hit(player) 		#  hits players 2nd card
    init_hit(dealer) 		#  hits computers 1st card
    init_hit(dealer)

    while k == False and bust == False:
    	pick_play(player,dealer)
    	bust_check(player)
    	if  k  == False and bust == False and h == True:
    		run1 = [score(player[:-1]),score([dealer[0]]),0,strategy[-1]]
    		results.append(run1)
    		change_matrices(player,dealer,1,1)
    		h = False

    if k ==  False and bust ==  True and h == True:
    	run1 =  [score(player[:-1]),score([dealer[0]]),-1,strategy[-1]]
    	results.append(run1)
    	change_matrices(player,dealer,1,0)
    	firstbust  = True
    h = False
    k = False
    bust = False
    tot_hands +=  1

    if s == 1:
    	tot_hands += 1
    while s == True and k ==  False and bust == False:
    	pick_play(player2,dealer)
    	bust_check(player2)
    	if s == True and k == False and bust == False and h == True:
    		run1 =  [score(player2[:-1]),score([dealer[0]]),0,strategy[-1]]
    		results.append(run1)
    		change_matrices(player2,dealer,1,1)
    		h = False

    if s == True and k == False and  bust == True and h == True:
    	run1 = [score(player2 [:-1]),score ([dealer [0]]),-1,strategy [-1]]
    	results.append(run1)
    	change_matrices(player2,dealer,1,0)
    	secondbust =  True	
    run_dealer(dealer)

    if firstbust == False:
    	points = score_check (player,dealer)
    	run1  =  [score(player[:-1]),score([dealer[0]]),points,strategy[-1]]
    	results.append(run1)
    	if points == 1:
    		change_stay_matrices(player,dealer,1,0)
    	elif points == -1:
    		change_stay_matrices(player,dealer,1,1)
    if  secondbust  == False  and s== True:
    	points2  =  score_check(player2,dealer)
    	run2  =  [score(player2[:-1]),score([dealer[0]]),points2,strategy[-1]]
    	results.append(run2)
    	if points2 == 1:
    		change_stay_matrices(player2,dealer,1,0)
    	elif points2 == -1:
    		change_stay_matrices(player2,dealer,1,1)

def hit(hand):
	global h
	strategy.append('Hit')
	h = True
	init_hit(hand)

def change_stay_matrices(play1, deal1, p1, p2):
	global total_used
	global hits_used
	row = score(play1)-4
	col = score([deal1[0]])-2

	total_used[row][col] += p1
	hits_used[row][col] += p2

def change_stay_matrices(play1, deal1, p1, p2):
	global total_used
	global hits_used
	row = score(play1)-4
	col = score([deal1[0]])-2

	total_used[row][col] += p1
	hits_used[row][col] += p2

def change_matrices(play1, deal1, p1, p2):
	global total_used
	global hits_used
	row = score(play1[:-1])-4
	col = score([deal1[0]])-2

	total_used[row][col] += p1
	hits_used[row][col] += p2

def score(hand):
	global bust

	total = 0
	a=0
	for cards in hand:
		if cards == "J" or cards == "Q" or cards == "K":
			total+= 10
		elif cards== "A":
			total+= 11
			a+= 1
		else:
			total += cards

	while a>0 and total > 21:
		total -= 10
		a  -= 1

	if total > 21: 
		bust =  True
	return total

def split(hand):
	global s
	strategy.append('Split')
	s = True
	hand.pop(1)
	player2.append(hand[0])
	hit(hand) 
	hit(player2)
def stay(hand):
	global k
	strategy.append('Stay')
	k = True
def bust_check(hand):
	global bust
	global k
	if score(hand) > 21:
		bust = True
		k = False

def  split_strategy(play1,hit1):
	if play1[0]==play1[1] and s ==False: 
		if play1[0]=="A":
			return 1
		elif play1[0]==8:
			return 1
		elif (play1[0]==2 or play1[0]==3 or play1[0]==7) and score([hit1[0]]) <  8:
			return 1
		elif play1[0]==6 and score([hit1[0]]) < 7:
			return 1
		elif play1[0]==9 and score([hit1[0]]) < 10 and score([hit1[0]]) != 7:
			return 1
		elif play1[0]==4 and score([hit1[0]]) < 7 and score([hit1[0]]) >  4:
			return 1
	else:
		return 0

def pick_play(p1,d1):
	global total_used
	global hits_used
	global bust

	if split_strategy(p1,d1) == 1:
		split(p1)

	tot = total_used[score(p1)-4] [score([d1[0]])-2]

	if score(p1) > 17:
		stay(p1)
	elif score(p1) < 12:
		hit(p1)
	else:
		if tot < 1:
			random.choice([stay(p1),hit(p1)])
		else:
			dnd = hits_used[score(p1)-4] [score([d1[0]])-2]
			r = float (dnd)/ float(tot)
			x = random.random()
			if x < r:
				hit(p1)
			else:
				stay(p1)

def run_dealer(comp):
	while score(comp) < 17:
		init_hit(comp)

def score_check(hand,comp):
	if score(hand) > 21:
		return -1
	elif score(hand) == 21:
		if score(hand) == score(comp):
			return 1
		else:
			return 1.5
	elif score(comp) > 21:
		return 1
	elif score(hand) >  score(comp):
		return 1
	elif score(hand) == score(comp):
		return 0
	else:
		return -1
if __name__ == '__main__':
	sim =  0 
	totals=[]
	n =  int(raw_input("How many simulations?:  "))
	while sim < 1:
		tot_hands = 0
		results = []
		total_deck = []
		hits_used = [[]]
		total_used = [[]]
		ratio_used = [[]]

		hits_used = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
		total_used = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
		ratio_used = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]

		i = 0
		wins =  0
		wins1 =  0
		losses = 0
		losses1 = 0
		ties =  0
		while i <  n:
			if len(total_deck)<5300: 
				new_deck()	
			game()
			i += 1

		m  =  0
		while m < len(results):
			if results[m][2] < 0:
				losses += (-1*results[m][2])
				losses1 += 1
			elif results[m][2] > 0:
				wins+= results[m][2]
				wins1 += 1
			else:
				ties += 1
			m  +=  1
		net_gain = wins-losses 
		net_gain1 = wins1-losses1

		z=0
		while z < 18:
			x = 0
			while x < 10:
				if float(total_used[z][x]) > 0:
					ratio_used[z][x] = round(float(hits_used[z][x])/float(total_used[z][x]),2)
				else:
					ratio_used[z][x] = 0
				x += 1
			z += 1

		gain = round(100*float((net_gain))/float ((tot_hands)),1) 
		totals.append(gain)
		sim += 1

	mean = sum(totals)/len(totals)
	Standard_Deviation = sum([math.sqrt((i-mean)*(i-mean)) for i in totals])/len(totals)
	print " mean gain ",sum(totals)/len(totals),"%"
	print "Net Gain: ", net_gain
	print "Standard Deviation",Standard_Deviation,"%"
	print totals
	for i in range(len(ratio_used)):
		print ratio_used[i]
	range = (-7,1)
	bins = 100
	plt.hist(totals,bins,range,color = 'blue',histtype ='bar',rwidth = .5)
	plt.xlabel('Gain(%)')
	plt.ylabel('Frequency')
	plt.title('Learning_strategy')
	plt.show()

