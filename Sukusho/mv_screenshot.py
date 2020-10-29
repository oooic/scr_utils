def mv_screenshot(prefix, dirname, savedirname, jikanwari_path, test=False):
    from datetime import datetime as dtdt
    import re
    from os.path import expanduser
    import os
    import pandas as pd
    import shutil
    import glob
    cvtpath = re.compile(
        prefix + r"[\s\S]*?(\d{4}).(\d\d).(\d\d)[\s\S]*?(\d\d?).(\d\d).(\d\d)")
    re_jikanwari = re.compile(r"(\d\d?):(\d\d)~(\d\d?):(\d\d)")
    savedirname = savedirname.replace("~", expanduser("~"))
    dirname = dirname.replace("~", expanduser("~"))
    jikanwari = pd.read_csv(jikanwari_path, index_col=0)

    def conv_jikanwari(txt):
        jikan = re.search(re_jikanwari, txt).groups()
        jikan = list(map(lambda x: int(x), jikan))
        strt = jikan[0] * 60 + jikan[1]
        end = jikan[2] * 60 + jikan[3]
        return strt, end

    def between(x, start, end):
        return start <= x < end
    jikanwariemb = jikanwari["jigen"].map(conv_jikanwari).to_dict()
    target = jikanwari.isnull()

    def movepath(path):
        flag = re.search(cvtpath, path)
        if flag is not None and len(flag.groups()) == 5:
            date = flag.groups()
            date = list(map(lambda x: int(x), date))
            day = dtdt(*date).strftime("%a")
            dateemb = date[3] * 60 + date[4]
            jigen = None
            for key in jikanwariemb.keys():
                if between(dateemb, *jikanwariemb[key]):
                    jigen = key
                    break
            if jigen is not None and not target.loc[jigen, day]:
                dirpath = os.path.join(savedirname, jikanwari.loc[jigen, day])
                os.makedirs(dirpath, exist_ok=True)
                if not test:
                    shutil.move(path, dirpath)

    def wrapper():
        pathlst = glob.glob(str(os.path.join(dirname, "*")))
        for path in pathlst:
            movepath(path)
    return wrapper


def mv_default(test=False):
    import yaml
    from os.path import expanduser
    import os

    home = expanduser("~")
    base = os.path.join(home, ".myscreenshot")
    with open(os.path.join(base, "settings.yml"), "r") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    cfgmv = cfg["MOVE"]
    jikanwari_path = os.path.join(base, "jikanwari.csv")
    myscr = mv_screenshot(**cfgmv, jikanwari_path=jikanwari_path, test=test)
    myscr()


if __name__ == "__main__":
    mv_default()
