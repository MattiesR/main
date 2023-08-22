import math
import matplotlib.pyplot as plt
import constructie as c
import balk as b
import kracht as k

#utility functions
def length(Punten):
  #returns the length of a Balk
  assert len(Punten) == 2, "Een balk moet 2 punten hebben"
  return math.sqrt((Punten[1][0] - Punten[0][0])**2 + (Punten[1][1] - Punten[0][1])**2)

def som(a,b):   #vectorsom
    #returns the sum of two vectors
    #input: tuple object, tuple object
    #output: tuple object
    assert (len(a) == 2 and len(b) == 2), "De punten moeten 2 coördinaten hebben"
    return ((a[0] + b[0]), (a[1] + b[1]))

def vector(a,b):
    #returns the vector of a to b
    #input: tuple object, tuple object
    #output: tuple object
    assert (len(a) == 2 and len(b) == 2), "De punten moeten 2 coördinaten hebben"
    return ((b[0] - a[0]), (b[1] - a[1]))

def grootte_vector(a):
    #returns the length of a vector
    #input: tuple object
    #output: float
    assert (len(a) == 2), "De vector moet 2 coördinaten hebben"
    return math.sqrt(a[0]**2 + a[1]**2)

def unit_vector(a, b):
    #returns the unit vector of vector a to b
    #input: tuple object, tuple object
    #output: tuple object
    assert (len(a) == 2 and len(b) == 2), "De punten moeten 2 coördinaten hebben"
    length = math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)
    return ((b[0] - a[0])/length, (b[1] - a[1])/length)

def normal_vector(unit_vector):
    #returns the normal vector of a Balk
    #input: tuple object
    #output: tuple object
    assert (len(unit_vector) == 2), "De unit vector moet 2 coördinaten hebben"
    assert abs(grootte_vector(unit_vector) - 1) < 0.0001, "De unit vector moet lengte 1 hebben"
    return (unit_vector[1], -unit_vector[0])

def dot(a,b):
    assert (len(a) == 2 and len(b) == 2), "De punten moeten 2 coördinaten hebben"
    return a[0]*b[0] + a[1]*b[1]

def cross(a,b):
    assert (len(a) == 2 and len(b) == 2), "De punten moeten 2 coördinaten hebben"
    return a[0]*b[1] - a[1]*b[0]

def check_on_constructie(constructie, kracht):
    #returns True if the kracht is on the constructie
    #input: Constructie object, kracht object
    #output: boolean
    assert type(constructie) == c.Constructie, "De constructie moet een Constructie object zijn"
    assert type(kracht) == k.Kracht, "De kracht moet een Kracht object zijn"
    for balk in constructie.balken:
        if check_on_balk(balk, kracht):
            return True
    return False

def check_on_balk(balk, kracht):
    #returns True if the kracht is on the balk
    #input: Balk object, tuple object
    #output: boolean
    #check if kracht is on the balk
    assert type(balk) == b.Balk, "De balk moet een Balk object zijn"
    assert type(kracht) == k.Kracht, "De kracht moet een Kracht object zijn"
    return is_between(kracht.Aangrijping, balk.Punten[0], balk.Punten[1])

def check_on_interval(interval,kracht):
    #returns True if the kracht is on the interval
    #input: [tuple object, tuple object], kracht object
    #output: boolean
    assert len(interval) == 2, "Het interval moet 2 punten hebben"
    assert type(kracht) == k.Kracht, "De kracht moet een Kracht object zijn"
    return is_between(kracht.Aangrijping, interval[0], interval[1])

def check_connectie_on_balk(balk, connectie):
    #returns True if the connectie is on the balk
    #input: Balk object, [tuple object, tuple object]
    #output: boolean
    #check if connectie is on the balk

    assert type(balk) == b.Balk, "De balk moet een Balk object zijn"
    return is_between(connectie, balk.Punten[0], balk.Punten[1])

def visualize(constructie, krachten):
    #visualizes the constructie and the krachten
    #input: Constructie object, list of kracht objects
    #output: None

    balken = constructie.get_balken()
    connecties = constructie.get_connecties()
    points = []

    for balk in balken:
        for punt in balk.Punten:
          points.append(punt)
        plot_points(points, "blue", "o")

        points = []
        for connectie in connecties:
            points.append(connectie)
            plot_points(points, "green", "o")

        points = []
        for kracht in krachten:
            points.append(kracht.Aangrijping)
            added = tuple(map(lambda x, y: x + y, kracht.Aangrijping, kracht.kracht_componenten)) #som van de aangrijpingspunt en de krachtcomponenten
            points.append(added)
        plot_points(points, "red", "x")
    plt.axis('equal')
    plt.grid()
    plt.show()

#MANIER OM MOMENTEN TE VISUALISEREN NOG VINDEN
"""
  for verankering in constructie.verankering:
    points.append(verankering.Aangrijping)
    added = tuple(map(lambda x, y: x + y, verankering.Aangrijping, verankering.kracht_componenten)) #som van de aangrijpingspunt en de krachtcomponenten
    points.append(added)
  plot_points(points, "purple", "+")

  plt.axis('equal')
  plt.grid()
  plt.show()
"""

def plot_points(points, colour, marker):
  x_coords = [point[0] for point in points]
  y_coords = [point[1] for point in points]

  plt.scatter(x_coords, y_coords, color=colour, marker=marker)
  plt.title("visualization")
  plt.xlabel('X-axis')
  plt.ylabel('Y-axis')

  for point in points:
    plt.annotate(f'({point[0]}, {point[1]})', point, textcoords="offset points", xytext=(0, 10), ha='center')


def distance(a,b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def is_between(c,a,b):
    return abs(distance(a,c) + distance(c,b) - distance(a,b)) < 0.0001

def sort_points(start, points): # Insertion sort algorithm to sort the array of points in ascending order of distance from the start point
    n = len(points)  # Get the length of the array

    if n <= 1:
        return  # If the array has 0 or 1 element, it is already sorted, so return

    for i in range(1, n):  # Iterate over the array starting from the second element
        key = points[i]  # Store the current element as the key to be inserted in the right position
        j = i - 1
        while j >= 0 and distance(start, key) < distance(start, points[j]):  # Move elements greater than key one position ahead
            points[j + 1] = points[j]  # Shift elements to the right
            j -= 1
        points[j + 1] = key  # Insert the key in the correct position
    return points

#INPUT: list of lists
#OUTPUT: list
def extract(list):
    extracted = []
    for interval in list:
        for i in interval:
            extracted.append(i)
    return extracted

#add lists pairwise of unknown length
def add_lists(list1, list2):
    assert (type(list1) == list and type(list2) == list), "De input moeten twee lijst zijn"
    added_list = []
    max_list = max(len(list1), len(list2))
    for i in range(max_list):
        try:
            added_list.append(list1[i] + list2[i])
        except IndexError:
            if len(list1) > len(list2):
                added_list.append(list1[i])
            else:
                added_list.append(list2[i])
    return added_list

# Sorting the array [12, 11, 13, 5, 6] using insertionSort
#points = [(12,2), (11,-1), (4,.3), (5,0), (6,0)]

#sort_points((11,-1), points)
#print(points)

#test add_lists
l1 = [1,2,3,4,5]
l2 = [1,2,3,4,5,6,7,8,9]
#more tests
l3 = [1,2,0,4,5,6,7,8,9]
l4 = []



