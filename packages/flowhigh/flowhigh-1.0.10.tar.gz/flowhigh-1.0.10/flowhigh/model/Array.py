
from flowhigh.model.Direction import Direction
from flowhigh.model.BaseExpr import BaseExpr


class Array(BaseExpr):
    type_: str = None
    items: list = []
    

    def __init__(self):
        super().__init__()



from flowhigh.model.TreeNode import TreeNode

class ArrayBuilder (object):
    construction: Array
    

    def __init__(self) -> None:
        super().__init__()
        self.construction = Array()
    
    def with_pos(self, pos: str):
        child = pos
        self.construction.pos = child
    
    def with_alias(self, alias: str):
        child = alias
        self.construction.alias = child
    
    def with_type(self, type_: str):
        child = type_
        self.construction.type_ = child
    
    def with_items(self, items: list):
        child = items
        for node in list(filter(lambda el: TreeNode in el.__class__.mro(), items)):
            self.construction.add_child(node)
        self.construction.items = child
    
    def with_direction(self, direction: Direction):
        child = direction
        self.construction.direction = child

    def build(self):
        return self.construction
