import object
import unittest


class TestStringHashKey(unittest.TestCase):
    def test_str_hashkey(self):
        hello1 = object.String(value='Hello World')
        hello2 = object.String(value='Hello World')
        diff1 = object.String(value='My name is johnny')
        diff2 = object.String(value='My name is johnny')
        if hello1.hash_key() != hello2.hash_key():
            print(hello1.hash_key(), hello2.hash_key())
            self.fail('strings with same content have different hash keys')

        if diff1.hash_key() != diff2.hash_key():
            self.fail('strings with same content have different hash keys')

        if hello1.hash_key() == diff1.hash_key():
            self.fail('strings with different content have same hash keys')


if __name__ == '__main__':
    unittest.main()