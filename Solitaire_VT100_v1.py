#!/bin/python

# Klondike Solitaire game written in Python by Jeff Artz (jeff.artz@gmail.com)
#
# This is my first Python program - it is a Text-mode version of a Solitaire game 
# that is based on a Tandem TACL version I wrote in about 1994
#
# A GUI version is on the way... ;-) 

import random

# Define the variables used in this program

# Used to provide 'full name' lookup of single-character abbreviations
dsuit = {}
dsuit['D']='Diamond'
dsuit['d']='Diamond'
dsuit['H']='Heart'
dsuit['h']='Heart'
dsuit['S']='Spade'
dsuit['C']='Club'

dface = {}
dface['A']='Ace'
dface['1']='One'
dface['2']='Two'
dface['3']='Three'
dface['4']='Four'
dface['5']='Five'
dface['6']='Six'
dface['7']='Seven'
dface['8']='Eight'
dface['9']='Nine'
dface['T']='Ten'
dface['J']='Jack'
dface['Q']='Queen'
dface['K']='King'

# Define the multi-dimentional arrays for the Table Columns and Home Piles:
col =[[[] for i in range(21)] for i in range(7)]
home=[[[] for i in range(13)] for i in range(4)]

# Define a non-shuffled deck of cards:
fulldeck = ['AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS',\
            'Ad', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd',\
            'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC',\
            'Ah', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh']

# Create the 'deck' array, a copy of fulldeck            
deck=fulldeck[:]

# Create the Waste Pile array:
wastepile=[]

# Initialize the 'hidden cards' count in each column
for colnum in xrange(0,7):
  col[colnum][0]=0

# Initialize the card selection variables
selcol=-1
selcard=-1
             
# Output a Banner            
print ' '
print ' Jeff\'s Python Solitaire Game v1 (Text based) '
print ' '

# Check if a value is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
# shuffle function  (Shuffle the deck of cards 3 times)
def shuffle():   
  global deck
  deck=fulldeck[:]
  random.shuffle(deck)
  random.shuffle(deck)
  random.shuffle(deck)

# Function to clear all the lists and arrays  
def clear_lists():
  global col,wastepile,home
  home[0][:]=[]
  home[1][:]=[]
  home[2][:]=[]
  home[3][:]=[]
  col[0][:]=[]
  col[1][:]=[]
  col[2][:]=[]
  col[3][:]=[]
  col[4][:]=[]
  col[5][:]=[]
  col[6][:]=[]
  for colnum in xrange(0,7):
    col[colnum].append(0)
  wastepile[:]=[]
  selcol=-1
  selcard=-1
  
# function to start a new game:
def newgame():
  global deck,col
  clear_lists()
  shuffle()
  # Deal the cards to the columns
  for cardnum in xrange(0,7):
    for tcolumn in xrange(cardnum,7):
      col[tcolumn][0]=tcolumn
      col[tcolumn].append(deck.pop(0))
 
# Function to determine what Color to print the card 
def colorcard(cardface,dim):
  if cardface[1]=='d' or cardface[1]=='h':
    # Diamond or Heart  # Red on White
    hlcol='\033[0;37;41m' # White on Red
  else:
    # Club or Spade
    #hlcol='\033[30;2;47m' # Black on White
    hlcol='\x1b[0;30;47m' # White on Black
  return hlcol + cardface + '\033[37;44m'
  
