from __future__ import annotations

from typing import Tuple, List


class point2d:
    def __init__(self, x, y):
        self._x = float(x)
        self._y = float(y)
    
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False


class line2d:

    def __init__(self, point1, point2):
        '''
            Initialises a 2d line

            :param point1: first point of line in x,y format
            :param point2: second point of line in x,y format
        '''
        if isinstance(point1, point2d):
            self._point1 = point1
        else:
            self._point1 = point2d(*point1)
        if isinstance(point2, point2d):
            self._point2 = point2
        else:
            self._point2 = point2d(*point2)

    @property
    def point1(self):
        return self._point1

    @property
    def point2(self):
        return self._point2

    def has_intersection(self, other : line2d) -> bool:
        '''
            Determine if this line has an intersection with another line

            :params other: Other line2d object to compare with
        '''
        p1 = self._point1
        q1 = self._point2
        p2 = other._point1
        q2 = other._point2
             
        # Find the 4 orientations required for
        # the general and special cases
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)
    
        # General case
        if ((o1 != o2) and (o3 != o4)):
            return True
    
        # Special Cases
    
        # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        if ((o1 == 0) and on_segment(p1, p2, q1)):
            return True
    
        # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        if ((o2 == 0) and on_segment(p1, q2, q1)):
            return True
    
        # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        if ((o3 == 0) and on_segment(p2, p1, q2)):
            return True
    
        # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        if ((o4 == 0) and on_segment(p2, q1, q2)):
            return True
    
        # If none of the cases
        return False

class polygon2d:
    
    def __init__(self, *vertices):
        '''
            Initialise a 2D polygon

            :param *vertices: any number of vertices. Should be provided as pairs of x,y coordinates
        '''
        self._vertices = []
        if len(vertices) < 3:
            raise ValueError('Number of vertices is less than 3. This is not a polygon.')
        for vertex in vertices:
            if len(vertex) != 2:
                raise ValueError('Vertex did not contain 2 coordinates: ' + str(vertex))
            try:
                vert = (float(vertex[0]), float(vertex[1]))
                self._vertices.append(point2d(*vert))
            except:
                raise ValueError('Vertex could not be passed as float: ' + str(vertex))
        
        if self._vertices[0] != self._vertices[-1]:
            self._vertices.append(self._vertices[0]) #close the loop
        
        self._edges = []


    @property
    def plot_coords_xy(self):
        '''
            Return 2 lists of x & y coordinates suitable for plotting
        '''
        x = []
        y = []
        vert : point2d
        for vert in self._vertices:
            x.append(vert.x)
            y.append(vert.y)
        return x, y

    @property
    def edges(self) -> List[line2d]:
        '''
            Return a list of all edges on the polygon as a list of line2d
        '''
        if self._edges:
            return self._edges
        for i in range(len(self._vertices)):
            point1 = self._vertices[i]
            try:
                point2 = self._vertices[i+1]
            except IndexError:
                point2 = self._vertices[0]
            self._edges.append(line2d(point1, point2))   
        return self._edges

    def has_intersect(self, other : polygon2d):
        '''
            Check for intersection between 2 polygon2d objects

            :param other: other polygon2d to check for intersection with
        '''

        edge1 : line2d
        edge2 : line2d
        for edge1 in self.edges:
            for edge2 in other.edges:
                if edge1.has_intersection(edge2):
                    return True
        return False


def orientation(p : point2d, q : point2d, r : point2d) -> int:
    '''
        Find orientation of ordered triplet
        function returns the following values:
        0 : Collinear points
        1 : Clockwise points
        2 : Counterclockwise
        
        See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
        for details of below formula.
    '''
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):
         
        # Clockwise orientation
        return 1
    elif (val < 0):
         
        # Counterclockwise orientation
        return 2
    else:
         
        # Collinear orientation
        return 0

def on_segment(p:point2d, q:point2d, r:point2d) -> bool:
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False