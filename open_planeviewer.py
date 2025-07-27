import os
from src.a00_data_toolbox.file_toolbox import create_path
from src.a22_plan_viewer.planview_server import planviewer
from src.a22_plan_viewer.test._util.a22_env import module_dir
import threading
import time
import webbrowser


def run_planview_server_flask():
    planviewer.run(debug=False, port=5000, use_reloader=False)


if __name__ == "__main__":

    html_file_path = os.path.abspath(f"{module_dir()}/planviewer.html")
    file_url = f"file://{html_file_path}"

    # Start Flask server in a background thread
    threading.Thread(target=run_planview_server_flask, daemon=True).start()
    time.sleep(1)

    # Open the HTML file in the default web browser
    webbrowser.open(file_url)

    # Keep the main thread alive so the server keeps running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down.")
