import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from math import sqrt


# Class of 3D Point
class Point:
    id = 0
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.id = Point.id
        Point.id += 1

    # Set Point`s Class
    def set_class(self, clas):
        self.clas = clas

    def show_coordinates(self):
        return f'x = {self.x}; y = {self.y}; z = {self.z}'

    def __repr__(self):
        return f'x = {self.x}; y = {self.y}; z = {self.z}'

# Realize KNN algorithm
class Knn:
    classes = [] # our known classes
    points = [] # array of points
    colors = ['red', 'green', 'blue', 'yellow', 'pink', 'black', 'white', 'mint', 'orange', 'violet'] # colors for point of each class

    def __init__(self, k):
        self.k = k # set k neighbours to check

    # add new class to the class list
    def add_clas(self, clas):
        if clas - 1 in self.classes:
            print('class already exist')
        else:
            self.classes.append(clas - 1)

    def is_classes_empty(self):
        if not self.classes:
            return True
        else:
            return False

    def reset(self):
        self.classes = []
        self.points = []

    def show(self):
        print(f'clases = {self.classes} \npoints = {self.points}')

    def set_k(self, k):
        self.k = k

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

    def get_neighbours(self, new_point):

        # neighbours is a list of nearest neighbours
        # class_count is a dict of nearest classes and their amount
        distances, neighbours = [], []

        # calculate distace for each point
        for point in self.points:
            if point.id != new_point.id:
                distances.append((self.get_distance(new_point, point), point))

        distances.sort(key=lambda x: x[0])
        # if we have less than k points, we take all
        if len(distances) < self.k:
            for i in range(len(distances)):
                neighbours.append(distances[i][1])


            neighbours.sort(key = lambda x: x.clas)

        else:
            expander = self.k

            # if distance[k] == distances[k + 1] we need to take k+1 neighbours
            if len(distances) > self.k:
                if distances[self.k - 1] == distances[self.k]:
                    expander = self.k - 1
                    while expander < len(distances) and distances[expander] == distances[expander + 1]:
                        expander += 1

            distances.sort(key= lambda x: x[0])

            for i in range(expander):
                neighbours.append(distances[i][1])

            neighbours.sort(key= lambda x: x.clas)

        return neighbours

    # add point which class we don`t know
    def add_new_point(self, x, y, z):

        class_count = {}
        new_point = Point(x, y, z)
        neighbours = self.get_neighbours(new_point)

        # count how many neighbours of each class we have
        for i in neighbours:
            if i.clas not in class_count:
                class_count[i.clas] = 1
            else:
                class_count[i.clas] += 1

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
        for point in self.points:
            x.append(point.x)
            y.append(point.y)
            z.append(point.z)
            color.append(self.colors[point.clas - 1])

        fig.add_scatter3d(mode='markers', x=x, y=y, z=z, marker={'color': color})

        plot(fig, filename='form/templates/plot.html', auto_open=False)

    def plot_with_lines(self):
        x, y, z = [], [], []  # arrays of coordinates for Scatter3d

        fig = go.Figure()
        color = []
        for point in self.points:
            x.append(point.x)
            y.append(point.y)
            z.append(point.z)
            color.append(self.colors[point.clas - 1])

        fig.add_scatter3d(mode='markers', x=x, y=y, z=z, marker={'color': color, 'size':7})

        new_point = self.points[-1]

        x_lines = list()
        y_lines = list()
        z_lines = list()
        line_color = []
        neighbours = self.get_neighbours(new_point)
        for neib in neighbours:
            x_lines.append(neib.x)
            x_lines.append(new_point.x)
            y_lines.append(neib.y)
            y_lines.append(new_point.y)
            z_lines.append(neib.z)
            z_lines.append(new_point.z)
            line_color.append(self.colors[neib.clas - 1])

        fig.add_scatter3d(
            x=x_lines,
            y=y_lines,
            z=z_lines,
            mode='lines',
            name='lines',
            #line_color= line_color
        )

        # fig.show()
        # print(help(plot))
        #print(help(fig.add_scatter3d))
        layout = go.layout(autofill=True)
        fig.add_scatter3d(layout=layout)

        plot(fig, filename='form/templates/plot.html', auto_open=False)