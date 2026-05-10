import json
import re
from collections import Counter, defaultdict

# Load datasets
datasets = {}
for name, filename in [('celery', 'yt_celery_juice_1777112787207.json'), 
                        ('turmeric', 'yt_turmeric_juice_1777185453824.json')]:
    with open(filename, 'r') as f:
        datasets[name] = json.load(f)

print("=" * 80)
print("CELERY & TURMERIC YOUTUBE ANALYSIS")
print("=" * 80)

def parse_views(views_str):
    views_str = views_str.replace(',', '').replace('views', '').strip()
    if 'M' in views_str:
        return float(views_str.replace('M', '')) * 1_000_000
    elif 'K' in views_str:
        return float(views_str.replace('K', '')) * 1_000
    return float(views_str)

for ingredient, data in datasets.items():
    print(f"\n{'=' * 80}")
    print(f"{ingredient.upper()} ANALYSIS")
    print("=" * 80)
    
    videos = data['videos']
    
    # Stats
    total_views = sum(parse_views(v['views']) for v in videos)
    print(f"\n📊 STATISTICS:")
    print(f"  Total Videos: {len(videos)}")
    print(f"  Total Views: {total_views:,.0f}")
    print(f"  Average Views: {total_views/len(videos):,.0f}")
    
    # Top 10 videos
    print(f"\n🎬 TOP 10 VIDEOS:")
    sorted_videos = sorted(videos, key=lambda x: parse_views(x['views']), reverse=True)
    for i, v in enumerate(sorted_videos[:10], 1):
        print(f"  {i}. {v['title'][:50]}... ({v['views']})")
    
    # Transcript analysis
    all_text = ""
    for v in videos:
        if v.get('transcript') and v['transcript'].get('fullText'):
            all_text += v['transcript']['fullText'] + " "
    
    # Health claims
    if ingredient == 'celery':
        claims = ['detox', 'liver', 'kidney', 'digest', 'gut', 'stomach', 'bloating', 
                  'inflammation', 'blood pressure', 'skin', 'energy', 'weight', 'morning',
                  '7 days', '7-day', 'medical medium', 'cleanse', 'hydrat', 'sodium',
                  'electrolyte', 'potassium', 'vitamin k', 'folate', 'magnesium']
    else:  # turmeric
        claims = ['anti-inflammatory', 'inflammation', 'curcumin', 'immune', 'arthritis',
                  'joint', 'pain', 'brain', 'heart', 'liver', 'detox', 'skin', 'cancer',
                  'antioxidant', 'golden milk', 'turmeric', 'ginger', 'black pepper',
                  'absorption', 'bioavailability', 'diabetes', 'weight', 'mood', 'depression']
    
    print(f"\n💊 KEY HEALTH CLAIMS IN TRANSCRIPTS:")
    for claim in claims:
        count = len(re.findall(claim, all_text, re.IGNORECASE))
        if count > 0:
            print(f"  - {claim.upper()}: {count} mentions")
    
    # Title patterns
    print(f"\n📝 TITLE PATTERNS:")
    patterns = {
        '7 Days Challenge': r'7\s*day',
        'Question Format': r'\?|what happens|should you|is ',
        'Personal Story': r'i drank|i tried|my (experience|journey|review)',
        'Medical/Doctor': r'dr\.|doctor|medical',
        'How To': r'how to|recipe|make',
        'Mistakes/Warnings': r'mistake|avoid|warning|stop|never|side effect'
    }
    
    for pattern_name, pattern in patterns.items():
        count = sum(1 for v in videos if re.search(pattern, v['title'].lower()))
        if count > 0:
            pattern_views = sum(parse_views(v['views']) for v in videos if re.search(pattern, v['title'].lower()))
            avg = pattern_views / count
            print(f"  - {pattern_name}: {count} videos, {pattern_views:,.0f} total views, {avg:,.0f} avg")

# Cross-product analysis
print(f"\n{'=' * 80}")
print("CROSS-PRODUCT SYNERGY")
print("=" * 80)

print("\n🔗 CELERY + OTHER INGREDIENTS MENTIONED:")
for ingredient, data in datasets.items():
    if ingredient == 'celery':
        all_text = ""
        for v in data['videos']:
            if v.get('transcript') and v['transcript'].get('fullText'):
                all_text += v['transcript']['fullText'].lower() + " "
        
        combos = ['ginger', 'lemon', 'honey', 'turmeric', 'beetroot', 'beet', 'apple', 'cucumber']
        for combo in combos:
            count = all_text.count(combo)
            if count > 0:
                print(f"  - Celery + {combo.upper()}: {count} mentions")

print("\n🔗 TURMERIC + OTHER INGREDIENTS MENTIONED:")
for ingredient, data in datasets.items():
    if ingredient == 'turmeric':
        all_text = ""
        for v in data['videos']:
            if v.get('transcript') and v['transcript'].get('fullText'):
                all_text += v['transcript']['fullText'].lower() + " "
        
        combos = ['ginger', 'lemon', 'honey', 'cayenne', 'chilli', 'black pepper', 'pineapple', 'orange', 'carrot']
        for combo in combos:
            count = all_text.count(combo)
            if count > 0:
                print(f"  - Turmeric + {combo.upper()}: {count} mentions")

# Save reports
for ingredient, data in datasets.items():
    videos = data['videos']
    total_views = sum(parse_views(v['views']) for v in videos)
    sorted_videos = sorted(videos, key=lambda x: parse_views(x['views']), reverse=True)
    
    report = {
        'ingredient': ingredient,
        'summary': {
            'total_videos': len(videos),
            'total_views': total_views,
            'average_views': total_views/len(videos)
        },
        'top_videos': [{'title': v['title'], 'views': v['views'], 'url': v['url']} 
                       for v in sorted_videos[:15]]
    }
    
    with open(f'{ingredient}_analysis_report.json', 'w') as f:
        json.dump(report, f, indent=2)

print(f"\n{'=' * 80}")
print("ANALYSIS COMPLETE - Reports saved!")
print("=" * 80)