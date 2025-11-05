"""
Utility functions for VERA project
"""
import json


def json_to_jsonl(input_file, output_file):
    """
    Convert JSON array file to JSONL format (one JSON object per line)
    
    Args:
        input_file: Path to input JSON file (array format)
        output_file: Path to output JSONL file
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"Converted {len(data)} items from {input_file} to {output_file}")


def jsonl_to_json(input_file, output_file):
    """
    Convert JSONL file to JSON array format
    
    Args:
        input_file: Path to input JSONL file
        output_file: Path to output JSON file (array format)
    """
    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Converted {len(data)} items from {input_file} to {output_file}")


if __name__ == "__main__":
    # Example: Convert test_data.json to test_data.jsonl
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python utils.py <input_file> <output_file>")
        print("Example: python utils.py test_data.json test_data.jsonl")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if input_file.endswith('.json') and output_file.endswith('.jsonl'):
        json_to_jsonl(input_file, output_file)
    elif input_file.endswith('.jsonl') and output_file.endswith('.json'):
        jsonl_to_json(input_file, output_file)
    else:
        print("Error: Input/output file extensions must match (.json <-> .jsonl)")
        sys.exit(1)

