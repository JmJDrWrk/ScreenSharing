from flask import Flask, Response
import mss
import mss.tools
from PIL import Image
import pyautogui
import io

app = Flask(__name__)


x_cal = 70
y_cal = 135


total_bytes_transferred = 0

def capture_screen():
    global total_bytes_transferred
    with mss.mss() as sct:
        monitor = sct.monitors[1]  
        cursor_img = Image.open("cursor.png")  
        cursor_img = cursor_img.convert("RGBA")  
        cursor_width, cursor_height = cursor_img.size

        while True:
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
            
            mouse_x, mouse_y = pyautogui.position()
            
            mouse_x += x_cal
            mouse_y += y_cal
            
            
            img_rgba = img.convert("RGBA")
            
            
            img_rgba.paste(cursor_img, (mouse_x - cursor_width // 2, mouse_y - cursor_height // 2), cursor_img)
            
            
            img_rgb = img_rgba.convert("RGB")
            
            
            img_io = io.BytesIO()
            img_rgb.save(img_io, 'JPEG')
            img_io.seek(0)
            
            
            frame_size = len(img_io.getvalue())
            total_bytes_transferred += frame_size  

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_io.read() + b'\r\n')

@app.route('/screen')
def screen():
    return Response(capture_screen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data')
def data():
    global total_bytes_transferred
    
    mb_transferred = total_bytes_transferred / (1024 * 1024)
    return f"Total data transferred: {mb_transferred:.2f} MB"

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000)
