import os

import pytest

if __name__ == '__main__':
    pytest.main(['-s', './pric.py', '--alluredir', 'allure_temp'])
    os.system('allure serve allure_temp')
