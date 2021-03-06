import os
import jenkins
import json
import urllib3

name = "FACADE"
name_branch = "FACADE_WAIBU_54"
# jenkins登录地址
jenkins_url = "http://192.168.1.106:8888/"
# 获取jenkins对象
server = jenkins.Jenkins(jenkins_url, username='niurunpeng', password='121476')
# job名称
job_name = "job/" + name + "/"
# 获取最后一次构建
job_last_build_url = server.get_info(job_name)['lastBuild']['url']
# job的url地址
# job_url = jenkins_url + job_name
job_url = job_last_build_url + "console"
# 报告地址
report_url = job_last_build_url + 'allure'
'''
钉钉推送方法：
读取report文件中"prometheusData.txt"，循环遍历获取需要的值。
使用钉钉机器人的接口，拼接后推送text
'''


def DingTalkSend():
    d = {}
    # 获取项目绝对路径
    path = os.path.abspath(os.path.dirname((__file__)))
    # 打开prometheusData 获取需要发送的信息
    f = open(path + '/report/export/prometheusData.txt')
    for lines in f:
        for c in lines:
            launch_name = lines.strip('\n').split(' ')[0]
            num = lines.strip('\n').split(' ')[1]
            d.update({launch_name: num})
    print(d)
    f.close()
    retries_run = d.get('launch_retries_run')  # 运行总数
    status_passed = d.get('launch_status_passed')  # 通过数量
    percent_passed = str(int(int(status_passed) / int(retries_run) * 100)) + "%"
    status_broken = d.get('launch_status_broken')  # 中断数量
    status_skipped = d.get('launch_status_skipped')  # 跳过数量
    status_unknown = d.get('launch_status_unknown')  # 未知错误数量
    status_retries = d.get('launch_retries_retries')  # 重试次数
    status_failed = d.get('launch_status_failed')  # 不通过数量
    print('运行总数:{}'.format(retries_run))
    print('通过数量：{}'.format(status_passed))
    print('失败数量：{}'.format(status_failed))
    print('中断数量:{}'.format(status_broken))
    print('跳过数量:{}'.format(status_skipped))
    print('未知错误数量:{}'.format(status_unknown))
    print('重试次数:{}'.format(status_retries))
    if (int(status_failed) > 0):
        result = "测试不通过"
        result_color = "warning"
    else:
        result = "测试通过"
        result_color = "info"
    # 企业微信推送

    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=30563df1-59d1-4c07-8c61-cdcbffe2030e'  # webhook
    con = {"msgtype": "markdown",
           "markdown": {
               "content": "<@niurunpeng>\n**" + name_branch + "\n**<font color =\"" + result_color + "\">  **" + result +
                          "**</font>\n >用例总数: <font color =\"info\">" + retries_run +
                          "  </font> 成功比例: <font color =\"info\">" + percent_passed +
                          "</font> \n>通过数量: <font color =\"info\">" + status_passed +
                          "  </font> 失败数量: <font color =\"warning\">" + status_failed +
                          "</font> \n>跳过数量: <font color =\"warning\">" + status_skipped +
                          "  </font> 未知错误: <font color =\"warning\">" + status_unknown +
                          "</font> \n>中断数量: <font color =\"warning\">" + status_broken +
                          "  </font> 重试次数: <font color =\"warning\">" + status_retries +
                          "</font> \n[控制台输出](" + job_url + ")    [查看测试报告](" + report_url + ")",
           }
           }
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    jd = json.dumps(con)
    jd = bytes(jd, 'utf-8')
    http.request('POST', url, body=jd, headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    DingTalkSend()
