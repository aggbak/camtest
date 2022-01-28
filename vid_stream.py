from flask import Flask, render_template, Response
import cv2
app = Flask(__name__)

camera = cv2.VideoCapture("/dev/video2")

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buff = cv2.imencode('.jpg', frame)
            frame = buff.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') # concat frame by one and show result

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')
