import json
import re
from collections import Counter, defaultdict

# Load the data
with open('yt_beetroot_juice_1777097248207.json', 'r') as f:
    data = json.load(f)

videos = data['videos']

print("=" * 80)
print("BEETROOT JUICE YOUTUBE ANALYSIS - MARKETING INSIGHTS")
print("=" * 80)

# 1. Video Statistics
print("\n" + "=" * 80)
print("1. VIDEO STATISTICS")
print("=" * 80)

def parse_views(views_str):
    """Parse views string to number"""
    views_str = views_str.replace(',', '').replace('views', '').strip()
    if 'M' in views_str:
        return float(views_str.replace('M', '')) * 1_000_000
    elif 'K' in views_str:
        return float(views_str.replace('K', '')) * 1_000
    return float(views_str)

total_views = sum(parse_views(v['views']) for v in videos)
print(f"Total Videos Analyzed: {len(videos)}")
print(f"Total Combined Views: {total_views:,.0f}")
print(f"Average Views per Video: {total_views/len(videos):,.0f}")

# Top 10 by views
print("\nTOP 10 VIDEOS BY VIEWS:")
sorted_videos = sorted(videos, key=lambda x: parse_views(x['views']), reverse=True)
for i, v in enumerate(sorted_videos[:10], 1):
    print(f"  {i}. {v['title'][:60]}...")
    print(f"     Views: {v['views']} | Channel: {v['channel']}")

# 2. Key Themes from Titles
print("\n" + "=" * 80)
print("2. KEY THEMES FROM VIDEO TITLES")
print("=" * 80)

title_keywords = [
    'blood pressure', 'stamina', 'performance', 'liver', 'detox', 'heart',
    'energy', 'muscle', 'exercise', 'workout', 'athlete', 'cycling', 'gym',
    'skin', 'brain', 'dementia', 'cancer', 'cholesterol', 'diabetes', 'erectile',
    'viagra', 'blood flow', 'oxygen', 'endurance', 'fitness', 'sport'
]

theme_counts = defaultdict(list)
for v in videos:
    title_lower = v['title'].lower()
    for keyword in title_keywords:
        if keyword in title_lower:
            theme_counts[keyword].append(v)

print("\nThemes found in video titles:")
for theme, vids in sorted(theme_counts.items(), key=lambda x: len(x[1]), reverse=True):
    total_theme_views = sum(parse_views(vv['views']) for vv in vids)
    print(f"  - {theme.upper()}: {len(vids)} videos, {total_theme_views:,.0f} total views")

# 3. Extract Key Claims from Transcripts
print("\n" + "=" * 80)
print("3. KEY HEALTH CLAIMS FROM TRANSCRIPTS")
print("=" * 80)

health_claims = []
claim_patterns = [
    r'lower[s]? blood pressure',
    r'boost[s]? stamina',
    r'increases? stamina',
    r'improves? athletic',
    r'improves? performance',
    r'increases? energy',
    r'detoxifies? the liver',
    r'liver detox',
    r'lowers? cholesterol',
    r'prevents? cancer',
    r'fight[s]? cancer',
    r'improves? brain',
    r'prevents? dementia',
    r'boost[s]? cognitive',
    r'improves? blood flow',
    r'increases? nitric oxide',
    r'rich in nitrates',
    r'improves? exercise',
    r'endurance',
    r'oxygen',
    r'athlete',
]

all_transcript_text = ""
for v in videos:
    if v.get('transcript') and v['transcript'].get('fullText'):
        all_transcript_text += v['transcript']['fullText'] + " "

# Find sentences with key claims
sentences = re.split(r'[.!?]', all_transcript_text)
claim_sentences = defaultdict(list)

for sentence in sentences:
    sentence = sentence.strip()
    if len(sentence) > 20:
        for pattern in claim_patterns:
            if re.search(pattern, sentence.lower()):
                claim_sentences[pattern].append(sentence)
                break

print("\nTop health claims found in transcripts:")
for claim, sentences in sorted(claim_sentences.items(), key=lambda x: len(x[1]), reverse=True)[:15]:
    print(f"\n  {claim.upper()}: Found {len(sentences)} times")
    # Show one example
    if sentences:
        example = sentences[0][:200] + "..." if len(sentences[0]) > 200 else sentences[0]
        print(f"    Example: \"{example}\"")

# 4. Sports/Performance Specific Content
print("\n" + "=" * 80)
print("4. SPORTS & PERFORMANCE CONTENT (GREAT FOR GYM/TEAM PITCHES)")
print("=" * 80)

sports_keywords = ['athlete', 'exercise', 'workout', 'gym', 'cycling', 'cyclist', 
                   'performance', 'stamina', 'endurance', 'sport', 'training', 'fitness']

