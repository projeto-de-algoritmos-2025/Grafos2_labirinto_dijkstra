class DisjointSet:
    class Element:
        def __init__(self, key):
            self.key = key
            self.parent = self
            self.rank = 0

    def __init__(self):
        self.tree = {}

    def make_set(self, key):
        e = self.Element(key)
        if key not in self.tree:
            self.tree[key] = e

    def find(self, key):
        if key in self.tree:
            element = self.tree[key]
            if element.parent != element:
                element.parent = self.find(element.parent.key)
            return element.parent

    def union(self, a, b):
        root_a = self.find(a.key)
        root_b = self.find(b.key)
        if root_a != root_b:
            if root_a.rank < root_b.rank:
                root_a.parent = root_b
            elif root_a.rank > root_b.rank:
                root_b.parent = root_a
            else:
                root_b.parent = root_a
                root_a.rank += 1