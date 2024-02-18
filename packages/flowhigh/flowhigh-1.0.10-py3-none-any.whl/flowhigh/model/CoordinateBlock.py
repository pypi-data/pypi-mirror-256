
from flowhigh.model.TreeNode import TreeNode
from flowhigh.model.Hashable import Hashable


class CoordinateBlock(TreeNode, Hashable):
    pos: str = None
    

    def __init__(self):
        super().__init__()



