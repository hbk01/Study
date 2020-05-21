#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "hbk"
__email__ = "3243430237@qq.com"
__github__ = "https://github.com/hbk01/Study"
__gitee__ = "https://gitee.com/hbk01/Study"

import os
from collections import OrderedDict


def main():
    directory = os.path.abspath(".") + os.path.sep
    src = [
        "非处方药营销与应用.md",
        "药学文献检索.md",
        "药学综合知识与技能.md",
        "医药商品经营与管理.md",
        "中药炮制技术.md",
        "计算机二级基础.md"
    ]
    temp = "temp.md"
    out = "目录.md"
    try:
        os.remove(directory + out)
    except IOError:
        pass
    print("-------------------------------")
    for index, i in enumerate(src):
        print("Generator [%d/%d] %s ..." % (index + 1, len(src), i))
        generate(directory + i, directory + temp)
        with open(directory + temp, "r", encoding="utf-8") as t, open(directory + out, "a", encoding="utf-8") as f:
            f.writelines(t.readlines())
    os.remove(directory + temp)
    print("-------------------------------")
    os.system("git status")
    print("-------------------------------")
    select = input("Push to github and gitee? (y/n)")
    if select == "y":
        msg = input("Commit Message: ")
        print("-------------------------------")
        os.system("git add .")
        os.system("git commit -m %s" % msg)
        print("-------------------------------")
        os.system("git push gitee")
        print("-------------------------------")
        os.system("git push github")


def generate(path, out, depth=4):
    index = OrderedDict()
    with open(path, "r", encoding="utf-8") as f:
        lines = []
        i = 0

        # get starts of '#' contents
        for line in f.readlines():
            if line.startswith("#"):
                lines.append(line[0:len(line) - 1])

        for line in lines:
            title_level = len(line[0:line.find(" ")])
            title = line[title_level + 1:]
            index[i] = title + "@" + str(title_level)
            i += 1

    with open(out, "w", encoding="utf-8") as f:
        filename = os.path.split(path)[1]
        # write file to title
        f.write("# " + filename[:len(filename) - 3])
        f.write(os.linesep)
        # it's white space number on start
        tab = 3 * " "
        # in this list, the value need clear repeat
        repeat = []
        for key in index.keys():
            value = index.get(key).split("@")
            link_title = clean_link(value[0])
            link = "[%s](%s#%s)" % (value[0], filename, link_title)
            # append to list, it's looks like "   * [title](filename.md#link)"
            repeat.append((int(value[1])) * tab + "* " + link)

        need_rename = []
        for i in repeat:
            need_rename.append(i[i.find("#") + 1:len(i) - 1])

        renamed = rename_list(need_rename)
        for i, value in enumerate(repeat):
            repeat[i] = value[:value.find("#")] + "#" + renamed[i] + ")"

        for link in repeat:
            title_level = len(link[:link.find(" ")])
            if int(title_level) < depth:
                f.write(link)
                # fix: Linux and Windows line separator inconsistency bug.
                if os.name == "nt":
                    f.write("\r")
                else:
                    f.write(os.linesep)


def rename_list(rename):
    result = []
    for i, v in enumerate(rename):
        if rename.count(v) > 1:
            # has repeat item.
            if rename[:i].count(v) == 0:
                result.append(v)
            else:
                result.append(v + "-" + str(rename[:i].count(v)))
        else:
            result.append(v)
    return result


def clean_link(string):
    result = string.replace(" ", "-").lower()
    clear = [
        "（", "）", "、", "/", ".", "？", "。"
    ]
    for c in clear:
        result = result.replace(c, "")
    return result


if __name__ == "__main__":
    # print("hello")
    # print("world")
    # print(os.name)
    main()
    pass
