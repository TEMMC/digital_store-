"""Start the bundled Flask marketplace on the Android device loopback interface."""
import importlib.util
import os
import threading
from werkzeug.serving import make_server

_server = None
_thread = None
_lock = threading.Lock()

def start(marketplace_dir, database_path, upload_dir, secret_key):
    global _server, _thread
    with _lock:
        if _server is not None:
            return "already-running"

        os.makedirs(marketplace_dir, exist_ok=True)
        os.makedirs(upload_dir, exist_ok=True)
        os.environ["DATABASE_URL"] = "sqlite:///" + os.path.abspath(database_path)
        os.environ["UPLOAD_FOLDER"] = os.path.abspath(upload_dir)
        os.environ["SECRET_KEY"] = secret_key
        os.chdir(marketplace_dir)

        app_path = os.path.join(marketplace_dir, "app.py")
        spec = importlib.util.spec_from_file_location("mt_marketplace_app", app_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        _server = make_server("127.0.0.1", 8765, module.app, threaded=True)
        _thread = threading.Thread(target=_server.serve_forever, name="MTMarketplaceServer", daemon=True)
        _thread.start()
        return "started"
