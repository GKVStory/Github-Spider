import unittest

def addition(a, b):
    return a + b

class TestMyFunction(unittest.TestCase):
    def test_addition(self):
        result = addition(1, 2)
        self.assertEqual(result, 3)

if __name__ == '__main__':
    unittest.main()