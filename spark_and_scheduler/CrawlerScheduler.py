#-*- codeing = utf-8 -*-
#@Time : 2024/4/11 22:31
#@Author : ZZJ
#@File : CrawlerScheduler.py.py
#@Software : PyCharm

import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler

def run_spider(script_path):
    # 启动爬虫脚本作为一个新的进程
    return subprocess.Popen(["python", script_path])

def process_data():
    # 在所有爬虫脚本完成后运行位于 code 文件夹下的 spark.py 来处理数据
    subprocess.run(["python", "code/spark.py"])

def run_all_spiders():
    # 定义位于 code 文件夹下的爬虫脚本的相对路径
    spiders = [
        "code/spider1.py",
        "code/spider2.py"
    ]

    # 存储所有运行中的爬虫进程
    processes = []

    # 同时启动所有爬虫脚本作为独立的进程
    for script in spiders:
        proc = run_spider(script)
        processes.append(proc)

    # 等待所有爬虫脚本完成
    for proc in processes:
        proc.communicate()

    # 所有爬虫完成后，处理数据
    process_data()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # 安排 run_all_spiders 函数立即运行
    # scheduler.add_job(run_all_spiders, 'date')
    # 安排调度器每天凌晨1点执行 run_all_spiders 函数
    scheduler.add_job(run_all_spiders, 'cron', hour=1)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass