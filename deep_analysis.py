import json
import re
from collections import Counter, defaultdict

# Load all datasets
datasets = {}
for name, filename in [
    ('beetroot', 'yt_beetroot_juice_1777097248207.json'),
    ('ginger', 'yt_ginger_juice_1777107852603.json'),
    ('lemon', 'yt_lemon_juice_1777110237405.json'),
    ('honey', 'yt_honey_benefits_1777114862253.json')
]:
    with open(filename, 'r') as f:
        datasets[name] = json.load(f)

print("=" * 80)
print("DEEP DIVE ANALYSIS - FINDING HIDDEN INSIGHTS")
print("=" * 80)

# 1. CHANNEL ANALYSIS - Who are the influential voices?
print("\n" + "=" * 80)
print("1. TOP CHANNELS BY TOTAL VIEWS (INFLUENCER OPPORTUNITIES)")
print("=" * 80)

all_channels = defaultdict(lambda: {'views': 0, 'videos': [], 'total_videos': 0})

for ingredient, data in datasets.items():
    for v in data['videos']:
        channel = v['channel']
        views_str = v['views'].replace(',', '').replace('views', '').strip()
        if 'M' in views_str:
            views = float(views_str.replace('M', '')) * 1_000_000
        elif 'K' in views_str:
            views = float(views_str.replace('K', '')) * 1_000
        else:
            views = float(views_str)
        
        all_channels[channel]['views'] += views
        all_channels[channel]['total_videos'] += 1
        all_channels[channel]['videos'].append({
            'title': v['title'],
            'views': v['views'],
            'ingredient': ingredient
        })

# Sort by total views
top_channels = sorted(all_channels.items(), key=lambda x: x[1]['views'], reverse=True)[:20]

print("\nTop 20 Channels (Potential Influencer Partnerships):")
for i, (channel, data) in enumerate(top_channels, 1):
    print(f"\n{i}. {channel}")
    print(f"   Total Views: {data['views']:,.0f}")
    print(f"   Videos in Dataset: {data['total_videos']}")
    ingredients = set(v['ingredient'] for v in data['videos'])
    print(f"   Covers: {', '.join(ingredients)}")

# 2. VIDEO DURATION ANALYSIS
print("\n" + "=" * 80)
print("2. VIDEO DURATION ANALYSIS (CONTENT FORMAT INSIGHTS)")
print("=" * 80)

duration_analysis = {'short': 0, 'medium': 0, 'long': 0, 'unknown': 0}
duration_views = {'short': 0, 'medium': 0, 'long': 0, 'unknown': 0}

def parse_duration(dur_str):
    if not dur_str:
        return None
    parts = dur_str.split(':')
    if len(parts) == 2:
        try:
            return int(parts[0]) * 60 + int(parts[1])
        except:
            return None
    elif len(parts) == 3:
        try:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        except:
            return None
    return None

def parse_views(views_str):
    views_str = views_str.replace(',', '').replace('views', '').strip()
    if 'M' in views_str:
        return float(views_str.replace('M', '')) * 1_000_000
    elif 'K' in views_str:
        return float(views_str.replace('K', '')) * 1_000
    return float(views_str)

for ingredient, data in datasets.items():
    for v in data['videos']:
        dur = parse_duration(v.get('duration', ''))
        views = parse_views(v['views'])
        
        if dur is None:
            duration_analysis['unknown'] += 1
            duration_views['unknown'] += views
        elif dur < 180:  # Under 3 mins (Shorts-style)
            duration_analysis['short'] += 1
            duration_views['short'] += views
        elif dur < 600:  # 3-10 mins
            duration_analysis['medium'] += 1
            duration_views['medium'] += views
        else:  # 10+ mins
            duration_analysis['long'] += 1
            duration_views['long'] += views

print("\nContent Format Distribution:")
for fmt in ['short', 'medium', 'long', 'unknown']:
    if duration_analysis[fmt] > 0:
        avg = duration_views[fmt] / duration_analysis[fmt]
        print(f"  {fmt.upper()}: {duration_analysis[fmt]} videos, {duration_views[fmt]:,.0f} total views, {avg:,.0f} avg views/video")

# 3. PUBLISH DATE ANALYSIS (if available)
print("\n" + "=" * 80)
print("3. PUBLISH TIMING ANALYSIS")
print("=" * 80)

