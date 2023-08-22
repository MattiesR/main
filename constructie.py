import matplotlib.pyplot as plt
class Constructie:
  def __init__(self, name, balken, connecties, verankering):
    self.name = name
    self.balken = balken    # list of Balk objects
    self.connecties = connecties    # list of Punt objects
    self.verankering = verankering  # Hoe een constructie vasthangt aan de omgeving ... list of verankeringen. verankering: kracht / moment


  def get_balken(self):
    return self.balken

  def get_connecties(self):
    return self.connecties

  def draw_balken(self):
    # draw the constructie
    points = []
    for balk in self.balken:
        for punt in balk.Punten:
            points.append(punt)
    plot_points(points,'Punten van Balken', "blue")

  def draw_connecties(self):
    # draw the connecties
    points = []
    for connectie in self.connecties:
        points.append(connectie)
    plot_points(points, 'Punten van Connecties', "red")

  def draw_Constructie(self):
    # draw the constructie
    #but the points of the balken are blue and the points of the connecties are red
    points = []
    for balk in self.balken:
        for punt in balk.Punten:
            points.append(punt)
    for connectie in self.connecties:
        points.append(connectie)
    plot_points(points, 'Punten van Constructie', "green")




def plot_points(points, title, colour):
  x_coords = [point[0] for point in points]
  y_coords = [point[1] for point in points]

  plt.scatter(x_coords, y_coords, color=colour, marker='o')
  plt.title(title)
  plt.xlabel('X-axis')
  plt.ylabel('Y-axis')

  for point in points:
    plt.annotate(f'({point[0]}, {point[1]})', point, textcoords="offset points", xytext=(0, 10), ha='center')

  plt.grid()
  plt.show()

