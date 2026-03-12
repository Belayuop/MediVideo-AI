import fitz  # PyMuPDF
import os

def process_pdf(pdf_path, output_dir="temp_slides"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    doc = fitz.open(pdf_path)
    text_content = []
    image_paths = []

    for i, page in enumerate(doc):
        # Extract Text
        text_content.append(page.get_text())
        
        # Save Page as Image (Slide)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # Higher res
        img_path = os.path.join(output_dir, f"slide_{i}.png")
        pix.save(img_path)
        image_paths.append(img_path)
        
    return "\n".join(text_content), image_paths
