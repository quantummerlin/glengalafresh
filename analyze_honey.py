import json
import re
from collections import Counter, defaultdict

# Load the data
with open('yt_honey_benefits_1777114862253.json', 'r') as f:
    data = json.load(f)

videos = data['videos']

print("=" * 80)
print("HONEY YOUTUBE ANALYSIS - MARKETING INSIGHTS")
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
    'benefits', 'health', 'raw', 'manuka', 'skin', 'diabetes', 'sugar',
    'wound', 'immune', 'digestion', 'weight', 'antibacterial', 'antimicrobial',
    'insulin', 'testosterone', 'cough', 'sore throat', 'energy', 'sleep',
    'antioxidant', 'liver', 'heart', 'blood'
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
    ('antioxidant', r'antioxidant'),
    ('antibacterial', r'antibacterial'),
    ('antimicrobial', r'antimicrobial'),
    ('anti-inflammatory', r'anti-?inflammatory'),
    ('wound', r'\bwound'),
    ('immune', r'immune'),
    ('digestion', r'digest(ion|ive)'),
    ('cough', r'\bcough'),
    ('sore throat', r'sore\s*throat'),
    ('sleep', r'\bsleep'),
    ('energy', r'\benergy\b'),
    ('skin', r'\bskin\b'),
    ('blood sugar', r'blood\s*sugar'),
    ('insulin', r'insulin'),
    ('diabetes', r'diabet'),
    ('heart', r'\bheart\b'),
    ('liver', r'\bliver\b'),
    ('weight', r'\bweight\b'),
    ('testosterone', r'testosterone'),
    ('honey', r'honey'),
    ('raw honey', r'raw\s*honey'),
    ('manuka', r'manuka'),
    ('sugar', r'\bsugar\b'),
    ('bacteria', r'\bbacteria'),
    ('infection', r'infection'),
    ('heal', r'\bheal'),
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

compounds = ['antioxidant', 'flavonoid', 'phenolic', 'enzyme', 'hydrogen peroxide',
             'glucose', 'fructose', 'vitamin', 'mineral', 'propolis', 'pollen',
             'amino acid', 'zinc', 'potassium', 'magnesium', 'iron']

compound_counts = Counter()
for compound in compounds:
    count = all_transcript_text.lower().count(compound)
    compound_counts[compound] = count

print("\nCompound/nutrient mentions:")
for compound, count in compound_counts.most_common():
    if count > 0:
        print(f"  - {compound.upper()}: {count} mentions")

# 6. Honey + Other Ingredients Content
print("\n" + "=" * 80)
print("6. HONEY COMBINATION CONTENT")
print("=" * 80)

honey_combo_videos = {'ginger': [], 'lemon': [], 'beetroot': [], 'cinnamon': [], 'warm water': []}
for v in videos:
    title_lower = v['title'].lower()
    transcript_text = ""
    if v.get('transcript') and v['transcript'].get('fullText'):
        transcript_text = v['transcript']['fullText'].lower()
    
    if 'ginger' in title_lower or 'ginger' in transcript_text:
        honey_combo_videos['ginger'].append(v)
    if 'lemon' in title_lower or 'lemon' in transcript_text:
        honey_combo_videos['lemon'].append(v)
    if 'beet' in title_lower or 'beetroot' in title_lower or 'beet' in transcript_text:
        honey_combo_videos['beetroot'].append(v)
    if 'cinnamon' in title_lower or 'cinnamon' in transcript_text:
        honey_combo_videos['cinnamon'].append(v)
    if 'warm water' in title_lower or 'warm water' in transcript_text or 'hot water' in transcript_text:
        honey_combo_videos['warm water'].append(v)

for combo, vids in honey_combo_videos.items():
    print(f"\nHoney + {combo.upper()}: {len(vids)} videos")
    for v in sorted(vids, key=lambda x: parse_views(x['views']), reverse=True)[:3]:
        print(f"  - {v['title'][:45]}... ({v['views']})")

# 7. Extract specific claims with context
print("\n" + "=" * 80)
print("7. SPECIFIC CLAIMS WITH CONTEXT")
print("=" * 80)

key_claim_patterns = [
    (r'(antibacterial|antimicrobial|anti-?inflammatory)', 'healing properties'),
    (r'(wound|burn|cut)\s*(heal|treat|help)', 'wound healing'),
    (r'(cough|sore\s*throat)', 'respiratory'),
    (r'(blood\s*sugar|insulin|diabet)', 'blood sugar'),
    (r'(improves?|boosts?|helps?)\s+(immune|digestion|energy|sleep)', 'health benefits'),
    (r'(raw|manuka)\s*honey', 'honey types'),
    (r'\d+\s*(%|percent|times?|spoon)', 'statistics'),
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
    for c in claims[:4]:
        print(f"  - \"{c['text'][:120]}...\"")
        print(f"    (Source: {c['source']}... - {c['views']})")

# 8. Target Audiences
print("\n" + "=" * 80)
print("8. TARGET AUDIENCE SEGMENTS")
print("=" * 80)

audiences = {
    'Immune Support': ['immune', 'cold', 'flu', 'sick'],
    'Wound/Skin Healing': ['wound', 'burn', 'cut', 'skin', 'heal'],
    'Respiratory Health': ['cough', 'throat', 'respiratory'],
    'Blood Sugar/Diabetes': ['blood sugar', 'insulin', 'diabet'],
    'Sleep/Relaxation': ['sleep', 'insomnia', 'relax'],
    'Digestive Health': ['digestion', 'stomach', 'gut'],
    'Energy/Fitness': ['energy', 'athlet', 'performance'],
    'Natural Remedy Seekers': ['natural', 'remedy', 'home', 'cure'],
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

honey_report = {
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
    'combo_videos': {k: [{'title': v['title'], 'views': v['views']} for v in vids] 
                     for k, vids in honey_combo_videos.items()}
}

with open('honey_analysis_report.json', 'w') as f:
    json.dump(honey_report, f, indent=2)

print("Honey analysis saved to honey_analysis_report.json")
print("\n" + "=" * 80)
print("HONEY ANALYSIS COMPLETE!")
print("=" * 80)