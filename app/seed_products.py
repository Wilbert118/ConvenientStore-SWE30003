from pathlib import Path
from models.product import upload_product_image, insert_product

class FileWrapper:
    def __init__(self, file, filename):
        self.file = file
        self.filename = filename

    def read(self):
        return self.file.read()

# Folder containing your product images
image_folder = Path("app\dummy_images")

dummy_products = [
    ("Coca-Cola Zero Can", 2.49, "Beverages", 60, "coke_zero.jpg"),
    ("Ritz Crackers", 3.29, "Snacks", 75, "ritz.jpg"),
    ("Mama Shrimp Tom Yum", 2.39, "Noodles", 85, "mama.jpg"),
    ("Powerade Blue", 3.59, "Beverages", 40, "powerade.jpg"),
    ("Toblerone Mini", 4.49, "Snacks", 50, "toblerone.jpg"),
    ("Barilla Spaghetti", 2.99, "Noodles", 90, "barilla.jpg"),
    ("V Guavana Energy Drink", 3.69, "Beverages", 55, "v_guavanaenergy.jpg"),
    ("Cadbury Dairy Milk", 3.99, "Snacks", 65, "cadbury.jpg"),
    ("Knorr Chicken Ndl Soup", 2.69, "Noodles", 70, "knorr.jpg"),
    ("San Pellegrino Sparkling", 4.29, "Beverages", 35, "sanpellegrino.jpg")
]


for name, price, category, stock, image_filename in dummy_products:
    image_path = image_folder / image_filename

    if not image_path.exists():
        print(f"❌ Image not found: {image_path}")
        continue

    with open(image_path, "rb") as f:
        try:
            wrapped_file = FileWrapper(f, image_filename)
            image_url = upload_product_image(wrapped_file)
            insert_product(name, price, category, stock, image_url)
            print(f"✅ Inserted: {name}")
        except Exception as e:
            print(f"⚠️ Error inserting {name}: {e}")
