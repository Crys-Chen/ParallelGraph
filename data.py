
from param import param

class Matrix:
    def __init__(self, name) -> None:
        self.name = name
    def __repr__(self) -> str:
        return self.name
    def __eq__(self, other) -> bool:
        return self.name == other.name

class Source:
    def __init__(self, 
                 name: str = "", 
                 cols: set = set()) -> None:
        if len(cols) != 0:
            self.src = {name: cols}
        else:
            self.src = {}


    def __eq__(self, other) -> bool:
        if len(self.src.keys() ^ other.src.keys()):
            return False
        for key in self.src.keys():
            if self.src[key] != other.src[key]:
                return False
        return True
    
    def __repr__(self) -> str:
        src_str = "\n\tSource: "
        for src in self.src.items():
            src_str += src[0] + "(" + str(list(src[1])) + ") "
        return src_str

    def combine(self, 
               other):
        for src in other.src.items():
            if self.src.get(src[0]):
                self.src[src[0]] = self.src[src[0]].union(src[1])
            else:
                self.src[src[0]] = src[1] 
        

class Data:
    def __init__(self, 
                 src: Source) -> None:
        self.src = src
        pass

class MatrixElement(Data):
    def __init__(self, 
                 matrix: Matrix, 
                 row: int, 
                 col: int) -> None:
        super().__init__(Source(matrix.name, {col}))
        self.matrix = matrix
        self.row = row
        self.col = col
        
    def __repr__(self) -> str:
        return self.matrix.name+"("+str(self.row)+","+str(self.col)+")"
    
class InterData(Data):
    def __init__(self,
                 src: Source,
                 inst: int) -> None:
        super().__init__(src)
        self.inst = inst

    def __repr__(self) -> str:
        return "inst("+str(self.inst)+") "

class VectorElement(Data):
    def __init__(self, 
                 name: str,
                 index: int) -> None:
        self.name = name
        self.index = index
        super().__init__(Source(self.name, {self.index}))

    def __repr__(self) -> str:
        return self.name+"("+str(self.index)+")"
