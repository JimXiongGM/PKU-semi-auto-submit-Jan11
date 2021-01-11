# 出入校半自动填写工具

PKU半自动填写出入校申请脚本（极简版），适配2021年01月11日新的报备系统。提交证明材料部分需要手动处理。

版本：beta v0.9 (2021年01月11日)

适用系统：macOS、Linux、Win10

python版本：3.7+

**重要** Chrome版本：87.* （点击 设置--关于chrome 查看版本号）

## 使用方法

1. 安装依赖：`pip install selenium -U`

2. 填写配置文件`config.json`

3. 指定配置文件并运行（支持多个）：`python run_submit.py --configs config-1.json config-2.json`

4. 等待程序暂停，手动选择证明材料并上传，在终端输入`go`继续

5. 检查`screen_shots`文件夹下的截图，确认提交成功

## 特别说明

1. 设置微信通知key的方法，请参考[PKUAutoSubmit](https://github.com/Bruuuuuuce/PKUAutoSubmit)

2. 本repo包含3个系统的chrome驱动，较大。可以到本项目的[码云地址](https://gitee.com/JimXiongGM/pku-semi-auto-submit-jan11)下载

## 更新日志

1. v0.9 2021年01月11日 星期一
- - 完成基础功能。
