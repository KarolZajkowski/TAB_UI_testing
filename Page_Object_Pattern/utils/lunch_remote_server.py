#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import time
import subprocess

"""" Karol Zajkowski """


class Main(object):

    def __init__(self):
        self.hub_port = 4444
        self._this_host_ip = 'localhost'
        super(Main, self).__init__()

    @property
    def this_host_ip(self):
        return self._this_host_ip

    @this_host_ip.setter
    def this_host_ip(self, other):
        self._this_host_ip = other

    def get_ip(self):
        IPv4 = []
        proces = self.command_output("ipconfig")

        for line in iter(proces.stdout.readline, b''):
            line = str(line.decode(encoding='utf-8', errors='replace'))

            formatedLine = re.search(r"IPv4 Address. . . . . . . . . . . :\D(\d+).(\d+).(\d+).(\d+)", line)

            if formatedLine is not None:
                # print(formatedLine)
                tupleInt = re.findall(r'(\d+).(\d+).(\d+).(\d+)', formatedLine.group())
                for intiger in tupleInt:
                    IPv4.append('.'.join(intiger))
        print(IPv4)
        return IPv4[-1]

    @staticmethod
    def command_output(command):
        return subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                stdin=subprocess.PIPE, )

    @staticmethod
    def run_terminal(command):
        p = subprocess.Popen(["start", "cmd", "/k", command],
                             shell=True)
        p.wait()

    def main(self):
        """ this function just run server (HUB) and nodes
        :param this_host_ip (localhost) can be changed
        :param get_ip return IPv4 Address
        """
        # self.this_host_ip = self.get_ip()
        # print(self.this_host_ip)
        actual_path = os.path.dirname(os.path.abspath(__file__))
        environment_path = actual_path + '\..\..\environment'

        self.run_terminal(
            f"java -jar {environment_path}\selenium-server-standalone-3.141.59.jar -role hub -port {self.hub_port}")
        time.sleep(10)

        self.run_terminal(
            f"java -Dwebdriver.gecko.driver={environment_path}\geckodriver.exe -jar {environment_path}\selenium"
            f"-server-standalone-3.141.59.jar -role node  -hub http://{self.this_host_ip}:"
            f"{self.hub_port}/grid/register -port 5558 -browser browserName=firefox -browser maxInstances=5".encode())

        time.sleep(15)
        self.run_terminal(
            f"java -Dwebdriver.chrome.driver={environment_path}\chromedriver.exe -jar {environment_path}\selenium"
            f"-server-standalone-3.141.59.jar -role node  -hub http://{self.this_host_ip}:"
            f"{self.hub_port}/grid/register -port 5556 -browser browserName=chrome -browser maxInstances=5".encode())

        time.sleep(15)


if __name__ == '__main__':
    underTest = Main()
    underTest.main()
