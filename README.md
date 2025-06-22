# Face Crop Tool

This script uses OpenCV to automatically detect and crop faces from images. It can process a single image file or an entire directory of images.

## Features

-   Detects and crops all faces in an image.
-   Processes single image files (`.jpg`, `.jpeg`, `.png`).
-   Processes all images within a directory.
-   Saves each cropped face as a new image file.

## Setup

1.  **Prerequisites**: Ensure you have Python 3 installed on your system.

2.  **Clone the repository (optional)**:
    ```bash
    git clone https://github.com/AgentGino/face-crop.git
    cd face-crop
    ```

3.  **Install dependencies**:
    This project requires `opencv-python`. You can install it using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

You can run the script from your terminal by providing a path to an image or a directory.

### Processing a Single Image

To process a single image file, provide its path as an argument:
```bash
python main.py /path/to/your/photo.jpg
```
If one or more faces are detected, the script will save them as new files in an `outputs` directory.

### Processing a Directory of Images

To process all images in a directory, provide the directory path:
```bash
python main.py /path/to/your/directory/
```
The script will scan the directory for images, process each one, and save the cropped faces in the `outputs` directory.

### Specifying an Output Directory

You can use the `-o` or `--output` flag to specify a custom directory for the cropped images:
```bash
python main.py /path/to/your/images -o /path/to/your/output_directory
```

## Important Considerations

### False Positives/Negatives
The face detection algorithm used (`Haar Cascades`) is fast and efficient, but it's not perfect. Please be aware of the following:

-   **False Positives**: Sometimes, the algorithm may mistakenly identify other objects (like patterns in a wall, trees, or clothing) as faces.
-   **False Negatives**: The algorithm might fail to detect faces that are at an angle, in poor lighting, or partially obscured.

It's always a good idea to review the output images to ensure the results meet your expectations. 
