
import sys, os, time, platform, json, datetime
from selenium.webdriver.chrome import webdriver
# from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import NoSuchElementException

from urllib.parse import quote
from urllib import request

import argparse

# ---------------functions--------------- #

def _switch_to_frame(driver):
    data_frame = driver.find_element_by_xpath('//*[@id="J_top_content"]')
    driver.switch_to.frame(data_frame)
    data_frame = driver.find_element_by_xpath('//*[@id="explorer_properties_content"]')
    driver.switch_to.frame(data_frame)

def click_by_xpath(driver, xpath, choose_last=False):
    """
    默认的 click 方法有的时候会失效
    下拉列表出现时，只有最后的xpath是有效的
    """
    if choose_last:
        element = driver.find_elements_by_xpath(xpath)[-1]
    else:
        element = driver.find_element_by_xpath(xpath)
    driver.execute_script("arguments[0].click();", element)

def remove_readonly_by_xpath(driver, xpath):
    element = driver.find_element_by_xpath(xpath)
    driver.execute_script('arguments[0].removeAttribute("readonly")', element)

def save_screen_shot(driver):
    path = "screen_shots"
    os.makedirs(path, exist_ok=True)
    date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    driver.save_screenshot(path + f'/{date_time}.png')

def wechat_notification(userName, sckey, state):
    """
    copy from https://github.com/Bruuuuuuce/PKUAutoSubmit
    """
    if state == "已保存":
        state_info = "已经保存，记得及时提交！"
    elif state == "已提交":
        state_info = "已经提交，请检查提交记录！"
    else:
        raise ValueError(f"state错误：{state}")

    url_text = f'https://sc.ftqq.com/{sckey}.send?text={state_info}&desp=学号{userName}成功提交申请'
    with request.urlopen(quote(url_text, safe='/:?=&')) as response:
        response = json.loads(response.read().decode('utf-8'))
    if response['errmsg'] == 'success':
        print('微信通知成功！')
    else:
        print(str(response['errno']) + ' error: ' + response['errmsg'])

# ---------------logic--------------- #

def get_in_page(driver, config):
    """
    登录并进入出入校申请
    """
    driver.get('https://portal.pku.edu.cn/')
    time.sleep(3)

    # 门户
    driver.find_element_by_xpath('//*[@id="user_name"]').send_keys(config["学号"])
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(config["密码"])
    time.sleep(0.5)

    # 登录
    click_by_xpath(driver, '//*[@id="logon_button"]')
    time.sleep(3)

    # 学生出入校
    driver.get('https://portal.pku.edu.cn/portal2017/util/appSysRedir.do?appId=stuCampusExEn')
    time.sleep(3)

    # 出入校申请
    click_by_xpath(driver, '/html/body/div/section/div/div/div[2]/main/div[3]/a/div/div/span')
    time.sleep(1)

    assert driver.find_element_by_xpath('/html/body/div/section/div/div/div[2]/main/div/div[1]/div/div/div[2]').text == '出入校申请', \
        "未能进入出入校申请"

    # 判断是否已保存
    if driver.find_element_by_xpath('//input[@placeholder="选择日期"]').get_attribute("disabled"):
        # 返回
        xpath = '//div[@class="el-page-header__title"][contains(string(), "返回")]'
        driver.find_element_by_xpath(xpath).click()
        time.sleep(1)
        
        # 点击 申请历史
        xpath = '//span[contains(string(), "申请历史")]'
        driver.find_element_by_xpath(xpath).click()
        time.sleep(1)

        # 第一个未审核的元素
        xpath = '//tr//div[contains(string(), "未审核")]'
        click_by_xpath(driver, xpath)
        time.sleep(1)

        config["history"] = True
    else:
        config["history"] = False

def find_div_by_name(driver, name):
    """
    根据label的text，找到下一个兄弟div节点
    """
    xpath = f'/html/body//form//label[contains(string(), "{name}")]/following-sibling::div[1]'
    div = driver.find_element_by_xpath(xpath)
    return div

