# Module 6: Visual Recognition - Face Recognition Agent

## Overview

This module demonstrates **multi-modal RAG** - applying the same RAG architecture you learned in Module 2, but with images instead of text. Instead of storing text embeddings in a vector database, we store image embeddings for face recognition.

## What You'll Build

A face recognition system that can:
- Register people by adding their photos to a vector database
- Recognize registered people in new photos
- Reject unknown faces with confidence
- Use CLIP (Contrastive Language-Image Pre-training) for robust image embeddings

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Test with Public Figure Photos

The `../test_photos/` directory contains publicly available photos of Arnold Schwarzenegger and Elon Musk for testing.

**Register Arnold (3 photos):**
```bash
python face_recognition_agent.py --add-person ../test_photos/arnold_schwarzenegger/arnold_001.jpg --name "Arnold Schwarzenegger" --note "Austrian-American actor and politician"

python face_recognition_agent.py --add-person ../test_photos/arnold_schwarzenegger/arnold_002.jpeg --name "Arnold Schwarzenegger" --note "Additional photo"

python face_recognition_agent.py --add-person ../test_photos/arnold_schwarzenegger/arnold_003.jpeg --name "Arnold Schwarzenegger" --note "Additional photo"
```

**Test Recognition (4th photo):**
```bash
python face_recognition_agent.py --test-image ../test_photos/arnold_schwarzenegger/arnold_005.jpg
```

Expected: Should recognize Arnold (distance ~0.344)

**Test Unknown Person (Elon, not yet registered):**
```bash
python face_recognition_agent.py --test-image ../test_photos/elon_musk/Elon_Musk_001.jpg
```

Expected: Should say "No match found" (distance to Arnold ~0.976)

**Register Elon (3 photos):**
```bash
python face_recognition_agent.py --add-person ../test_photos/elon_musk/Elon_Musk_001.jpg --name "Elon Musk" --note "Entrepreneur and business magnate"

python face_recognition_agent.py --add-person ../test_photos/elon_musk/Elon_Musk_002.jpg --name "Elon Musk" --note "Additional photo"

python face_recognition_agent.py --add-person ../test_photos/elon_musk/Elon_Musk_003.jpg --name "Elon Musk" --note "Additional photo"
```

**Test Recognition (4th photo):**
```bash
python face_recognition_agent.py --test-image ../test_photos/elon_musk/Elon_Musk_004.jpg
```

Expected: Should recognize Elon (distance ~0.151)

### 3. Register Yourself (Optional)

**Option A: Use Webcam**
```bash
python register_with_webcam.py
```

Follow the prompts to capture 3 photos of yourself.

**Option B: Use Existing Photos**
```bash
python face_recognition_agent.py --add-person /path/to/your/photo.jpg --name "Your Name" --note "Any notes"
```

**Tip:** Register 3-5 different photos of yourself (different angles, lighting) for better recognition.

## Architecture

This system follows the **RAG pattern**:

```
Query Image → CLIP Encoder → 512d Vector → ChromaDB (L2 Search) → Match/No Match
```

**Key Components:**
- **CLIP Model:** `openai/clip-vit-base-patch32` (512-dimensional embeddings)
- **Vector Database:** ChromaDB with L2 (Euclidean) distance metric
- **Threshold:** 0.80 (empirically tuned - see below)

## The Threshold Problem: A Real Learning Experience

One of the most valuable lessons in this module is **empirical threshold tuning**. You can't just pick a random threshold - you need to test with real data.

### How the Threshold Was Found

1. **Initial Testing (Same Person):**
   - Same photo: distance 0.000 (perfect match)
   - Different photos of same person: 0.522 - 0.740

2. **Testing Different People:**
   - Different people: 0.839 - 0.896+

3. **Finding the Gap:**
   - Same person max: 0.740
   - Different people min: 0.839
   - Gap: 0.099

4. **Setting the Threshold:**
   - Chose 0.80 (in the middle of the gap)
   - **Result:** 100% accuracy on test cases

### Your Task: Experiment

Try different thresholds and observe the results:
- **Too High (e.g., 2.0):** False positives (everyone matches)
- **Too Low (e.g., 0.3):** False negatives (can't recognize same person)
- **Just Right (0.80):** Reliable separation

## Files

- **[face_recognition_agent.py](face_recognition_agent.py)** - Main agent with CLIP implementation
- **[register_with_webcam.py](register_with_webcam.py)** - Helper script for webcam registration
- **[requirements.txt](requirements.txt)** - Python dependencies
- **faces_db/** - ChromaDB database (created at runtime)
- **logs/** - JSON interaction logs (created at runtime)

## Command Line Arguments

```bash
# Register a person
python face_recognition_agent.py --add-person <image_path> --name <name> --note <note>

# Test recognition
python face_recognition_agent.py --test-image <image_path>

# Interactive mode
python face_recognition_agent.py
```

## Understanding the Output

When testing an image, you'll see:

```
Distance to match: 0.344
```

**Distance Interpretation:**
- **< 0.80:** Match found (recognized person)
- **≥ 0.80:** No match (unknown person)

Lower distance = stronger match.

## Key Concepts

1. **Multi-modal RAG:** Same architecture as text RAG, different modality
2. **CLIP Embeddings:** 512 dimensions (vs 1536 for text in Module 2)
3. **L2 Distance:** Euclidean distance (different from cosine similarity)
4. **Threshold Tuning:** Empirical process based on real test data
5. **Vector Database:** ChromaDB configured for L2 metric

## Common Issues

**Issue:** Recognition fails for similar lighting/angles
**Solution:** Register more diverse photos (3-5 minimum)

**Issue:** False positives (wrong person recognized)
**Solution:** Lower the threshold (but test to avoid false negatives)

**Issue:** False negatives (can't recognize registered person)
**Solution:** Raise the threshold or register more photos

## Next Steps

1. Complete the testing exercises above
2. Experiment with different thresholds (modify `FACE_MATCH_THRESHOLD` in face_recognition_agent.py)
3. Try registering multiple people and testing cross-recognition
4. Read [CONCEPTS.md](../CONCEPTS.md) for deeper understanding
5. See [PROJECT.md](../PROJECT.md) for implementation details

## Learning Objectives

By completing this module, you'll understand:
- How to apply RAG patterns to non-text data
- Multi-modal embeddings with CLIP
- Vector database configuration for different distance metrics
- Empirical threshold tuning methodology
- Real-world challenges in computer vision systems

---

**Note:** This module uses publicly available photos of Arnold Schwarzenegger and Elon Musk for testing purposes only (educational use). All photos are sourced from publicly available online images.