time_patterns = Counter()
for ingredient, data in datasets.items():
    for v in data['videos']:
        pub_time = v.get('publishedTime', '')
        if pub_time:
            time_patterns[pub_time] += 1

print("\nPublish Time Distribution:")
for time, count in time_patterns.most_common(15):
    print(f"  {time}: {count} videos")

# 4. TITLE ANALYSIS - What words drive views?
print("\n" + "=" * 80)
print("4. HIGH-PERFORMING TITLE PATTERNS")
print("=" * 80)

# Extract words from high-performing videos
high_performer_words = []
low_performer_words = []

for ingredient, data in datasets.items():
    for v in data['videos']:
        views = parse_views(v['views'])
        title = v['title'].lower()
        words = re.findall(r'\b[a-z]+\b', title)
        
        if views > 500000:  # 500K+ views
            high_performer_words.extend(words)
        elif views < 50000:  # Under 50K views
            low_performer_words.extend(words)

high_counter = Counter(high_performer_words)
low_counter = Counter(low_performer_words)

print("\nMost Common Words in HIGH-PERFORMING Videos (500K+ views):")
for word, count in high_counter.most_common(30):
    if len(word) > 3 and word not in ['this', 'that', 'with', 'when', 'what', 'your', 'from', 'have', 'about']:
        print(f"  {word}: {count}")

# 5. MISTAKES/WARNINGS CONTENT (High engagement format)
print("\n" + "=" * 80)
print("5. 'MISTAKES' & 'WARNING' CONTENT (High Engagement Format)")
print("=" * 80)

mistake_videos = []
for ingredient, data in datasets.items():
    for v in data['videos']:
        title_lower = v['title'].lower()
        if any(word in title_lower for word in ['mistake', 'avoid', 'warning', 'never', 'stop', 'wrong', 'don\'t', 'dont']):
            views = parse_views(v['views'])
            mistake_videos.append({
                'title': v['title'],
                'views': v['views'],
                'views_num': views,
                'ingredient': ingredient,
                'channel': v['channel']
            })

mistake_videos.sort(key=lambda x: x['views_num'], reverse=True)

print(f"\nFound {len(mistake_videos)} 'Mistakes/Warning' style videos:")
for v in mistake_videos[:10]:
    print(f"\n  - \"{v['title'][:50]}...\"")
    print(f"    {v['views']} | {v['ingredient']} | {v['channel']}")

total_mistake_views = sum(v['views_num'] for v in mistake_videos)
print(f"\nTOTAL VIEWS for 'Mistakes' content: {total_mistake_views:,.0f}")
print(f"Average views: {total_mistake_views/len(mistake_videos):,.0f}" if mistake_videos else "N/A")

# 6. QUESTION-BASED TITLES
print("\n" + "=" * 80)
print("6. QUESTION-BASED CONTENT (Curiosity Gap)")
print("=" * 80)

question_videos = []
for ingredient, data in datasets.items():
    for v in data['videos']:
        title = v['title']
        if '?' in title or any(word in title.lower() for word in ['what happens', 'should you', 'can you', 'does ', 'is ', 'why ']):
            views = parse_views(v['views'])
            question_videos.append({
                'title': title,
                'views': v['views'],
                'views_num': views,
                'ingredient': ingredient
            })

question_videos.sort(key=lambda x: x['views_num'], reverse=True)

print(f"\nFound {len(question_videos)} question-based videos:")
for v in question_videos[:10]:
    print(f"\n  - \"{v['title'][:55]}...\"")
    print(f"    {v['views']} | {v['ingredient']}")

total_q_views = sum(v['views_num'] for v in question_videos)
avg_q = total_q_views / len(question_videos) if question_videos else 0
print(f"\nTOTAL VIEWS: {total_q_views:,.0f}")
print(f"Average views per question video: {avg_q:,.0f}")

# 7. TIME-BASED CLAIMS (Morning, Night, Before/After)
print("\n" + "=" * 80)
print("7. TIME-BASED CLAIMS (When to consume)")
print("=" * 80)

timing_content = []
timing_keywords = ['morning', 'night', 'evening', 'before bed', 'empty stomach', 
                   'before workout', 'after workout', 'first thing', '30 minutes',
                   'best time', 'when to']

