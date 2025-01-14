import os
import struct
import numpy as np
from PIL import Image, ImageOps

# Configuration
input_files = {
    "train": "Persian-Character-DB-Training.cdb",
    "test": "Persian-Character-DB-Test.cdb",
}
output_dir = "./data"  # Base output directory for train/test images
MAX_COMMENT = 512
TARGET_SIZE = (128, 128)  # Consistent size for all images

def preprocess_and_resize(data, target_size):
    """Preprocess and resize images with padding to preserve aspect ratio."""
    # Create a grayscale image ("L" mode)
    img = Image.fromarray(data).convert("L")
    
    # Determine padding to make the image square
    max_dim = max(img.size)
    delta_w = max_dim - img.size[0]
    delta_h = max_dim - img.size[1]
    padding = (delta_w // 2, delta_h // 2, delta_w - delta_w // 2, delta_h - delta_h // 2)
    
    # Add padding and resize
    padded_img = ImageOps.expand(img, border=padding, fill=255)  # White background
    resized_img = padded_img.resize(target_size, Image.Resampling.LANCZOS)
    return resized_img

def read_cdb(file_path, output_dir, dataset_type, target_size):
    """Read .cdb file and save images with consistent resolution."""
    os.makedirs(output_dir, exist_ok=True)
    with open(file_path, "rb") as f:
        # Read header
        _ = f.read(7)  # Skip private header
        yy, m, d = struct.unpack("HBB", f.read(4))
        W, H = struct.unpack("HH", f.read(4))
        total_records = struct.unpack("I", f.read(4))[0]
        max_count = struct.unpack("H", f.read(2))[0]
        letter_count = struct.unpack(f"{max_count}I", f.read(4 * max_count))
        img_type = struct.unpack("B", f.read(1))[0]
        comments = f.read(MAX_COMMENT).decode("utf-8").strip()
        _ = f.read(490)  # Reserved bytes

        normal = (W > 0 and H > 0)

        print(f"Processing {dataset_type} dataset: {total_records} records")
        for record in range(total_records):
            # Read each record
            start_word = struct.unpack("H", f.read(2))[0]
            if start_word != 0xFFFF:
                raise ValueError(f"Invalid start word at record {record}")
            
            label = struct.unpack("H", f.read(2))[0]
            confidence = struct.unpack("H", f.read(2))[0]

            if not normal:
                W, H = struct.unpack("HH", f.read(4))
            
            byte_count = struct.unpack("H", f.read(2))[0]
            
            # Read image data
            if img_type == 0:  # Binary image
                data = np.zeros((H, W), dtype=np.uint8)
                for y in range(H):
                    counter = 0
                    b_white = True
                    while counter < W:
                        wb_count = struct.unpack("B", f.read(1))[0]
                        value = 255 if b_white else 0
                        data[y, counter:counter+wb_count] = value
                        counter += wb_count
                        b_white = not b_white
            else:  # Grayscale image
                data = np.frombuffer(f.read(W * H), dtype=np.uint8).reshape((H, W))

            # Resize image to target size with padding
            resized_data = preprocess_and_resize(data, target_size)

            # Save image
            label_dir = os.path.join(output_dir, str(label))
            os.makedirs(label_dir, exist_ok=True)
            img_path = os.path.join(label_dir, f"{record}.png")
            resized_data.save(img_path)
            
            if record % 1000 == 0:
                print(f"Processed {record}/{total_records} records...")
    
    print(f"Finished processing {dataset_type} dataset. Images saved to {output_dir}")

# Convert train and test datasets
for dataset_type, input_file in input_files.items():
    dataset_dir = os.path.join(output_dir, dataset_type)
    read_cdb(input_file, dataset_dir, dataset_type, TARGET_SIZE)

