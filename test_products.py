import unittest, zipfile, csv, io
from pathlib import Path
from generate import build, OUT
class ProductsTest(unittest.TestCase):
 def test_products(self):
  build()
  for name in ('cafe','beauty','shop'):
   with zipfile.ZipFile(OUT/f'{name}-social-posts.zip') as z:
    rows=list(csv.DictReader(io.StringIO(z.read('posts.csv').decode('utf-8-sig'))))
    self.assertEqual(len(rows),100)
    self.assertTrue(all(row['投稿文'] for row in rows))
if __name__=='__main__': unittest.main()
