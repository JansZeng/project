"""
需求：
1、根目录下通过后缀文.sln的文件名如：PROTOCOL.sln，定位到名称为PROTOCOL的目录

2、在PROTOCOL目录中查找所有后缀为.c  .h文件的头文件（如：#include "..\interface\protocol_define.h"），将正斜杠‘\’全部改反斜杠‘/’。

3、处理PROTOCOL/interface/protocol_interface.h文件，如果有#ifdef WIN32这行，把这行删除。

4、将所有后缀为.c  .h文件转换为utf-8编码。
"""

import os


PATH = os.getcwd()
print(PATH)


def locate_file():
    """第一步：根目录下通过后缀文.sln的文件名如：PROTOCOL.sln，定位到名称为PROTOCOL的目录"""
    lis = []
    for root, dirs, files in os.walk(PATH):
        for file in files:
            if os.path.splitext(file)[1] == '.sln':
                lis.append(os.path.join(root, os.path.splitext(file)[0]))
    return lis


def modify_header(lis):
    """第二步：在PROTOCOL目录中查找所有后缀为.c  .h文件的头文件（如：#include "..\interface\protocol_define.h"），将正斜杠‘\’全部改反斜杠‘/’。"""
    for li in lis:
        for root, dirs, files in os.walk(li):
            for file in files:
                if os.path.splitext(file)[1] == '.c' or os.path.splitext(file)[1] == '.h':
                    file_name = os.path.join(root, file)
                    content = []
                    try:
                        for line in open(file_name, 'r', encoding='gb2312'):
                            # 第三步：处理PROTOCOL/interface/protocol_interface.h文件，如果有#ifdef WIN32这行，把这行删除。
                            if '#ifdef WIN32' in line and 'interface/protocol_interface.h' in file_name:
                                continue
                            if '#include' in line:
                                content.append(line.replace('\\', '/'))
                                continue
                            content.append(line)
                    except UnicodeDecodeError:
                        for line in open(file_name, 'r', encoding='utf-8'):
                            # 第三步：处理PROTOCOL/interface/protocol_interface.h文件，如果有#ifdef WIN32这行，把这行删除。
                            if '#ifdef WIN32' in line and 'interface/protocol_interface.h' in file_name:
                                continue
                            if '#include' in line:
                                content.append(line.replace('\\', '/'))
                                continue
                            content.append(line)
                    with open(file_name, 'w+', encoding='utf-8') as f:
                        for data in content:
                            f.write(data)
                    print(f'{file_name} 处理完成！')


if __name__ == '__main__':
    lis = locate_file()
    modify_header(lis=lis)
