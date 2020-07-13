#!/usr/bin/python3
import os
import sys
from .app import App


def main():
    print("Scan Image WEB UI")
    print("=================")
    print("Use command {} APP_PORT".format(sys.argv[0]))

    scan_folder_path = "{}/static/img/scan".format(os.path.dirname(__file__))
    if not os.path.exists(scan_folder_path):
        os.makedirs(scan_folder_path, exist_ok=True)
    print("Images will scaned into folder: '{}'".format(scan_folder_path))
    print("")
    app = App()
    app.init(scan_folder_path=scan_folder_path, port=7800)
    app.run()


if __name__ == '__main__':
    main()
