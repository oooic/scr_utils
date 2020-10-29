def mv_screenshot(jikanwari_path, prefix, dirname):
    from datetime import datetime as dtdt
    import re
    from os.path import expanduser
    import os
    import pandas as pd
    import shutil
    import glob
    home = expanduser("~")
    cvtpath = re.compile(
        prefix + r"[\s\S]*?(\d{4}).(\d\d).(\d\d)[\s\S]*?(\d\d?).(\d\d).\d\d")
    re_jikanwari = re.compile(r"(\d\d?):(\d\d)~(\d\d?):(\d\d)")
    namepath = re.compile(
        prefix + r"[\s\S]*?(\d{4}.\d\d.\d\d[\s\S]*?\d\d?.\d\d.\d\d\..*)")
    jikanwari = pd.read_csv(jikanwari_path, index_col=0)
    dirname = dirname.replace("~", home)

    def conv_jikanwari(txt):
        jikan = re.search(re_jikanwari, txt).groups()
        jikan = list(map(lambda x: int(x), jikan))
        strt = jikan[0] * 60 + jikan[1]
        end = jikan[2] * 60 + jikan[3]
        return strt, end

    def between(x, start, end):
        return start < x < end
    jikanwariemb = jikanwari["jigen"].map(conv_jikanwari).to_dict()

    def movepath(path):
        flag = re.search(cvtpath, path)
        if flag is not None and len(flag.groups()) == 5:
            date = flag.groups()
            date = list(map(lambda x: int(x), date))
            day = dtdt(*date).strftime("%a")
            dateemb = date[3] * 60 + date[4]
            for key in jikanwariemb.keys():
                if between(dateemb, *jikanwariemb[key]):
                    jigen = key
                    break
            lesson = jikanwari.loc[jigen, day]
            if lesson != pd.NA:
                dirpath = os.path.join(dirname, jikanwari.loc[jigen, day])
                filename = re.search(namepath, path).groups()[0]
                os.makedirs(dirpath, exist_ok=True)
                shutil.move(path, os.path.join(dirpath, filename))

    def wrapper():
        pathlst = glob.glob(os.path.join(dirname, "*"))
        for path in pathlst:
            movepath(path)
    return wrapper


if __name__ == "__main__":
    import yaml
    PATH_TO_BIN = "../"
    with open(PATH_TO_BIN + "config/settings.yml", "r") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)["DEFAULT"]
    cfg["jikanwari_path"] = PATH_TO_BIN + cfg["jikanwari_path"]
    myscr = mv_screenshot(**cfg)
    myscr()
