import os
from PIL import Image

# Mapping for correct image format names required by Pillow
OUTPUT_FORMAT_MAPPING = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "webp": "WEBP"
}


def optimize_images(
        folder_path: str,
        input_image_types: str = "jpg,png",  # Default value is "jpg,png"
        output_image_type: str = None,
        output_folder: str = None
):
    """
    Tối ưu hóa hình ảnh trong một thư mục nhất định sang định dạng được chỉ định.

    Tham số:
        folder_path (str): Đường dẫn đến thư mục chứa hình ảnh.
        input_image_types (str): Các loại định dạng hình ảnh đầu vào, phân tách bằng dấu phẩy (ví dụ: "jpg,png"). Mặc định là "jpg,png".
        output_image_type (str): Loại định dạng hình ảnh đầu ra (ví dụ: "webp"). Mặc định sử dụng loại định dạng gốc.
        output_folder (str): Đường dẫn đến thư mục đầu ra. Mặc định là thư mục đầu vào.
    """
    # Split input types into a list and normalize (e.g., "jpg, png" -> ["jpg", "png"])
    input_types = [ext.strip().lower() for ext in input_image_types.split(",")]

    # If no output folder is specified, use the input folder
    if not output_folder:
        output_folder = folder_path

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Loop through files in the folder
    for filename in os.listdir(folder_path):
        input_ext = os.path.splitext(filename)[-1].lower().lstrip(".")
        if input_ext in input_types:
            input_path = os.path.join(folder_path, filename)

            # Determine output extension: keep original if not specified
            output_ext = output_image_type if output_image_type else input_ext
            output_filename = os.path.splitext(filename)[0] + f".{output_ext}"
            output_path = os.path.join(output_folder, output_filename)

            # Get the correct format for Pillow
            output_format = OUTPUT_FORMAT_MAPPING.get(output_ext, output_ext.upper())

            try:
                # Open and optimize image
                with Image.open(input_path) as img:
                    img.save(output_path, format=output_format, optimize=True)
                    print(f"Optimized: {input_path} -> {output_path}")
            except Exception as e:
                print(f"Failed to process {input_path}: {e}")


if __name__ == "__main__":
    folder_path = input("Nhập đường dẫn đến thư mục: ")
    output_folder = input("Nhập đường dẫn đến thư mục đầu ra (tùy chọn, nhấn Enter để sử dụng thư mục đầu vào): ") or None
    input_image_types = input(
        "Nhập các loại định dạng hình ảnh đầu vào (phân tách bằng dấu phẩy, mặc định: jpg,png): ") or "jpg,png"
    output_image_type = input(
        "Nhập loại định dạng hình ảnh đầu ra (tùy chọn, nhấn Enter để giữ nguyên định dạng gốc): ") or None

    optimize_images(folder_path, input_image_types, output_image_type, output_folder)