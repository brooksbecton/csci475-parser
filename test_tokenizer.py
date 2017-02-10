"""For ughh.. unit testing"""
import unittest

from Tokenizer import Tokenizer


class TokenizerTest(unittest.TestCase):

    test_tokenizer = Tokenizer()

    def tearDown(self):
        self.test_tokenizer.symbolTable = []
        self.test_tokenizer.tokens = []


    def test_int_token_lookup(self):
        test_string = "int "
        self.test_tokenizer.target_str = test_string
        expected_result = ["<INT>"]
        self.test_tokenizer.getTokens()
        self.assertEqual(self.test_tokenizer.tokens, expected_result)


    def test_int_and_id(self):
        test_string = "int b"
        self.test_tokenizer.target_str = test_string
        expected_result = ["<INT>", "<ID, 0>"]
        self.test_tokenizer.getTokens()
        self.assertEqual(self.test_tokenizer.tokens, expected_result)

    def test_int_and_number(self):
        test_string = "int 4"
        self.test_tokenizer.target_str = test_string
        expected_result = ["<INT>", "<INTEGER, 0>"]
        self.test_tokenizer.getTokens()
        self.assertEqual(self.test_tokenizer.tokens, expected_result)

    def test_float_token_lookup(self):
        test_string = "float "
        self.test_tokenizer.target_str = test_string
        expected_result = ["<FLOAT>"]
        self.test_tokenizer.getTokens()
        self.assertEqual(self.test_tokenizer.tokens, expected_result)

    def test_float_and_id(self):
        test_string = "float a"
        self.test_tokenizer.target_str = test_string
        expected_result = ["<FLOAT>", "<ID, 0>"]
        self.test_tokenizer.getTokens()
        self.assertEqual(self.test_tokenizer.tokens, expected_result)

    def test_lsqb(self):
        test_string = "["
        self.test_tokenizer.target_str = test_string
        expected_result = ["<LSQB>"]
        self.test_tokenizer.getTokens()
        self.assertEqual(self.test_tokenizer.tokens, expected_result)

    def test_rsqb(self):
        test_string = "]"
        self.test_tokenizer.target_str = test_string
        expected_result = ["<RSQB>"]
        self.test_tokenizer.getTokens()
        self.assertEqual(self.test_tokenizer.tokens, expected_result)

    def test_lsqb_id_rsqb(self):
        test_string = "[a]"
        self.test_tokenizer.target_str = test_string
        expected_result = ["<LSQB>", "<ID, 0>", "<RSQB>"]
        self.test_tokenizer.getTokens()
        self.assertEqual(self.test_tokenizer.tokens, expected_result)




unittest.main()