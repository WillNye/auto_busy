from pywinauto.application import Application
import psutil

def maximize():
    # app = Application(backend='uia').active()
    # print(app)
    for proc in psutil.process_iter():
        if proc.name() == 'pycharm.exe':
            try:
                app = Application(backend="uia").connect(process=proc.pid)
                continue
            except Exception as e:
                print(e)

    dlg_spec = app.window(best_match='camstat - [C:\\Users\\wbeasley\\PycharmProjects\\camstat] - ...\\non_vsm_scripts\\update_tables.py - PyCharm 2016.2.3')
    dlg_spec.wrapper_object().maximize()


maximize()