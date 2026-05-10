import json
import re
from collections import Counter, defaultdict

# Load the data
with open('yt_ginger_juice_1777107852603.json', 'r') as f:
    data = json.load(f)

videos = data['videos']

print("=" * 80)
print("GINGER JUICE YOUTUBE ANALYSIS - MARKETING INSIGHTS")
print("=" * 80)

# Parse views function
def parse_views(views_str):
    views_str = views_str.replace(',', '').replace('views', '').strip()
    if 'M' in views_str:
        return float(views_str.replace('M', '')) * 1_000_000
    elif 'K' in views_str:
        return float(views_str.replace('K', '')) * 1_000
    return float(views_str)

# 1. Video Statistics
print("\n" + "=" * 80)
print("1. VIDEO STATISTICS")
print("=" * 80)

total_views = sum(parse_views(v['views']) for v in videos)
print(f"Total Videos Analyzed: {len(videos)}")
print(f"Total Combined Views: {total_views:,.0f}")
print(f"Average Views per Video: {total_views/len(videos):,.0f}")

# Top 10 by views
print("\nTOP 10 VIDEOS BY VIEWS:")
sorted_videos = sorted(videos, key=lambda x: parse_views(x['views']), reverse=True)
for i, v in enumerate(sorted_videos[:10], 1):
    print(f"  {i}. {v['title'][:55]}...")
    print(f"     Views: {v['views']} | Channel: {v['channel']}")

# 2. Key Themes from Titles
print("\n" + "=" * 80)
print("2. KEY THEMES FROM VIDEO TITLES")
print("=" * 80)

