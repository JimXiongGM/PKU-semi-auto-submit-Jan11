# 出入校半自动填写工具

PKU半自动填写出入校申请脚本（极简版），适配2021年01月11日新的报备系统。提交证明材料部分需要手动处理。

版本：beta v0.9.3

适用系统：macOS、Linux、Win10

python版本：3.7+

**重要** Chrome版本：88.* （点击 设置--关于chrome 查看版本号）

## 使用方法

1. 安装依赖：`pip install selenium -U`

2. 填写配置文件`config.json`

3. 指定配置文件并运行（支持多个）：`python run_submit.py --configs config-1.json config-2.json`

4. 等待程序暂停，手动选择证明材料并上传，在终端输入`go`继续

5. 检查`screen_shots`文件夹下的截图，确认提交成功

**推荐用法**：将`程序暂停`字段设置为`否`，程序将自动填写保存除证明材料之外的字段，不会暂停、不会提交。之后需自行上传证明材料并提交。

## 特别说明

1. 设置`微信通知key`的方法，请参考[PKUAutoSubmit](https://github.com/Bruuuuuuce/PKUAutoSubmit)

2. 本repo包含3个系统的chrome驱动，较大。若太慢可到对应的[码云仓库](https://gitee.com/JimXiongGM/pku-semi-auto-submit-jan11)下载

3. 测试阶段，建议将`提交`字段设置为`否`，防止填写错误

## 字段取值

config文件的字段合理取值为：

```python
config["出入校起点"] = "校外" # 燕园 校外 ... 请自行确认字段无误
config["出入校终点"] = "燕园" # 燕园 校外 ... 请自行确认字段无误
config["起点/终点校门"] = "西南门" # ["畅春园新门", "东南门", "南门", "西门", "校医院便民通道", "小东门", "东侧门", "东门", "西南门", "燕园大厦门"]
config["出入校事由"] = "科研" # ["就业", "就学", "科研", "就医"]
config["出入校具体事项"] = "递交材料、食堂就餐" # 200字
# config["起点/终点所在国家地区"] = "中国" # 不支持修改
# config["起点/终点所在省"] = "北京市" # 不支持修改
# config["起点/终点所在地级市"] = "市辖区" # 不支持修改
config["起点/终点所在区县"] = "海淀区" # ["东城区", "西城区", "朝阳区", "丰台区", "石景山区", "海淀区", "顺义区", "通州区", "大兴区", "房山区", "门头沟区", "昌平区", "平谷区", "密云区", "怀柔区", "延庆区"]
config["起点/终点所在街道"] = "海淀街道" # 100字
config["基本轨迹"] = "西南门进，到新太阳交材料，食堂就餐，西南门出" # 200字
config["补充说明"] = "暂无" # 200字
config["证明材料上传"] = "北京健康宝" # 若要增加多个材料，需要手动增加
config["邮箱"] = "123@qq.com"
config["手机号"] = "123"
config["宿舍园区"] = "燕园" # ["燕园", "万柳园区", "圆明园校区", "畅春园", "中关新园", "大兴校区", "医学部", "昌平校区", "无宿舍"]
config["宿舍楼"] = "29号"
config["宿舍房间号"] = "123"
config["程序暂停"] = "否" # 是 否
config["提交"] = "否" # 是 否
config["微信通知key"] = ""
```


## 更新日志

1. v0.9 2021年01月11日 星期一
- 完成基础功能。

2. v0.9.1 2021年01月13日 星期二
- 出入校起点/终点取消约束（不同学生选项不一样）。

3. v0.9.2 2021年01月14日 星期四
- 修正提交逻辑。

4. v0.9.3 2021年01月16日 星期六
- 适配15号的新页面，重写所有的填写逻辑