from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import mysql.connector
from dotenv import load_dotenv
import os

# Inisialisasi Flask
app = Flask(__name__)

load_dotenv()

#koneksi database
def get_connection_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS')
    )


# Memuat dua model h5
SKIN_TYPE_MODEL_PATH = 'model_ML/skin_type_model1.h5'
SKIN_CONDITION_MODEL_PATH = 'model_ML/skin_condition_model.h5'

try:
    skin_type_model = tf.keras.models.load_model(SKIN_TYPE_MODEL_PATH)
    skin_condition_model = tf.keras.models.load_model(SKIN_CONDITION_MODEL_PATH)
except Exception as e:
    print(f"Error loading models: {e}")

# Dictionary rekomendasi berdasarkan kombinasi tipe dan kondisi kulit
RECOMMENDATIONS = {
    "normalacne": [
        {"saran_kandungan": "Salicylic acid, tea tree oil, niacinamide"},
        {"nama_produk": "CeraVe Smoothing Cream 177ml", "link_produk": "https://www.lookfantastic.com/cerave-smoothing-cream-177ml/12207665.html"},
        {"nama_produk": "La Roche-Posay Effaclar K(+) Anti-Blackhead Moisturiser 40ml", "link_produk": "https://www.lookfantastic.com/la-roche-posay-effaclar-k-anti-blackhead-moisturiser-40ml/11134733.html"},
        {"nama_produk": "Origins GinZing Ultra Hydrating Energy-Boosting Cream Moisturiser 50ml", "link_produk": "https://www.lookfantastic.com/origins-ginzing-ulta-hydrating-energy-boosting-cream-moisturiser-50ml/12193057.html"},
        {"nama_produk": "PIXI Collagen and Retinol Serum 30ml", "link_produk": "https://www.lookfantastic.com/pixi-collagen-and-retinol-serum-30ml/12040130.html"},
        {"nama_produk": "bareMinerals SkinLongevity Vital Power Infusion Serum 50ml", "link_produk": "https://www.lookfantastic.com/bareminerals-skinlongevity-vital-power-infusion-serum-50ml/11262516.html"},
        {"nama_produk": "La Roche-Posay Pure Vitamin C10 Serum 30ml", "link_produk": "https://www.lookfantastic.com/la-roche-posay-pure-vitamin-c10-serum-30ml/12049143.html"},
        {"nama_produk": "Dermalogica AGE Bright Clearing Serum 30ml", "link_produk": "https://www.lookfantastic.com/dermalogica-age-bright-clearing-serum-30ml/12134833.html"}
    ],

    "normaldark_spot": [
        {"saran_kandungan": "Niacinamide, vitamin C, retinol (mulailah dengan konsentrasi rendah)"},
        {"nama_produk": "Clinique Even Better Clinical Radical Dark Spot Corrector + Interrupter 50ml", "link_produk": "https://www.lookfantastic.com/clinique-even-better-clinical-radical-dark-spot-corrector-interrupter-50ml/12483689.html"},
        {"nama_produk": "L'Oreal Paris Dermo Expertise Revitalift Laser Renew Anti-ageing Triple Action Super Serum (30ml)", "link_produk": "https://www.lookfantastic.com/l-oreal-paris-dermo-expertise-revitalift-laser-renew-anti-aging-triple-action-super-serum-30ml/10726513.html"},
        {"nama_produk": "La Roche-Posay Pure Vitamin C10 Serum 30ml", "link_produk": "https://www.lookfantastic.com/la-roche-posay-pure-vitamin-c10-serum-30ml/12049143.html"},
        {"nama_produk": "DECLÉOR Hydra Floral White Petal Skin Perfecting Concentrate 30ml", "link_produk": "https://www.lookfantastic.com/decleor-hydra-floral-white-petal-skin-perfecting-concentrate/11423420.html"},
        {"nama_produk": "PIXI Collagen and Retinol Serum 30ml", "link_produk": "https://www.lookfantastic.com/pixi-collagen-and-retinol-serum-30ml/12040130.html"},
        {"nama_produk": "Elizabeth Arden Retinol Ceramide Capsules Line Erasing Night Serum - 30 Pieces (Sleeved Version)", "link_produk": "https://www.lookfantastic.com/elizabeth-arden-retinol-ceramide-capsules-line-erasing-night-serum-30-pieces-sleeved-version/11845677.html"},
        {"nama_produk": "Peter Thomas Roth Retinol Fusion PM 30ml", "link_produk": "https://www.lookfantastic.com/peter-thomas-roth-retinol-fusion-pm-30ml/11289146.html"}
    ],
    

    "normallarge_pores": [
        {"saran_kandungan": "Niacinamide, retinol, hyaluronic acid"},
        {"nama_produk": "PIXI Collagen and Retinol Serum 30ml", "link_produk": "https://www.lookfantastic.com/pixi-collagen-and-retinol-serum-30ml/12040130.html"},
        {"nama_produk": "bareMinerals SkinLongevity Vital Power Infusion Serum 50ml", "link_produk": "https://www.lookfantastic.com/bareminerals-skinlongevity-vital-power-infusion-serum-50ml/11262516.html"},
        {"nama_produk": "Elizabeth Arden Skin Illuminating Advanced Brightening Night Capsules (50 Capsules)", "link_produk": "https://www.lookfantastic.com/elizabeth-arden-skin-illuminating-advanced-brightening-night-capsules-50-capsules/11247489.html"},
        {"nama_produk": "Dermalogica AGE Bright Clearing Serum 30ml", "link_produk": "https://www.lookfantastic.com/dermalogica-age-bright-clearing-serum-30ml/12134833.html"},
        {"nama_produk": "Dr Dennis Gross Skincare C+Collagen Brighten and Firm Vitamin C Serum 30ml", "link_produk": "https://www.lookfantastic.com/dr-dennis-gross-skincare-c-collagen-brighten-and-firm-vitamin-c-serum-30ml/11540506.html"},
        {"nama_produk": "Murad Retinol Youth Renewal Serum Travel Size", "link_produk": "https://www.lookfantastic.com/murad-retinol-youth-renewal-serum-travel-size/11925166.html"},
        {"nama_produk": "Zelens Youth Concentrate Supreme Age-Defying Serum (30ml)", "link_produk": "https://www.lookfantastic.com/zelens-youth-concentrate-supreme-age-defying-serum-30ml/11097958.html"}
    ],
    

    "normalwrinkles": [
        {"saran_kandungan": "Retinol, hyaluronic acid, peptides"},
        {"nama_produk": "PIXI Collagen and Retinol Serum 30ml", "link_produk": "https://www.lookfantastic.com/pixi-collagen-and-retinol-serum-30ml/12040130.html"},
        {"nama_produk": "Elizabeth Arden Retinol Ceramide Capsules Line Erasing Night Serum - 30 Pieces (Sleeved Version)", "link_produk": "https://www.lookfantastic.com/elizabeth-arden-retinol-ceramide-capsules-line-erasing-night-serum-30-pieces-sleeved-version/11845677.html"},
        {"nama_produk": "Peter Thomas Roth Retinol Fusion PM 30ml", "link_produk": "https://www.lookfantastic.com/peter-thomas-roth-retinol-fusion-pm-30ml/11289146.html"},
        {"nama_produk": "Murad Retinol Youth Renewal Serum Travel Size", "link_produk": "https://www.lookfantastic.com/murad-retinol-youth-renewal-serum-travel-size/11925166.html"},
        {"nama_produk": "NIP+FAB Retinol Fix Sheet Mask 10g", "link_produk": "https://www.lookfantastic.com/nip-fab-retinol-fix-sheet-mask-10g/12192676.html"},
        {"nama_produk": "Shiseido Benefiance Pure Retinol Express Smoothing Eye Mask x 12 Sachets", "link_produk": "https://www.lookfantastic.com/shiseido-benefiance-pure-retinol-express-smoothing-eye-mask-x-12-sachets/10991445.html"}
    ],
    

    "normal": [
        {"saran_kandungan": "Hyaluronic acid, vitamin C, ceramides"},
        {"nama_produk": "The Ordinary Vitamin C Suspension Cream 30/100 in Silicone 30ml", "link_produk": "https://www.lookfantastic.com/the-ordinary-vitamin-c-suspension-cream-30-in-silicone-30ml/11638504.html"},
        {"nama_produk": "Fade Out ADVANCED Even Skin Tone Night Cream 50ml", "link_produk": "https://www.lookfantastic.com/fade-out-advanced-even-skin-tone-night-cream-50ml/11284055.html"},
        {"nama_produk": "JASON Age Renewal Vitamin E 25,000iu Cream (120g)", "link_produk": "https://www.lookfantastic.com/jason-age-renewal-vitamin-e-25-000iu-cream-113g/10546498.html"},
        {"nama_produk": "DECLÉOR Hydra Floral White Petal Skin Perfecting Concentrate 30ml", "link_produk": "https://www.lookfantastic.com/decleor-hydra-floral-white-petal-skin-perfecting-concentrate/11423420.html"},
        {"nama_produk": "NUXE Huile Prodigieuse Multi Usage Dry Oil 50ml", "link_produk": "https://www.lookfantastic.com/nuxe-huile-prodigieuse-multi-usage-dry-oil-50ml/11401781.html"},
        {"nama_produk": "Pestle & Mortar Balance Facial Spritz", "link_produk": "https://www.lookfantastic.com/pestle-mortar-balance-facial-spritz/11887746.html"}
    ],
    
    
    "oilyacne": [
        {"saran_kandungan": "Salicylic acid, tea tree oil, niacinamide"},
        {"nama_produk": "Aveda Hand Relief Night Renewal Serum 30ml", "link_produk": "https://www.lookfantastic.com/aveda-hand-relief-night-renewal-serum-30ml/11032875.html"},
        {"nama_produk": "COSRX Salicylic Acid Daily Gentle Cleanser 170g", "link_produk": "https://www.lookfantastic.com/cosrx-salicylic-acid-daily-gentle-cleanser-170g/11540297.html"},
        {"nama_produk": "La Roche-Posay Pigmentclar Serum 30ml", "link_produk": "https://www.lookfantastic.com/la-roche-posay-pigmentclar-serum-30ml/11091881.html"},
        {"nama_produk": "Dermalogica AGE Bright Clearing Serum 30ml", "link_produk": "https://www.lookfantastic.com/dermalogica-age-bright-clearing-serum-30ml/12134833.html"},
        {"nama_produk": "Elizabeth Arden Skin Illuminating Advanced Brightening Day Serum (30ml)", "link_produk": "https://www.lookfantastic.com/elizabeth-arden-skin-illuminating-advanced-brightening-day-serum-30ml/11247488.html"},
        {"nama_produk": "CeraVe Smoothing Cream 177ml", "link_produk": "https://www.lookfantastic.com/cerave-smoothing-cream-177ml/12207665.html"},
        {"nama_produk": "La Roche-Posay Effaclar Duo+ SPF30 40ml", "link_produk": "https://www.lookfantastic.com/la-roche-posay-effaclar-duo-spf30-40ml/11434756.html"}
    ],
    

    "oilydark_spot": [
        {"saran_kandungan": "Niacinamide, vitamin C, retinol (mulailah dengan konsentrasi rendah)"},
        {"nama_produk": "Elizabeth Arden Skin Illuminating Advanced Brightening Day Serum (30ml)", "link_produk": "https://www.lookfantastic.com/elizabeth-arden-skin-illuminating-advanced-brightening-day-serum-30ml/11247488.html"},
        {"nama_produk": "CeraVe Smoothing Cream 177ml", "link_produk": "https://www.lookfantastic.com/cerave-smoothing-cream-177ml/12207665.html"},
        {"nama_produk": "La Roche-Posay Effaclar Duo+ SPF30 40ml", "link_produk": "https://www.lookfantastic.com/la-roche-posay-effaclar-duo-spf30-40ml/11434756.html"},
        {"nama_produk": "Fade Out ADVANCED Even Skin Tone Night Cream 50ml", "link_produk": "https://www.lookfantastic.com/fade-out-advanced-even-skin-tone-night-cream-50ml/11284055.html"},
        {"nama_produk": "JASON Age Renewal Vitamin E 25,000iu Cream (120g)", "link_produk": "https://www.lookfantastic.com/jason-age-renewal-vitamin-e-25-000iu-cream-113g/10546498.html"},
        {"nama_produk": "DECLÉOR Hydra Floral White Petal Skin Perfecting Concentrate 30ml", "link_produk": "https://www.lookfantastic.com/decleor-hydra-floral-white-petal-skin-perfecting-concentrate/11423420.html"},
        {"nama_produk": "PIXI Collagen and Retinol Serum 30ml", "link_produk": "https://www.lookfantastic.com/pixi-collagen-and-retinol-serum-30ml/12040130.html"}
    ],
    

    "oilylarge_pores": [
        {"saran_kandungan": "Niacinamide, retinol, clay mask"},
        {"nama_produk": "La Roche-Posay Effaclar Clay Mask 100ml", "link_produk": "https://www.lookfantastic.com/la-roche-posay-effaclar-clay-mask-100ml/11434755.html"},
        {"nama_produk": "Elizabeth Arden Skin Illuminating Advanced Brightening Night Capsules (50 Capsules)", "link_produk": "https://www.lookfantastic.com/elizabeth-arden-skin-illuminating-advanced-brightening-night-capsules-50-capsules/11247489.html"},
        {"nama_produk": "Dermalogica AGE Bright Clearing Serum 30ml", "link_produk": "https://www.lookfantastic.com/dermalogica-age-bright-clearing-serum-30ml/12134833.html"},
        {"nama_produk": "Dr Dennis Gross Skincare C+Collagen Brighten and Firm Vitamin C Serum 30ml", "link_produk": "https://www.lookfantastic.com/dr-dennis-gross-skincare-c-collagen-brighten-and-firm-vitamin-c-serum-30ml/11540506.html"},
        {"nama_produk": "Murad Retinol Youth Renewal Serum Travel Size", "link_produk": "https://www.lookfantastic.com/murad-retinol-youth-renewal-serum-travel-size/11925166.html"},
        {"nama_produk": "Zelens Youth Concentrate Supreme Age-Defying Serum (30ml)", "link_produk": "https://www.lookfantastic.com/zelens-youth-concentrate-supreme-age-defying-serum-30ml/11097958.html"},
        {"nama_produk": "PIXI Collagen and Retinol Serum 30ml", "link_produk": "https://www.lookfantastic.com/pixi-collagen-and-retinol-serum-30ml/12040130.html"}
    ],
    

    "oilywrinkles": [
        {"saran_kandungan": "Retinol, hyaluronic acid, peptides"},
        {"nama_produk": "PIXI Collagen and Retinol Serum 30ml", "link_produk": "https://www.lookfantastic.com/pixi-collagen-and-retinol-serum-30ml/12040130.html"},
        {"nama_produk": "Elizabeth Arden Retinol Ceramide Capsules Line Erasing Night Serum - 30 Pieces (Sleeved Version)", "link_produk": "https://www.lookfantastic.com/elizabeth-arden-retinol-ceramide-capsules-line-erasing-night-serum-30-pieces-sleeved-version/11845677.html"},
        {"nama_produk": "Peter Thomas Roth Retinol Fusion PM 30ml", "link_produk": "https://www.lookfantastic.com/peter-thomas-roth-retinol-fusion-pm-30ml/11289146.html"},
        {"nama_produk": "Murad Retinol Youth Renewal Serum Travel Size", "link_produk": "https://www.lookfantastic.com/murad-retinol-youth-renewal-serum-travel-size/11925166.html"},
        {"nama_produk": "NIP+FAB Retinol Fix Sheet Mask 10g", "link_produk": "https://www.lookfantastic.com/nip-fab-retinol-fix-sheet-mask-10g/12192676.html"},
        {"nama_produk": "Shiseido Benefiance Pure Retinol Express Smoothing Eye Mask x 12 Sachets", "link_produk": "https://www.lookfantastic.com/shiseido-benefiance-pure-retinol-express-smoothing-eye-mask-x-12-sachets/10991445.html"}
    ],
    

    "oilynormal": [
        {"saran_kandungan": "Niacinamide, hyaluronic acid, gel moisturizer"},
        {"nama_produk": "The INKEY List Peptide Moisturizer 50ml", "link_produk": "https://www.lookfantastic.com/the-inkey-list-peptide-moisturizer-50ml/12435692.html"},
        {"nama_produk": "CeraVe Facial Moisturising Lotion SPF 25 52ml", "link_produk": "https://www.lookfantastic.com/cerave-facial-moisturising-lotion-spf-25-52ml/11798689.html"},
        {"nama_produk": "La Roche-Posay Effaclar Duo+ SPF30 40ml", "link_produk": "https://www.lookfantastic.com/la-roche-posay-effaclar-duo-spf30-40ml/11434756.html"},
        {"nama_produk": "Origins GinZing Ultra Hydrating Energy-Boosting Cream Moisturiser 50ml", "link_produk": "https://www.lookfantastic.com/origins-ginzing-ulta-hydrating-energy-boosting-cream-moisturiser-50ml/12193057.html"},
        {"nama_produk": "bareMinerals SkinLongevity Vital Power Infusion Serum 50ml", "link_produk": "https://www.lookfantastic.com/bareminerals-skinlongevity-vital-power-infusion-serum-50ml/11262516.html"},
        {"nama_produk": "Elizabeth Arden Skin Illuminating Advanced Brightening Day Serum (30ml)", "link_produk": "https://www.lookfantastic.com/elizabeth-arden-skin-illuminating-advanced-brightening-day-serum-30ml/11247488.html"}
    ],
    
    
    "dryacne": [
        {"saran_kandungan": "Salicylic acid (konsentrasi rendah), tea tree oil, hyaluronic acid"},
        {"nama_produk": "CeraVe Smoothing Cream 177ml", "link_produk": "https://www.lookfantastic.com/cerave-smoothing-cream-177ml/12207665.html"},
        {"nama_produk": "Origins GinZing Ultra Hydrating Energy-Boosting Cream Moisturiser 50ml", "link_produk": "https://www.lookfantastic.com/origins-ginzing-ulta-hydrating-energy-boosting-cream-moisturiser-50ml/12193057.html"},
        {"nama_produk": "Neutrogena Refreshingly Clear Oil-Free Moisturiser 50ml", "link_produk": "https://www.lookfantastic.com/neutrogena-refreshingly-clear-oil-free-moisturiser-50ml/12309605.html"},
        {"nama_produk": "La Roche-Posay Pure Vitamin C10 Serum 30ml", "link_produk": "https://www.lookfantastic.com/la-roche-posay-pure-vitamin-c10-serum-30ml/12049143.html"},
        {"nama_produk": "L'Oreal Paris Dermo Expertise Revitalift Laser Renew Anti-ageing Triple Action Super Serum (30ml)", "link_produk": "https://www.lookfantastic.com/l-oreal-paris-dermo-expertise-revitalift-laser-renew-anti-aging-triple-action-super-serum-30ml/10726513.html"},
        {"nama_produk": "GLAMGLOW Superserum 30ml", "link_produk": "https://www.lookfantastic.com/glamglow-superserum-30ml/12036336.html"},
        {"nama_produk": "Aurelia Skincare Firm & Replenish Body Serum 250ml", "link_produk": "https://www.lookfantastic.com/aurelia-skincare-firm-replenish-body-serum-250ml/11491745.html"}
    ],
    

    "drydark_spot": [
        {"saran_kandungan": "Niacinamide, vitamin C, hyaluronic acid"},
        {"nama_produk": "La Roche-Posay Toleriane Sensitive Fluid Moisturiser 40ml", "link_produk": "https://www.lookfantastic.com/la-roche-posay-toleriane-sensitive-fluid-moisturiser-40ml/11855110.html"},
        {"nama_produk": "Fade Out ADVANCED + Age Protection Even Skin Tone Day Cream SPF 25 50ml", "link_produk": "https://www.lookfantastic.com/fade-out-advanced-age-protection-even-skin-tone-day-cream-spf-25-50ml/11490811.html"},
        {"nama_produk": "Bioderma Hydrabio Gel Cream 40ml", "link_produk": "https://www.lookfantastic.com/bioderma-hydrabio-gel-cream-40ml/11688484.html"},
        {"nama_produk": "PIXI Overnight Glow Serum", "link_produk": "https://www.lookfantastic.com/pixi-overnight-glow-serum/11200045.html"},
        {"nama_produk": "PIXI Collagen and Retinol Serum 30ml", "link_produk": "https://www.lookfantastic.com/pixi-collagen-and-retinol-serum-30ml/12040130.html"},
        {"nama_produk": "Liz Earle Superskin Face Serum 30ml Pump", "link_produk": "https://www.lookfantastic.com/liz-earle-superskin-face-serum-30ml-pump/12528852.html"}
    ],
    

    "drylarge_pores": [
        {"saran_kandungan": "Hyaluronic acid, niacinamide, retinol (mulailah dengan konsentrasi rendah)"},
        {"nama_produk": "La Roche-Posay Toleriane Sensitive Fluid Moisturiser 40ml", "link_produk": "https://www.lookfantastic.com/la-roche-posay-toleriane-sensitive-fluid-moisturiser-40ml/11855110.html"},
        {"nama_produk": "Fade Out ADVANCED + Age Protection Even Skin Tone Day Cream SPF 25 50ml", "link_produk": "https://www.lookfantastic.com/fade-out-advanced-age-protection-even-skin-tone-day-cream-spf-25-50ml/11490811.html"},
        {"nama_produk": "Bioderma Hydrabio Gel Cream 40ml", "link_produk": "https://www.lookfantastic.com/bioderma-hydrabio-gel-cream-40ml/11688484.html"},
        {"nama_produk": "PIXI Collagen and Retinol Serum 30ml", "link_produk": "https://www.lookfantastic.com/pixi-collagen-and-retinol-serum-30ml/12040130.html"},
        {"nama_produk": "NIP+FAB Retinol Fix Serum Extreme 50ml", "link_produk": "https://www.lookfantastic.com/nip-fab-retinol-fix-serum-extreme-50ml/12192674.html"},
        {"nama_produk": "Murad Retinol Youth Renewal Serum Travel Size", "link_produk": "https://www.lookfantastic.com/murad-retinol-youth-renewal-serum-travel-size/11925166.html"}
    ],
    

    "drywrinkles": [
        {"saran_kandungan": "Retinol, hyaluronic acid, peptides, ceramides"},
        {"nama_produk": "PIXI Collagen and Retinol Serum 30ml", "link_produk": "https://www.lookfantastic.com/pixi-collagen-and-retinol-serum-30ml/12040130.html"},
        {"nama_produk": "NIP+FAB Retinol Fix Serum Extreme 50ml", "link_produk": "https://www.lookfantastic.com/nip-fab-retinol-fix-serum-extreme-50ml/12192674.html"},
        {"nama_produk": "Murad Retinol Youth Renewal Serum Travel Size", "link_produk": "https://www.lookfantastic.com/murad-retinol-youth-renewal-serum-travel-size/11925166.html"},
        {"nama_produk": "Elizabeth Arden Retinol Ceramide Capsules Line Erasing Night Serum - 30 Pieces (Sleeved Version)", "link_produk": "https://www.lookfantastic.com/elizabeth-arden-retinol-ceramide-capsules-line-erasing-night-serum-30-pieces-sleeved-version/11845677.html"},
        {"nama_produk": "Peter Thomas Roth Retinol Fusion PM 30ml", "link_produk": "https://www.lookfantastic.com/peter-thomas-roth-retinol-fusion-pm-30ml/11289146.html"},
        {"nama_produk": "Murad Retinol Youth Renewal Serum Travel Size", "link_produk": "https://www.lookfantastic.com/murad-retinol-youth-renewal-serum-travel-size/11925166.html"},
        {"nama_produk": "Zelens Youth Concentrate Supreme Age-Defying Serum (30ml)", "link_produk": "https://www.lookfantastic.com/zelens-youth-concentrate-supreme-age-defying-serum-30ml/11097958.html"}
    ],


    "drynormal": [
        {"saran_kandungan": "Hyaluronic acid, ceramides, oil-based moisturizer"},
        {"nama_produk": "Dr.Jart+ Ceramidin Cream 50ml", "link_produk": "https://www.lookfantastic.com/dr.jart-ceramidin-cream-50ml/12099664.html"},
        {"nama_produk": "First Aid Beauty Ultra Repair Cream (56.7g)", "link_produk": "https://www.lookfantastic.com/first-aid-beauty-ultra-repair-cream-56.7g/11054496.html"},
        {"nama_produk": "CeraVe Moisturising Cream 177ml", "link_produk": "https://www.lookfantastic.com/cerave-smoothing-cream-177ml/12207665.html"},
        {"nama_produk": "bareMinerals Butter Drench Intense Moisurising Day Cream", "link_produk": "https://www.lookfantastic.com/bareminerals-butter-drench-intense-moisurising-day-cream/11262518.html"},
        {"nama_produk": "Elizabeth Arden Ceramide Capsules Advanced (90 Capsules)", "link_produk": "https://www.lookfantastic.com/elizabeth-arden-ceramide-capsules-advanced-90-capsules/11382385.html"},
        {"nama_produk": "COSRX AC Collection Blemish Spot Clearing Serum 40ml", "link_produk": "https://www.lookfantastic.com/cosrx-ac-collection-blemish-spot-clearing-serum-40ml/12269561.html"},
        {"nama_produk": "Murad Retinol Youth Renewal Serum Travel Size", "link_produk": "https://www.lookfantastic.com/murad-retinol-youth-renewal-serum-travel-size/11925166.html"},
        {"nama_produk": "Manuka Doctor 24K Gold & Manuka Honey Face Oil 12ml", "link_produk": "https://www.lookfantastic.com/manuka-doctor-24k-gold-manuka-honey-face-oil-12ml/11465862.html"}
    ],
    
}


# Endpoint untuk prediksi
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Periksa apakah file gambar ada dalam request
        if 'image' not in request.files:
            return jsonify({'status': 'error', 'message': 'No image file provided.'})
        
        # Ambil id_user dari form
        id_user_str = request.form.get('id_user')
        if not id_user_str or not id_user_str.isdigit():
            return jsonify({'status': 'error', 'message': 'Invalid or missing id_user. Must be an integer.'})
        
        id_user = int(id_user_str)

        # Baca file gambar dari request
        image_file = request.files['image']
        image = Image.open(io.BytesIO(image_file.read())).resize((224, 224))  # Resize sesuai kebutuhan model

        # Preprocessing gambar
        image_array = np.array(image) 
        image_array = np.expand_dims(image_array, axis=0) 

        # Prediksi dengan kedua model
        skin_type_prediction = skin_type_model.predict(image_array)
        skin_condition_prediction = skin_condition_model.predict(image_array)

        print(f"Skin type prediction: {skin_type_prediction}")
        print(f"Skin condition prediction: {skin_condition_prediction}")

        # Ambil hasil prediksi
        skin_type_result = decode_skin_type(skin_type_prediction)
        skin_condition_result = decode_skin_condition(skin_condition_prediction)

        print(f"Skin type result: {skin_type_result}")
        print(f"Skin condition result: {skin_condition_result}")

        # Gabungkan hasil prediksi untuk menentukan rekomendasi berdasarkan kombinasi
        combined_key = f"{skin_type_result['name'].split()[0].lower()}{skin_condition_result['name'].split()[0].lower()}"
        recommendation = RECOMMENDATIONS.get(combined_key)

        # Kembalikan hasil rekomendasi
        if recommendation:
            saran_kandungan = recommendation[0].get('saran_kandungan', '')
            for product in recommendation[1:]:  # melakukan terasi untuk banyaknya produk
                save_to_database(id_user, skin_type_result['name'], skin_condition_result['name'], saran_kandungan, product)
            return jsonify({
                'status': 'success',
                'recommendation': recommendation,
                'skin_type': skin_type_result['name'],
                'skin_condition': skin_condition_result['name']
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'Kombinasi {combined_key} tidak ditemukan dalam rekomendasi.'
            })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