title_keywords = [
    'anti-inflammatory', 'anti inflammatory', 'inflammation', 'immune', 'immunity',
    'detox', 'digestion', 'stomach', 'nausea', 'weight loss', 'weight', 'skin',
    'liver', 'heart', 'blood', 'cancer', 'diabetes', 'blood pressure', 'morning',
    'glowing', 'flat stomach', 'wellness', 'shot', 'shots'
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

# 3. Extract all transcript text
print("\n" + "=" * 80)
print("3. EXTRACTING TRANSCRIPT CONTENT...")
print("=" * 80)

all_transcript_text = ""
for v in videos:
    if v.get('transcript') and v['transcript'].get('fullText'):
        all_transcript_text += v['transcript']['fullText'] + " "

# 4. Key Health Claims from Transcripts
print("\n" + "=" * 80)
print("4. KEY HEALTH CLAIMS FROM TRANSCRIPTS")
print("=" * 80)

health_claims = [
    ('anti-inflammatory', r'anti-?inflammatory'),
    ('reduce inflammation', r'reduc(e|es|ed|ing)\s+inflammation'),
    ('nausea', r'nausea'),
    ('digestion', r'digest(ion|ive)'),
    ('immune', r'immune'),
    ('stomach', r'stomach'),
    ('muscle', r'muscle'),
    ('pain', r'pain'),
    ('arthritis', r'arthritis'),
    ('blood sugar', r'blood\s*sugar'),
    ('weight loss', r'weight\s*loss'),
    ('antioxidant', r'antioxidant'),
    ('gingerol', r'gingerol'),
    ('morning sickness', r'morning\s*sickness'),
    ('cold', r'\bcold\b'),
    ('flu', r'\bflu\b'),
    ('cancer', r'cancer'),
    ('heart', r'heart'),
    ('diabetes', r'diabetes'),
    ('blood pressure', r'blood\s*pressure'),
]

claim_counts = {}
for claim_name, pattern in health_claims:
    matches = re.findall(pattern, all_transcript_text, re.IGNORECASE)
    claim_counts[claim_name] = len(matches)

print("\nHealth claims mentioned in transcripts:")
for claim, count in sorted(claim_counts.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        print(f"  - {claim.upper()}: mentioned {count} times")

# 5. Key Compounds
print("\n" + "=" * 80)
print("5. KEY COMPOUNDS & NUTRIENTS")
print("=" * 80)

compounds = ['gingerol', 'shogaol', 'zingiberene', 'antioxidant', 'vitamin', 'magnesium', 
             'potassium', 'copper', 'manganese', 'fiber']

compound_counts = Counter()
for compound in compounds:
    count = all_transcript_text.lower().count(compound)
    compound_counts[compound] = count

print("\nCompound/nutrient mentions:")
for compound, count in compound_counts.most_common():
    if count > 0:
        print(f"  - {compound.upper()}: {count} mentions")

# 6. Ginger + Beetroot Specific Content
print("\n" + "=" * 80)
print("6. GINGER + BEETROOT COMBINATION CONTENT")
print("=" * 80)

ginger_beet_videos = []
for v in videos:
    title_lower = v['title'].lower()
    transcript_text = ""
    if v.get('transcript') and v['transcript'].get('fullText'):
        transcript_text = v['transcript']['fullText'].lower()
    
    if 'beet' in title_lower or 'beetroot' in title_lower or 'beet' in transcript_text:
        ginger_beet_videos.append(v)

print(f"\nVideos mentioning ginger + beetroot: {len(ginger_beet_videos)}")
for v in sorted(ginger_beet_videos, key=lambda x: parse_views(x['views']), reverse=True)[:5]:
    print(f"  - {v['title'][:50]}... ({v['views']})")

# 7. Extract specific claims with context
print("\n" + "=" * 80)
print("7. SPECIFIC CLAIMS WITH CONTEXT (MARKETING GOLD)")
print("=" * 80)

key_claim_patterns = [
    (r'ginger\s+(is|has|contains|can|helps?|reduces?|improves?)\s+\w+\s+\w+', 'benefit claims'),
    (r'(reduces?|lowers?|improves?|boosts?|fights?)\s+inflammation', 'inflammation claims'),
    (r'(helps?|aids?|improves?)\s+digestion', 'digestion claims'),
    (r'(immune|immunity)\s+(boost|support|system)', 'immune claims'),
    (r'\d+\s*(%|percent|times?|hours?|minutes?)', 'statistics'),
]

claims_with_context = defaultdict(list)
for v in videos:
    if not v.get('transcript') or not v['transcript'].get('fullText'):
        continue
    
    text = v['transcript']['fullText']
    sentences = re.split(r'[.!?]', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 30:
            continue
        
        for pattern, claim_type in key_claim_patterns:
            if re.search(pattern, sentence.lower()):
                claims_with_context[claim_type].append({
                    'text': sentence[:200],
                    'source': v['title'][:40],
                    'views': v['views']
                })
                break

for claim_type, claims in claims_with_context.items():
    print(f"\n{claim_type.upper()}:")
    for c in claims[:5]:
        print(f"  - \"{c['text'][:150]}...\"")
        print(f"    (Source: {c['source']}... - {c['views']})")

# 8. Target Audiences
print("\n" + "=" * 80)
print("8. TARGET AUDIENCE SEGMENTS")
print("=" * 80)

audiences = {
    'Morning Routine': ['morning', 'empty stomach', 'wake up', 'daily'],
    'Digestive Health': ['digestion', 'stomach', 'nausea', 'bloating', 'gut'],
    'Immune Support': ['immune', 'immunity', 'cold', 'flu', 'wellness'],
    'Weight Management': ['weight loss', 'flat stomach', 'metabolism'],
    'Skin/Beauty': ['skin', 'glowing', 'beauty', 'radiant'],
    'Pain/Inflammation': ['pain', 'inflammation', 'arthritis', 'joint'],
    'Pregnancy/Morning Sickness': ['pregnancy', 'morning sickness', 'pregnant'],
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

# 9. Save analysis
print("\n" + "=" * 80)
print("9. SAVING ANALYSIS...")
print("=" * 80)

ginger_report = {
    'summary': {
        'total_videos': len(videos),
        'total_views': total_views,
        'average_views': total_views/len(videos)
    },
    'top_videos': [{'title': v['title'], 'views': v['views'], 'url': v['url']} 
                   for v in sorted_videos[:15]],
    'theme_counts': {k: len(v) for k, v in theme_counts.items()},
    'claim_counts': claim_counts,
    'compound_mentions': dict(compound_counts),
    'ginger_beetroot_videos': [{'title': v['title'], 'views': v['views'], 'url': v['url']} 
                               for v in sorted(ginger_beet_videos, key=lambda x: parse_views(x['views']), reverse=True)]
}

with open('ginger_analysis_report.json', 'w') as f:
    json.dump(ginger_report, f, indent=2)

print("Ginger analysis saved to ginger_analysis_report.json")
print("\n" + "=" * 80)
print("GINGER ANALYSIS COMPLETE!")
print("=" * 80)