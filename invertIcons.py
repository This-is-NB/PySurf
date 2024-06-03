import os
from PIL import Image

def invert_images(folder_path):
    # Get a list of all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    for image_file in image_files:
        try:
            # Open the image
            image_path = os.path.join(folder_path, image_file)
            img = Image.open(image_path)

            # Check if the image has an alpha channel (transparency)
            if img.mode == 'RGBA':
                # Separate the alpha channel
                r, g, b, a = img.split()

                # Invert the RGB channels
                inverted_r = Image.eval(r, lambda px: 255 - px)
                inverted_g = Image.eval(g, lambda px: 255 - px)
                inverted_b = Image.eval(b, lambda px: 255 - px)

                # Combine the inverted channels with the original alpha channel
                inverted_img = Image.merge('RGBA', (inverted_r, inverted_g, inverted_b, a))
            else:
                # For non-transparent images, invert normally
                inverted_img = Image.eval(img, lambda px: 255 - px)

            # Save the inverted image
            inverted_image_path = os.path.join(folder_path, f"inverted_{image_file}")
            inverted_img.save(inverted_image_path)

            print(f"Inverted {image_file} and saved as {inverted_image_path}")
        except Exception as e:
            print(f"Error processing {image_file}: {e}")

if __name__ == "__main__":
    folder_to_process = "Icons"
    invert_images(folder_to_process)
