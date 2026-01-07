#!/usr/bin/env python3
"""
Module 6: Visual Recognition - Face Recognition Agent
======================================================

This demonstrates MULTI-MODAL RAG - applying the same RAG pattern from Module 2
to visual data instead of text.

The pattern is identical:
  Input → Embedding → Vector DB → Similarity Search → Result

Only the modality changes:
  Text (Module 2): "What is RAG?" → text-embedding-3-small → 1536d vector
  Image (Module 6): face.jpg → CLIP → 512d vector

Usage:
    # Register a person
    python face_recognition_agent.py --add-person path/to/photo.jpg --name "Gene Arnold" --note "Instructor"

    # Test recognition
    python face_recognition_agent.py --test-image path/to/test_photo.jpg

    # List all people
    python face_recognition_agent.py --list-people
"""

import argparse
from typing import List, Optional, Dict
from datetime import datetime

# Image processing
from PIL import Image

# CLIP embeddings
from transformers import CLIPProcessor, CLIPModel
import torch

# Vector database
import chromadb
from chromadb.config import Settings


# ============================================================================
# CONFIGURATION
# ============================================================================

# CLIP Model Configuration
# We use OpenAI's CLIP (Contrastive Language-Image Pre-training)
# Model: clip-vit-base-patch32 (512-dimensional embeddings)
CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"

# Match Threshold (Empirically tuned!)
# This is the most important parameter - see CONCEPTS.md for tuning process
#
# Our testing with CLIP + L2 distance showed:
#   - Same person, different photos: Distance 0.522 - 0.740
#   - Different people:              Distance 0.839 - 0.896+
#
# Threshold 0.80 provides perfect separation (sits in the 0.099 gap)
FACE_MATCH_THRESHOLD = 0.80

# Database Configuration
CHROMA_DB_PATH = "./faces_db"
COLLECTION_NAME = "face_embeddings"


# ============================================================================
# CLIP MODEL (Load once, use globally)
# ============================================================================

print("Loading CLIP model...")
clip_model = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
clip_processor = CLIPProcessor.from_pretrained(CLIP_MODEL_NAME)
clip_model.eval()  # Set to evaluation mode
print("CLIP model loaded!\n")


# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def initialize_chromadb() -> chromadb.Collection:
    """
    Initialize ChromaDB with L2 distance metric.

    CRITICAL: CLIP embeddings require L2 (Euclidean) distance, not cosine!
    This is configured via the metadata parameter.
    """
    client = chromadb.PersistentClient(
        path=CHROMA_DB_PATH,
        settings=Settings(anonymized_telemetry=False)
    )

    # Get or create collection with L2 distance metric
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "l2"}  # L2 distance for CLIP
    )

    print(f"✅ Connected to collection: {COLLECTION_NAME}")
    return collection


def generate_clip_embedding(image_path: str) -> Optional[List[float]]:
    """
    Generate CLIP embedding for an image.

    This is the equivalent of text_embedding_3_small for images!

    Args:
        image_path: Path to image file

    Returns:
        512-dimensional embedding vector, or None if failed
    """
    try:
        # Load image
        image = Image.open(image_path).convert("RGB")

        # Process image through CLIP
        inputs = clip_processor(images=image, return_tensors="pt")

        # Generate embedding (no gradients needed for inference)
        with torch.no_grad():
            features = clip_model.get_image_features(**inputs)

            # Normalize (CLIP convention)
            features = features / features.norm(dim=-1, keepdim=True)

            # Convert to list for ChromaDB
            embedding = features[0].cpu().numpy().tolist()

        return embedding

    except Exception as e:
        print(f"❌ Error generating embedding: {e}")
        return None


def add_person_to_database(
    collection: chromadb.Collection,
    image_path: str,
    name: str,
    note: str
) -> bool:
    """
    Add a person to the face database.

    This is the equivalent of adding a document to the text RAG database!

    Args:
        collection: ChromaDB collection
        image_path: Path to person's photo
        name: Person's name
        note: Note about the person

    Returns:
        True if successful, False otherwise
    """
    print(f"\n📸 Processing: {image_path}")

    # Generate embedding
    embedding = generate_clip_embedding(image_path)
    if embedding is None:
        return False

    print("✅ Generated CLIP embedding (512 dimensions)")

    # Create unique ID based on name and timestamp
    timestamp = datetime.now().isoformat()
    person_id = f"{name.lower().replace(' ', '_')}_{timestamp}"

    # Store in ChromaDB
    collection.add(
        ids=[person_id],
        embeddings=[embedding],
        metadatas=[{
            "name": name,
            "note": note,
            "image_path": image_path,
            "added_at": timestamp
        }]
    )

    print(f"✅ Added {name} to database")
    return True


