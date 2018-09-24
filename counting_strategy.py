import matplotlib.pyplot as plt
import math
import random


global results 
global total_deck 
global true_count
global tot_hands


def new_deck():
	global running_count

	del total_deck[:]
	one_suit= [2,3,4,5,6,7,8,9,10,"J","Q","K","A"]
	q=0
	while q < 24:
		for i in one_suit:
			total_deck.append(i)
		q +=1
	random.shuffle(total_deck)

	running_count = 0

def get_run_count(card0):
	global true_count
	global running_count

	if score(card0) < 7:
		running_count +=1
	elif score(card0) < 10:
		running_count += 0
	else:
		running_count -= 1
	true_count = running_count/int(len(total_deck)/52)

def  init_hit (hand):
	card= [total_deck.pop(0)]
	get_run_count(card)
	hand.append(card[0])


def no_record_hit(hand):
	card= [total_deck.pop(0)]
	hand.append(card[0])

def wager():
	if prehand_count >= 8:
		val = 5
	elif prehand_count >= 6:
		val = 4
	elif prehand_count >= 4:
		val = 3
	elif prehand_count >= 2:
		val = 2
	else:
		val = 1
	return val

def game():
    global s
    global k
    global player2
    global strategy
    global bust
    global prehand_count
    global tot_hands
    global double

    double = 1
    k  = False				# Stay counter
    s = False				# Split  counter
    bust  =  False			# Bust  counter
    firstbust = False 		# First hand has been busted
    secondbust = False      	# Second hand has been busted

    player=[]
    player2=[]
    dealer=[]
    strategy=[]
    init_hit(player) 		#  hits players 1st card
    init_hit(player) 		#  hits players 2nd card
    init_hit(dealer) 		#  hits computers 1st card
    no_record_hit(dealer)
    prehand_count = true_count
    while k == False and bust == False:
        counting_strategy(player,dealer)
        if  k  == False and bust == False:
        	run1 = [score(player[:-1]),score([dealer[0]]),0,strategy[-1]]
        	results.append(run1)
    if k ==  False and bust ==  True:
    	run1 =  [score(player[:-1]),score([dealer[0]]),-1*double*wager(),strategy[-1]]
    	results.append(run1)
    	firstbust  = True
    k  = False
    bust = False
    tot_hands +=  1
    if s  == True:
    	tot_hands += 1
    while s == True and k ==  False and bust == False:
    	counting_strategy(player2,dealer)
    	if k == False and bust == False:
    		run1 =  [score(player2[:-1]),score([dealer[0]]),0,strategy[-1]]
    		results.append(run1)

    if s == True and k == False and  bust == True:
    	run1 = [score(player2 [:-1]),score ([dealer [0]]),-1*double*wager(),strategy [-1]]
    	results.append(run1)
    	secondbust =  True	
    run_dealer(dealer)

    if firstbust == False:
    	points = score_check (player,dealer)
    	run1  =  [score(player[:-1]),score([dealer[0]]),points*double*wager(),strategy[-1]]
    	results.append(run1)
    if  secondbust  == False  and s== True:
    	points2  =  score_check(player2,dealer)
    	run2  =  [score(player2[:-1]),score([dealer[0]]),points2*double*wager(),strategy[-1]]
    	results.append(run2)

def hit(hand):
	strategy.append('Hit')
	init_hit(hand)

def score(hand):
	global bust 
	global hardtotal
	total = 0 
	hardtotal = True 
	a=0
	for cards in hand:
		if cards == "J" or cards == "Q" or cards == "K":
			total+= 10
		elif cards== "A":
			total+= 11
			a+= 1
			hardtotal = False
		else:
			total += cards

	while a>0 and total > 21:
		total -= 10
		a  -= 1
	if a == 0:
		hardtotal = True
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
	k  = True

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

