import unittest
from static.models.account import Account


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.account = Account()

    def test_create_account(self):
        self.assertIsNotNone(self.account)

    def test_get_account_name(self):
        self.account.email = "test@mail.com"
        self.assertEqual("test@mail.com", self.account.email)

    def test_encoded_password(self):
        self.account.password = "password"
        self.assertNotEqual("password", self.account.password)
        self.assertTrue(self.account.validatePassword("password"))

    def test_deposit(self):
        self.account.deposit(1000)
        self.assertEqual(1000, self.account.balance)

    def test_negative_deposit(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-1000)
        self.assertEqual(0, self.account.balance)

    def test_withdraw(self):
        self.account.deposit(1000)
        self.account.withdraw(1000)
        self.assertEqual(0, self.account.balance)

    def test_withdraw_amount_greater_than_balance(self):
        self.account.deposit(1000)
        with self.assertRaises(ValueError):
            self.account.withdraw(2000)
        self.assertEqual(1000, self.account.balance)

    def test_account_numbers(self):
        self.assertEqual(1, self.account.account_number)
        account2 = Account()
        self.assertEqual(2, account2.account_number)


if __name__ == '__main__':
    unittest.main()
