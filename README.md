# AI-Powered Chemistry Question Generator

## Overview

The AI-Powered Chemistry Question Generator is a Python-based application that uses Google's Gemini AI and ChromaDB to generate multiple-choice questions (MCQs) from chemistry lecture presentations.

The project uses a Retrieval-Augmented Generation (RAG) approach to ensure that generated questions are based on the content of the provided lecture slides rather than relying on general knowledge.

Users can provide a topic, and the application retrieves relevant information from an indexed PowerPoint presentation and uses Gemini AI to generate a context-based question.

## Features

- **PowerPoint Text Extraction:** Extracts textual content from `.pptx` presentations, organizing the extracted information slide by slide.
- **Text Embeddings:** Uses Google's Gemini embedding model to convert slide content into numerical vector representations.
- **Vector Database:** Uses ChromaDB to store slide embeddings, original text, and associated metadata.
- **Semantic Search:** Retrieves the most relevant lecture content based on the user's input topic.
- **AI-Powered Question Generation:** Uses Gemini 2.5 Flash to generate multiple-choice questions using the retrieved lecture content.
- **Context-Based Responses:** Restricts question generation to the information available in the retrieved database.

## Technologies Used

- **Python** – Core programming language.
- **Google Gemini API** – Generates text embeddings and multiple-choice questions.
- **ChromaDB** – Stores and retrieves vector embeddings.
- **python-pptx** – Extracts text from PowerPoint presentations.

## Project Structure

```text
Chemistry-Question-Generator/
│
├── Embedding.py
├── Question agent.py
├── FoC_09.pptx
├── chroma_db/
│
├── requirements.txt
└── README.md
```

## How It Works

The project consists of two main Python scripts.

### 1. Embedding.py – Data Processing and Storage

This script processes the PowerPoint presentation and prepares its content for semantic retrieval.

The process involves:

1. Reading the PowerPoint presentation using `python-pptx`.
2. Extracting text from individual slides.
3. Combining the text from each slide into a separate document.
4. Generating vector embeddings for each slide using Google's `gemini-embedding-2` model.
5. Storing the embeddings, original slide text, and metadata in a persistent ChromaDB collection named `Chem_ppt`.

Each slide is assigned a unique ID and its corresponding slide number is stored as metadata.

### 2. Question agent.py – Retrieval and Question Generation

This script allows users to generate questions based on a topic of their choice.

The process involves:

1. Accepting a topic from the user.
2. Converting the topic into a search query.
3. Generating an embedding for the query using the same Gemini embedding model.
4. Performing a similarity search in ChromaDB to retrieve the three most relevant slides.
5. Combining the retrieved slide content into a context block.
6. Passing the context and user's topic to Gemini 2.5 Flash.
7. Generating a multiple-choice question based strictly on the retrieved information.

The application also includes an instruction that prevents the AI from using external knowledge when generating its response.

## Installation and Setup

### Prerequisites

- Python 3.9 or later.
- A Google Gemini API key.
- Internet connection for accessing Google's Gemini API.

### 1. Clone the Repository

```bash
git clone https://github.com/USERNAME/REPOSITORY-NAME.git
cd REPOSITORY-NAME
```

Replace the repository URL with your own GitHub repository URL.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Gemini API Key

Set your Google API key as an environment variable named `GOOGLE_API_KEY`.

On Windows Command Prompt:

```cmd
set GOOGLE_API_KEY=your_api_key
```

On macOS/Linux:

```bash
export GOOGLE_API_KEY=your_api_key
```

Do not upload your actual API key to GitHub.

### 4. Run the Embedding Script

```bash
python Embedding.py
```

This extracts the presentation content, generates embeddings, and stores them in ChromaDB.

### 5. Run the Question Generator

```bash
python "Question agent.py"
```

Enter a chemistry topic when prompted.

The application searches the vector database and generates a multiple-choice question using the retrieved lecture content.

## Dependencies

The project uses the following Python libraries:

- `python-pptx`
- `chromadb`
- `google-genai`

## Future Improvements

- Support for multiple PowerPoint presentations.
- Generation of multiple questions at once.
- Difficulty-based question generation.
- Improved question formatting with separate answer choices and explanations.
- Support for additional document formats such as PDF.

## Author

Developed as a Python-based AI project exploring semantic search, vector databases, and Retrieval-Augmented Generation (RAG).
