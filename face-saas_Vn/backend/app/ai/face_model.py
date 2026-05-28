from insightface.app import FaceAnalysis

app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0, det_size=(640, 640))


def extract_embedding(image):
    faces = app.get(image)

    if len(faces) == 0:
        return None

    return faces[0].embedding