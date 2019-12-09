import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from math import sqrt

# Class of 3D Point
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # Set Point`s Class
    def set_class(self, clas):
        self.clas = clas

# Realize KNN algorithm
class KNN:
    classes = [] # our known classes
    points = [] # array of points
    colors = ['red', 'green', 'blue', 'yellow', 'pink'] # colors for point of each class

    def __init__(self, k):
        self.k = k # set k neighbours to check

    # add new class to the class list
    def add_clas(self, clas):
        if clas - 1 in self.classes:
            print('class already exist')
        else:
            self.classes.append(clas - 1)

    def show(self):
        print(f'clases = {self.classes} \npoints = {self.points}')

    # Distance between 2 points
    def get_distance(self, Point1, Point2):
        return sqrt((Point2.x - Point1.x)**2 + (Point2.y - Point1.y)**2 + (Point2.z - Point1.z)**2)

    # add point which class we already know
    def add_known_point(self, x, y, z, clas):
        if clas - 1 in self.classes:
            p = Point(x, y, z)
            p.set_class(clas)
            self.points.append(p)
        else:
            self.classes.append(clas - 1)
            p = Point(x, y, z)
            p.set_class(clas)
            self.points.append(p)

    # add point which class we don`t know
    def add_new_point(self, x, y, z):
        new_point = Point(x, y, z)

        # class_list is a list of nearest neighbours
        # class_count is a dict of nearest classes and their amount
        distances, class_count, class_list = [], {}, []

        # calculate distace for each point
        for point in self.points:
            distances.append((self.get_distance(new_point, point), point.clas))

        # if we have less than k points, we take all
        if len(distances) < self.k:
            for i in range(len(distances)):
                class_list.append(distances[i][1])

            class_list.sort()

            # count how many neighbours of each class we have
            for i in class_list:
                if i not in class_count:
                    class_count[i] = 1
                else:
                    class_count[i] += 1
        else:
            expander = self.k

            # if distance[k] == distances[k + 1] we need to take k+1 neighbours
            if len(distances) > self.k:
                if distances[self.k - 1] == distances[self.k]:
                    expander = self.k - 1
                    while expander < len(distances) and distances[expander] == distances[expander + 1]:
                        expander += 1

            distances.sort()

            for i in range(expander):
                class_list.append(distances[i][1])

            class_list.sort()

            # count how many neighbours of each class we have
            for i in class_list:
                if i not in class_count:
                    class_count[i] = 1
                else:
                    class_count[i] += 1

        # find class with the most amount of neighbours
        maximum_value = -1
        new_point_clas = -1

        for i in class_count.items():
            if i[1] > maximum_value:
                maximum_value = i[1]
                new_point_clas = i[0]

        # set class for new point
        new_point.clas = new_point_clas
        # add point to the list of points
        self.points.append(new_point)


    def plot(self):
        x, y, z = [], [], [] # massives of coordinates for Scatter3d

        fig = go.Figure()
        color = []
        print(self.points)
        for point in self.points:
            x.append(point.x)
            y.append(point.y)
            z.append(point.z)
            color.append(self.colors[point.clas - 1])

        fig.add_scatter3d(mode='markers', x=x, y=y, z=z, marker={'color': color})

        plot(fig, filename='plot.html')