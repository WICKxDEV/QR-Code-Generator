import os
from PIL import Image
import qrcode


def create_qr(data, output_dir="output", filename="qrcode.png", logo_path=None):
    """
    Generate a QR code from the provided data and save it as an image.

    Parameters:
    - data (str): The data to encode in the QR code.
    - output_dir (str): Directory to save the QR code image.
    - filename (str): Name of the output image file.
    - logo_path (str): Path to the logo image to overlay on the QR code.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create the QR code
    qr = qrcode.QRCode(
        version=5,  # Increase version if logo makes QR unreadable
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logo
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Generate the QR code image
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Add the logo if provided
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path)

        # Resize the logo to fit within the QR code
        qr_width, qr_height = img.size
        logo_size = int(qr_width / 4)  # Adjust the size (1/4 of the QR code width)
        logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)

        # Calculate the position to overlay the logo
        logo_x = (qr_width - logo_size) // 2
        logo_y = (qr_height - logo_size) // 2

        # Overlay the logo onto the QR code
        img.paste(logo, (logo_x, logo_y), logo)

    # Save the image
    filepath = os.path.join(output_dir, filename)
    img.save(filepath)
    print(f"QR Code saved at: {filepath}")


if __name__ == "__main__":
    # Example usage
    data_to_encode = input("Enter the data to encode in the QR code: ")
    logo_file = input("Enter the path to the logo image (or press Enter to skip): ").strip()
    create_qr(data_to_encode, logo_path=logo_file if logo_file else None)
