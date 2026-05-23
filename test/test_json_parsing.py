#!/usr/bin/env python3
"""
Test exact JSON parsing behavior
"""

import json

# Test the exact JSON response from our server
json_response = '{"success": true, "message": "Session cleared successfully"}'

print("🔍 TESTING JSON PARSING BEHAVIOR")
print("=" * 35)

print(f"Raw JSON string: {json_response}")

# Parse the JSON
data = json.loads(json_response)
print(f"Parsed data: {data}")
print(f"Data type: {type(data)}")

# Test the success field
print(f"Success field: {data['success']}")
print(f"Success field type: {type(data['success'])}")

# Test different comparison methods
print(f"data['success'] === True: {data['success'] is True}")
print(f"data['success'] == True: {data['success'] == True}")
print(f"bool(data['success']): {bool(data['success'])}")

# Test JavaScript-style truthiness
if data['success']:
    print("✅ Truthy check passed (JavaScript style)")
else:
    print("❌ Truthy check failed")

# Test strict comparison
if data['success'] is True:
    print("✅ Strict comparison passed (Python 'is')")
else:
    print("❌ Strict comparison failed")

# Test loose comparison
if data['success'] == True:
    print("✅ Loose comparison passed (Python '==')")
else:
    print("❌ Loose comparison failed")

print("\n💡 The issue is NOT with JSON parsing!")
print("The JSON response is perfectly valid and parseable.")
print("The problem must be elsewhere in the JavaScript flow.")
