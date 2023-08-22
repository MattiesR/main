import numpy as np
#TESTEN GESLAAGD!!!!

#format energiepotentiaal_lijst: [FF, FP, FH, P^2, PH, H^2]
#format aantal_krachten: int
def differentiaal(energiepotentiaal_lijst, aantal_krachten):
    energie_matrix = build_matrix(energiepotentiaal_lijst, aantal_krachten)

    rechterlid = -energie_matrix[:,0]
    rechterlid = np.delete(rechterlid, (0), axis=0)
    energie_matrix = np.delete(energie_matrix, (0), axis=0)
    energie_matrix = np.delete(energie_matrix, (0), axis=1)
    opl = np.linalg.solve(energie_matrix, rechterlid)
    return opl

def build_matrix(energiepotentiaal_lijst, aantal_krachten):
    matrix = []
    hulp_matrix = []
    row_index = 0
    index = 0
    element_index = 0
    next_row = aantal_krachten
    while next_row > 0:
        index = 0
        hulp_matrix = []
        while index < next_row and element_index < len(energiepotentiaal_lijst):
            hulp_matrix.append(energiepotentiaal_lijst[element_index])
            element_index += 1
            index += 1
        next_row -= 1
        matrix.append(hulp_matrix)
    matrix_with_zeros = complete_with_zeros(matrix)
    matrix1 = np.array(matrix_with_zeros)
    matrix2 = np.transpose(matrix1)
    matrix = np.add(matrix1,matrix2)
    return matrix

def complete_with_zeros(matrix):
    completed_matrix = []
    for i in matrix:
        while len(i) < len(matrix):
            i.insert(0,0)
        completed_matrix.append(i)
    return completed_matrix


test = [1,2,3,4,5,6]


"""test1 = build_matrix(test,3)
print(test1)
test2 = differentiaal(test,3)
print(test2)
completed_matrix = complete_with_zeros(test1)
"""

"""matrix1 = np.array(completed_matrix)
print(matrix1)
matrix2 = np.transpose(matrix1)
print(matrix1)
print(np.add(matrix1,matrix2))
"""

"""
a = np.array([[1, 2], [3, 5]])
b = np.array([1, 2])
x = np.linalg.solve(a, b)
"""
#print(x)
