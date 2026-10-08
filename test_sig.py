from PySide6.QtCore import QObject, Signal

class TestObj(QObject):
    sig = Signal(tuple, tuple, str)
    
def handler(a, b, c):
    print("Received:", a, b, c)
    
obj = TestObj()
obj.sig.connect(handler)

try:
    obj.sig.emit((1,1), (2,2), None)
    print("Emitted successfully")
except Exception as e:
    print("Exception:", e)
