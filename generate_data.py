"""
generate_data.py - KartShelf E-Commerce Dataset Generator
Generates 80 realistic Indian marketplace products with rich metadata:
Exact matching Unsplash high-res product photos, IDs, SKUs, categories,
subcategories, pricing in INR, ratings, tags, variant grouping (for Disjoint Set),
and related products (for Graphs).
"""

import json
import os
import random

def generate_products():
    random.seed(42)  # Deterministic seed for reproducible testing

    categories = {
        "Electronics": {
            "subcategories": ["Audio", "Wearables", "Accessories", "Smart Home"],
            "brands": ["boAt", "Noise", "Titan", "Portronics", "Zebronics", "OnePlus", "Boult"],
            "items": [
                ("Airdopes 441 TWS Earbuds", "Wireless earbuds with IWP technology and IPX7 water resistance.", 1999, 3999,
                 "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&auto=format&fit=crop&q=80"),
                ("ColorFit Pulse Smartwatch", "1.69 inch HD display, 24/7 heart rate monitor, 10-day battery.", 2499, 4999,
                 "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80"),
                ("Rockerz 550 Over-Ear Wireless Headphones", "Physical noise isolation with 50mm dynamic drivers.", 1799, 3990,
                 "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80"),
                ("PowerPro 20000mAh Power Bank", "Triple output ports with 22.5W fast charging support.", 1499, 2999,
                 "https://images.unsplash.com/photo-1609592426861-122e0e0a5d4d?w=600&auto=format&fit=crop&q=80"),
                ("Breeze Mini Bluetooth Speaker", "5W stereo driver with rich bass and built-in FM tuner.", 899, 1799,
                 "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600&auto=format&fit=crop&q=80"),
                ("ErgoLift Aluminum Laptop Stand", "6-level adjustable height with ventilated thermal design.", 1199, 2499,
                 "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&auto=format&fit=crop&q=80"),
                ("Aura RGB Mechanical Gaming Keyboard", "Tactile blue switches with braided USB-C cable.", 2999, 5499,
                 "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop&q=80"),
                ("Smart Plug 16A with Energy Monitor", "Wi-Fi enabled automation for heavy appliances up to 3500W.", 999, 1999,
                 "https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=600&auto=format&fit=crop&q=80"),
                ("TruView 1080p Web Camera", "Full HD with noise cancelling dual stereo microphones.", 1349, 2499,
                 "https://images.unsplash.com/photo-1588508065123-287b28e013da?w=600&auto=format&fit=crop&q=80"),
                ("RapidCharge 65W GaN Charger", "Dual Type-C and USB-A compact multi-device fast adapter.", 2199, 3999,
                 "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600&auto=format&fit=crop&q=80"),
                ("SoundMax 2.1 Soundbar with Subwoofer", "120W cinematic soundbar with Bluetooth 5.3 and HDMI ARC.", 4999, 9999,
                 "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=600&auto=format&fit=crop&q=80"),
                ("FitTrack Smart Fitness Band", "SpO2 and sleep tracking with 14 sports modes and swim proofing.", 1299, 2499,
                 "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=600&auto=format&fit=crop&q=80"),
                ("SilentClick Ergonomic Wireless Mouse", "Dual mode Bluetooth & 2.4GHz with 4000 DPI sensor.", 799, 1499,
                 "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=600&auto=format&fit=crop&q=80"),
                ("Smart LED Desk Lamp with Qi Charger", "Stepless dimming with 10W wireless charging phone pad.", 1699, 3299,
                 "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&auto=format&fit=crop&q=80"),
            ]
        },
        "Handicrafts & Decor": {
            "subcategories": ["Terracotta", "Brass & Metal", "Woodcraft", "Wall Art"],
            "brands": ["Kaveri Crafts", "Dastkar", "Jaipur Blue", "Hastashilp", "FabIndia", "BrassRoots"],
            "items": [
                ("Handcrafted Terracotta Chai Kulhad (Set of 6)", "Traditional clay cups fired in wood kilns, unglazed and earthy.", 449, 799,
                 "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=600&auto=format&fit=crop&q=80"),
                ("Pure Brass Traditional Filter Coffee Davarah Set", "Heavy gauge engraved brass tumbler and dabara for authentic filter kaapi.", 899, 1499,
                 "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&auto=format&fit=crop&q=80"),
                ("Dhokra Tribal Art Brass Figurine", "Lost-wax casting handcrafted by Bastar indigenous artisans.", 1899, 3200,
                 "https://images.unsplash.com/photo-1567225557594-88d73e55f2cb?w=600&auto=format&fit=crop&q=80"),
                ("Sheesham Wood Hand-Carved Spice Box", "9-compartment masala dani with glass lid and brass latch.", 1299, 2199,
                 "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=600&auto=format&fit=crop&q=80"),
                ("Blue Pottery Decorative Wall Plate 10-inch", "Authentic quartz-clay Jaipur glazed pottery with floral motifs.", 999, 1699,
                 "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?w=600&auto=format&fit=crop&q=80"),
                ("Moradabad Hand-Engraved Brass Urli", "Floating flower bowl with peacock pedestal for festive foyer decor.", 2499, 4500,
                 "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=600&auto=format&fit=crop&q=80"),
                ("Channapatna Lacquer Wood Toy Train", "Non-toxic vegetable dyed natural ivory wood handcrafted toy.", 699, 1199,
                 "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=600&auto=format&fit=crop&q=80"),
                ("Madhubani Hand-Painted Canvas Wall Hanging", "Mithila folk art depicting the Tree of Life in natural dyes.", 1599, 2799,
                 "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=600&auto=format&fit=crop&q=80"),
                ("Carved Mango Wood Coasters (Set of 4)", "Distressed rustic finish with brass inlay geometric accents.", 499, 899,
                 "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=600&auto=format&fit=crop&q=80"),
                ("Bastar Iron Craft Wall Lamp Sconce", "Forged wrought iron tribal silhouette with frosted glass chimney.", 1799, 3100,
                 "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600&auto=format&fit=crop&q=80"),
                ("Kutch Embroidered Cushion Cover (Set of 2)", "Mirror-work and chain stitch cotton handloom covers.", 849, 1499,
                 "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=600&auto=format&fit=crop&q=80"),
                ("Sandalwood Aroma Diffuser with Brass Burner", "Hand-turned wooden base with beaten brass oil bowl.", 1149, 1999,
                 "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=600&auto=format&fit=crop&q=80"),
                ("Warli Art Terracotta Table Vase", "Maharashtra tribal painted earthenware pot in terracotta and white.", 649, 1100,
                 "https://images.unsplash.com/photo-1612196808214-b8e1d6145a8c?w=600&auto=format&fit=crop&q=80"),
            ]
        },
        "Fashion & Apparel": {
            "subcategories": ["Traditional Wear", "Footwear", "Stoles & Scarves", "Bags"],
            "brands": ["FabIndia", "Manyavar", "Kalamkari Co", "Mojari Crafts", "Bunkar Heritage", "Zouk"],
            "items": [
                ("Chanderi Handloom Cotton-Silk Kurta", "Lightweight breathable woven kurta with subtle zari piping.", 2199, 3999,
                 "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=600&auto=format&fit=crop&q=80"),
                ("Jaipuri Hand-Block Printed Cotton Shirt", "Bagru natural indigo dye printed slim-fit casual shirt.", 1299, 2299,
                 "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600&auto=format&fit=crop&q=80"),
                ("Handmade Camel Leather Juttis", "Embroidered Rajasthani mojari with cushioned insole for festive wear.", 1499, 2799,
                 "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600&auto=format&fit=crop&q=80"),
                ("Pashmina Blend Kashmiri Stole", "Intricate aari-embroidered floral border with tassel fringes.", 2899, 5499,
                 "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=600&auto=format&fit=crop&q=80"),
                ("Vegan Leather Office Laptop Bag", "Indian craft print lining with padded 15.6 inch compartment.", 2499, 4299,
                 "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&auto=format&fit=crop&q=80"),
                ("Khadi Handspun Nehru Jacket", "Structured mandarin collar waistcoat with coconut shell buttons.", 1899, 3299,
                 "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=600&auto=format&fit=crop&q=80"),
                ("Bandhani Tie & Dye Georgette Dupatta", "Traditional Kutchi speckle-dyed dupatta with golden gota patti.", 999, 1799,
                 "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=600&auto=format&fit=crop&q=80"),
                ("Hand-Woven Ikat Canvas Tote Bag", "Telia Rumal geometric pattern with genuine brass zip hardware.", 899, 1499,
                 "https://images.unsplash.com/photo-1544816155-12df9643f363?w=600&auto=format&fit=crop&q=80"),
                ("Pure Linen Casual Drawstring Trousers", "Breathable enzyme-washed relaxed fit linen for summer.", 1799, 2999,
                 "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=600&auto=format&fit=crop&q=80"),
                ("Ajrakh Printed Cotton Saree", "Block printed modal silk-cotton drape with contrast pallu.", 3299, 5999,
                 "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=600&auto=format&fit=crop&q=80"),
                ("Embroidered Velvet Kolhapuri Sandals", "Braided leather straps with cushioned sole and golden sequins.", 1199, 1999,
                 "https://images.unsplash.com/photo-1560343090-f0409e92791a?w=600&auto=format&fit=crop&q=80"),
                ("Handwoven Bengal Muslin Scarf", "Ultra-fine lightweight handspun drape in pastel ecru.", 799, 1399,
                 "https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=600&auto=format&fit=crop&q=80"),
                ("Jute & Cotton Weekend Duffel", "Reinforced vegan leather handles with luggage pass-through sleeve.", 1999, 3499,
                 "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&auto=format&fit=crop&q=80"),
            ]
        },
        "Kitchen & Dining": {
            "subcategories": ["Cookware", "Tableware", "Storage", "Beverage"],
            "brands": ["Prestige", "Hawkins", "ClayCraft", "Vinod", "Borosil", "The Indus Valley"],
            "items": [
                ("Pre-Seasoned Cast Iron Dosa Tawa 11-inch", "Heavy skillet for crispy dosas, roti and skillet baking.", 1399, 2399,
                 "https://images.unsplash.com/photo-1590794056226-79ef3a8147e1?w=600&auto=format&fit=crop&q=80"),
                ("Pure Copper Water Bottle 1000ml", "Hammered ayurvedic wellness bottle with leak-proof brass cap.", 899, 1599,
                 "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&auto=format&fit=crop&q=80"),
                ("Tri-Ply Stainless Steel Kadai with Lid 2.5L", "Even heat distribution with cast cool-touch handles.", 2299, 3899,
                 "https://images.unsplash.com/photo-1584990347449-39b56bc693fb?w=600&auto=format&fit=crop&q=80"),
                ("Ceramic Serving Bowl Set with Chopsticks", "Hand-glazed stoneware bowls in deep teal and oatmeal speckle.", 1099, 1899,
                 "https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=600&auto=format&fit=crop&q=80"),
                ("Organic Bamboo Cutlery & Straw Travel Kit", "Eco-friendly fork, spoon, knife, straw and brush in canvas roll.", 399, 699,
                 "https://images.unsplash.com/photo-1584365685547-9a5fb6f3a70c?w=600&auto=format&fit=crop&q=80"),
                ("Traditional Kalchatti Soapstone Pot 2L", "Handmade rock stoneware for nutrient-rich slow-cooked gravies.", 2699, 4499,
                 "https://images.unsplash.com/photo-1585515320310-259814833e62?w=600&auto=format&fit=crop&q=80"),
                ("Borosilicate Glass Spice Jar Carousel (8 pcs)", "Airtight bamboo lids with rotating stainless steel lazy susan.", 1599, 2799,
                 "https://images.unsplash.com/photo-1532336414038-cf19250c5757?w=600&auto=format&fit=crop&q=80"),
                ("Heavy Brass Mortar & Pestle (Khalbatta)", "Traditional pounding bowl for whole spices and ginger-garlic.", 1199, 1999,
                 "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?w=600&auto=format&fit=crop&q=80"),
                ("Clay Biryani Handi with Lid 3L", "Naturally alkaline unglazed clay vessel for dum cooking.", 749, 1299,
                 "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&auto=format&fit=crop&q=80"),
                ("Acacia Wood Charcuterie Chopping Board", "End-grain reversible cutting block with deep juice groove.", 1249, 2199,
                 "https://images.unsplash.com/photo-1594998893017-36147cbcae05?w=600&auto=format&fit=crop&q=80"),
                ("Enamelled Cast Iron Dutch Oven 4L", "Heavy-duty oven-safe casserole for sourdough and slow stews.", 3999, 6999,
                 "https://images.unsplash.com/photo-1584990347449-39b56bc693fb?w=600&auto=format&fit=crop&q=80"),
                ("Stainless Steel Lunch Box 3-Tier (Dabba)", "Classic tiffin container with sturdy side clip clamps.", 699, 1199,
                 "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&auto=format&fit=crop&q=80"),
                ("Cold Brew Coffee Pitcher with Fine Mesh", "1 Litre heat-resistant carafe for smooth overnight cold extraction.", 1299, 2199,
                 "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?w=600&auto=format&fit=crop&q=80"),
            ]
        },
        "Wellness & Beauty": {
            "subcategories": ["Skincare", "Haircare", "Aromatherapy", "Personal Care"],
            "brands": ["Forest Essentials", "Kama Ayurveda", "Organic India", "Bombay Shaving Co", "Khadi Naturals", "Plum"],
            "items": [
                ("Kumkumadi Miraculous Ayurvedic Face Oil 15ml", "Infused with saffron, sandalwood and 24 classical herbs for radiance.", 2299, 3999,
                 "https://images.unsplash.com/photo-1608248597359-57778a48ba26?w=600&auto=format&fit=crop&q=80"),
                ("Cold-Pressed Virgin Coconut Oil 500ml", "Single-origin raw unfiltered oil for deep hair and skin nourishment.", 499, 799,
                 "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600&auto=format&fit=crop&q=80"),
                ("Pure Brass Kansa Wand Facial Massager", "Traditional bronze alloy dome for lymphatic drainage and relaxation.", 1299, 2299,
                 "https://images.unsplash.com/photo-1512290900672-1f5518b08244?w=600&auto=format&fit=crop&q=80"),
                ("Organic Ashwagandha & Tulsi Herbal Tea 100g", "Whole leaf antioxidant stress-relief infusion in tin caddy.", 449, 750,
                 "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?w=600&auto=format&fit=crop&q=80"),
                ("Neem Wood Handcrafted Wide-Tooth Comb", "Anti-static natural comb preventing hair breakage and scalp irritation.", 249, 450,
                 "https://images.unsplash.com/photo-1590159763121-7c9ff3149e0a?w=600&auto=format&fit=crop&q=80"),
                ("Sandalwood & Vetiver Luxury Bath Bar (Pack of 3)", "Cold-processed handmade soap enriched with shea butter.", 599, 999,
                 "https://images.unsplash.com/photo-1607006314045-8c010c26c117?w=600&auto=format&fit=crop&q=80"),
                ("Natural Soy Wax Scented Candle - Mogra & Oud", "Slow burning 50-hour crackling wooden wick aromatherapy candle.", 899, 1599,
                 "https://images.unsplash.com/photo-1603006905003-be475563bc59?w=600&auto=format&fit=crop&q=80"),
                ("Rose Water Facial Mist 200ml", "Steam-distilled pure Kannauj damask rose water toner.", 649, 1099,
                 "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=600&auto=format&fit=crop&q=80"),
                ("Activated Bamboo Charcoal Detox Face Pack", "Deep pore cleansing clay with tea tree and bentonite.", 499, 850,
                 "https://images.unsplash.com/photo-1567928815104-b676646b9ec7?w=600&auto=format&fit=crop&q=80"),
                ("Precision Safety Razor with 10 Swedish Blades", "Zinc-alloy double edge zero-waste grooming razor.", 1099, 1899,
                 "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&auto=format&fit=crop&q=80"),
                ("Brahmi & Bhringraj Scalp Revitalizer Oil", "Traditional taila infused for hair root strengthening.", 799, 1399,
                 "https://images.unsplash.com/photo-1608248597359-57778a48ba26?w=600&auto=format&fit=crop&q=80"),
                ("Kashmiri Lavender Essential Oil 15ml", "100% pure therapeutic grade therapeutic calming essence.", 699, 1199,
                 "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=600&auto=format&fit=crop&q=80"),
                ("Ayurvedic Copper Tongue Cleaner (Pack of 2)", "Ergonomic curved anti-microbial oral hygiene scrapers.", 199, 399,
                 "https://images.unsplash.com/photo-1559599101-f09722fb4948?w=600&auto=format&fit=crop&q=80"),
            ]
        },
        "Home & Living": {
            "subcategories": ["Bedding", "Stationery", "Organizers", "Planters"],
            "brands": ["SleepyCat", "Dastkar", "Nappa Dori", "Chumbak", "FabIndia", "ArtisanGuild"],
            "items": [
                ("100% Organic Bamboo Cotton Bedsheet Set (Queen)", "400 TC sateen weave with 2 matching pillowcases.", 2799, 4999,
                 "https://images.unsplash.com/photo-1631679706909-1844bbd07221?w=600&auto=format&fit=crop&q=80"),
                ("Full Grain Leather Journal with Handmade Paper", "200 deckle edge cotton rag pages with wrap-around thong tie.", 899, 1599,
                 "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&auto=format&fit=crop&q=80"),
                ("Natural Jute Braided Area Rug 4x6 ft", "Reversible eco-friendly floor mat handwoven by rural weavers.", 2499, 4499,
                 "https://images.unsplash.com/photo-1600121848594-d8644e57abab?w=600&auto=format&fit=crop&q=80"),
                ("Minimalist Ceramic Planter with Wooden Stand", "Matte ivory planter with drainage hole and rubberwood tripod.", 999, 1799,
                 "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=600&auto=format&fit=crop&q=80"),
                ("Handmade Macrame Cotton Wall Hanging", "Boho geometric woven fringe tapestries on driftwood rod.", 799, 1499,
                 "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=600&auto=format&fit=crop&q=80"),
                ("Canvas & Vegan Leather Desk Mat", "Water-resistant smooth mouse-friendly desk pad 80x40cm.", 849, 1499,
                 "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=600&auto=format&fit=crop&q=80"),
                ("Brass Incense Cone Burner with Ash Catcher", "Pyramid filigree cutwork holder for dhoop and sambrani.", 549, 950,
                 "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&auto=format&fit=crop&q=80"),
                ("Memory Foam Ergonomic Lumbar Support Cushion", "Breathable 3D mesh posture pillow with chair strap.", 1299, 2299,
                 "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=600&auto=format&fit=crop&q=80"),
                ("Hand-Woven Cotton Throw Blanket 50x60 inch", "Textured waffle weave sofa throw with fringed tassels.", 1399, 2399,
                 "https://images.unsplash.com/photo-1580301762395-21ce84d00bc6?w=600&auto=format&fit=crop&q=80"),
                ("Handcrafted Wood Document Tray & Pen Holder", "Polished teak wood desktop organizer with brass rivets.", 1499, 2599,
                 "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&auto=format&fit=crop&q=80"),
                ("Jaipuri Cotton Quilt (Razai) Hand-Stitched", "Pure surgical cotton fluffed lightweight reversible quilt.", 2299, 3999,
                 "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=600&auto=format&fit=crop&q=80"),
                ("Glazed Ceramic Coffee Mug 350ml (Set of 2)", "Dual tone rustic studio stoneware cups with wide comfortable handle.", 699, 1199,
                 "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&auto=format&fit=crop&q=80"),
                ("Aromatic Cedar Shoe Trees (Pair)", "Solid wood moisture absorbent shoe shaper with brass coil.", 1199, 2099,
                 "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600&auto=format&fit=crop&q=80"),
                ("Kashmir Papier-Mache Lacquered Trinket Box", "Gold foil hand-painted floral keepsake jewelry box.", 899, 1599,
                 "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=600&auto=format&fit=crop&q=80"),
            ]
        }
    }

    cities = ["Bengaluru", "Mumbai", "Delhi", "Chennai", "Kolkata", "Hyderabad", "Pune", "Jaipur"]
    ratings_pool = [4.0, 4.5, 4.5, 5.0, 4.0, 4.5, 4.5, 4.0, 5.0]

    products = []
    prod_id = 1

    # First flatten and collect raw items
    all_raw = []
    for cat_name, cat_data in categories.items():
        subcats = cat_data["subcategories"]
        brands = cat_data["brands"]
        for idx, (item_name, item_desc, price, orig_price, img_url) in enumerate(cat_data["items"]):
            subcat = subcats[idx % len(subcats)]
            brand = brands[idx % len(brands)]
            all_raw.append((cat_name, subcat, brand, item_name, item_desc, price, orig_price, img_url))

    all_raw = all_raw[:80]
    while len(all_raw) < 80:
        all_raw.append(all_raw[len(all_raw) % len(all_raw)])

    # Group every 5 consecutive products into variant families (for Disjoint Set)
    for i, item in enumerate(all_raw):
        cat_name, subcat, brand, item_name, item_desc, price, orig_price, img_url = item
        family_id = (i // 5) + 1

        sku_cat = cat_name[:4].upper()
        sku = f"KS-{sku_cat}-{prod_id:03d}"
        rating = random.choice(ratings_pool)
        reviews = random.randint(32, 1420)
        stock = random.randint(5, 75)
        discount_pct = round(((orig_price - price) / orig_price) * 100, 1)

        # Tags
        tags = [cat_name.lower().replace(" & ", "-"), subcat.lower()]
        if discount_pct >= 40:
            tags.append("super-deal")
        if rating >= 4.5:
            tags.append("top-rated")
        if stock <= 8:
            tags.append("low-stock")
        if random.random() < 0.4:
            tags.append("bestseller")
        if "Craft" in brand or "Hand" in item_name or "Handicrafts" in cat_name:
            tags.append("handmade")

        city = cities[(prod_id * 3 + 2) % len(cities)]

        product = {
            "id": prod_id,
            "sku": sku,
            "name": item_name,
            "brand": brand,
            "category": cat_name,
            "subcategory": subcat,
            "price": price,
            "original_price": orig_price,
            "discount_pct": discount_pct,
            "rating": rating,
            "reviews_count": reviews,
            "stock": stock,
            "tags": tags,
            "description": item_desc,
            "image_url": img_url,
            "image_seed": f"kartshelf-prod-{prod_id}",
            "variant_group_id": family_id,
            "warehouse_city": city,
            "related_ids": []
        }
        products.append(product)
        prod_id += 1

    # Populate realistic graph connections:
    for p in products:
        cands = [other["id"] for other in products if other["id"] != p["id"] and other["category"] == p["category"]]
        random.shuffle(cands)
        related = cands[:random.randint(2, 4)]
        other_cat_cands = [other["id"] for other in products if other["id"] != p["id"] and other["category"] != p["category"]]
        random.shuffle(other_cat_cands)
        if other_cat_cands:
            related.append(other_cat_cands[0])
        p["related_ids"] = sorted(related)

    # Symmetry in graph
    for p in products:
        for r_id in p["related_ids"]:
            target = next((x for x in products if x["id"] == r_id), None)
            if target and p["id"] not in target["related_ids"]:
                target["related_ids"].append(p["id"])
                target["related_ids"].sort()

    return products

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "data", "products.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    products = generate_products()
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {len(products)} products with matching images at {output_path}")

if __name__ == "__main__":
    main()