def  counting_strategy(p1,d1):
	global double
	score(p1)
	if score(p1) == 16 and score([d1[0]]) == 10:
		if true_count > 0:
			if split_strategy(p1,d1) == 1:
				split(p1)
			else:
				stay(p1)
		else:
			hit(p1)
	elif score(p1) == 15 and score([d1[0]]) == 10:
		if true_count >= 4:
			if split_strategy(p1,d1) == 1:
				split(p1)
			else:
				stay(p1)
		else:
			hit(p1)
	elif p1[0]==p1[1] and score([p1[0]]) == 10 and score([p1[1]]) == 10 and score([d1[0]]) == 5:
		if true_count >= 5:
			split(p1)
		else:
			stay(p1)
	elif p1[0] == p1[1] and score([p1[0]]) == 10 and score([p1[1]]) == 10 and score([d1[0]]) == 6:
		if true_count >= 4:
			split(p1)
		else:
			stay(p1)
	elif score(p1) == 10 and score([d1[0]]) == 10:
		if true_count >= 4:
			double *=2
			hit(p1)
			stay(p1)
		else:
			hit(p1)
	elif score(p1) == 12 and score([d1[0]]) == 3:
		if true_count >=2:
			if split_strategy(p1,d1) == 1:
				split(p1)
			else:
				stay(p1)
		else:
			hit(p1)
	elif score(p1) == 12 and score([d1[0]]) ==2:
		if true_count >= 3:
			if split_strategy(p1,d1) == 1:
				split(p1)
			else:
				stay(p1)
		else:
			hit(p1)
	elif score(p1) ==11 and score([d1[0]]) == 11:
		if true_count >= 1:
			double *=2
			hit(p1)
			stay(p1)
		else:
			hit(p1)
	elif score(p1) == 9 and score([d1[0]]) == 2:
		if true_count >= 1:
			double *=2
			hit(p1)
			stay(p1)
		else:
			hit(p1)
	elif score(p1) == 10 and score([d1[0]]) == 11:
		if true_count >= 4:
			double *= 2
			hit(p1)
			stay(p1)
		else:
			hit(p1)
	elif score(p1) == 9 and score([d1[0]]) == 7:
		if true_count >= 3:
			double *= 2
			hit(p1)
			stay(p1)
		else:
			hit(p1)
	elif score(p1) == 16 and score([d1[0]]) == 9:
		if true_count >= 5:
			if split_strategy(p1,d1) == 1:
				split(p1)
			else:
				stay(p1)
		else:
			hit(p1)
	elif score(p1) == 13 and score([d1[0]]) == 2:
		if true_count >= -1:
			if split_strategy(p1,d1) == 1:
				split(p1)
			else:
				stay(p1)
		else:
			hit(p1)
	elif score(p1) == 12 and score([d1[0]]) == 4:
		if true_count >= 0:
			if split_strategy(p1,d1) == 1:
				split(p1)
			else:
				stay(p1)
		else:
			hit(p1)
	elif score(p1) == 12 and score([d1[0]]) == 5:
		if true_count >= -1:
			if split_strategy(p1,d1) == 1:
				split(p1)
			else:
				stay(p1)
		else:
			hit(p1)
	elif score(p1) == 12 and score([d1[0]]) == 6:
		if true_count >= -1:
			if split_strategy(p1,d1) == 1:
				split(p1)
			else:
				stay(p1)
		else:
			hit(p1)
	elif score(p1) == 13 and score([d1[0]]) == 3:
		if true_count >= -2:
			if split_strategy(p1,d1) == 1:
				split(p1)
			else:
				stay(p1)
		else:
			hit(p1)
	elif split_strategy(p1,d1) == 1:
		split(p1)
	elif hardtotal == False:
		if score(p1) == 13 and score([d1[0]]) > 4 and score([d1[0]]) < 7:
			double *= 2
			hit(p1)
			stay(p1)
		elif score(p1) == 14 and score([d1[0]]) > 4 and score([d1[0]]) < 7:
			double *= 2
			hit(p1)
			stay(p1)
		elif score(p1) == 15 and score([d1[0]]) > 3 and score([d1[0]]) < 7:
			double *= 2
			hit(p1)
			stay(p1)
		elif score(p1) == 16 and score([d1[0]]) > 3 and score([d1[0]]) < 7:
			double *= 2
			hit(p1)
			stay(p1)
		elif score(p1) == 17 and score([d1[0]]) > 2 and score([d1[0]]) < 7:
			double *= 2
			hit(p1)
			stay(p1)
		elif score(p1) == 18 and score([d1[0]]) > 2 and score([d1[0]]) < 7:
			double *= 2
			hit(p1)
			stay(p1)
		elif score(p1) < 18:
			hit(p1)
		elif score(p1) == 18 and score([d1[0]]) > 8:
			hit(p1)
		else:
			stay(p1)
	elif hardtotal == True:
		if score(p1) == 9 and score([d1[0]]) > 2 and score([d1[0]]) < 7:
			double *=2
			hit(p1)
			stay(p1)
		elif score(p1) == 10 and score([d1[0]]) < 10:
			double *=2
			hit(p1)
			stay(p1)
		elif score(p1) == 11 and score([d1[0]]) < 11:
			double *=2
			hit(p1)
			stay(p1)
		elif score(p1) < 12:
			hit(p1)
		elif score(p1) < 17 and score([d1[0]]) > 6:
			hit(p1)
		elif score(p1) == 12 and score([d1[0]]) < 4:
			hit(p1)
		else:
			stay(p1)

