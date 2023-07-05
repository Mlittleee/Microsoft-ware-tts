# @Time: 2023/7/3 10:23
# @Auther: MHC
# @File: mytts.py
# @Description:根据传入的字符串来修改xml文件

import xml.etree.ElementTree as ET
import subprocess
import sys


def change_xml(text):
    tree = ET.parse('D:/MHC/pycharm/Microsoft-ware-tts/tts/python_cli_demo/SSML.xml')
    root = tree.getroot()
    # 找到要修改的元素
    # 找到 <prosody> 元素
    namespace = {'speak': 'http://www.w3.org/2001/10/synthesis'}
    prosody_element = root.find('.//speak:prosody', namespace)


    # 修改元素的文本内容
    #print(prosody_element.text)
    prosody_element.text = text

    # 保存修改后的XML文件
    tree.write('D:/MHC/pycharm/Microsoft-ware-tts/tts/python_cli_demo/SSML.xml', encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    # 传入的参数
    text = sys.argv[1]
    change_xml(text)

    subprocess.call('python D:/MHC/pycharm/Microsoft-ware-tts/tts/python_cli_demo/tts.py --input '
                    'D:/MHC/pycharm/Microsoft-ware-tts/tts/python_cli_demo/SSML.xml', shell=True)

