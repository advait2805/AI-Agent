import os
from pptx import Presentation
import chromadb
from google import genai

client = genai.Client()

def parse_pptx(file_path: str):
    """
    Parses a PPTX file and returns text chunked by slide.
    """


    fp = os.path.abspath(file_path)
    if os.path.exists(file_path):
        prs = Presentation(file_path)        
        
        slides_data = []
        
        for slide_num, slide in enumerate(prs.slides, start=1):
            slide_text = []
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    slide_text.append(shape.text.strip())
            
            # Combine text from the same slide
            full_slide_text = "\n".join(slide_text)
            if full_slide_text:
                slides_data.append({
                    "text": full_slide_text,
                    "metadata": {
                        "source": os.path.basename(file_path),
                        "slide_number": slide_num}})
                    
        print("File found")
        return slides_data
    else:
        print("File not found")
        return None
    
   
def get_google_embeddings(text: list):
    """
    Takes the structured slides list, generates embeddings, 
    and returns a list of separate, standalone slide data dictionaries.
    """
    separated_slides_data = []
    for i in text:    
        response = client.models.embed_content(
            model="gemini-embedding-2",
            contents=i,
        )
        
        # Unpack vectors
        vectors = [embedding.values for embedding in response.embeddings]
        separated_slides_data.append(vectors[0])
    return separated_slides_data


pptx_path="FoC_09.pptx"

slides = parse_pptx(pptx_path)
print("⏳ Parsing PPTX file...")

if not slides:
    print("❌ No text found in the PowerPoint file.")


# Extract clean list of texts for embedding
texts_to_embed = [slide["text"] for slide in slides]

print(f"⏳ Generating embeddings for {len(texts_to_embed)} slides via Google Gen AI SDK...")
embeddings = get_google_embeddings(texts_to_embed)

# Prepare data for Chroma ingestion
ids = [f"slide_{slide['metadata']['slide_number']}" for slide in slides]
metadatas = [slide["metadata"] for slide in slides]

print("⏳ Storing vectors into ChromaDB...")
# Initialize Chroma persistent client
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "chroma_db")

print(f"📁 Database path locked to: {db_path}")
chroma_client = chromadb.PersistentClient(path=db_path)

# Create or get a collection
collection = chroma_client.get_or_create_collection(name="Chem_ppt")


# Upsert vectors, raw documents, and metadata into Chroma
collection.upsert(
    ids=ids,
    embeddings=embeddings,
    documents=texts_to_embed,
    metadatas=metadatas
)

print("✅ Successfully indexed PPTX into ChromaDB!")