sports_videos = []
for v in videos:
    title_lower = v['title'].lower()
    transcript_text = ""
    if v.get('transcript') and v['transcript'].get('fullText'):
        transcript_text = v['transcript']['fullText'].lower()
    
    for kw in sports_keywords:
        if kw in title_lower or kw in transcript_text:
            sports_videos.append(v)
            break

print(f"\nVideos with sports/performance content: {len(sports_videos)}")
for v in sorted(sports_videos, key=lambda x: parse_views(x['views']), reverse=True)[:8]:
    print(f"  - {v['title'][:55]}... ({v['views']})")

# 5. Extract Specific Statistics and Numbers
print("\n" + "=" * 80)
print("5. SPECIFIC STATISTICS MENTIONED (GREAT FOR MARKETING)")
print("=" * 80)

# Look for percentages and numbers
stat_patterns = [
    r'\d+%\s*(reduction|decrease|increase|improvement|lower)',
    r'\d+\s*(percent|%)',
    r'\d+\s*(hours?|minutes?|days?|weeks?)\s*(before|after|later)',
    r'up to\s*\d+%',
    r'by\s*\d+%',
]

stats_found = []
for v in videos:
    if v.get('transcript') and v['transcript'].get('fullText'):
        text = v['transcript']['fullText']
        for pattern in stat_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                stats_found.append({
                    'stat': m if isinstance(m, str) else ' '.join(m),
                    'video': v['title'],
                    'channel': v['channel']
                })

print("\nStatistics found in transcripts:")
for s in stats_found[:15]:
    print(f"  - \"{s['stat']}\" (from: {s['video'][:40]}...)")

# 6. Key Nutrients Mentioned
print("\n" + "=" * 80)
print("6. NUTRIENTS & COMPOUNDS MENTIONED")
print("=" * 80)

nutrients = ['nitrate', 'nitric oxide', 'potassium', 'magnesium', 'iron', 'folate', 
             'vitamin', 'betaine', 'betalain', 'antioxidant', 'fiber']

nutrient_counts = Counter()
for nutrient in nutrients:
    count = all_transcript_text.lower().count(nutrient)
    nutrient_counts[nutrient] = count

print("\nNutrient mentions across all transcripts:")
for nutrient, count in nutrient_counts.most_common():
    print(f"  - {nutrient.upper()}: mentioned {count} times")

# 7. Audience Segments
print("\n" + "=" * 80)
print("7. TARGET AUDIENCE SEGMENTS IDENTIFIED")
print("=" * 80)

audiences = {
    'Athletes/Fitness': ['athlete', 'exercise', 'workout', 'gym', 'training', 'fitness', 'performance'],
    'Cyclists': ['cycling', 'cyclist', 'bike'],
    'Heart Health': ['blood pressure', 'heart', 'cardiovascular'],
    'Seniors (50+)': ['over 50', 'over 60', 'senior', 'elderly', 'age'],
    'Detox/Liver Health': ['detox', 'liver', 'cleanse'],
    'Brain Health': ['brain', 'dementia', 'cognitive', 'memory'],
    'Diabetics': ['diabetes', 'diabetic', 'blood sugar'],
}

for audience, keywords in audiences.items():
    matching_videos = []
    for v in videos:
        text = (v['title'] + ' ' + (v.get('transcript', {}).get('fullText', ''))).lower()
        for kw in keywords:
            if kw in text:
                matching_videos.append(v)
                break
    total_audience_views = sum(parse_views(vv['views']) for vv in matching_videos)
    print(f"  {audience}: {len(matching_videos)} videos, {total_audience_views:,.0f} total views")

# 8. Save detailed analysis to file
print("\n" + "=" * 80)
print("8. SAVING DETAILED ANALYSIS...")
print("=" * 80)

# Create a comprehensive report
report = {
    'summary': {
        'total_videos': len(videos),
        'total_views': total_views,
        'average_views': total_views/len(videos)
    },
    'top_videos': [{'title': v['title'], 'views': v['views'], 'url': v['url']} 
                   for v in sorted_videos[:20]],
    'themes': {k: len(v) for k, v in theme_counts.items()},
    'nutrients_mentioned': dict(nutrient_counts),
    'sports_videos': [{'title': v['title'], 'views': v['views'], 'url': v['url']} 
                      for v in sorted(sports_videos, key=lambda x: parse_views(x['views']), reverse=True)]
}

with open('beetroot_analysis_report.json', 'w') as f:
    json.dump(report, f, indent=2)

print("Analysis saved to beetroot_analysis_report.json")
print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)