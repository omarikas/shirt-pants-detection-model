import keras as tf
from keras._tf_keras.keras.preprocessing.image import ImageDataGenerator

# Define constants
IMAGE_HEIGHT = 150  # Desired image height after cropping
IMAGE_WIDTH = 150   # Desired image width after cropping
BATCH_SIZE = 32     # Number of images to be processed in a batch
EPOCHS = 10         # Number of epochs for training

# Create data generators for loading and preprocessing images
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    'data/train',
    target_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='binary'  # Use 'categorical' for more than 2 classes
)

validation_generator = validation_datagen.flow_from_directory(
    'data/validation',
    target_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

# Step 4: Build the CNN Model
model = tf.Sequential([
    tf.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_HEIGHT, IMAGE_WIDTH, 3)),
    tf.layers.MaxPooling2D(pool_size=(2, 2)),
    
    tf.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.layers.MaxPooling2D(pool_size=(2, 2)),
    
    tf.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.layers.MaxPooling2D(pool_size=(2, 2)),
    
    tf.layers.Flatten(),
    tf.layers.Dense(128, activation='relu'),
    tf.layers.Dropout(0.5),
    tf.layers.Dense(1, activation='sigmoid')  # Use softmax for multi-class classification
])

# Step 5: Compile the Model
model.compile(optimizer='adam',
              loss='binary_crossentropy',  # Use 'categorical_crossentropy' for multi-class
              metrics=['accuracy'])

# Step 6: Train the Model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // BATCH_SIZE,
    epochs=EPOCHS
)

# Step 7: Save the Model
model.save('shirt_or_pants_model.h5')
