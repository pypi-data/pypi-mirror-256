import unittest
from src.insulaClient.InsulaFilesJobResult import InsulaFilesJobResult
from src.insulaClient.InsulaApiConfig import InsulaApiConfig


class TestInsulaFilesJobResult(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def setUp(cls):
        cls.results = InsulaFilesJobResult(InsulaApiConfig('https://iride-lot3.ope.insula.earth', 'cgi.campaign.bot',
                                                           'the_token'))

    @classmethod
    def tearDown(cls):
        cls.results = None

    @classmethod
    def tearDownClass(cls):
        pass

    # def test_get_result_from_job(self):
    #     print(self.results.get_result_from_job(1367))


if __name__ == '__main__':
    unittest.main()
