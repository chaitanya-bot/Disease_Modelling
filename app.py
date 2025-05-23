from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image

app = Flask(__name__)

# Load the  Keras model
model = load_model('model.h5')


# Function to predict the label of an image
def predict_label(img_path):
    # Loading the image and resizing it
    i = image.load_img(img_path, target_size=(64, 64))
    i = image.img_to_array(i) / 255.0
    i = i.reshape(1, 64, 64, 3)
    # predicting if patient is positive or negative
    p = model.predict(i)
    if p < 0.5:
        p = 0
    else:
        p = 1
    # adding labels and returning it
    labels = {0: 'The patient is negative for malaria', 1: 'The patient is positive for malaria'}
    predicted_label = labels[p]

    return predicted_label


# Route to the main page
@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")


# Route to handle image submission
@app.route("/submit", methods=['GET', 'POST'])
def get_output():
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = "static/" + img.filename
        img.save(img_path)

        p = predict_label(img_path)

    return render_template("index.html", prediction=p, img_path=img_path)


if __name__ == '__main__':
    # app.debug = True
    app.run(debug=True)
