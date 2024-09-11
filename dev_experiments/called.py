import sys
import json

# Get the input from the command line
json_input = sys.argv[1]

# Parse the JSON input
data = json.loads(json_input)

print(f"Received input: {data}")