# Function to print out the Solitaire board on the terminal in ASCII text with ANSI highlights  
def printboard(debugflag):
  print '\033[37;44m'
  print '           d     w          h0    h1    h2    h3'
  print '         ',
  
  # If the Deck pile has cards in it, show the back of a card 
  if len(deck)>0:
    #print '\033[2;42;30m##\033[37;44m   ',  # '##' Number Signs 
    print '\033[2;42;30m' + '\032\032' + '\033[37;44m   ', # Graphical Hash pattern
  else:
    print '     ',
    
  #if the Waste Pile has at least one card in it, print it, otherwise print dashes
  if len(wastepile)>0:
    print colorcard(wastepile[0],0),
  else:
    print '--',
  print '        ',

  # Print the 4 'home' piles, or dashes if empty
  for hpile in xrange(0,4):
    if len(home[hpile])>0:
      print colorcard(home[hpile][0],0),
    else:
      print '--',
    print '  ',
  print ''

  # Now print the 2nd card in the Waste Pile (if any) on the 2nd line
  print '              ',
  if len(wastepile)>1:
    print colorcard(wastepile[1],1)
  else:
    print '--'
    
  # Now print the 3rd card in the Waste Pile (if any) on the 3rd line
  print '             ',
  if len(wastepile)>2:
    print colorcard(wastepile[2],1)
  else:
    print '--'

  # Print the column header (sequence of numbers for now for movements)  
  if debugflag:
    # if Debug mode, print the counts for each column instead... 
    print '        ',
    for tcolumn in xrange (0,7):
      print ' ',
      print str(col[tcolumn][0]),
      print ' ',
      print ''
  else:
    print ''
    print '           0     1     2     3     4     5     6'
  
  # Print the Card Table
  for cardnum in xrange(1,20):
    print '        ',
    for tcolumn in xrange(0,7):
      # No card 
      if cardnum>=len(col[tcolumn]):
	if debugflag:
          print ' --  ',
        else:
          print '     ',
      else: 
        if col[tcolumn][0]>cardnum-1:
  	  # Face-down card
  	  if debugflag:
            print '[' + col[tcolumn][cardnum] + '] ',
	  else:
            #print ' \033[2;42;30m##\033[37;44m  ',
            print ' \033[2;42;30m' + '\032\032' + '\033[37;44m  ',
        else:
          if selcol==tcolumn and selcard==cardnum:
            # Selected Card
            print '\033[33m>\033[0m'+ colorcard(col[tcolumn][cardnum],0) + '  ',
          else:
  	    # Non-Selected Card
  	    print ' ' + colorcard(col[tcolumn][cardnum],0) + '  ',
    print ''

# Debugging function to Dump all the cards
def dump_cards():
  global col
  for colnum in xrange(0,7):
    print 'Column ' + str(colnum)
    for tcolumn in xrange(0,19):
      if col[colnum][tcolumn]!='00':
        print '   Card: ' + str(tcolumn) + ' ',
        print col[colnum][tcolumn]
    
# Debugging function to Dump all the card arrays    
def debugdump():
  print ' '
  print 'Deck:',
  print len(deck),
  print deck
  print 'Pile:',
  print len(wastepile),
  print wastepile
  print 'Columns:'
  print len(col[0]),
  print col[0]
  print len(col[1]),
  print col[1]
  print len(col[2]),
  print col[2]
  print len(col[3]),
  print col[3]
  print len(col[4]),
  print col[4]
  print len(col[5]),
  print col[5]
  print len(col[6]),
  print col[6]
  print 'Home Piles:'
  print len(home[0]),
  print home[0]
  print len(home[1]),
  print home[1]
  print len(home[2]),
  print home[2]
  print len(home[3]),
  print home[3]
  print ''

# function to check if a move is valid.  Used for all checks except to HOME piles.
def checkmove(fromcard,tocard):
  # String used for Color Order 
  colorder='KQJT98765432A'
  # Create the Suit Check dictionary  
  suitcheck = {'dS':1,'hS':1,'dC':1,'hC':1,'Sd':1,'Sh':1,'Cd':1,'Ch':1} 
  scvar=fromcard[1] + tocard[1]
  fsuit=fromcard[1]
  tsuit=tocard[1]
  
  if suitcheck.get(scvar,0):
    legalsuit=1
  else:
    legalsuit=0

  if legalsuit==0:
    print 'Invalid move!  You cannot place a ' + dsuit[fsuit] + ' on a ' + dsuit[tsuit] + '!'
    return 0
  else:
    fvar=tocard[0]+fromcard[0]
    print 'fvar=' + fvar
    print colorder
    #if fvar in colorder:
    if tocard[0]+fromcard[0] in colorder:
      #print 'valid move!  You can put a '+ dface[fromcard[0]] + ' on a ' + dface[tocard[0]] + '  ;-) ' 
      return 1
    else:
      print 'Invalid move!  You cannot place a ' + dface[fromcard[0]] + ' on a ' + dface[tocard[0]] + '!' 
      return 0

# function to check if a move to a HOME pile is valid.  
def checkhome(fromcard,tocard):
  colorder='KQJT98765432A'
  
  if fromcard[1]!=tocard[1]:
    print 'Invalid move!  You cannot place a ' + dsuit[fromcard[1]] + ' on a ' + dsuit[tocard[1]] + '!'
    return 0
  elif fromcard[0]+tocard[0] in colorder:
    #print 'valid move!  You can put a '+ dface[fromcard[0]] + ' on a ' + dface[tocard[0]] + '  ;-) ' 
    return 1
  else:
    print 'Invalid move!  You cannot place a ' + dface[fromcard[0]] + ' on a ' + dface[tocard[0]] + '!' 
    return 0

