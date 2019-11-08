class ModelStrTestCaseMixin:
    obj = None
    string = ''

    def test_str(self):
        self.assertEqual(self.obj.__str__(), self.string)

