import os

import pytest

if __name__ == '__main__':
    pytest.main(['-s', './pric.py', '--alluredir', 'temp'])
    # os.system('allure serve temp')
