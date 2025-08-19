import json

with open('/Users/anujthakkar/Documents/develop/daily_digest/database/daily_summaries/summaries_20250818.json', 'r') as f:
    data = json.load(f)

for topic, summary_data in data.items():
    print('\n',f"Topic: {topic}", '\n','-------------------------------------------------------------')
    print(f"Summary: {summary_data['summary']}",'\n')
    print(f"URLs: {', '.join(summary_data['urls'])}")