# Fungsi untuk menyimpan hasil ke database
def save_to_database(id_user, skin_type, skin_condition, saran_kandungan, product):
    try: 

        connection = get_connection_db()
        cursor = connection.cursor()

        insert_query = """
            INSERT INTO user_data (id_user, skin_type, skin_condition, saran_kandungan, nama_produk, link_produk) VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            id_user,
            skin_type, 
            skin_condition, 
            saran_kandungan,
            product['nama_produk'],
            product['link_produk']
        ))
        connection.commit()
        cursor.close()
        connection.close()
        print("successfuly")
    except Exception as e:
        print(f"Error save data to database: {e}")


# Fungsi untuk mendekode hasil prediksi tipe kulit
def decode_skin_type(prediction):
    skin_type_recommendations = {
        'dry': 0,
        'normal': 1,
        'oily': 2
    }   

    # Periksa hasil prediksi dan kembalikan label numeriknya
    pred_index = np.argmax(prediction)
    skin_type_label = list(skin_type_recommendations.values())[pred_index]
    skin_type_name = list(skin_type_recommendations.keys())[pred_index]
    return {"name": skin_type_name, "label": skin_type_label}

# Fungsi untuk mendekode hasil prediksi kondisi kulit
def decode_skin_condition(prediction):
    skin_condition_recommendations = {
        'acne': 0,
        'dark_spot': 1,
        'large_pores': 2,
        'normal': 3,
        'wrinkles': 4
    }
     # Periksa hasil prediksi dan kembalikan label numeriknya
    pred_index = np.argmax(prediction)
    skin_condition_label = list(skin_condition_recommendations.values())[pred_index]
    skin_condition_name = list(skin_condition_recommendations.keys())[pred_index]
    
    return {"name": skin_condition_name, "label": skin_condition_label}

# Menjalankan server Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
