import re
from typing import List, Dict, Any

# Standard English stopwords
STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t',
    'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can\'t',
    'cannot', 'could', 'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t', 'down',
    'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn\'t', 'has', 'hasn\'t', 'have', 'haven\'t',
    'having', 'he', 'he\'d', 'he\'ll', 'he\'s', 'her', 'here', 'here\'s', 'hers', 'herself', 'him', 'himself',
    'his', 'how', 'how\'s', 'i', 'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t', 'it',
    'it\'s', 'its', 'itself', 'let\'s', 'me', 'more', 'most', 'mustn\'t', 'my', 'myself', 'no', 'nor', 'not',
    'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
    'same', 'shan\'t', 'she', 'she\'d', 'she\'ll', 'she\'s', 'should', 'shouldn\'t', 'so', 'some', 'such',
    'than', 'that', 'that\'s', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'there\'s',
    'these', 'they', 'they\'d', 'they\'ll', 'they\'re', 'they\'ve', 'this', 'those', 'through', 'to', 'too',
    'under', 'until', 'up', 'very', 'was', 'wasn\'t', 'we', 'we\'d', 'we\'ll', 'we\'re', 'we\'ve', 'were',
    'weren\'t', 'what', 'what\'s', 'when', 'when\'s', 'where', 'where\'s', 'which', 'while', 'who', 'who\'s',
    'whom', 'why', 'why\'s', 'with', 'won\'t', 'would', 'wouldn\'t', 'you', 'you\'d', 'you\'ll', 'you\'re',
    'you\'ve', 'your', 'yours', 'yourself', 'yourselves'
}

def clean_text(text: str) -> str:
    """Normalize whitespace and strip unprintable characters."""
    if not text:
        return ""
    # Normalize unicode / line breaks
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Replace non-breaking spaces and tabs
    text = text.replace('\xa0', ' ').replace('\t', ' ')
    # Replace multiple spaces
    text = re.sub(r' +', ' ', text)
    # Replace excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def split_into_sentences(text: str) -> List[str]:
    """Split text into sentences using regex boundary detection."""
    clean = clean_text(text)
    if not clean:
        return []
    # Split by sentence-ending punctuation followed by space or newline
    sentences = re.split(r'(?<=[.!?])\s+', clean)
    return [s.strip() for s in sentences if s.strip()]

def tokenize(text: str) -> List[str]:
    """Tokenize text into lowercase alphanumeric tokens."""
    return re.findall(r'\b[A-Za-z0-9_\-#]+\b', text.lower())

def preprocess_text(text: str) -> str:
    """Clean text and remove standard stopwords."""
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    filtered = [t for t in tokens if t not in STOPWORDS and len(t) >= 2]
    return " ".join(filtered)

def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> List[Dict[str, Any]]:
    """
    Split text into overlapping token chunks respecting sentence boundaries.
    Default: 512 tokens with 50-token overlap.
    """
    sentences = split_into_sentences(text)
    if not sentences:
        return []

    chunks = []
    current_sentences = []
    current_tokens = 0
    start_pos = 0

    for sentence in sentences:
        sent_tokens = len(sentence.split())
        if current_tokens + sent_tokens > chunk_size and current_sentences:
            chunk_str = " ".join(current_sentences)
            end_pos = start_pos + len(chunk_str)
            chunks.append({
                "chunk_index": len(chunks),
                "chunk_text": chunk_str,
                "token_count": current_tokens,
                "start_position": start_pos,
                "end_position": end_pos,
                "page_number": 1
            })
            # Carry over overlap
            overlap_sentences = []
            overlap_tokens = 0
            for s in reversed(current_sentences):
                s_toks = len(s.split())
                if overlap_tokens + s_toks <= overlap:
                    overlap_sentences.insert(0, s)
                    overlap_tokens += s_toks
                else:
                    break
            current_sentences = overlap_sentences + [sentence]
            current_tokens = overlap_tokens + sent_tokens
            start_pos = end_pos - len(" ".join(overlap_sentences)) if overlap_sentences else end_pos
        else:
            current_sentences.append(sentence)
            current_tokens += sent_tokens

    if current_sentences:
        chunk_str = " ".join(current_sentences)
        chunks.append({
            "chunk_index": len(chunks),
            "chunk_text": chunk_str,
            "token_count": current_tokens,
            "start_position": start_pos,
            "end_position": start_pos + len(chunk_str),
            "page_number": 1
        })

    return chunks