# Draw 3 cards from the Deck to the Wastepile
def draw3():
  global deck,wastepile,selcol,selcard
  # If the draw deck is empty, flip the Wastepile back over to it... 
  if len(deck)==0:
    deck=wastepile[:]
    deck.reverse()
    wastepile[:]=[]
  else:
    if len(deck)>0:
      wastepile.insert(0,deck.pop(0))
    if len(deck)>0:
      wastepile.insert(0,deck.pop(0))
    if len(deck)>0:
      wastepile.insert(0,deck.pop(0))
  selcol=-1
  selcard=-1

# Setup by starting a new game
newgame()
  
# Get started with an Infinite loop:
while 1:
  global deck,col,wastepile,home,selcard,selcol
  #debugdump()

  # Draw the board
  printboard(0)
  
  # Get the user's input and shift it to upper case:
  choice = raw_input('Enter Action: ').upper()

  # Parse the input and act on it
  clen=len(choice)
  if clen==1:
    if choice[0]=='D':
       # Draw 3 cards from the Deck to the Wastepile
       draw3()
       
    if choice[0]=='Z':
       # Debugging function - dump the variables
       debugdump()

    if choice[0]=='S':
       # S)huffle - Start a new game.
       newgame()
       
    if choice[0]>='0' and choice[0]<='6': 
      # Selecting a column or next card in the same column
      n0=int(choice[0])
      # If this column is already selected, select the next card in the pile.
      if selcol<>n0:
        selcol=n0
        selcard=len(col[n0])-1
      else:
	if selcard>col[n0][0]+1:
  	   selcard-=1
  	else:
  	  selcard=len(col[n0])-1

  elif clen==0:
    # Nothing was entered... 
    print 'No entry, try again.'

  else:  # clen>1      
    # Command is more than 1 character long... 
  
    # If taking the top Waste Pile card... 
    if choice[0]=='W':
      if len(wastepile)>0:
        if choice[1]>='0' and choice[1]<='9' and clen==2:
	  n1=int(choice[1])
          if len(col[n1])==1:
	    if wastepile[0][0]!='K':
	      print "INVALID MOVE!  You can only move a King to an empty column!"
	    else:
	      col[n1].append(wastepile.pop(0))
              selcol=-1
              selcard=-1
	  else:
	    if checkmove(wastepile[0],col[n1][len(col[n1])-1]):
	      col[n1].append(wastepile.pop(0))
              selcol=-1
              selcard=-1
        else:
          if choice[1]=='H' and clen==3:
            # Moving to a HOME column... 
            if choice[2]>='0' and choice[2]<='3':
	      n2=int(choice[2])
	      if len(home[n2])>0:
                if checkhome(wastepile[0],home[n2][0]):
    	          selcol=-1
                  selcard=-1
    	          home[int(choice[2])].insert(0,wastepile.pop(0))
              else:
		if wastepile[0][0]!='A':
		  print "Illegal Move!  You can only start off a Home Stack with an Ace!"
		else:
     	         selcol=-1
                 selcard=-1
    	         home[int(choice[2])].insert(0,wastepile.pop(0))
            else:
              print 'Invalid Entry!!!  Mode requires 3 characters!  Ex: wh0'
          else:
            print 'Invalid Entry!!!  Mode requires 2 or 3 characters!  Ex: w3 or wh0'
      else:
        print 'Invalid Entry: Waste pile is EMPTY!'

    # If moving FROM a Home column:    
    if choice[0]=='H':
      # Make sure the command is 3 digits long - ie: h12 would move from Home 1 column to column 2
      if len(choice)==3:
        if choice[1]>='0' and choice[1]<='3':
	  n1=int(choice[1])
          if len(home[n1])>0:
            # If the HOME pile is NOT empty...
            if choice[2]>='0' and choice[2]<='9' and clen==3:
	      n2=int(choice[2])
              if len(col[n2])==1:
		# If the COLUMN is empty, we can only move a KING... 
                if home[n1][0]!='K':
	          print "INVALID MOVE!  You can only move a King to an empty column!"
	      else:
  	        if checkmove(home[n1][0],col[n2][len(col[n2])-1]):
  	          col[n2].append(home[n1].pop(0))
                  selcol=-1
                  selcard=-1
	  else:
	    print 'INVALID MOVE!  Home pile ' + str(n1) + ' is EMPTY!'
        else:
          print 'Invalid Entry!!!  Command requires 3 characters!  Ex: H01'
      else:
        print 'INVALID MOVE!  Home pile ' + str(n0) + ' is EMPTY!'

    # If moving a card or pile from a Table column:
    if choice[0]>='0' and choice[0]<='6': 
      n0=int(choice[0])
      #print 'Source column is ' + choice[0]
      if len(col[n0])-1==0:
	print 'INVALID MOVE!  Column ' + choice[0] + ' is empty!'
      elif len(choice)>1:
        # Moving from a COLumn to a Home Column 
        if choice[1]=='H' and clen==3:
          if choice[2]>='0' and choice[2]<='3': 
            #print 'Destination Home column is ' + choice[1:2]
            n2=int(choice[2])
            #debugdump()
            if len(home[n2])==0:
	      if col[n0][len(col[n0])-1][0]!='A':
	        print "INVALID MOVE!  You can only move an Ace to an empty Home column!"
	      else:
		# It's an ACE - move it to the empty Home Column...
                #print ' Moving card from column ' + str(n0) + ' to Home pile ' + str(n2) + ' ...' 
                home[n2].insert(0,col[n0][len(col[n0])-1])
                col[n0].remove(home[n2][0])
                if col[n0][0] == len(col[n0])-1:
                  if col[n0][0]> 0: 
                     col[n0][0]-=1
            else:
	      # Home column is not empty... check if it's a legal move, then move it...
              #print ' Moving card from column ' + str(n0) + ' to Home pile ' + str(n2) + ' ...' 
              if checkhome(col[n0][len(col[n0])-1],home[n2][0]):
                home[n2].insert(0,col[n0][len(col[n0])-1])
                col[n0].remove(home[n2][0])
                if col[n0][0] == len(col[n0])-1:
                  if col[n0][0]> 0: 
                     col[n0][0]-=1
          else:
            print 'Invalid Home Column entry!!!  Must be 0-3'
        else:
          if choice[1]>='0' and choice[1]<='6' and clen==2:  
            #print 'Destination column is ' + choice[1]
  	    n1=int(choice[1])
  	    if n0==selcol:
	      if len(col[n1])==1:
		if col[n0][selcard][0]!='K':
		  print "INVALID MOVE!  You can only move a King to an empty column!"
		else:
 	          for movecard in range(selcard,len(col[n0])):
	            col[n1].append(col[n0][selcard])
                    col[n0].remove(col[n1][len(col[n1])-1])
                    if col[n0][0] == len(col[n0])-1:
                      if col[n0][0]> 0:  
  	                 col[n0][0]-=1
                  selcol=-1
                  selcard=-1
	      else:
                if checkmove(col[n0][selcard],col[n1][len(col[n1])-1]):
		  #print 'moving Selected STACK...'
	          # More than one card selected...
	          for movecard in range(selcard,len(col[n0])):
	            col[n1].append(col[n0][selcard])
                    col[n0].remove(col[n1][len(col[n1])-1])
                    if col[n0][0] == len(col[n0])-1:
                      if col[n0][0]> 0:  
  	                 col[n0][0]-=1
                  selcol=-1
                  selcard=-1

            else:
	      if len(col[n1])==1:
		if col[n0][selcard][0]!='K':
		  print "INVALID MOVE!  You can only move a King to an empty column!"
	        #print 'moving Single card...'
	        else:
		  # Single Card
                  col[n1].append(col[n0][len(col[n0])-1])
	          col[n0].remove(col[n1][len(col[n1])-1])
                  if col[n0][0] == len(col[n0])-1:
                    if col[n0][0]> 0:
	              col[n0][0]-=1
                      selcol=-1
                      selcard=-1
      	      else:
                # Single Card
                if checkmove(col[n0][len(col[n0])-1],col[n1][len(col[n1])-1]):
		  #jla - test of checkmove
  	          col[n1].append(col[n0][len(col[n0])-1])
	          col[n0].remove(col[n1][len(col[n1])-1])
                  if col[n0][0] == len(col[n0])-1:
                    if col[n0][0]> 0:
	              col[n0][0]-=1
                      selcol=-1
                      selcard=-1
 
