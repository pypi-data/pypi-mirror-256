import unittest

from onepyece import functions
from onepyece.common import ENDPOINTS, NO_RESOURCE_SEARCHES


class TestFunctions(unittest.TestCase):
    def test_functions(self):
        """Test if all functions are present for all endpoints and searches"""
        for endpoint in ENDPOINTS:
            for search in ENDPOINTS[endpoint]:
                current_endpoint = endpoint[:-1] if endpoint.endswith("s") else endpoint
                current_endpoint = current_endpoint.replace("/", "_")
                if search not in NO_RESOURCE_SEARCHES:
                    function_name = f"{current_endpoint}_by_{search}"
                else:
                    function_name = f"{search}_{current_endpoint}s"
                print(function_name)
                self.assertTrue(hasattr(functions, function_name))
