import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from math import sqrt

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def set_class(self, clas):
        self.clas = clas


class KNN:

    classes = [] # our known classes
    points = [] # array of points
    colors = ['red', 'green', 'blue', 'yellow', 'pink']

    def __init__(self, k):
        self.k = k

    # add new class to the class list
    def add_clas(self, clas):
        if clas - 1 in self.classes:
            print('class already exist')
        else:
            self.classes.append(clas - 1)

    def show(self):
        print(f'clases = {self.classes} \npoints = {self.points}')


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



    def add_new_point(self, x, y, z):
        new_point = Point(x, y, z)
        distances, class_count, class_list = [], {}, []

        for point in self.points:
            distances.append((self.get_distance(new_point, point), point.clas))

        if len(distances) < self.k:
            for i in range(len(distances)):
                class_list.append(distances[i][1])

            class_list.sort()

            for i in class_list:
                if i not in class_count:
                    class_count[i] = 1
                else:
                    class_count[i] += 1
        else:
            expander = self.k - 1
            if distances[self.k - 1] == distances[self.k]:

                while distances[expander] == distances[expander + 1]:
                    expander += 1

            distances.sort()

            for i in range(expander + 1):
                class_list.append(distances[i][1])

            class_list.sort()

            for i in class_list:
                if i not in class_count:
                    class_count[i] = 1
                else:
                    class_count[i] += 1

        new_point.clas = class_count[max(class_count.values())]

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


k = KNN(3)

k.add_clas(1)
k.add_clas(2)
k.add_clas(3)

k.add_known_point(0,0,0,1)
k.add_known_point(2,2,2,2)

k.plot()
k.add_new_point(1,1,1)


# x = [1, 2, 3, 0]
# y = [1, 2, 3, 0]
# z = [1, 2, 3, 0]
#
# trace1 = go.Scatter3d(
#     x=x,
#     y=y,
#     z=z,
#     mode='markers',
#     marker=dict(
#     size=12,
#     color=z,
#     colorscale='Viridis',
#     opacity=0.8))
#
# pairs = [(0,0), (1,1)]
#
#
# x_lines = list()
# y_lines = list()
# z_lines = list()
#
# for p in pairs:
#     for i in range(2):
#         x_lines.append(x[p[i]])
#         y_lines.append(x[p[i]])
#         z_lines.append(x[p[i]])
#
# trace2 = go.Scatter3d(
#     x = x_lines,
#     y = y_lines,
#     z = z_lines,
#     mode = 'lines',
#     name = 'lines'
# )
# data = [trace1, trace2]
# layout = go.Layout(
#     margin=dict(
#     l=0,
#     r=0,
#     b=0,
#     t=0)
# )
#
# fig = go.Figure(data=data, layout=layout)
# plot(fig, filename='3d-TEST-plot.html')
