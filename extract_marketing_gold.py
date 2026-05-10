import json
import re

# Load the data
with open('yt_beetroot_juice_1777097248207.json', 'r') as f:
    data = json.load(f)

videos = data['videos']

print("=" * 80)
print("MARKETING GOLD EXTRACTION - BEETROOT JUICE")
print("=" * 80)

# 1. Extract specific performance statistics
print("\n" + "=" * 80)
print("1. PERFORMANCE & ATHLETIC CLAIMS (GREAT FOR GYM/SPORTS PITCHES)")
print("=" * 80)

performance_claims = []

for v in videos:
    if not v.get('transcript') or not v['transcript'].get('fullText'):
        continue
    
    text = v['transcript']['fullText']
    title = v['title']
    channel = v['channel']
    views = v['views']
    
    # Look for specific performance-related sentences
    sentences = re.split(r'[.!?]', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 30:
            continue
        
        # Performance keywords
        perf_keywords = ['stamina', 'endurance', 'performance', 'athlete', 'exercise', 
                        'workout', 'training', 'cyclist', 'oxygen', 'blood flow',
                        'nitric oxide', 'energy', 'muscle']
        
        sentence_lower = sentence.lower()
        if any(kw in sentence_lower for kw in perf_keywords):
            # Check for numbers/percentages
            if re.search(r'\d+[%]|\d+\s*(percent|hours?|minutes?|times?)', sentence_lower):
                performance_claims.append({
                    'claim': sentence,
                    'source': title,
                    'channel': channel,
                    'views': views
                })

print("\nSpecific Performance Claims with Numbers:")
for i, claim in enumerate(performance_claims[:15], 1):
    print(f"\n{i}. \"{claim['claim'][:250]}...\"")
    print(f"   Source: {claim['source'][:50]}... ({claim['views']})")

# 2. Blood Pressure & Heart Health Claims
print("\n" + "=" * 80)
print("2. BLOOD PRESSURE & HEART HEALTH CLAIMS")
print("=" * 80)

bp_claims = []
for v in videos:
    if not v.get('transcript') or not v['transcript'].get('fullText'):
        continue
    
    text = v['transcript']['fullText']
    sentences = re.split(r'[.!?]', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 30:
            continue
        
        sentence_lower = sentence.lower()
        if 'blood pressure' in sentence_lower or 'heart' in sentence_lower:
            if any(word in sentence_lower for word in ['lower', 'reduce', 'improve', 'study', 'research']):
                bp_claims.append({
                    'claim': sentence,
                    'source': v['title'],
                    'views': v['views']
                })

print("\nHeart Health Claims:")
for i, claim in enumerate(bp_claims[:10], 1):
    print(f"\n{i}. \"{claim['claim'][:250]}...\"")
    print(f"   Source: {claim['source'][:50]}... ({claim['views']})")

# 3. Detox & Liver Claims
print("\n" + "=" * 80)
print("3. LIVER DETOX CLAIMS")
print("=" * 80)

liver_claims = []
for v in videos:
    if not v.get('transcript') or not v['transcript'].get('fullText'):
        continue
    
    text = v['transcript']['fullText']
    sentences = re.split(r'[.!?]', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 30:
            continue
        
        sentence_lower = sentence.lower()
        if any(word in sentence_lower for word in ['liver', 'detox', 'cleanse']):
            if any(word in sentence_lower for word in ['support', 'help', 'detox', 'toxin', 'betaine']):
                liver_claims.append({
                    'claim': sentence,
                    'source': v['title'],
                    'views': v['views']
                })

print("\nLiver/Detox Claims:")
for i, claim in enumerate(liver_claims[:10], 1):
    print(f"\n{i}. \"{claim['claim'][:250]}...\"")
    print(f"   Source: {claim['source'][:50]}... ({claim['views']})")

# 4. Key Nutritional Facts
print("\n" + "=" * 80)
print("4. NUTRITIONAL FACTS & COMPOUNDS")
print("=" * 80)

nutrition_facts = []
for v in videos:
    if not v.get('transcript') or not v['transcript'].get('fullText'):
        continue
    
    text = v['transcript']['fullText']
    sentences = re.split(r'[.!?]', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 30:
            continue
        
        sentence_lower = sentence.lower()
        if any(word in sentence_lower for word in ['mg', 'milligram', 'vitamin', 'potassium', 'iron', 'magnesium']):
            if 'beet' in sentence_lower or 'contain' in sentence_lower or 'rich' in sentence_lower:
                nutrition_facts.append({
                    'fact': sentence,
                    'source': v['title']
                })

print("\nNutritional Facts:")
for i, fact in enumerate(nutrition_facts[:10], 1):
    print(f"\n{i}. \"{fact['fact'][:250]}...\"")

# 5. Timing Recommendations
print("\n" + "=" * 80)
print("5. WHEN TO DRINK BEETROOT JUICE (TIMING ADVICE)")
print("=" * 80)

timing_advice = []
for v in videos:
    if not v.get('transcript') or not v['transcript'].get('fullText'):
        continue
    
    text = v['transcript']['fullText']
    sentences = re.split(r'[.!?]', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 20:
            continue
        
        sentence_lower = sentence.lower()
        if any(phrase in sentence_lower for phrase in ['best time', 'morning', 'before workout', 'before exercise', 'hours before', 'drink before']):
            timing_advice.append({
                'advice': sentence,
                'source': v['title']
            })

print("\nTiming Recommendations:")
for i, advice in enumerate(timing_advice[:10], 1):
    print(f"\n{i}. \"{advice['advice'][:250]}...\"")

# 6. Save all claims for marketing use
print("\n" + "=" * 80)
print("6. COMPILING MARKETING ASSETS...")
print("=" * 80)

marketing_assets = {
    'performance_claims': performance_claims[:20],
    'heart_health_claims': bp_claims[:15],
    'liver_detox_claims': liver_claims[:15],
    'nutrition_facts': nutrition_facts[:15],
    'timing_advice': timing_advice[:10]
}

with open('marketing_assets.json', 'w') as f:
    json.dump(marketing_assets, f, indent=2)

print("Marketing assets saved to marketing_assets.json")

# 7. Generate catchy headlines for social media
print("\n" + "=" * 80)
print("7. SUGGESTED SOCIAL MEDIA HEADLINES")
print("=" * 80)

headlines = [
    "🥤 Fuel Your Workout: Why Athletes Are Drinking Beetroot Juice Before Training",
    "❤️ Lower Blood Pressure Naturally - The Beetroot Juice Secret (Backed by Science)",
    "🏃‍♂️ Boost Stamina by Up to 16%? The Nitric Oxide Power of Beetroot",
    "🔋 Natural Energy Without the Crash: Beetroot Juice for Sustained Performance",
    "💪 Gym-Goers Secret Weapon: Beetroot Juice Increases Blood Flow to Muscles",
    "🧠 Brain + Body Boost: How Beetroot Juice Improves Oxygen Delivery",
    "⚡ 30 Minutes Before Your Workout: Why Timing Matters with Beetroot Juice",
    "🏆 Elite Athletes Use It: The Performance Benefits of Dietary Nitrates",
    "🩸 Improve Circulation Naturally: The Nitric Oxide Effect",
    "Liver Detox in a Glass: How Beetroot Supports Your Body's Natural Cleansing",
]

print("\nSuggested Headlines:")
for i, headline in enumerate(headlines, 1):
    print(f"  {i}. {headline}")

print("\n" + "=" * 80)
print("EXTRACTION COMPLETE!")
print("=" * 80)