import allure


@allure.feature('自动化框架测试')
class Test:
    @allure.story('用例A')
    @allure.description('测试多步骤的情况')
    @allure.title('用例A的标题')
    def test_py_a(self):
        with allure.step('断言一'):
            assert 1 == 1
        with allure.step('断言二'):
            assert 6 == 6

    @allure.story('用例B')
    def test_py_b(self):
        assert 1 == 1

    @allure.story('用例C')
    def test_py_c(self):
        assert 6 > 2
