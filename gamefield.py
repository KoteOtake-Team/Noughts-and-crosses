import pprint

class GameField:

	self.marks = ['O', 'X']
	self.player1 = []
	self.player2 = []
	
	def __init__(self):
		self.field = [
			['-','-','-'],
        	['-','-','-'],
        	['-','-','-'],
        ]

   	def __is_cell_empty(self, x, y):
   		if self.field[x][y] not in self.marks: return True
   		else: False

   	def __is_final(self, player):

   		
    
    def make_move(self, x, y, player):
    	if self.__is_cell_empty(x,y):
    		self.field[x][y] = self.marks[player]	
