import json

with open('all-sources.json', encoding='utf-8') as f:
    data = json.load(f)

boats = data['data']
metadata = data['metadata']

print(f"=== BOAT DATA STATISTICS ===\n")
print(f"Total boats in current page: {len(boats)}")
print(f"Total records: {metadata['total']}")
print(f"Total pages: {metadata['totalPage']}")
print(f"Current page: {metadata['page']}")
print(f"Limit per page: {metadata['limit']}")

# Price analysis
prices = [float(b['Price'].split()[0]) for b in boats if 'Price' in b and b['Price']]
print(f"\n=== PRICE STATISTICS ===")
print(f"Min price: ${min(prices):,.2f}")
print(f"Max price: ${max(prices):,.2f}")
print(f"Average price: ${sum(prices)/len(prices):,.2f}")

# Year analysis
years = [b['ModelYear'] for b in boats if 'ModelYear' in b and b['ModelYear']]
print(f"\n=== YEAR RANGE ===")
print(f"Oldest: {min(years)}")
print(f"Newest: {max(years)}")

# Manufacturer analysis
makes = {}
for b in boats:
    if 'MakeString' in b and b['MakeString']:
        makes[b['MakeString']] = makes.get(b['MakeString'], 0) + 1

print(f"\n=== TOP 10 MANUFACTURERS ===")
for make, count in sorted(makes.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"{make}: {count} boats")

# Location analysis
states = {}
for b in boats:
    if 'BoatLocation' in b and 'BoatStateCode' in b['BoatLocation']:
        state = b['BoatLocation']['BoatStateCode']
        states[state] = states.get(state, 0) + 1

print(f"\n=== TOP 10 LOCATIONS (by state) ===")
for state, count in sorted(states.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"{state}: {count} boats")

# Engine analysis
engine_types = {}
for b in boats:
    if 'Engines' in b and b['Engines']:
        for engine in b['Engines']:
            if 'Type' in engine:
                etype = engine['Type']
                engine_types[etype] = engine_types.get(etype, 0) + 1

print(f"\n=== ENGINE TYPES ===")
for etype, count in sorted(engine_types.items(), key=lambda x: x[1], reverse=True):
    print(f"{etype}: {count}")
