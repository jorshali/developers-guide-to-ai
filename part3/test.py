import csv
import random

# -------------------------------
# 1. PREPARE RANDOM DATA POOLS
# -------------------------------

# Product categories
categories = ["Electronics", "Home Decor", "Apparel"]

# Possible product names
electronic_names = [
    "QuantumSound Headphones","HexaDrive Portable Charger","NovaVision Smartwatch","UltraNet Wi-Fi Router",
    "SkyBeam LED TV","SonicPulse Bluetooth Speaker","OptiCore Laptop","HyperFlash SSD","AirGlide Drone",
    "EzCap Pro Microphone","MechBoard Mechanical Keyboard","LensScope Digital Camera","MultiDock USB Hub",
    "Titanium Shield Phone Case","GalaxyBeam Projector","PulseFit Fitness Tracker","CloudSync External Drive",
    "GlideTrack Gaming Mouse","ThunderBolt Gaming Console","PixelView 4K Monitor"
]

home_decor_names = [
    "Lumina Table Lamp","SereneWave Wall Art","CloudCushion Throw Pillow","AquaGlass Vase","Soleil Window Curtains",
    "EverSoft Area Rug","BreezeBlock Desk Fan","MetroFrame Photo Frame","CedarCraft Bookshelf","Harmony Scented Candle",
    "ZenFlo Table Fountain","ModernEdge Side Table","UrbanLeaf Potted Plant","CosmoChic Decorative Mirror",
    "RusticOak Coffee Table","CrystalLite Chandelier","VelvetHue Plush Ottoman","MarbleVista Coasters",
    "Aurora Standing Lamp","WildBloom Flower Pot"
]

apparel_names = [
    "EverFlex Yoga Pants","UrbanStride Sneakers","CloudFit Running Shirt","StyleMend Denim Jacket","BoldVenture Leather Belt",
    "SunSette Summer Dress","NightSky Hoodie","ClassicEdge Oxford Shoes","AeroWeave Windbreaker","TerraForm Hiking Boots",
    "GoldenGlow Evening Gown","CoolCotton Casual Tee","EvoFit Track Pants","PrimeWear Wristwatch","RoyalWeave Beanie",
    "TrueThread Crew Socks","LightBloom Jacket","SteelCrest Sunglasses","AllureWrap Scarf","NatureTrek Cargo Shorts"
]

def get_random_product_name(category: str) -> str:
    """Return a random product name based on the category."""
    if category == "Electronics":
        return random.choice(electronic_names)
    elif category == "Home Decor":
        return random.choice(home_decor_names)
    else:
        return random.choice(apparel_names)

# For a bit of fun variation in descriptions
adjectives = ["sleek", "modern", "vibrant", "durable", "premium", "versatile", "sturdy", "sophisticated"]
colors = ["red", "blue", "charcoal", "silver", "beige", "emerald", "navy", "white", "black"]
purposes = ["home use", "office tasks", "professional settings", "casual relaxation", "travel situations"]
features = ["Bluetooth compatibility", "water resistance", "quick-assembly parts", "expandable capacity"]
sizes = ["10x6 inches", "12x8 inches", "15x10 inches", "20x14 inches"]
brand_names = ["Artemis", "EverTrue", "ProVantage", "Xenora", "Vertigon", "CloudWave", "MyriadTech", "LuminaCo"]

