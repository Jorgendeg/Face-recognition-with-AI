python3 -m pip install --upgrade pip setuptools wheel 

python3 -m pip install opencv-python-headless 

python3 -m pip install opencv-python 

sudo apt update 

sudo apt install -y \ 

    python3-numpy \ 

    libatlas-base-dev \ 

    libjasper-dev \ 

    libqt5gui5 \ 

    libhdf5-dev \ 

   libhdf5-serial-dev \ 

    libopenblas-dev \ 

    libprotobuf-dev \ 

   protobuf-compiler \ 

   libzbar0 \ 

   libgtk-3-dev 

 

python3 -m pip install opencv-python 

python3 -m pip install opencv-python-headless 

python3 -m pip install deepface 

sudo fallocate -l 2G /swapfile 

sudo chmod 600 /swapfile 

sudo mkswap /swapfile 

sudo swapon /swapfile 

cap = cv2.VideoCapture("libcamerasrc ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! appsink", cv2.CAP_GSTREAMER) 

sudo apt install -y gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav 

sudo apt update 

sudo apt install python3-opencv –y 

python3 -m pip install --upgrade pip setuptools wheel 

python3 -m pip install numpy 

python3 -m pip install opencv-python-headless 

sudo apt install -y python3-numpy libatlas-base-dev libjasper-dev libqt5gui5 

python3 -m pip install opencv-contrib-python 

sudo apt update 

sudo apt install opencv-data –y 

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') 

face_cascade = cv2.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml') 

sudo apt install -y \ gstreamer1.0-plugins-base \ gstreamer1.0-plugins-good \ gstreamer1.0-plugins-bad \ gstreamer1.0-plugins-ugly \ gstreamer1.0-libav \ libgstreamer1.0-dev \ libgstreamer-plugins-base1.0-dev 

sudo apt install -y python3-numpy libatlas-base-dev libopenblas-dev libjasper-dev 

python3 -m pip install --upgrade pip 

python3 -m pip install opencv-contrib-python 

python3 -m pip install opencv-contrib-python-headless 

python3 -c "import cv2; print(cv2.version); print(hasattr(cv2, 'face'))" 

sudo apt update 

sudo apt install opencv-data –y 

ls -l /usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml 

python3 -m pip install opencv-contrib-python 

sudo apt update 

sudo apt install -y opencv-data python3-opencv gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav 

python3 -m pip install opencv-contrib-python 

sudo apt update 

sudo apt install -y \ 

    gstreamer1.0-plugins-base \ 

    gstreamer1.0-plugins-good \ 

    gstreamer1.0-plugins-bad \ 

    gstreamer1.0-plugins-ugly \ 

    gstreamer1.0-libav \ 

    gstreamer1.0-tools \ 

    libgstreamer-plugins-base1.0-dev \ 

   libgstreamer1.0-dev \ 

   opencv-data 

gst-launch-1.0 libcamerasrc ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! autovideosink 

sudo apt install -y python3-picamera2 

sudo apt update 

sudo apt install -y gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav libgstreamer-plugins-base1.0-0 

sudo apt install -y python3-picamera2 

sudo apt update 

sudo apt install gstreamer1.0-tools –y 

gst-launch-1.0 libcamerasrc ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! Autovideosink 

gst-launch-1.0 libcamerasrc ! video/x-raw,format=NV12,width=640,height=480,framerate=30/1 ! videoconvert ! video/x-raw,format=BGR ! Autovideosink 

sudo apt install gstreamer1.0-libcamera –y 

sudo apt update 

sudo apt install gstreamer1.0-libcamera –y 

sudo apt update 

sudo apt install --reinstall gstreamer1.0-libcamera libcamera0.3 libcamera-apps-lite -y 

sudo gst-inspect-1.0 --gst-plugin-path=/usr/lib/aarch64-linux-gnu/gstreamer-1.0/ libcamerasrc   # force check 

gst-inspect-1.0 libcamerasrc    

gst-launch-1.0 libcamerasrc ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! Autovideosink 

GST_DEBUG=3 gst-launch-1.0 libcamerasrc ! Fakesink 

gst-launch-1.0 libcamerasrc ! videoconvert ! Autovideosink 

sudo apt install python3-picamera2 –y 

gst-launch-1.0 libcamerasrc ! video/x-raw,format=NV12,width=640,height=480,framerate=30/1 ! videoconvert ! Autovideosink 

gst-launch-1.0 libcamerasrc ! capsfilter caps=video/x-raw,format=NV12,width=640,height=480,framerate=30/1 ! videoconvert ! Autovideosink 

gst-launch-1.0 libcamerasrc camera-name="/base/axi/pcie@1000120000/rp1/i2c@88000/imx708@1a" ! video/x-raw,format=NV12,width=640,height=480,framerate=30/1 ! videoconvert ! Autovideosink 

gst-launch-1.0 libcamerasrc ! video/x-raw,format=I420,width=640,height=480,framerate=30/1 ! videoconvert ! Autovideosink 

sudo apt update 

sudo apt install python3-picamera2 –y 

sudo apt update 

sudo apt install --reinstall python3-picamera2 -y 

sudo reboot    

ps aux | grep -i camera   # of ps aux | grep -i picam / libcamera / python 

sudo kill 1234 

# als het niet wil stoppen: 

sudo kill -9 1234 

pkill -f python 

# of specifieker: 

pkill -f picamera2 

pkill -f libcamera 

ps aux | grep -iE 'python|picamera|libcamera|camera' 

sudo kill 12345 

sudo apt update 

sudo apt full-upgrade -y 

sudo apt install --reinstall python3-picamera2 libcamera-apps libcamera0.3 -y 

sudo reboot 