def run_dealer(comp):
	while score(comp) < 17:
		init_hit(comp)

def score_check(hand,comp):
	if score(hand) > 21:
		return -1
	elif score(hand) == 21 and len(hand) == 2:
		if score(hand) == score(comp) and len(comp) == 2:
			return 1
		else:
			return 1.5
	elif score(hand) > score(comp):
		return 1
	elif score(comp) >  21:
		return 1
	elif score(hand) == score(comp):
		return 0
	else:
		return -1
if __name__ == '__main__':
	sim =  0 
	totals=[]
	win_or_lose= []
	win_probability= []
	number_of_hands= []
	n =  int(input("How many simulations?:  "))
	while sim < 1000: 
		tot_hands = 0
		results = [] 
		total_deck = []
		true_count = 0
		running_count = 0
		i = 0
		wins =  0
		wins1 =  0
		losses = 0
		losses1 = 0
		ties =  0
		while i <  n:
			if len(total_deck)<75: 
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
		gain = round(100*float((net_gain))/float ((tot_hands)),1)
		probability = wins1/float(len(results))
		win_probability.append(probability)
		win_or_lose.append(net_gain1)
		number_of_hands.append(tot_hands) 
		totals.append(gain)
		sim += 1

	mean = sum(totals)/len(totals)
	Standard_Deviation = sum([math.sqrt((i-mean)*(i-mean)) for i in totals])/len(totals)
	line0 =str([("total gain ",sum(totals))])
	line1 = str(["mean ",mean,"%"])
	line2 = str(["Standard Deviation ",Standard_Deviation,"%"])
	line3 =  str(["win probability ",sum(win_probability)/float(len(win_probability))])
	line4 =  str(["win_or_lose ",sum(win_or_lose)/float(len(win_or_lose))])
	line5 = str(["number of hands ",sum(number_of_hands)])
	fo = open("counting_strategy.txt", "a")
	fo.write(line0+"\n")
	fo.write(line1+"\n")
	fo.write(line2+"\n")
	fo.write(line3+"\n")
	fo.write(line4+"\n")
	fo.write(line5+"\n")
	fo.write("\n")
	fo.close()
	print ("total gain ",sum(totals))
	print ("mean ",mean,"%")
	print ("Standard Deviation ",Standard_Deviation,"%")
	print ("win probability ",sum(win_probability)/float(len(win_probability)))
	print ("win_or_lose ",sum(win_or_lose)/float(len(win_or_lose)))
	print ("number of hands ",sum(number_of_hands))
	range = (-7,7)
	bins = 100
	plt.hist(totals,bins,range,color = 'blue',histtype ='bar',rwidth = .5)
	plt.xlabel('Gain(%)')
	plt.ylabel('Frequency')
	plt.title('Counting_strategy')
	plt.show()
