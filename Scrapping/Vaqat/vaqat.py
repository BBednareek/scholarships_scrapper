import json

with open("vaqat.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    Title = item['title']
    Description = item['description']
    Deadline = item['application_deadline'][:10]
    parts = Deadline.split('-')
    formatted_deadline = f"{parts[2]}.{parts[1]}.{parts[0]}"
    Category = 'Inne'
    Range = 'Ogólnopolskie'