def find_matching_person(
    collection: chromadb.Collection,
    test_embedding: List[float]
) -> Optional[Dict]:
    """
    Find matching person in database using similarity search.

    This is the equivalent of querying the text RAG database!

    Args:
        collection: ChromaDB collection
        test_embedding: CLIP embedding to search for

    Returns:
        Person data dict if match found, None otherwise
    """
    # Query for nearest neighbor
    results = collection.query(
        query_embeddings=[test_embedding],
        n_results=1
    )

    # Check if we have results
    if not results["distances"] or len(results["distances"][0]) == 0:
        return None

    distance = results["distances"][0][0]
    metadata = results["metadatas"][0][0]

    # Apply threshold
    if distance < FACE_MATCH_THRESHOLD:
        # Match found!
        return {
            "name": metadata["name"],
            "note": metadata["note"],
            "distance": distance,
            "confidence": 1.0 - (distance / FACE_MATCH_THRESHOLD)
        }
    else:
        # No match (return distance for debugging)
        return None


def list_all_people(collection: chromadb.Collection) -> List[Dict]:
    """List all people in the database."""
    try:
        results = collection.get(include=["metadatas"])

        # Group by person name (same person might have multiple photos)
        people_dict = {}
        for metadata in results["metadatas"]:
            name = metadata["name"]
            if name not in people_dict:
                people_dict[name] = {
                    "name": name,
                    "note": metadata["note"],
                    "added_at": metadata["added_at"],
                    "count": 1
                }
            else:
                people_dict[name]["count"] += 1

        return list(people_dict.values())

    except Exception as e:
        print(f"❌ Error listing people: {e}")
        return []


# ============================================================================
# MAIN CLI
# ============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Face Recognition Agent - Multi-modal RAG with CLIP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Register a person
  python face_recognition_agent.py --add-person photo.jpg --name "Gene Arnold" --note "Instructor"

  # Test recognition
  python face_recognition_agent.py --test-image test_photo.jpg

  # List all people
  python face_recognition_agent.py --list-people
        """
    )

    parser.add_argument(
        "--add-person",
        metavar="IMAGE_PATH",
        help="Add a person to the database"
    )
    parser.add_argument(
        "--name",
        help="Person's name (required with --add-person)"
    )
    parser.add_argument(
        "--note",
        help="Note about the person (required with --add-person)"
    )
    parser.add_argument(
        "--test-image",
        metavar="IMAGE_PATH",
        help="Test recognition with an image"
    )
    parser.add_argument(
        "--list-people",
        action="store_true",
        help="List all people in database"
    )

    args = parser.parse_args()

    # Display configuration
    print(f"CLIP Model: {CLIP_MODEL_NAME}")
    print(f"Embedding Dimensions: 512")
    print(f"Distance Metric: L2 (Euclidean)")
    print(f"Match Threshold: {FACE_MATCH_THRESHOLD}\n")

    # Initialize database
    collection = initialize_chromadb()

    # Route to appropriate function
    if args.add_person:
        # Validate required arguments
        if not args.name or not args.note:
            print("❌ Error: --name and --note are required with --add-person")
            parser.print_help()
            return

        # Add person
        success = add_person_to_database(
            collection,
            args.add_person,
            args.name,
            args.note
        )

        if success:
            print(f"\n🎉 Successfully added {args.name}!")
        else:
            print(f"\n❌ Failed to add {args.name}")

    elif args.test_image:
        # Test recognition
        print(f"\n🧪 Testing recognition with: {args.test_image}\n")

        # Generate embedding
        embedding = generate_clip_embedding(args.test_image)
        if embedding is None:
            print("❌ Failed to generate embedding")
            return

        print("✅ Embedding generated!")
        print("🔍 Searching database...\n")

        # Search for match
        person_data = find_matching_person(collection, embedding)

        if person_data:
            # Match found!
            print("=" * 60)
            print(f"✅ MATCH FOUND!")
            print("=" * 60)
            print(f"Name:       {person_data['name']}")
            print(f"Note:       {person_data['note']}")
            print(f"Distance:   {person_data['distance']:.3f}")
            print(f"Confidence: {person_data['confidence']:.1%}")
            print("=" * 60)
        else:
            # No match - show debug info
            print("=" * 60)
            print("❓ NO MATCH FOUND")
            print("=" * 60)

            # Get closest match for debugging
            results = collection.query(
                query_embeddings=[embedding],
                n_results=1
            )

            if results["distances"] and len(results["distances"][0]) > 0:
                closest_distance = results["distances"][0][0]
                closest_name = results["metadatas"][0][0]["name"]
                print(f"Closest match: {closest_name}")
                print(f"Distance:      {closest_distance:.3f}")
                print(f"Threshold:     {FACE_MATCH_THRESHOLD}")
                print(f"Gap:           {closest_distance - FACE_MATCH_THRESHOLD:.3f}")
            else:
                print("(Database is empty)")

            print("=" * 60)

    elif args.list_people:
        # List all people
        people = list_all_people(collection)

        print(f"\n📋 People in database: {len(people)}")
        print("=" * 70)

        if people:
            for person in people:
                print(f"Name:     {person['name']}")
                print(f"Note:     {person['note']}")
                print(f"Photos:   {person['count']}")
                print(f"Added:    {person['added_at'][:10]}")
                print("-" * 70)
        else:
            print("(Database is empty)")

    else:
        # No arguments - show help
        parser.print_help()


if __name__ == "__main__":
    main()
