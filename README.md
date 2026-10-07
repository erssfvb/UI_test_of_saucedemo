# UI_Test_of_SauceDemo

基于Python + Playwright + pytest 的WebUI自动化测试demo,使用SauceDemo 公开网站(https://www.saucedemo.com/)演示Web测试中的POM设计，数据驱动，用户行为测试



## 本地安装

```bash
git clone https://github.com/erssfvb/UI_test_of_saucedemo

cd 你的目录/UI_test_of_saucedemo
# 创建虚拟环境
python -m venv .venv
# 激活虚拟环境
.venv/Scripts/activate
# 安装软件包
python -m pip -r install requirements.txt
# 安装browser或者设置环境变量PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=...\Chromium
playwright install chromium
# 先收集测试(预计有83个子项)
pytest --collect-only 
# 收集成功的话就可以运行测试了(allure报告，可选)
pytest --alluredir=allure-results
# 有allure的可以用allure生成测试报告
allure serve .../allure-results
```



## CI

每次git推送代码都要保证冒烟测试运行成功，以免流程错误