def find_textarea_by_name(driver, name):
    """
    根据label的text，找到下一个兄弟div节点下的textarea
    """
    div = find_div_by_name(driver, name)
    textarea = div.find_element_by_xpath(".//textarea")
    return textarea

def find_input_by_name(driver, name):
    """
    根据label的text，找到下一个兄弟div节点下的input
    """
    div = find_div_by_name(driver, name)
    _input = div.find_element_by_xpath(".//input")
    return _input

def click_element_in_drop_by_name(driver, name, value):
    """
    点击-选择元素。下拉列表的xpath都是 /html/body/div[5]
    """
    # 点击
    find_div_by_name(driver, name).click()
    time.sleep(0.5)
    # 选择
    xpath = f'/html/body//li[contains(string(), "{value}")]'
    click_by_xpath(driver, xpath, choose_last=True)
    time.sleep(0.5)

def write_info(driver, config):

    # 先填写 下拉-点击 。不存在的字段跳过
    driver.implicitly_wait(0.5)
    for name in ["出入校起点", "出入校终点", "起点校门", "终点校门", "出入校事由",
                "起点所在省", "起点所在地级市", "起点所在区县",
                "终点所在省", "终点所在地级市", "终点所在区县",
                "宿舍园区",]:
        try:
            if name in ["终点校门", "起点校门"]:
                value = config["起点/终点校门"]
            elif name in ["起点所在省", "终点所在省"]:
                value = "北京市"
            elif name in ["起点所在地级市", "终点所在地级市"]:
                value = "市辖区"
            elif name in ["起点所在区县", "终点所在区县"]:
                value = "海淀区"
            else:
                value = config[name]
            click_element_in_drop_by_name(driver, name, value)
        except Exception as e:
            print(f"找不到：{name}")
    
    # input字段
    for name in ["起点所在街道", "终点所在街道", "邮箱", "手机号", "宿舍楼", "宿舍房间号",]:
        try:
            if name in ["起点所在街道", "终点所在街道",]:
                value = config["起点/终点所在街道"]
            else:
                value = config[name]

            if name in ["宿舍楼", "宿舍房间号"] and config["宿舍园区"] == "无宿舍": continue

            _input = find_input_by_name(driver, name)
            _input.clear()
            _input.send_keys(value)
        except Exception as e:
            print(f"找不到：{name}")

    # textarea字段
    for name in ["出入校具体事项", "基本轨迹", "补充说明",]:
        try:
            value = config[name]
            textarea = find_textarea_by_name(driver, name)
            textarea.clear()
            textarea.send_keys(value)
        except Exception as e:
            print(f"找不到：{name}")


    # 证明材料上传
    if config["程序暂停"] == "是":
        driver.implicitly_wait(60)
        driver.find_element_by_xpath(f'//form//button[contains(string(), "{config["证明材料上传"]}")]').click()
        print("\n上传附件后，输入go继续；输入exit结束程序，请在1分钟内上传附件")
        while True:
            _input = input()
            if _input.lower() == "go": break
            elif _input.lower() == "exit": exit()
            else: print("输入错误")
    
    print("程序继续")

    # 勾选已读 已经保存则不能勾选
    if not config["history"]:
        driver.find_element_by_xpath('//form//label[contains(string(), "本人承诺遵守")]').click()
        time.sleep(0.5)

    # 点击保存
    driver.find_element_by_xpath('//button[contains(string(), "保存")]').click()
    time.sleep(0.5)
    config["state"] = "已保存"

    # 暂不提交
    try:
        # 若历史页面且无需保存，这里不会出现弹窗，触发implicitly_wait
        driver.implicitly_wait(3)
        driver.find_element_by_xpath('//button[contains(string(), "暂不提交")]').click()
        driver.implicitly_wait(10)
        time.sleep(0.5)
    except Exception as e:
        pass

def submit(driver, config):
    """
    提交
    """
    if config["提交"] == "是" and config["程序暂停"] == "是":
        driver.find_element_by_xpath('//button[contains(string(), "提交")]').click()
        time.sleep(0.3)
        driver.find_element_by_xpath('//button[contains(string(), "确定")]').click()
        time.sleep(0.3)
        config["state"] = "已提交"