# -------------------------------
# 2. PREPARE SENTENCES FOR DESCRIPTIONS
#    Each sentence is *exactly* 10 words to facilitate a 200-word paragraph
# -------------------------------
SENTENCES = [
    # 10 words each exactly. We'll use placeholders for variety.
    "The {adjective} design elevates appeal with a refined {color} accent.",
    "Built by {brand}, this product guarantees reliable performance and longevity.",
    "Its sturdy structure excels under demanding daily or professional usage.",
    "Owners appreciate the balanced dimensions measuring around {size} overall.",
    "Unique craftsmanship merges practicality with captivating style and flair.",
    "Integration of {feature} enhances user experience in countless real scenarios.",
    "Meticulous quality checks ensure a dependable solution for frequent handling.",
    "This item suits {purpose}, adapting effortlessly to multiple circumstances.",
    "Consumers praise the comfortable grip and convenient setup procedure here.",
    "A robust exterior material helps protect vital components from damage.",
    "Particular attention to detail fosters intuitive operation for any audience.",
    "Continuous innovation from {brand} refines each outstanding product iteration perfectly.",
    "Vibrant design contrasts elegantly with subtle {color} finishing throughout construction.",
    "Careful engineering balances weight, making transport safe and stress-free.",
    "Ownership extends beyond function, creating personal connection and meaningful value.",
    "Whether indoors or outdoors, durability stands unwavering amid harsh conditions.",
    "Each purchase includes user resources ensuring smooth assembly and maintenance.",
    "Efficiency pairs with {feature}, enabling straightforward control in modern lifestyles.",
    "After rigorous testing, the final result meets international safety standards.",
    "Practical proportions measuring {size} simplify placement in both large areas.",
    "From production to packaging, {brand} excels in ecological manufacturing choices.",
    "Various {color} options cater to distinct decorative preferences or requirements.",
    "Versatility makes it highly recommended for broad consumer demographics worldwide.",
    "The consistent shape optimizes space for functional and aesthetic balance.",
    "Extended warranties underline the unwavering confidence behind every {brand} model.",
    "Continuous improvements reflect changing needs without compromising timeless attractiveness.",
    "Convenient features integrate seamlessly for quick adaptation amid daily routines.",
    "It maintains structural integrity even under different environmental constraints easily.",
    "Advanced details like {feature} personalize usage with unwavering dependability forever.",
    "The final assembly emerges sleek, capturing minimalism alongside dynamic capability.",
    "Manufactured using carefully sourced materials for an eco-friendly market presence.",
    "Portable form factor, around {size}, fits standard baggage or storage.",
    "Appreciation grows among novices and experts witnessing polished reliability here.",
    "Cutting-edge fabrication ensures longevity and minimal upkeep costs over time.",
    "Visually, the {color} theme accentuates an appealing, unforgettable first impression.",
    "Company heritage under {brand} fosters customer loyalty spanning multiple generations.",
    "Ergonomic designs grant maximum comfort during prolonged interactive experiences daily.",
    "Comprehensive documentation helps buyers navigate advanced settings confidently anytime.",
    "Bold structure transcends typical expectations while respecting classic functional norms.",
    "Reinforced edges preserve immaculate condition against scratches or accidental drops.",
    "Ownership signifies a step toward simplifying hectic modern life thoroughly."
]

# -------------------------------
# 3. GENERATE A UNIQUE DESCRIPTION
#    Each description: 20 random unique sentences x 10 words = 200 words
# -------------------------------
def generate_unique_description() -> str:
    """Return a 200-word unique description by sampling 20 distinct sentences from SENTENCES."""
    chosen_sentences = random.sample(SENTENCES, 20)
    # Fill placeholders in each chosen sentence
    filled_sentences = []
    for sentence in chosen_sentences:
        sentence = sentence.format(
            adjective=random.choice(adjectives),
            color=random.choice(colors),
            brand=random.choice(brand_names),
            feature=random.choice(features),
            purpose=random.choice(purposes),
            size=random.choice(sizes)
        )
        filled_sentences.append(sentence)
    # Join them into one paragraph
    # (Space separates sentences. There's no period inside each sentence beyond what's already there.)
    paragraph = " ".join(filled_sentences)
    return paragraph

# -------------------------------
# 4. BUILD THE CSV
# -------------------------------
def build_csv(filename="unique_products.csv", num_products=100):
    """Generate CSV file with 100 products, each with unique 200-word description."""
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Header
        writer.writerow(["id", "name", "category", "price", "description"])

        for i in range(1, num_products + 1):
            # Choose category and product name
            category = random.choice(categories)
            name = get_random_product_name(category)
            price = random.randint(10, 999)
            # Generate a unique 200-word description
            desc = generate_unique_description()

            writer.writerow([i, name, category, price, desc])

    print(f"CSV file '{filename}' generated successfully with {num_products} products.")

# -------------------------------
# 5. RUN IT!
# -------------------------------
if __name__ == "__main__":
    build_csv()
