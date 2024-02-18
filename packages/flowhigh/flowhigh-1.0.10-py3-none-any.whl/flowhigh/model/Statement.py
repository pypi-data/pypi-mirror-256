
from flowhigh.model.CoordinateBlock import CoordinateBlock


class Statement(CoordinateBlock):
    clusterTopologyHiID: int = None
    clusterTopologyLoID: int = None
    pos: str = None
    clusterLogicalID: int = None
    antiPatterns: list = []
    rawInput: str = None
    clusterRawID: int = None
    ds: list = []
    

    def __init__(self):
        super().__init__()



from flowhigh.model.TreeNode import TreeNode

class StatementBuilder (object):
    construction: Statement
    

    def __init__(self) -> None:
        super().__init__()
        self.construction = Statement()
    
    def with_clusterTopologyLoID(self, clusterTopologyLoID: int):
        child = clusterTopologyLoID
        self.construction.clusterTopologyLoID = child
    
    def with_clusterTopologyHiID(self, clusterTopologyHiID: int):
        child = clusterTopologyHiID
        self.construction.clusterTopologyHiID = child
    
    def with_pos(self, pos: str):
        child = pos
        self.construction.pos = child
    
    def with_rawInput(self, rawInput: str):
        child = rawInput
        self.construction.rawInput = child
    
    def with_antiPatterns(self, antiPatterns: list):
        child = antiPatterns
        for node in list(filter(lambda el: TreeNode in el.__class__.mro(), antiPatterns)):
            self.construction.add_child(node)
        self.construction.antiPatterns = child
    
    def with_clusterLogicalID(self, clusterLogicalID: int):
        child = clusterLogicalID
        self.construction.clusterLogicalID = child
    
    def with_clusterRawID(self, clusterRawID: int):
        child = clusterRawID
        self.construction.clusterRawID = child
    
    def with_ds(self, ds: list):
        child = ds
        for node in list(filter(lambda el: TreeNode in el.__class__.mro(), ds)):
            self.construction.add_child(node)
        self.construction.ds = child

    def build(self):
        return self.construction
