#!/usr/bin/python3
import os
import sys
from .app import App


def main():
    print("Scan Image WEB UI")
    print("Use command {} APP_PORT".format(sys.argv[0]))

    scan_folder_path = "{}/static/img/scan".format(os.path.dirname(__file__))
    app = App()
    app.init(scan_folder_path=scan_folder_path, port=7800)
    app.run()


if __name__ == '__main__':
    main()
