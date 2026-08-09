def chunk_documents(documents, chunk_size=800):
    chunks = []
    for document in documents:
        for i in range(0, len(document), chunk_size):
            chunks.append(document[i:i + chunk_size])
    return chunks