def get_in_history(driver):
    xpath = '//div[@class="el-page-header__title"][contains(string(), "返回")]'
    driver.find_element_by_xpath(xpath).click()
    time.sleep(1)
    # 滑动到最底
    driver.execute_script("window.scrollBy(0,8000)")

def logout(driver):
    driver.find_element_by_xpath('/html/body/div[1]/section/header/div[1]/div[3]/div/div[2]/button').click()
    time.sleep(3)
    driver.find_elements_by_xpath('//a[contains(string(), "退出")]')[-1].click()
    time.sleep(2)

# ---------------helper--------------- #

def make_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--configs", required=True, nargs='+', type=str, help="config.json文件列表",)
    args = parser.parse_args()
    return args

def config_check(config):
    """
    配置检查
    """
    # if config["出入校起点"] not in ["燕园", "校外", "大兴校区"]:
    #     raise ValueError("起点设置有误")
    # if config["出入校终点"] not in ["燕园", "校外", "大兴校区"]:
    #     raise ValueError("终点设置有误")
    if config["出入校起点"] == config["出入校终点"]:
        raise ValueError("起点和终点不能一样")
    if config["起点/终点校门"] not in ["畅春园新门", "东南门", "南门", "西门", "校医院便民通道", "小东门", "东侧门", "东门", "西南门", "燕园大厦门"]:
        raise ValueError("起点/终点校门设置有误")
    if config["出入校事由"] not in ["就业", "就学", "科研", "就医"]:
        raise ValueError("出入校事由设置有误")
    if len(config["出入校具体事项"]) > 200:
        raise ValueError("出入校具体事项过长")
    if config["起点/终点所在区县"] not in ["东城区", "西城区", "朝阳区", "丰台区", "石景山区",
        "海淀区", "顺义区", "通州区", "大兴区", "房山区", "门头沟区", "昌平区", "平谷区", "密云区", "怀柔区", "延庆区"]:
        raise ValueError("起点/终点所在区县设置有误")
    if len(config["起点/终点所在街道"]) > 100:
        raise ValueError("起点/终点所在街道过长")
    if len(config["基本轨迹"]) > 200:
        raise ValueError("基本轨迹过长")
    if len(config["补充说明"]) > 200:
        raise ValueError("补充说明过长")
    if config["证明材料上传"] not in ["导师同意书", "核酸检测证明", "北京健康宝", "通行大数据行程卡", "其他材料"]:
        raise ValueError("证明材料上传设置有误")
    if config["宿舍园区"] not in ["燕园", "万柳园区", "圆明园校区", "畅春园", "中关新园", "大兴校区", "医学部", "昌平校区", "无宿舍"]:
        raise ValueError("宿舍园区设置有误")
    if config["提交"] not in ["是", "否"]:
        raise ValueError("提交设置有误")

def get_driver_path():
    plat_info = platform.platform()
    if plat_info.startswith("Linux"):
        driver_path = "chromedrivers/chromedriver_linux64/chromedriver"
    elif plat_info.startswith("macOS"):
        driver_path = "chromedrivers/chromedriver_mac64/chromedriver"
    elif plat_info.startswith("Windows"):
        driver_path = "chromedrivers/chromedriver_win32/chromedriver.exe"
    else:
        raise Exception(f"不支持平台: {plat_info}")
    return driver_path

if __name__ == "__main__":

    args = make_args()

    configs_path = args.configs

    driver_path = get_driver_path()

    driver = webdriver.WebDriver(executable_path=driver_path)
    # driver.implicitly_wait(60)

    # 逐个填写
    for path in configs_path:
        config = json.load(open(path, "r", encoding="utf-8"))
        config_check(config)
        get_in_page(driver, config)
        write_info(driver, config)
        submit(driver, config)
        get_in_history(driver)
        save_screen_shot(driver)
        logout(driver)
        if config["微信通知key"]:
            wechat_notification(userName = config["学号"], sckey = config["微信通知key"], state = config["state"])
    
    print("完成，感谢您的使用")
