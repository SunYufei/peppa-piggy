import cv2
import dlib

face_detector = dlib.get_frontal_face_detector()

piggy = cv2.imread('piggy.png', cv2.IMREAD_UNCHANGED)


def location(gray):
    ret = face_detector(gray, 0)
    if len(ret) > 0:
        return ret[0]
    else:
        return None


def draw_peggy(image, face_location, top, side):
    l = face_location.left()
    t = face_location.top()
    r = face_location.right()
    b = face_location.bottom()
    x, y, w, h = l, t, r - l, b - t
    ratio = h / piggy.shape[0] * 0.9
    small = cv2.resize(piggy, (0, 0), None, ratio, ratio)
    r, c = small.shape[0], small.shape[1]
    start = (w - c) // 2
    if top:
        for i in range(c):
            for j in range(r):
                if y - r + j >= 0 and small[j, i][3] != 0:
                    for k in range(3):
                        image[y - r + j, x + start + i][k] = small[j, i][k]
    if side:
        for i in range(c):
            for j in range(r):
                if small[j, i][3] != 0:
                    if x + 0.9 * w + i < image.shape[1]:
                        for k in range(3):
                            image[y + j, x + int(0.9 * w) + i][k] = small[j, i][k]
                    if x + 0.1 * w - i > 0:
                        for k in range(3):
                            image[y + j, x + w // 10 - i][k] = small[j, i][k]


capture = cv2.VideoCapture(0)

while capture.isOpened():
    ret, frame = capture.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        loc = location(gray)
        if loc is not None:
            draw_piggy(frame, piggy, location, True, True)

        cv2.imshow('Monitor', frame)
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()
