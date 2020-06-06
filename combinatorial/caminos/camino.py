class Camino():

  """ Un camino es una sucesion de vertices de un grafo
    Se puede inicializar sin vertices (camino vacio) o puede
    inicializarse con una lista previa de vertices.

    La razon por la que creamos esta representacion para un camino
    es para que se consulte rapidamente si un vertice pertenece o no
    al camino. Una implementación alternativa consistiría en usar
    simplemente un objeto OrderedSet (el cual no es nativo de python)."""

  def __init__(self, vertices=None, peso=0):

    self._vertices = []
    """ Vertices ordenados del camino """

    self._arcos = []
    """Arcos ordenados del camino"""

    self._vertices_set = set()
    """ Conjunto de vertices del camino """

    """Esto nos permite tratar al camino como lista o conjunto, según convenga. Nos interesa la estructura de conjunto
    para poder acceder a un vértice en tiempo O(1)"""
    self._peso = peso

    if vertices is not None:
      for v in vertices:
        self.add(v)




  """Los siguientes son instance methods de la clase Camino. El parámetro self apunta a una instancia de la clase Camino
     cuando el método se llama. add agrega vértices a las representaciones de lista y conjunto del camino y actualiza 
     el peso. extend representa la operación que hace una extensión "unitaria" de un camino, i.e. recibe un vértice, 
     hace una copia del camino, añade el vértice y actualiza el peso. tail retorna el último vértice en el camino"""

  def add(self, v, peso=0):

    if len(self._vertices)>=1:
      self._arcos.append((self.tail(), v))
    else:
      pass
    self._vertices.append(v)
    self._vertices_set.add(v)
    self._peso += peso



  def extend(self, v, peso=0, copy=False):
    if copy:
      new_path = Camino(self._vertices, peso=self._peso)
      new_path.add(v, peso=peso)
      return new_path
    else:
      self.add(v, peso=peso)
      return self

  def tail(self):
    if len(self) == 0:
      raise ValueError()
    else:
      return self._vertices[-1]


  def peso(self):
    return self._peso

  def lista_camino(self):
    return self._vertices

  def lista_arcos(self):
    return self._arcos


  """__foo__: this is just a convention, a way for the Python system to use names that won't conflict with user names.

_foo: this is just a convention, a way for the programmer to indicate that the variable is private 
 (whatever that means in Python).

__foo: this has real meaning: the interpreter replaces this name with _classname__foo as a way to ensure that the name 
will not overlap with a similar name in another class."""


  def __str__(self):
    return str(self._vertices)


  def __contains__(self, v):
    return v in self._vertices_set


  def __len__(self):
    return len(self._vertices)