for ingredient, data in datasets.items():
    for v in data['videos']:
        title_lower = v['title'].lower()
        transcript = v.get('transcript', {}).get('fullText', '').lower()
        
        for keyword in timing_keywords:
            if keyword in title_lower or keyword in transcript:
                views = parse_views(v['views'])
                timing_content.append({
                    'title': v['title'],
                    'views': v['views'],
                    'views_num': views,
                    'ingredient': ingredient,
                    'timing': keyword
                })
                break

timing_content.sort(key=lambda x: x['views_num'], reverse=True)

print(f"\nFound {len(timing_content)} videos with timing recommendations:")
for v in timing_content[:15]:
    print(f"  - [{v['timing']}] {v['title'][:45]}... ({v['views']})")

# 8. DEMOGRAPHIC INDICATORS
print("\n" + "=" * 80)
print("8. DEMOGRAPHIC TARGETING OPPORTUNITIES")
print("=" * 80)

demo_keywords = {
    'over 50': ['over 50', 'over 60', 'senior', 'elderly', 'aging', 'age'],
    'men': ['men', 'male', 'testosterone', 'prostate', 'erectile'],
    'women': ['women', 'female', 'pregnancy', 'pregnant', 'menstrual', 'menopause'],
    'athletes': ['athlete', 'runner', 'cyclist', 'gym', 'workout', 'training'],
    'diabetics': ['diabetes', 'diabetic', 'blood sugar'],
    'heart patients': ['heart', 'blood pressure', 'cardiovascular', 'cholesterol'],
}

demo_results = {}
for demo, keywords in demo_keywords.items():
    videos_found = []
    for ingredient, data in datasets.items():
        for v in data['videos']:
            text = (v['title'] + ' ' + v.get('transcript', {}).get('fullText', '')).lower()
            for kw in keywords:
                if kw in text:
                    views = parse_views(v['views'])
                    videos_found.append({
                        'title': v['title'],
                        'views': views,
                        'ingredient': ingredient
                    })
                    break
    
    total_demo_views = sum(v['views'] for v in videos_found)
    demo_results[demo] = {
        'videos': len(videos_found),
        'views': total_demo_views,
        'avg_views': total_demo_views / len(videos_found) if videos_found else 0
    }

print("\nDemographic Content Analysis:")
for demo, data in sorted(demo_results.items(), key=lambda x: x[1]['views'], reverse=True):
    print(f"  {demo.upper()}: {data['videos']} videos, {data['views']:,.0f} total views")

# 9. RECIPE/HOW-TO CONTENT
print("\n" + "=" * 80)
print("9. RECIPE & HOW-TO CONTENT")
print("=" * 80)

recipe_videos = []
for ingredient, data in datasets.items():
    for v in data['videos']:
        title_lower = v['title'].lower()
        if any(word in title_lower for word in ['recipe', 'how to', 'make', 'homemade', 'diy']):
            views = parse_views(v['views'])
            recipe_videos.append({
                'title': v['title'],
                'views': v['views'],
                'views_num': views,
                'ingredient': ingredient
            })

recipe_videos.sort(key=lambda x: x['views_num'], reverse=True)

print(f"\nFound {len(recipe_videos)} recipe/how-to videos:")
total_recipe_views = sum(v['views_num'] for v in recipe_videos)
print(f"Total views: {total_recipe_views:,.0f}")
print(f"Average: {total_recipe_views/len(recipe_videos):,.0f}" if recipe_videos else "N/A")

print("\nTop 10 Recipe/How-To Videos:")
for v in recipe_videos[:10]:
    print(f"  - {v['title'][:50]}... ({v['views']})")

# 10. SAVE DEEP ANALYSIS
print("\n" + "=" * 80)
print("10. SAVING DEEP ANALYSIS...")
print("=" * 80)

deep_report = {
    'top_channels': [{'name': ch, 'views': data['views'], 'videos': data['total_videos']} 
                     for ch, data in top_channels[:15]],
    'duration_analysis': duration_analysis,
    'duration_views': duration_views,
    'mistake_videos': [{'title': v['title'], 'views': v['views']} for v in mistake_videos[:15]],
    'question_videos': [{'title': v['title'], 'views': v['views']} for v in question_videos[:15]],
    'demo_results': demo_results,
    'recipe_video_count': len(recipe_videos),
    'recipe_total_views': total_recipe_views
}

with open('deep_analysis_report.json', 'w') as f:
    json.dump(deep_report, f, indent=2)

print("Deep analysis saved to deep_analysis_report.json")
print("\n" + "=" * 80)
print("DEEP ANALYSIS COMPLETE!")
print("=" * 80)