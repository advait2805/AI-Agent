import os
import chromadb
from google import genai
from google.genai import types

client = genai.Client()

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "chroma_db")
chroma_client = chromadb.PersistentClient(path=db_path)


def query_vector_db(collection_name: str, query_text: str, n_results: int = 3) -> str:
    """
    Queries ChromaDB for the most relevant context.
    Assumes your Chroma client is running locally or persisted in a directory.
    """
    
    # Get your existing collection
    collection = chroma_client.get_collection(name=collection_name)
    
    # Convert the user's text query into a vector embedding
    # Crucial: Use the SAME model used during data ingestion!
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=query_text
    )
    query_embedding = response.embeddings[0].values

    # Query the database using the vector
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    
    # Extract and format the text content from the results
    # Chroma returns a list of lists, so we grab the first element [0]
    documents = results.get("documents", [[]])[0]
    
    if not documents:
        return ""
        
    # Join the top snippets together into a single context block
    context = "\n\n".join(documents)
    return context


def ask_gemini_with_context(query: str, context: str) -> str:
    """
    Sends the prompt and context to Gemini, enforcing a strict constraint
    to only use the provided information.
    """
    # Initialize the standard Google GenAI client
    client = genai.Client()
    
    # Define system instructions to enforce the "grounding" constraint
    system_instruction = (
        "You are a strict factual assistant. Your task is to answer the user's question "
        "using ONLY the provided Context block. If the answer cannot be completely and "
        "truthfully derived from the Context, reply exactly with: 'Information in this is not "
        "present in the provided database.' Do not use any prior knowledge or external facts."
    )
    
    # Structure the user prompt clearly separating context from the question
    user_prompt = f"""
Context information is below.
---------------------
{context}
---------------------

Given the context information above and no prior knowledge, answer the following question.
Question: {query}
Answer:
"""

    # Call the model (using gemini-2.5-flash for fast and accurate RAG tasks)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.0, # Low temperature ensures deterministic, factual adherence
        ),
    )
    return response.text


# Initialize the Google Gen AI client
# The client automatically pulls the API key from the GOOGLE_API_KEY environment variable

COLLECTION_NAME = "Chem_ppt"
topic = input("What topic would you like to be asked a question on:")
USER_QUESTION = "Make a multiple choice question on the following topic: " + topic

try:
    # Fetch relevant data from ChromaDB
    print("Searching vector database...")
    db_context = query_vector_db(COLLECTION_NAME, USER_QUESTION, n_results=3)
    
    if not db_context.strip():
        print("No relevant context found in the database.")
    else:
        # Generate the strictly grounded answer
        print("Generating answer from Gemini...")
        answer = ask_gemini_with_context(USER_QUESTION, db_context)
        
        print("\n=== Result ===")
        print(answer)
        
except Exception as e:
    print(f"An error occurred: {e}")
