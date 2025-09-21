# Fruit-and-vegetable-computer-vision
This project combines computer vision and nutrition tracking in a practical **Streamlit** web application.

## Dataset
The model was trained using the **LVIS Fruits and Vegetables Detection Dataset**: 
https://github.com/henningheyen/Fruits-And-Vegetables-Detection-Dataset

The original dataset contains 62 classes, but many of them are highly imbalanced (some with very few images compared to others). Training on the full dataset required a heavy computational load, which was not suitable given our limited resources.

## Class selection
To improve efficiency, we reduced the dataset to the 12 classes with the largest number of images, going from **62** to **12**:

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
After retraining with the reduced dataset of 12 classes, the model achieved a noticeable improvement in detection quality compared to the initial training with 62 classes. The evaluation metrics are the following:

### Interpretation
- **Precision (0.515):** Around half of the predicted detections are correct. This shows the model has a reasonable ability to avoid false positives, but there is still space for refinement.

- **Recall (0.573):** The model successfully detects more than half of the ground-truth objects. This indicates that, while it misses some instances, it has a solid baseline recall considering the dataset’s variability.

- **mAP@50 (0.540):** The model reaches 54% mean Average Precision at an IoU threshold of 0.5. This is a clear improvement compared to the original training with all 62 classes, confirming that reducing and balancing the dataset helped the model learn more representative features.

- **mAP@50-95 (0.345):** The stricter mAP metric highlights that the model still struggles with higher IoU thresholds, showing that bounding box localization can be further improved.

### Takeaways
The model performance is acceptable for a lightweight proof-of-concept application, but still with room for improvement

## Streamlit Application
Once the model was trained, we developed a small Streamlit app as a practical use case:

  - Users can upload an image containing one of the trained food items.

  - The model predicts the food type and logs it into a SQLite database.

  - The app keeps track of what the user has eaten during the day and displays daily calorie consumption.

This way, the project not only demonstrates computer vision with YOLO, but also integrates it into a realistic nutritional tracking tool.

## How to use

Install the dependencies from requirements.txt

If you only want to execute it locally, in the app directory execute **"python -m streamlit run app.py"** and try some of the images from the **"meals_image"** folder or try uploading your own.

On the other hand if you want to train with the cropped dataset, donwload it from "https://github.com/henningheyen/Fruits-And-Vegetables-Detection-Dataset" and run the **dataset_cleaner script**.

Otherwise you can view the app from this link: https://calorydatabase.streamlit.app/
