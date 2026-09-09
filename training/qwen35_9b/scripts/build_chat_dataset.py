import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with open(args.output, "w", encoding="utf-8") as out:
        for task in data:
            record = {
                "messages": [
                    {
                        "role": "user",
                        "content": task["instruction"]
                    },
                    {
                        "role": "assistant",
                        "content": task["output"]
                    }
                ]
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1

    print("Saved:", count)
    print("Output:", args.output)

if __name__ == "__main__":
    main()
