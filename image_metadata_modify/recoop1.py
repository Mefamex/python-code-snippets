from PIL import Image
import piexif

def get_image_metadata(image_path):
    """Retrieve and display the current metadata of the image."""
    image = Image.open(image_path)
    exif_data = image._getexif()
    metadata = {}
    
    if exif_data is not None:
        for tag_id, value in exif_data.items():
            tag = piexif.TAGS.get(tag_id, tag_id)
            metadata[tag] = value
            
    return metadata

def modify_image_metadata(image_path, output_path):
    """Modify existing metadata and add new metadata to the image."""
    # Step 1: Display existing metadata
    print("Current Metadata:")
    metadata = get_image_metadata(image_path)
    for key, value in metadata.items():
        print(f"{key}: {value}")

    # Step 2: Modify existing metadata
    print("\nEnter new values for the existing metadata (leave blank to keep current value):")
    new_metadata = {}
    for key in metadata.keys():
        new_value = input(f"{key} (current: {metadata[key]}): ")
        if new_value:
            new_metadata[key] = new_value

    # Step 3: Add new metadata
    print("\nAdd any new metadata (key:value format, type 'done' to finish):")
    while True:
        new_entry = input("New Metadata Entry: ")
        if new_entry.lower() == 'done':
            break
        try:
            key, value = new_entry.split(':')
            new_metadata[key.strip()] = value.strip()
        except ValueError:
            print("Invalid format. Please use 'key:value' format.")

    # Load the image and existing EXIF data
    image = Image.open(image_path)
    exif_dict = piexif.load(image.info['exif'])

    # Update the EXIF data with new values
    for tag, value in new_metadata.items():
        if tag in exif_dict['0th']:
            exif_dict['0th'][tag] = value

    # Convert the modified EXIF data back to bytes
    exif_bytes = piexif.dump(exif_dict)

    # Save the image with the new EXIF data
    image.save(output_path, exif=exif_bytes)
    print(f"Modified image saved as: {output_path}")

# Example usage
if __name__ == "__main__":
    image_path = 'input_image.jpg'  # Replace with your image path
    output_path = 'output_image.jpg'  # Output path for the modified image
    modify_image_metadata(image_path, output_path)