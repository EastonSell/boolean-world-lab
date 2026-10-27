"""Exact prefix-count reuse, no new solver or observer-specific simplification."""
from boolean_world import World, ImpossibleEvent
class CachedWorld(World):
    def __init__(self,circuit):
        super().__init__(circuit)
        self.total=self.cnf.count()
        self.solves=1
        self.requests=1
        self.hits=0
        self.cache={}
    def count(self):
        self.requests+=1
        self.hits+=1
        return self.total
    def unrank(self,rank):
        if not self.total: raise ImpossibleEvent('cannot condition on probability-zero event')
        if type(rank) is not int or not 0<=rank<self.total: raise ValueError('rank out of range')
        prefix=()
        for variable in range(1,self.circuit.n_inputs+1):
            self.requests+=1
            if prefix not in self.cache:
                self.cache[prefix]=self.cnf.count(dict(enumerate(prefix+(False,),1)))
                self.solves+=1
            else:self.hits+=1
            c0=self.cache[prefix]
            bit=rank>=c0
            if bit:rank-=c0
            prefix+=(bit,)
        return prefix
