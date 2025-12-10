import json
from flask import Flask, render_template, request, send_from_directory
from .libs.scanner import Scanner
from typing import Optional, Any
from datetime import datetime


class WebUI:
    PORT = 5000
    SCAN_FOLDER = ""
    app = Flask(__name__)
    scanner: Optional[Scanner] = None

    @classmethod
    def init(cls, scan_folder_path: str, version: str, port: int = 5000):
        cls.PORT = port
        cls.SCAN_FOLDER = scan_folder_path
        cls.VERSION = version
        cls.scanner = Scanner(cls.SCAN_FOLDER)
        print("Serving app at port: {}".format(port))

    @classmethod
    def run(cls):
        cls.app.run(host="0.0.0.0", port=cls.PORT)

    @staticmethod
    @app.route("/")
    def index() -> Flask.response_class:
        return render_template("index.html", data={"version": WebUI.VERSION})

    @staticmethod
    @app.route("/scanimage/<path:filename>")
    def serve_scanimage_folder(filename: str):
        return send_from_directory(WebUI.SCAN_FOLDER, filename, as_attachment=True)

    @staticmethod
    @app.route("/api/scanStatus")
    def scan_status() -> Flask.response_class:
        if not WebUI.scanner:
            return WebUI.response500("Scanner not initialized")
        ret = WebUI.scanner.get_scan_status()
        if ret:
            return WebUI.response_json(ret)
        return WebUI.response500("Error getting scanner status")

    @staticmethod
    @app.route("/api/initScanner")
    def init_scanner():
        if not WebUI.scanner:
            return WebUI.response500("Scanner not initialized")
        ret = WebUI.scanner.init_scanner_device()
        if ret:
            return WebUI.response_json(ret)
        return WebUI.response500("Error getting scanner status")

    @staticmethod
    @app.route("/api/scanImage", methods=["GET"])
    def scan_image() -> Flask.response_class:
        """
        GET PARAMS:
        str format: jpg, png, tif
        str mode: Color, Gray, Lineart
        int resolution: 96, 200, 300, 600
        :return: { result: true/
        """
        if not WebUI.scanner:
            return WebUI.response500("Scanner not initialized")
        args = request.args
        format_ = args.get("format", "jpg")
        params = {
            "mode": args.get("mode", "Color"),
            "format": args.get("format", "jpg"),
            "resolution": args.get("resolution", "300"),
            "gamma": args.get("gamma", "2.2"),
        }
        base_filename = "scan-{}".format(datetime.now().strftime("%Y%m%d-%H%M%S"))
        filename = "{}.{}".format(base_filename, format_)
        result = WebUI.scanner.scan_image(filename, params)
        ret = {"result": result, "filename": filename}
        return WebUI.response_json(ret)

    @staticmethod
    @app.route("/api/scanPreview", methods=["GET"])
    def scan_preview() -> Flask.response_class:
        if not WebUI.scanner:
            return WebUI.response500("Scanner not initialized")
        args = request.args
        filename = "scan-preview.jpeg"
        params = {
            "mode": "Color",
            "format": "jpeg",
            "resolution": "75",
            "gamma": args.get("gamma", "2.2"),
        }
        result = WebUI.scanner.scan_image(filename, params)
        ret = {"result": result, "filename": filename}
        return WebUI.response_json(ret)

    @staticmethod
    @app.route("/api/getPreviewImage", methods=["GET"])
    def get_preview_image() -> Flask.response_class:
        if not WebUI.scanner:
            return WebUI.response500("Scanner not initialized")
        return WebUI.response_json(
            {"filename": WebUI.scanner.get_preview_file_path("scan-preview.jpeg")}
        )

    @staticmethod
    @app.route("/api/listImages", methods=["GET"])
    def list_images() -> Flask.response_class:
        if not WebUI.scanner:
            return WebUI.response500("Scanner not initialized")
        return WebUI.response_json(WebUI.scanner.get_file_list())

    @staticmethod
    @app.route("/api/deleteImage", methods=["GET"])
    def delete_image() -> Flask.response_class:
        """
        Avaliable GET args:
        str: filename - * delete all
        :return:
        """
        args = request.args
        filename = args.get("filename")
        if not WebUI.scanner:
            return WebUI.response500("Scanner not initialized")
        if filename:
            deleted = WebUI.scanner.delete_file(filename)
            return WebUI.response_json({"removed": deleted})
        return WebUI.response404()

    @staticmethod
    @app.route("/api/cropImage", methods=["GET"])
    def crop_image():
        if not WebUI.scanner:
            return WebUI.response500("Scanner not initialized")

        args = request.args
        filename = args.get("filename")
        if not filename:
            return WebUI.response404()

        try:
            x1 = int(args.get("x1", "0"))
            y1 = int(args.get("y1", "0"))
            x2 = int(args.get("x2", "0"))
            y2 = int(args.get("y2", "0"))
        except (TypeError, ValueError):
            return WebUI.response500("Invalid crop coordinates")

        result = WebUI.scanner.crop_image(filename, x1, y1, x2, y2)
        return WebUI.response_json({"result": result})

    @staticmethod
    @app.route("/api/rotateImage", methods=["GET"])
    def rotate_image():
        if not WebUI.scanner:
            return WebUI.response500("Scanner not initialized")

        args = request.args
        filename = args.get("filename")
        if not filename:
            return WebUI.response404()

        try:
            angle = int(args.get("angle", 0))
        except (TypeError, ValueError):
            return WebUI.response500("Invalid angle")

        result = WebUI.scanner.rotate_image(filename, angle)
        return WebUI.response_json({"result": result})

    @classmethod
    def response_json(cls, data: Any) -> Flask.response_class:
        if data is None:
            return cls.response404()
        # normalize string payloads into a JSON object with a message field
        payload = {"message": data} if isinstance(data, str) else data
        response = WebUI.app.response_class(
            response=json.dumps(payload), status=200, mimetype="application/json"
        )
        return response

    @classmethod
    def response404(cls):
        response = cls.app.response_class(
            response={"message": "No data for your request"},
            status=404,
            mimetype="application/json",
        )
        return response

    @classmethod
    def response500(cls, message: str = ""):
        response = cls.app.response_class(
            response={"message": message}, status=500, mimetype="application/json"
        )
        return response
