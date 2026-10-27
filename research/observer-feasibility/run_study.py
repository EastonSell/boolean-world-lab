"""Single-run, isolated-process frozen-suite study; timings are descriptive."""
import collections, fractions, hashlib, itertools, json, os, pathlib, platform
import resource, subprocess, sys, time
from boolean_world import World, ImpossibleEvent
from observer_world import EVENTS, accepts, compile_world, forward
ROOT=pathlib.Path(__file__).resolve().parent

def case(steps,event):
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    start=time.perf_counter()
    ts=time.perf_counter()
    forward_count=sum(accepts(forward(tape[:steps]),event) for tape in itertools.product((False,True),repeat=steps+1))
    baseline_count_s=time.perf_counter()-ts
    ts=time.perf_counter()
    baseline=collections.Counter()
    for tape in itertools.product((False,True),repeat=steps+1):
        transcript=forward(tape[:steps])
        if accepts(transcript,event): baseline[transcript]+=1
    baseline_s=time.perf_counter()-ts
    ts=time.perf_counter(); circuit=compile_world(steps,event); world=World(circuit)
    compile_s=time.perf_counter()-ts
    calls=0
    original=world.cnf.count
    def counted(*args,**kwargs):
        nonlocal calls
        calls+=1
        return original(*args,**kwargs)
    # Frozen CNF dataclass: wrapper preserves original immutable instance.
    class CountedCNF:
        def count(self,*args,**kwargs): return counted(*args,**kwargs)
    world.cnf=CountedCNF()
    ts=time.perf_counter(); count=world.count(); count_s=time.perf_counter()-ts
    ts=time.perf_counter(); ranked=collections.Counter()
    for rank in range(count): ranked[forward(world.unrank(rank)[:steps])]+=1
    generation_s=time.perf_counter()-ts
    impossible_error=None
    if not count:
        try: world.sample()
        except ImpossibleEvent: impossible_error='ImpossibleEvent'
    def rows(counter):
        return [{'transcript':[[int(x),int(m)] for x,m in t],'multiplicity':v} for t,v in sorted(counter.items())]
    return {'T':steps,'event':event,'status':'completed','n':circuit.n_inputs,
       'g':len(circuit.gates),'N':circuit.n_inputs+len(circuit.gates),
       'clauses':len(circuit.compile().clauses),'numerator':count,'denominator':1<<circuit.n_inputs,
       'probability':str(fractions.Fraction(count,1<<circuit.n_inputs)),
       'support_transcripts':len(baseline),'transcript_multiplicities':rows(baseline),
       'ranked_transcript_multiplicities':rows(ranked),
       'forward_count':forward_count,'count_equal':count==forward_count==sum(baseline.values()),
       'transcript_multiset_equal':baseline==ranked,'impossible_error':impossible_error,
       'count_calls':calls,'baseline_count_s':baseline_count_s,'baseline_multiset_s':baseline_s,'baseline_s':baseline_s,'compile_s':compile_s,'count_s':count_s,
       'generation_s':generation_s,'count_contract_s':compile_s+count_s,
       'multiset_contract_s':compile_s+count_s+generation_s,
       'case_work_s':time.perf_counter()-start,'peak_rss':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
       'peak_rss_units':'KiB on Linux; bytes on macOS'}

def main():
    if len(sys.argv)>1 and sys.argv[1]=='--case':
        print(json.dumps(case(int(sys.argv[2]),sys.argv[3]))); return
    protocol=ROOT/'docs/PROTOCOL.md'; digest=hashlib.sha256(protocol.read_bytes()).hexdigest()
    expected=(ROOT/'docs/PROTOCOL.sha256').read_text().split()[0]
    if digest!=expected: raise ValueError('protocol hash mismatch')
    start=time.monotonic(); results=[]
    for steps,event in itertools.product((2,4,6,8),EVENTS):
        remaining=600-(time.monotonic()-start)
        if remaining<=0:
            results.append({'T':steps,'event':event,'status':'total_budget_exhausted'}); continue
        ts=time.perf_counter()
        try:
            p=subprocess.run([sys.executable,__file__,'--case',str(steps),event],text=True,capture_output=True,timeout=min(60,remaining),cwd=ROOT)
            if p.returncode==0: row=json.loads(p.stdout)
            else: row={'T':steps,'event':event,'status':'error','returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
        except subprocess.TimeoutExpired as exc:
            row={'T':steps,'event':event,'status':'timeout','limit_s':min(60,remaining)}
        row['process_wall_s']=time.perf_counter()-ts
        results.append(row)
    report={'protocol_sha256':digest,'case_denominator':16,'repetitions':1,'caching':'No cross-case caching. Each case starts a new process. Reference counter has no memoization.',
      'host':{'platform':platform.platform(),'python':sys.version,'processor':platform.processor(),'machine':platform.machine(),'cpu_count':os.cpu_count()},
      'limits':{'case_wall_s':60,'address_space_MiB':512,'study_wall_s':600,'processes_at_once':1},
      'study_wall_s':time.monotonic()-start,'cases':results}
    report['completed']=sum(r['status']=='completed' for r in results)
    report['H1']=all(r.get('count_equal',False) for r in results)
    report['H2']=all(r.get('transcript_multiset_equal',False) for r in results)
    report['H3']=all(r.get('impossible_error')=='ImpossibleEvent' for r in results if r['event']=='impossible')
    report['H4']=report['completed']==16 and report['study_wall_s']<=600 and all(r['process_wall_s']<=60 for r in results)
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results/study.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('cases','host','caching')},indent=2))

if __name__=='__main__': main()
