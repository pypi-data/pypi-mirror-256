import unittest
from pds.api_client import Configuration
from pds.api_client import ApiClient

from pds.api_client.api.all_products_api import AllProductsApi


class PaginationTestCase(unittest.TestCase):
    def setUp(self):
        # create an instance of the API class
        configuration = Configuration()
        configuration.host = 'http://localhost:8080'
        api_client = ApiClient(configuration)
        self.products = AllProductsApi(api_client)

    def test_pages(self):
        results_1 = self.products.product_list(
            keywords=['kernel'],
            sort=['ops:Harvest_Info.ops:harvest_date_time'],
            limit=2
        )

        self.assertEqual(len(results_1.data), 2)  # add assertion here

        latest_harvest_date_time = results_1.data[-1].properties['ops:Harvest_Info.ops:harvest_date_time'][0]

        results_2 = self.products.product_list(
            keywords=['kernel'],
            sort=['ops:Harvest_Info.ops:harvest_date_time'],
            search_after=[latest_harvest_date_time],
            limit=2
        )

        self.assertEqual(len(results_2.data), 1)


if __name__ == '__main__':
    unittest.main()
