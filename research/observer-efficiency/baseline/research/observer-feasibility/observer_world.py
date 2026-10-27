"""Finite two-bit feedback observer; operational memory, not consciousness."""
from boolean_world import Circuit
EVENTS=('none','terminal_memory_true','all_observations_true','impossible')

def forward(tape):
    """Independent transition interpreter, returning (observation, memory) per tick."""
    x=m=False
    log=[]
    for u in tape:
        if type(u) is not bool: raise ValueError('tape entries must be Boolean')
        x=(x != u) != m
        m=m != x
        log.append((x,m))
    return tuple(log)

def accepts(transcript,event):
    if event not in EVENTS: raise ValueError('unknown event')
    if event=='none': return True
    if event=='impossible': return False
    if event=='terminal_memory_true': return bool(transcript and transcript[-1][1])
    return all(x for x,m in transcript)

def compile_world(steps,event):
    """Compile T fair innovations and one deliberately unused fair input."""
    if type(steps) is not int or steps < 1: raise ValueError('steps must be positive integer')
    if event not in EVENTS: raise ValueError('unknown event')
    n=steps+1
    gates=[]
    def gate(op,*args):
        gates.append((op,tuple(args)))
        return n+len(gates)
    x=m=gate('FALSE')
    observations=[]
    for u in range(1,steps+1):
        x=gate('XOR',gate('XOR',x,u),m)
        m=gate('XOR',m,x)
        observations.append(x)
    if event=='none': out=gate('TRUE')
    elif event=='impossible': out=gate('FALSE')
    elif event=='terminal_memory_true': out=m
    else:
        out=observations[0]
        for x in observations[1:]: out=gate('AND',out,x)
    return Circuit(n,tuple(gates),out)
