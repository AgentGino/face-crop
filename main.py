import cv2
import argparse
import os
import sys

def detect_and_crop_faces(image_path, output_dir):
    """
    Detects all faces in an image, crops them, and saves them as separate files
    in the specified output directory.
    Returns a list of paths to the cropped images.
    """
    # Load the pre-trained face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Read the input image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read the image at {image_path}")
        return []

    # Convert to grayscale (helps detection)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return []

    output_paths = []
    base_name, ext = os.path.splitext(os.path.basename(image_path))

    for i, (x, y, w, h) in enumerate(faces):
        # Define crop with 1:1 aspect ratio and padding
        # Center of the face
        cx = x + w / 2
        cy = y + h / 2

        # Make crop size proportional to face size
        crop_size = int(max(w, h) * 1.8)

        # Calculate crop coordinates
        x1 = int(cx - crop_size / 2)
        y1 = int(cy - crop_size / 2)
        x2 = int(cx + crop_size / 2)
        y2 = int(cy + crop_size / 2)

        # Ensure crop coordinates are within image bounds
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(img.shape[1], x2)
        y2 = min(img.shape[0], y2)
        
        # Crop the image
        cropped_img = img[y1:y2, x1:x2]

        # Handle cases where the crop is empty
        if cropped_img.size == 0:
            print(f"Warning: Could not crop face #{i+1} from {os.path.basename(image_path)}, it might be too close to an edge.")
            continue

        # Save the result
        if len(faces) > 1:
            output_filename = f"{base_name}_cropped_{i+1}{ext}"
        else:
            output_filename = f"{base_name}_cropped{ext}"
        
        output_path = os.path.join(output_dir, output_filename)
        cv2.imwrite(output_path, cropped_img)
        output_paths.append(output_path)
        
    return output_paths

def process_path(path, output_dir=None):
    """Processes a single file or a directory of files."""
    if output_dir is None:
        output_dir = "outputs"
    
    os.makedirs(output_dir, exist_ok=True)

    if os.path.isfile(path):
        image_paths = [path]
    elif os.path.isdir(path):
        print(f"Processing directory: {path}")
        image_extensions = ('.png', '.jpg', '.jpeg')
        image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith(image_extensions)]
    else:
        print(f"Error: Input path '{path}' is not a valid file or directory.", file=sys.stderr)
        sys.exit(1)

    if not image_paths:
        print("No image files found to process.")
        return

    total_faces_cropped = 0
    for image_path in image_paths:
        result_paths = detect_and_crop_faces(image_path, output_dir)
        if result_paths:
            total_faces_cropped += len(result_paths)
            print(f"Success: Cropped {len(result_paths)} face(s) from {os.path.basename(image_path)}.")
            for p in result_paths:
                print(f"  -> Saved {p}")
        else:
            print(f"Info: No faces detected in {os.path.basename(image_path)}.")
    
    print(f"\nProcessing complete. Total faces cropped: {total_faces_cropped}.")


def main():
    """
    Main function to parse arguments and run face detection.
    """
    parser = argparse.ArgumentParser(description="Detects and crops faces in an image or a directory of images.")
    parser.add_argument("path", help="Path to the input photo or directory.")
    parser.add_argument("-o", "--output", help="Path to the output directory. Defaults to 'outputs/'.")
    args = parser.parse_args()

    process_path(args.path, args.output)

if __name__ == '__main__':
    main()
