import json
import re
from collections import Counter
from datetime import datetime

def parse_views(views_str):
    """Parse view count string to integer"""
    if not views_str:
        return 0
    views_str = views_str.lower().replace(',', '').strip()
    match = re.match(r'([\d.]+)\s*([km]?)', views_str)
    if match:
        num = float(match.group(1))
        multiplier = match.group(2)
        if multiplier == 'm':
            return int(num * 1_000_000)
        elif multiplier == 'k':
            return int(num * 1_000)
        return int(num)
    return 0

def analyze_dataset(filepath, ingredient_name):
    """Analyze a YouTube dataset"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    videos = data.get('videos', [])
    total_views = sum(parse_views(v.get('views', '0')) for v in videos)
    
    # Duration analysis
    durations = []
    for v in videos:
        dur = v.get('duration', '0:00')
        parts = dur.split(':')
        if len(parts) == 2:
            minutes, seconds = int(parts[0]), int(parts[1])
            durations.append(minutes * 60 + seconds)
        elif len(parts) == 3:
            hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
            durations.append(hours * 3600 + minutes * 60 + seconds)
    
    avg_duration = sum(durations) / len(durations) if durations else 0
    
    # Channel analysis
    channels = Counter(v.get('channel', 'Unknown') for v in videos)
    
    # Title patterns
    titles = [v.get('title', '') for v in videos]
    title_words = []
    for t in titles:
        words = re.findall(r'\b[a-zA-Z]{4,}\b', t.lower())
        title_words.extend(words)
    common_title_words = Counter(title_words).most_common(15)
    
    # Transcript analysis
    health_keywords = [
        'detox', 'cleanse', 'immune', 'inflammation', 'anti-inflammatory',
        'antioxidant', 'energy', 'digestion', 'gut', 'liver', 'kidney',
        'heart', 'blood', 'pressure', 'sugar', 'diabetes', 'weight loss',
        'metabolism', 'bacteria', 'virus', 'infection', 'healing', 'cure',
        'benefits', 'health', 'nutrients', 'vitamins', 'minerals',
        'pain', 'relief', 'natural', 'remedy', 'cure', 'treatment',
        'cancer', 'disease', 'prevent', 'boost', 'support'
    ]
    
    synergy_keywords = {
        'beetroot': ['beetroot', 'beet', 'beets'],
        'ginger': ['ginger', 'ginger root'],
        'lemon': ['lemon', 'lemon juice', 'citrus'],
        'honey': ['honey', 'raw honey'],
        'turmeric': ['turmeric', 'curcumin'],
        'celery': ['celery', 'celery juice'],
        'cayenne': ['cayenne', 'cayenne pepper', 'capsaicin', 'chilli', 'chili'],
        'apple_cider_vinegar': ['apple cider vinegar', 'acv'],
        'ozone': ['ozone', 'ozonated', 'o3']
    }
    
    found_health_claims = Counter()
    found_synergies = Counter()
    full_transcripts = []
    
    for v in videos:
        transcript = v.get('transcript', {})
        if isinstance(transcript, dict):
            text = transcript.get('fullText', '')
        else:
            text = str(transcript)
        
        full_transcripts.append(text.lower())
        
        # Find health keywords
        for keyword in health_keywords:
            if keyword in text.lower():
                found_health_claims[keyword] += 1
        
        # Find synergies
        for ingredient, keywords in synergy_keywords.items():
            for kw in keywords:
                if kw in text.lower():
                    found_synergies[ingredient] += 1
                    break
    
    # Unique health claims from transcripts
    unique_claims = []
    claim_patterns = [
        r'(\w+)\s+(?:helps?|aids?|supports?|boosts?|improves?|reduces?|prevents?|fights?)\s+(\w+)',
        r'(?:good|great|best)\s+for\s+(\w+)',
        r'(?:cure|treat|heal)s?\s+(\w+)',
        r'(?:anti-?\w+)',
        r'(?:high|rich)\s+in\s+(\w+)',
    ]
    
    for text in full_transcripts:
        for pattern in claim_patterns:
            matches = re.findall(pattern, text)
            unique_claims.extend(matches)
    
    # Most viewed videos
    sorted_videos = sorted(videos, key=lambda x: parse_views(x.get('views', '0')), reverse=True)
    top_videos = []
    for v in sorted_videos[:10]:
        top_videos.append({
            'title': v.get('title', ''),
            'channel': v.get('channel', ''),
            'views': parse_views(v.get('views', '0')),
            'views_str': v.get('views', ''),
            'url': v.get('url', '')
        })
    
    # Content themes
    themes = {
        'recipe': 0,
        'benefits': 0,
        'tutorial': 0,
        'challenge': 0,
        'weight_loss': 0,
        'detox': 0,
        'medical': 0,
        'mistake': 0,
        'science': 0
    }
    
    for t in titles:
        t_lower = t.lower()
        if 'recipe' in t_lower or 'how to' in t_lower or 'make' in t_lower:
            themes['recipe'] += 1
        if 'benefit' in t_lower or 'why' in t_lower:
            themes['benefits'] += 1
        if 'mistake' in t_lower or 'wrong' in t_lower or 'stop' in t_lower or 'don\'t' in t_lower:
            themes['mistake'] += 1
        if 'challenge' in t_lower or 'day' in t_lower or 'week' in t_lower:
            themes['challenge'] += 1
        if 'weight' in t_lower or 'fat' in t_lower or 'loss' in t_lower:
            themes['weight_loss'] += 1
        if 'detox' in t_lower or 'cleanse' in t_lower:
            themes['detox'] += 1
        if 'dr' in t_lower or 'doctor' in t_lower or 'medical' in t_lower:
            themes['medical'] += 1
        if 'science' in t_lower or 'study' in t_lower or 'research' in t_lower:
            themes['science'] += 1
    
    return {
        'ingredient': ingredient_name,
        'total_videos': len(videos),
        'total_views': total_views,
        'avg_views': total_views // len(videos) if videos else 0,
        'avg_duration_seconds': avg_duration,
        'avg_duration_formatted': f"{int(avg_duration // 60)}:{int(avg_duration % 60):02d}",
        'top_channels': channels.most_common(10),
        'common_title_words': common_title_words,
        'health_claims_found': found_health_claims.most_common(20),
        'synergies_found': found_synergies.most_common(15),
        'top_videos': top_videos,
        'content_themes': themes,
        'unique_claims': Counter(unique_claims).most_common(20)
    }

# Analyze both datasets
print("=" * 60)
print("ANALYZING CAYENNE DATASET")
print("=" * 60)

cayenne_report = analyze_dataset('yt_cayenne_juice_1777187913287.json', 'Cayenne')

print(f"\n📊 CAYENNE OVERVIEW:")
print(f"   Videos: {cayenne_report['total_videos']}")
print(f"   Total Views: {cayenne_report['total_views']:,}")
print(f"   Average Views: {cayenne_report['avg_views']:,}")
print(f"   Avg Duration: {cayenne_report['avg_duration_formatted']}")

print(f"\n📺 TOP CHANNELS:")
for channel, count in cayenne_report['top_channels'][:5]:
    print(f"   - {channel}: {count} videos")

print(f"\n🔥 HEALTH CLAIMS FOUND:")
for claim, count in cayenne_report['health_claims_found'][:10]:
    print(f"   - {claim}: {count} mentions")

print(f"\n🤝 SYNERGIES WITH OTHER INGREDIENTS:")
for ingredient, count in cayenne_report['synergies_found']:
    print(f"   - {ingredient}: {count} videos")

print(f"\n🎬 CONTENT THEMES:")
for theme, count in sorted(cayenne_report['content_themes'].items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        print(f"   - {theme}: {count} videos")

print(f"\n📈 TOP PERFORMING VIDEOS:")
for i, v in enumerate(cayenne_report['top_videos'][:5], 1):
    print(f"   {i}. {v['views_str']} - {v['title'][:60]}...")

# Save cayenne report
with open('cayenne_analysis_report.json', 'w') as f:
    json.dump(cayenne_report, f, indent=2)

print("\n" + "=" * 60)
print("ANALYZING OZONATED WATER DATASET")
print("=" * 60)

ozone_report = analyze_dataset('yt_ozonated_water_veggies_drink_1777191022178.json', 'Ozonated Water')

print(f"\n📊 OZONATED WATER OVERVIEW:")
print(f"   Videos: {ozone_report['total_videos']}")
print(f"   Total Views: {ozone_report['total_views']:,}")
print(f"   Average Views: {ozone_report['avg_views']:,}")
print(f"   Avg Duration: {ozone_report['avg_duration_formatted']}")

print(f"\n📺 TOP CHANNELS:")
for channel, count in ozone_report['top_channels'][:5]:
    print(f"   - {channel}: {count} videos")

print(f"\n💧 HEALTH CLAIMS FOUND:")
for claim, count in ozone_report['health_claims_found'][:10]:
    print(f"   - {claim}: {count} mentions")

print(f"\n🤝 SYNERGIES WITH OTHER INGREDIENTS:")
for ingredient, count in ozone_report['synergies_found']:
    print(f"   - {ingredient}: {count} videos")

print(f"\n🎬 CONTENT THEMES:")
for theme, count in sorted(ozone_report['content_themes'].items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        print(f"   - {theme}: {count} videos")

print(f"\n📈 TOP PERFORMING VIDEOS:")
for i, v in enumerate(ozone_report['top_videos'][:5], 1):
    print(f"   {i}. {v['views_str']} - {v['title'][:60]}...")

# Save ozone report
with open('ozonated_water_analysis_report.json', 'w') as f:
    json.dump(ozone_report, f, indent=2)

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE!")
print("=" * 60)
print(f"\n✅ Reports saved to:")
print(f"   - cayenne_analysis_report.json")
print(f"   - ozonated_water_analysis_report.json")