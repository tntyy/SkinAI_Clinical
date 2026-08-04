import cv2

def blur_score(path):

    img = cv2.imread(path)

    if img is None:
        print("Không đọc được ảnh:", path)
        return 0.0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    score = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    print("Blur =", score)

    return float(score)


def is_blur(path):

    return blur_score(path)<100