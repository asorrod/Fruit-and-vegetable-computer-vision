# Fruit-and-vegetable-computer-vision
This project combines computer vision and nutrition tracking in a practical Streamlit web application.

## Dataset
The model was trained using the LVIS Fruits and Vegetables Detection Dataset: 
https://github.com/henningheyen/Fruits-And-Vegetables-Detection-Dataset

The original dataset contains 62 classes, but many of them are highly imbalanced (some with very few images compared to others). Training on the full dataset required a heavy computational load, which was not suitable given our limited resources.

## Class selection
To improve efficiency, we reduced the dataset to the 12 classes with the largest number of images, going from 62 to 12:

- apple
- banana
- broccoli
- carrot
- orange
- strawberry
- tomato
- grape
- lemon
- pineapple
- cucumber
- lettuce

We cleaned the dataset using the dataset_cleaner script to keep only the relevant images before training

## Results 
After retraining with the reduced dataset, the model achieved significantly better performance (still with room for improvement):

Class     Images  Instances      Box(P     R     mAP50   mAP50-95)
all        107        793        0.515   0.573   0.540    0.345

## Streamlit Application

Once the model was trained, we developed a small Streamlit app as a practical use case:

  - Users can upload an image containing one of the trained food items.

  - The model predicts the food type and logs it into a SQLite database.

  - The app keeps track of what the user has eaten during the day and displays daily calorie consumption.

This way, the project not only demonstrates computer vision with YOLO, but also integrates it into a realistic nutritional tracking tool.
