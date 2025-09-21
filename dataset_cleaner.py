import os
import yaml
from pathlib import Path

# ⚙️ CONFIG - rutas directas a tu dataset
DATASET_DIR = "datasets/LVIS_Fruits_And_Vegetables"
TRAIN_IMAGES = f"{DATASET_DIR}/images/train"
VAL_IMAGES   = f"{DATASET_DIR}/images/val"
TEST_IMAGES  = f"{DATASET_DIR}/images/test"

TRAIN_LABELS = f"{DATASET_DIR}/labels/train"
VAL_LABELS   = f"{DATASET_DIR}/labels/val"
TEST_LABELS  = f"{DATASET_DIR}/labels/test"

DATA_YAML = f"{DATASET_DIR}/data.yaml"

# Preserved Classes
KEEP_CLASSES = [
    "apple",
    "banana",
    "broccoli",
    "carrot",
    "orange/orange fruit",
    "strawberry",
    "tomato",
    "grape",
    "lemon",
    "pineapple",
    "cucumber/cuke",
    "lettuce"
]

with open(DATA_YAML, "r") as f:
    data = yaml.safe_load(f)

old_classes = data["names"]
print(f"Clases originales ({len(old_classes)}):")
for k, v in old_classes.items():
    print(f"  {k}: {v}")

keep_ids = {old_id: cls for old_id, cls in old_classes.items() if cls in KEEP_CLASSES}
new_classes = list(keep_ids.values())
class_map = {old_id: new_id for new_id, (old_id, cls) in enumerate(keep_ids.items())}

print("\nMapping (old_id → new_id):", class_map)

data["names"] = {i: cls for i, cls in enumerate(new_classes)}
with open(DATA_YAML, "w") as f:
    yaml.dump(data, f, sort_keys=False)

print(f"\nNuevo data.yaml guardado con {len(new_classes)} clases.")

def process_labels(label_dir, image_dir):
    label_dir = Path(label_dir)
    image_dir = Path(image_dir)

    for label_file in label_dir.glob("*.txt"):
        new_lines = []
        with open(label_file, "r") as f:
            for line in f:
                parts = line.strip().split()
                old_id = int(parts[0])
                if old_id in class_map:
                    new_id = class_map[old_id]
                    parts[0] = str(new_id)
                    new_lines.append(" ".join(parts))
        if new_lines:
            with open(label_file, "w") as f:
                f.write("\n".join(new_lines) + "\n")
        else:
            os.remove(label_file)
            for ext in [".jpg", ".png", ".jpeg"]:
                img_path = image_dir / (label_file.stem + ext)
                if img_path.exists():
                    os.remove(img_path)

process_labels(TRAIN_LABELS, TRAIN_IMAGES)

process_labels(VAL_LABELS, VAL_IMAGES)

process_labels(TEST_LABELS, TEST_IMAGES)

print("\n🎉 Dataset cleaned")
