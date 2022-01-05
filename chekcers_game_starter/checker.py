'''
Peter Tsanev
This checker.py file is responsible for defining and setting up each
checker piece. Only self.is_king in constructor can be tested. All
else is Turtle related.
'''
from constants import RADIUS, PIECE_ADJUSTMENTS


class Checker():
    '''
        Class -- Checkers
            The checkers of the game.
        Attributes:
            is_king -- Determines if the current piece is a king.
            pen -- Turtle pen used to draw checkers.
            RADIUS -- The radius of each checker.
        Methods:
            (none intended to be accessed outside the class)
    '''

    def __init__(self, pen, is_king, radius):
        '''
            Constructor -- Creates a new instance of Checker.
            Parameters:
                self -- The current Checker object.
                pen -- Turtle pen used to draw checkers.
                is_king -- Assigns True if piece piece is a king,
                False otherwise.
        '''
        self.is_king = is_king
        self.pen = pen

        # Defines and adjusts size of piece radius to fit squares
        self.RADIUS = radius
        self.draw_circle()
        if self.is_king:
            x, y = self.pen.pos()
            self.pen.color("WHITE")
            self.pen.setposition(x, y + self.RADIUS/2)
            self.draw_king()

    def draw_circle(self):
        '''
            Function -- draw_circle
                Draw a circle with a given radius.
            Parameters:
                self -- The current Checker object.
                size -- the radius of the circle
            Returns:
                Nothing. Draws a circle in the graphics window.
        '''
        self.pen.pensize(0)
        self.pen.begin_fill()
        self.pen.pendown()
        self.pen.circle(self.RADIUS)
        self.pen.penup()
        self.pen.end_fill()

    def draw_king(self):
        '''
            Method -- draw_king
                Draws a white circle on a piece signifying it is a
                king.
            Parameters:
                self -- The current Checker object.
            Returns:
                Nothing. Draws king piece.
        '''
        self.pen.pensize(1)
        self.pen.pendown()
        self.pen.circle(self.RADIUS/2)
        self.pen.penup()
        self.pen.pensize(0)
