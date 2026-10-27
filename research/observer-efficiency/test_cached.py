import sys,pathlib,unittest,itertools
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'baseline/research/observer-feasibility'))
from boolean_world import World,ImpossibleEvent
from observer_world import compile_world,EVENTS
try:
 from cached_world import CachedWorld
except ImportError:
 CachedWorld=None
class Tests(unittest.TestCase):
 def test_feature_exists(self):self.assertIsNotNone(CachedWorld)
 @unittest.skipIf(CachedWorld is None,'feature absent')
 def test_exact_ranks(self):
  for t,e in itertools.product((1,3),EVENTS):
   a=World(compile_world(t,e));b=CachedWorld(compile_world(t,e))
   self.assertEqual(a.count(),b.count())
   for r in range(a.count()):self.assertEqual(a.unrank(r),b.unrank(r))
 @unittest.skipIf(CachedWorld is None,'feature absent')
 def test_reuse_and_isolation(self):
  a=CachedWorld(compile_world(3,'none')); b=CachedWorld(compile_world(3,'none'))
  for r in range(16):a.unrank(r)
  self.assertEqual(a.solves,16);self.assertEqual(len(a.cache),15)
  for r in reversed(range(16)):a.unrank(r)
  self.assertEqual(a.solves,16);self.assertEqual(b.solves,1);self.assertEqual(b.cache,{})
 @unittest.skipIf(CachedWorld is None,'feature absent')
 def test_invalid_and_impossible(self):
  a=CachedWorld(compile_world(1,'none'))
  for r in (-1,4,True,1.1):
   with self.assertRaises(ValueError):a.unrank(r)
  b=CachedWorld(compile_world(1,'impossible'))
  with self.assertRaises(ImpossibleEvent):b.unrank(0)
  with self.assertRaises(ImpossibleEvent):b.sample()
  self.assertEqual(b.solves,1)
if __name__=='__main__':unittest.main()
