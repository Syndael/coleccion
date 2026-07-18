import urllib.request, tarfile, os, glob, shutil

url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz"
print("Descargando ffmpeg estatico...")
urllib.request.urlretrieve(url, "/tmp/ffmpeg.tar.xz")
print("Extrayendo...")
with tarfile.open("/tmp/ffmpeg.tar.xz") as tf:
    tf.extractall("/tmp/ffmpeg")
for f in glob.glob("/tmp/ffmpeg/*/bin/ff*"):
    shutil.copy2(f, "/usr/local/bin/")
shutil.rmtree("/tmp/ffmpeg")
os.unlink("/tmp/ffmpeg.tar.xz")
print("ffmpeg estatico instalado.")
