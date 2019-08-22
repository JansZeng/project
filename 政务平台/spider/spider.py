# coding=utf-8
# 作者    ： Administrator
# 文件    ：spider.py
# IED    ：PyCharm
# 创建时间 ：2019/8/10 14:07
import os
import sys
import time
import shutil
import pytesseract
import pandas as pd
from PIL import Image
# from aip import AipOcr
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import fateadm_api
from read_phone import Code


def run_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.now()
        print("程序开始时间：{}".format(start_time))
        func(*args, **kwargs)
        end_time = datetime.now()
        print("程序结束时间：{}".format(end_time))
        print("程序执行用时：{}s".format((end_time - start_time)))

    return new_func


class Spider:
    def __init__(self):
        print('**********程序启动中**********')
        # selenium无界面模式
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # keep_alive 设置浏览器连接活跃状态
        # self.driver = webdriver.Chrome(chrome_options=chrome_options, keep_alive=False)
        print('**********程序启动成功**********')
        # 有界面模式
        self.driver = webdriver.Chrome(keep_alive=False)
        # 隐形等待时间
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        # 浏览器窗口最大化
        self.driver.maximize_window()
        # 保存数据
        self.phone = 0
        self.number = 0
        self.rsp = None

    def login(self):
        """登录"""
        count = 1
        while True:
            print('**********账号登录中**********')
            url = 'http://tyrz.gdbs.gov.cn/am/login/initAuth.do?gotoUrl=http%3A%2F%2Ftyrz.gdbs.gov.cn%2Fam%2Foauth2%2Fauthorize%3Fclient_id%3Dszjxgcxt%26service%3DinitService%26scope%3Dall%26redirect_uri%3Dhttps%253A%252F%252Famr.sz.gov.cn%252Fpsout%252Fjsp%252Fgcloud%252Fpubservice%252Fuserstsso%252Fgodeal.jsp%26response_type%3Dcode'
            self.driver.get(url)
            username = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginName')))
            username.clear()
            username.send_keys('wyn16888')
            password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginPwd')))
            password.clear()
            password.send_keys('wyn16888')
            self.get_code_image(True)
            code = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tempValidateCode')))
            spot_code = self.spot_code()
            print('验证码：{}'.format(spot_code))
            code.clear()
            code.send_keys(spot_code)

            enter = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#userLoginBtn')))
            enter.click()

            time.sleep(2)
            try:
                self.driver.find_element_by_xpath('//*[(@id="tempValiCode_msg")]')
                print('验证码输入错误：重试')
                self.spot_code(just_flag=True)
                if count > 2:
                    print('登录失败，联系开发者！！！')
                    exit()
                count += 1
                continue
            except:
                print('登录成功')
                break

    def get_code_image(self, login):
        """
        获取验证码图片
        指定元素 截屏
        selenium 截屏方法
        get_screenshot_as_file() 获取当前window的截图
        save_screenshot() 获取屏幕截图
        :return:
        """
        # 当前浏览器屏幕截图
        self.driver.save_screenshot('./code/button.png')
        if login:
            # 登录页面 定位需要截图的元素
            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#codeIm')))
            # print(element.location)  # 打印元素坐标
            # print(element.size)  # 打印元素大小
            # 构造元素坐标
            left = element.location['x']
            top = element.location['y']
            right = element.location['x'] + element.size['width']
            bottom = element.location['y'] + element.size['height']
        else:
            # 查询页面
            left = 820
            top = 510
            right = 910
            bottom = 545

        # 根据坐标位置拷贝
        im = Image.open('./code/button.png')
        im = im.crop((left, top, right, bottom))
        im.save('./code/code.png')

    def spot_code(self, login=False, just_flag=False, balances=False):
        """
        验证码识别
        balances 查询余额
        :return:
        """
        # 斐斐打码
        count = 1
        while True:
            # 余额查询
            if balances:
                balance = fateadm_api.TestFunc(balances=True)
                if balance < 1000:
                    print('余额不足及时充值：{}'.format(balance))
                elif balance < 100:
                    print('余额严重不足即将不能使用：{}'.format(balance))
                elif balance < 10:
                    print('*' * 30)
                    print('余额不足,请充值：{}'.format(balance))
                    print('*' * 30)
                    sys.exit()
                return print('打码平台余额：{}'.format(balance))
            # 调用退款接口
            if just_flag:
                fateadm_api.TestFunc(just_flag=self.rsp)
                return

            print('打码平台验证码识别中...')
            # 判断登录还是查询
            if login:
                rsp = fateadm_api.TestFunc(pred_type_id='304000001')
            else:
                rsp = fateadm_api.TestFunc()
            if count > 3:
                print('验证码识别失败! 请联系开发者')
                sys.exit()
            if not rsp.pred_rsp.value:
                count += 1
                continue
            # 拷贝验证码图片至新目录
            shutil.copy('./code/code.png', './codes/{}.png'.format(rsp.pred_rsp.value))
            self.rsp = rsp
            print(self.rsp.ret_code, self.rsp.request_id)
            return rsp.pred_rsp.value

    def get_phone(self, pre_name, pre_code, pre_type):
        """获取账号登录状态"""
        count = 1
        while True:
            if count > 3:
                return '暂无数据', '暂无数据'
            # 填写请求信息
            self.driver.get('https://amr.sz.gov.cn/aicmerout/jsp/gcloud/giapout/industry/aicmer/processpage/step_one.jsp?ywType=30')
            num = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#regno')))
            num.send_keys(pre_code)
            name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#entNa')))
            name.send_keys(pre_name)
            # 验证码识别
            self.get_code_image(False)
            code = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#validCode')))
            spot_code = self.spot_code(login=True)
            print('验证码：{}'.format(spot_code))
            code.send_keys(spot_code)
            # code.send_keys(input('123'))
            enter = self.driver.find_elements_by_css_selector('.btn-primary')[0]
            enter.click()

            # 处理弹窗 异常弹窗
            time.sleep(1)
            try:
                error_con = self.driver.find_element_by_xpath('//*[@class="layui-layer layui-layer-dialog  layer-anim"]/div[2]').text
                print('错误信息：{}'.format(error_con))
                if error_con == '验证码填写错误！':
                    # 退款
                    self.spot_code(just_flag=True)
                    count += 1
                    continue
                elif error_con == '验证码失效！':
                    count += 1
                    continue
                elif error_con == '草稿数校验代码异常：Bad Gateway':
                    exit()
                else:
                    return error_con, error_con
            except:
                pass

            # 切换iframe 弹窗
            co = 1
            while True:
                try:
                    ups_iframe = self.driver.find_element_by_css_selector('.layui-layer-content > iframe')
                    self.driver.switch_to.frame(ups_iframe)
                    confirmBtn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#confirmBtn')))
                    confirmBtn.click()
                    break
                except:
                    if co > 3:
                        return '暂无数据', '暂无数据'
                    co += 1
                    continue

            # 提取数据
            print('数据加载中...')
            # time.sleep(5)
            # 切换详细信息 iframe
            detail_iframe = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#formRender')))
            self.driver.switch_to.frame(detail_iframe)
            while True:
                try:
                    if pre_type == '个体工商户':
                        JingYingZhe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="JingYingZhe_GtBg"]/div[1]/div')))
                        JingYingZhe.click()
                        FamilyMem = self.driver.find_element_by_xpath('//*[@id="FamilyMem_Bg"]/div[1]/div')
                        FamilyMem.click()
                        phone, number = self.process_phone(pre_type=1)
                        return phone, number
                    elif pre_type == '有限责任公司分公司':
                        FZRBG = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="FZRBG"]/div')))
                        FZRBG.click()
                        LSQYBG = self.driver.find_element_by_xpath('//*[@id="LSQYBG"]/div')
                        LSQYBG.click()
                        phone, number = self.process_phone(pre_type=2)
                        return phone, number
                    elif pre_type == '有限责任公司':
                        Farendaibiao = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="FaDingDaiBiaoRenXinXi"]/div')))
                        Farendaibiao.click()
                        guquanbiangeng = self.driver.find_element_by_xpath('//*[@id="GQBGHGZS"]/div')
                        guquanbiangeng.click()
                        phone, number = self.process_phone(pre_type=3)
                        return phone, number
                    elif pre_type == '外商投资企业分公司' or pre_type == '台、港、澳投资企业分公司':
                        FuZeRen = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="FuZeRenBianGeng"]/div')))
                        FuZeRen.click()
                        LSQYBG = self.driver.find_element_by_xpath('//*[@id="LSQYBG"]/div')
                        LSQYBG.click()
                        phone, number = self.process_phone(pre_type=4)
                        return phone, number
                    elif pre_type == '有限合伙' or pre_type == '有限合伙企业':
                        ZhiDingLianXiRen = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ZhiDingLianXiRen"]/div')))
                        ZhiDingLianXiRen.click()
                        XuKeXinXi = self.driver.find_element_by_xpath('//*[@id="XuKeXinXi"]/div')
                        XuKeXinXi.click()
                        phone, number = self.process_phone(pre_type=5)
                        return phone, number
                    elif pre_type == '有限责任公司分公司(自然人投资或控股的法人独资)' or pre_type == '其他有限责任公司分公司':
                        FZRBG = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="FZRBG"]/div')))
                        FZRBG.click()
                        LSQYBG = self.driver.find_element_by_xpath('//*[@id="LSQYBG"]/div')
                        LSQYBG.click()
                        phone, number = self.process_phone(pre_type=6)
                        return phone, number
                    elif pre_type == '个人独资企业':
                        FaDingDaiBiaoRenXinXi = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="FaDingDaiBiaoRenXinXi"]/div')))
                        FaDingDaiBiaoRenXinXi.click()
                        FenZhiJiGou = self.driver.find_element_by_xpath('//*[@id="FenZhiJiGou"]/div')
                        FenZhiJiGou.click()
                        phone, number = self.process_phone(pre_type=7)
                        return phone, number
                    else:
                        Farendaibiao = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="FaDingDaiBiaoRenXinXi"]/div')))
                        Farendaibiao.click()
                        guquanbiangeng = self.driver.find_element_by_xpath('//*[@id="GQBGHGZS"]/div')
                        guquanbiangeng.click()
                        phone, number = self.process_phone(pre_type=3)
                        return phone, number
                except:
                    print('获取数据失败：重试')
                    if count >= 2:
                        return '暂无数据', '暂无数据'
                    count += 1
                    continue

    def process_phone(self, pre_type):
        """
        处理手机号图片
        指定元素 截屏
        selenium 截屏方法
        get_screenshot_as_file() 获取当前window的截图
        save_screenshot() 获取屏幕截图
        pre_type: 1=个体工商户
                  2=有限责任公司分公司
                  3=有限责任公司
                  4=外商投资企业分公司
                  5=有限合伙
                  6=有限责任公司分公司(自然人投资或控股的法人独资)
                  7=个人独资企业
        :return:
        """
        # 当前浏览器屏幕截图
        self.driver.save_screenshot('./code/phone_page.png')
        # 根据坐标位置拷贝
        im = Image.open('./code/phone_page.png')
        if pre_type == 1:
            phone_image = im.crop((310, 100, 660, 130))
            number_image = im.crop((935, 175, 1130, 205))
        elif pre_type == 2:
            phone_image = im.crop((310, 205, 440, 235))
            number_image = im.crop((940, 125, 1120, 155))
        elif pre_type == 3:
            phone_image = im.crop((310, 160, 500, 185))
            number_image = im.crop((935, 80, 1130, 110))
        elif pre_type == 4:
            phone_image = im.crop((310, 185, 430, 215))
            number_image = im.crop((940, 115, 1120, 145))
        elif pre_type == 5:
            phone_image = im.crop((935, 270, 1060, 300))
            phone_image.save('./code/phone.png')
            phone_img = Image.open('code/phone.png')
            phone = pytesseract.image_to_string(phone_img)
            return phone, 0
        elif pre_type == 6:
            phone_image = im.crop((310, 210, 460, 240))
            number_image = im.crop((940, 130, 1140, 160))
        elif pre_type == 7:
            phone_image = im.crop((310, 205, 430, 235))
            number_image = im.crop((935, 125, 1110, 155))

        phone_image.save('./code/phone.png')
        number_image.save('./code/number.png')
        # print('成功获取手机号图片')
        phone_img = Image.open('code/phone.png')
        number_img = Image.open('code/number.png')
        # 识别图片
        phone = pytesseract.image_to_string(phone_img)
        number = pytesseract.image_to_string(number_img)
        # print('成功获取手机号：{}'.format(phone))
        # print('成功获取身份证号：{}'.format(number))
        return phone, number

    def read_xls(self, filename):
        """
        读取 XLS表格数据
        :return:
        """
        # 加载数据
        df_read = pd.read_excel(filename)
        df = pd.DataFrame(df_read)
        # 获取指定表头的列数
        phone_num = 0  # 电话列
        name_num = 0  # 企业名称列
        code_num = 0  # 统一社会信用代码列
        type_num = 0  # 企业类型列
        user_num = 0  # 身份证号码
        for i in range(len(df.keys())):
            if df.keys()[i] == '电话':
                phone_num = i
            elif df.keys()[i] == '企业名称':
                name_num = i
            elif df.keys()[i] == '统一社会信用代码':
                code_num = i
            elif df.keys()[i] == '企业类型':
                type_num = i
            elif df.keys()[i] == '更多电话':
                user_num = i
        # 循环每一行
        for indexs in df.index:
            #  fillna(0)将该列nan值修改为0 方便后续判断
            df.ix[indexs] = df.ix[indexs].fillna(0)
            # 读取指定行列数据 df.ix[行,列]
            data1 = df.ix[indexs, phone_num]
            # 修改指定单元格数据df.iloc[行, 列]
            if data1:
                continue

            # 获取企业信息 查询用
            pre_name = df.ix[indexs, name_num]
            pre_code = df.ix[indexs, code_num]
            pre_type = df.ix[indexs, type_num]
            yield (indexs, pre_name, pre_code, pre_type)
            df.iloc[indexs, phone_num] = self.phone  # 电话
            df.iloc[indexs, user_num] = self.number  # 身份证号
            # 查询一条保存一条 sheet_name工作表名 index是否添加索引 header表头
            df.to_excel(filename, sheet_name='data', index=False, header=True)
            # 备份
            shutil.copy(filename, '备份数据.xlsx')

    @run_time
    def run(self, filename):
        self.login()
        print('**********读取数据文件**********')
        print(filename)
        datas = self.read_xls(filename=filename)
        for indexs, pre_name, pre_code, pre_type in datas:
            print('*' * 20, '第:', indexs, '条数据获取中', '*' * 20)
            print(indexs, pre_name, pre_code, pre_type)
            # 获取信息提取手机号
            self.phone, self.number = self.get_phone(pre_name, pre_code, pre_type)
            print('{} {} {} 数据写入成功'.format(pre_name, self.phone, self.number))
            print('*' * 60, '\n')

        # 查询打码平台余额
        self.spot_code(balances=True)
        # 移动已处理完文件
        shutil.move(filename, '完成/')


if __name__ == '__main__':
    path = os.getcwd()
    files = os.listdir(path)
    files = [i for i in files if '.xlsx' in i if '备份数据' not in i]
    print(files)
    for i in files:
        filename = i
        count = 1
        while True:
            try:
                spider = Spider()
                spider.run(filename)
                break
            except:
                if count >= 50:
                    print('程序异常退出')
                    break
                count += 1
                continue
