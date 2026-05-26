import cv2

def is_real_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    # low texture = fake image
    if laplacian_var < 40:
        return False

    return True