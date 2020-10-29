import pandas as pd
from datetime import datetime as dtdt
from os.path import expanduser
import os
import yaml
import subprocess


def reset_jikanwari():
    jigen = {
        1: "08:30~10:25",
        2: "10:25~12:10",
        3: "13:00~14:55",
        4: "14:55~16:50",
        5: "16:50~18:45",
        6: "18:45~20:30",
    }
    jigen = pd.DataFrame(jigen, index=["jigen"]).T
    dirname = []
    for i in range(22, 29):
        dirname.append(dtdt(*[2020, 6, i]).strftime("%a"))
    jikanwari = [[d + str(i) for d in dirname]for i in range(1, 7)]
    jikanwari = pd.DataFrame(
        jikanwari,
        columns=dirname,
        index=[i for i in range(1, 7)])
    home = expanduser("~")
    base = os.path.join(home, ".myscreenshot")
    os.makedirs(base, exist_ok=True)
    jikanwari_path = os.path.join(base, "jikanwari.csv")
    pd.concat([jigen, jikanwari], axis=1).to_csv(jikanwari_path)


def reset_settings():
    home = expanduser("~")
    base = os.path.join(home, ".myscreenshot")
    setting_path = os.path.join(base, "settings.yml")
    res = subprocess.run(
        "defaults read com.apple.screencapture location",
        shell=True,
        stdout=subprocess.PIPE)
    if res.returncode == 0:
        dirname = res.stdout[:-1].decode()
    else:
        dirname = "~/Desktop"
    res = subprocess.run(
        "defaults read com.apple.screencapture name",
        shell=True,
        stdout=subprocess.PIPE)
    if res.returncode == 0:
        prefix = res.stdout[:-1].decode()
    else:
        prefix = "スクリーンショット"
    with open(setting_path, "w") as yf:
        yaml.dump({
            "MOVE": {
                "prefix": prefix,
                "dirname": dirname,
                "savedirname": "~/Desktop"

            }
        }, yf, default_flow_style=False)


def change_jikanwari():
    home = expanduser("~")
    base = os.path.join(home, ".myscreenshot")
    jikanwari_path = os.path.join(base, "jikanwari.csv")
    res = subprocess.run(f"open {jikanwari_path} -a 'Microsoft Excel'",
                         shell=True)
    if res.returncode != 0:
        res = subprocess.run(f"open {jikanwari_path}", shell=True)


def change_savedir():
    home = expanduser("~")
    base = os.path.join(home, ".myscreenshot")
    with open(os.path.join(base, "settings.yml"), "r") as f:
        cfgold = yaml.load(f, Loader=yaml.FullLoader)
    reset_settings()
    setting_path = os.path.join(base, "settings.yml")
    with open(os.path.join(base, "settings.yml"), "r") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    savedirname = input(
        f"[now:{cfg['MOVE']['savedirname']}]/press enter or input savedir path")
    if savedirname == "":
        cfg["MOVE"]["savedirname"] = cfgold["MOVE"]["savedirname"]
    elif os.path.isdir(savedirname):
        cfg["MOVE"]["savedirname"] = savedirname
    else:
        flg = "No"
        while True:
            flg = input(f"create {savedirname}:Yes/[No]")
            if flg == "Yes" or flg == "No":
                break
            else:
                print("invalid input;type Yes or No")
        if flg == "Yes":
            os.makedirs(savedirname)
            cfg["MOVE"]["savedirname"] = savedirname
        else:
            cfg["MOVE"]["savedirname"] = cfgold["MOVE"]["savedirname"]
    with open(setting_path, "w") as yf:
        yaml.dump(
            cfg,
            yf,
            default_flow_style=False
        )


def init():
    reset_jikanwari()
    reset_settings()
    change_savedir()
    change_jikanwari()
