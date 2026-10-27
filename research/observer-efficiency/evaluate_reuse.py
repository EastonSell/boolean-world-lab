import sys,pathlib,collections,itertools,time,resource,json,hashlib,subprocess,platform,os,fractions
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'baseline/research/observer-feasibility'))
from boolean_world import World,ImpossibleEvent
from observer_world import compile_world,forward,accepts,EVENTS
from cached_world import CachedWorld

def size_cache(cache):
    # Container plus unique owned tuple and int objects; singleton booleans excluded.
    seen=set(); total=sys.getsizeof(cache)
    for k,v in cache.items():
        for obj in (k,v):
            if id(obj) not in seen:seen.add(id(obj));total+=sys.getsizeof(obj)
    return total

def run_cell(t,e,method):
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,)*2)
    cpu=time.process_time();start=time.perf_counter();out=collections.Counter();work={}
    if method=='forward':
        ts=time.perf_counter()
        count=sum(accepts(forward(x[:t]),e) for x in itertools.product((False,True),repeat=t+1))
        count_s=time.perf_counter()-ts
        ts=time.perf_counter()
        for x in itertools.product((False,True),repeat=t+1):
            y=forward(x[:t])
            if accepts(y,e):out[y]+=1
        multiset_s=time.perf_counter()-ts
        compile_s=0;probe=None
        work={'count_tapes':1<<(t+1),'multiset_tapes':1<<(t+1),'count_replay_ticks':t*(1<<(t+1)),'multiset_replay_ticks':t*(1<<(t+1)),'actual_cnf_calls':0}
    else:
        ts=time.perf_counter(); circuit=compile_world(t,e)
        world=(CachedWorld if method=='cached' else World)(circuit)
        compile_s=time.perf_counter()-ts
        calls=0
        original=world.cnf
        class Counted:
            def count(self,*args,**kwargs):
                nonlocal calls
                calls+=1
                return original.count(*args,**kwargs)
        world.cnf=Counted()
        ts=time.perf_counter();count=world.count();count_s=compile_s+time.perf_counter()-ts
        ts=time.perf_counter()
        for rank in range(count):out[forward(world.unrank(rank)[:t])]+=1
        generation_s=time.perf_counter()-ts
        multiset_s=count_s+generation_s
        probe=None
        if not count:
            try:world.sample()
            except ImpossibleEvent:probe='ImpossibleEvent'
        work={'actual_cnf_calls':calls+(1 if method=='cached' else 0),'rank_requests':count,'replay_ticks':count*t,'n_inputs':circuit.n_inputs,'gates':len(circuit.gates),'cnf_variables':original.n_variables,'clauses':len(original.clauses),'compiled_literals':sum(map(len,original.clauses))}
        if method=='cached':
            work.update(count_requests=world.requests,cache_hits=world.hits,cache_entries=len(world.cache),cache_key_slots=sum(map(len,world.cache)),cache_owned_shallow_bytes=size_cache(world.cache))
            assert work['actual_cnf_calls']==world.solves
    return {'T':t,'event':e,'method':method,'status':'completed','numerator':count,'denominator':1<<(t+1),'probability':str(fractions.Fraction(count,1<<(t+1))),'support':len(out),'rows':[[[[int(a),int(b)] for a,b in k],v] for k,v in sorted(out.items())],'count_contract_s':count_s,'multiset_contract_s':multiset_s,'initialization_s':compile_s,'work':work,'impossible_error':probe,'method_work_s':time.perf_counter()-start,'process_cpu_s':time.process_time()-cpu,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}

def main():
    if len(sys.argv)>1:
        print(json.dumps(run_cell(int(sys.argv[1]),sys.argv[2],sys.argv[3])));return
    frozen=json.loads((ROOT/'FREEZE.json').read_text())
    for name,digest in frozen['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    path=ROOT/'results.jsonl';start=time.monotonic();rows=[]
    with path.open('x') as f:
        for i,(t,e) in enumerate(itertools.product((2,4,6,8),EVENTS)):
            for method in ['forward']+(['original','cached'] if i%2==0 else ['cached','original']):
                remaining=600-(time.monotonic()-start);ts=time.perf_counter()
                row={'T':t,'event':e,'method':method}
                if remaining<=0:row['status']='total_budget_exhausted'
                else:
                    try:
                        p=subprocess.run([sys.executable,__file__,str(t),e,method],capture_output=True,text=True,timeout=min(60,remaining))
                        if p.returncode:row.update(status='error',returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
                        else:row=json.loads(p.stdout)
                    except subprocess.TimeoutExpired as ex:row.update(status='timeout',stdout=str(ex.stdout),stderr=str(ex.stderr))
                    except Exception as ex:row.update(status='runner_error',error=repr(ex))
                row['process_wall_s']=time.perf_counter()-ts;rows.append(row);f.write(json.dumps(row)+'\n');f.flush()
                print(t,e,method,row['status'],row.get('multiset_contract_s'),flush=True)
    comparisons=[]
    for t,e in itertools.product((2,4,6,8),EVENTS):
        rs={r['method']:r for r in rows if (r['T'],r['event'])==(t,e)}
        ok=all(r['status']=='completed' for r in rs.values())
        equal=ok and len({json.dumps([r['numerator'],r['denominator'],r['rows']]) for r in rs.values()})==1
        d={'T':t,'event':e,'all_methods_complete':ok,'exact_equal':equal}
        if ok:d.update(cached_vs_original_speedup=rs['original']['multiset_contract_s']/rs['cached']['multiset_contract_s'],cached_over_forward=rs['cached']['multiset_contract_s']/rs['forward']['multiset_contract_s'])
        comparisons.append(d)
    report={'planned_method_cells':48,'completed':sum(r['status']=='completed' for r in rows),'planned_comparisons':16,'exact_equal':sum(d['exact_equal'] for d in comparisons),'planned_impossible_probes':8,'impossible_errors':sum(r.get('impossible_error')=='ImpossibleEvent' for r in rows),'wall_s':time.monotonic()-start,'repetitions':1,'host':{'platform':platform.platform(),'python':sys.version,'cpu_count':os.cpu_count(),'cpuinfo':pathlib.Path('/proc/cpuinfo').read_text().split('model name')[1].split('\n')[0] if pathlib.Path('/proc/cpuinfo').exists() else platform.processor()},'limits':{'method_cell_s':60,'address_space_MiB':512,'study_s':600},'freeze':frozen,'comparisons':comparisons}
    with (ROOT/'summary.json').open('x') as f:json.dump(report,f,indent=2)
if __name__=='__main__':main()
