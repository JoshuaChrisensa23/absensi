from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

#--------------------------

CAMERA_INDEX = 0

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

FACE_RESIZE_SCALE = 0.25

#-------------------------

DATABASE_DIR = BASE_DIR / "face" / "dataset"

ENCODING_DIR = BASE_DIR / "face" / "encodings"

FACE_TOLERANCE = 0.50

# ------------------------

SERIAL_PORT = "/dev/serial0"

BAUDRATE = 57600

ADDRESS = 0xFFFFFFFF

PASSWORD = 0x00000000

# -----------------------

DATABASE = BASE_DIR / "database" / "smartaccess.db"

# -----------------------

LOG_DIR = BASE_DIR / "logs"

# -----------------------

HOST = "0.0.0.0"
PORT = 5000
