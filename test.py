import keras as tf
from keras._tf_keras.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Load the trained model
model = tf.models.load_model('shirt_or_pants_model.h5',compile=True)

# Function to load and preprocess the image
def load_and_preprocess_image(img_path):
    # Load the image
    img = image.load_img(img_path, target_size=(150, 150))  # Resize to the same size used during training
    img_array = image.img_to_array(img)  # Convert image to array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Scale pixel values to [0, 1]
    return img_array

# Step 2: Provide the path to the image you want to predict
image_path = './data/train/shirt/image_10.jpg'  # Replace with your image path
processed_image = load_and_preprocess_image(image_path)

# Step 3: Make a prediction
prediction = model.predict(processed_image)
predicted_class = 'shirt' if prediction[0][0] > 0.5 else 'pants'

# Output the prediction
print(f'The predicted class is: {predicted_class}')
print(prediction)
# Optional: Display the image
plt.imshow(image.load_img(image_path))
plt.axis('off')  # Hide axes
plt.show()
