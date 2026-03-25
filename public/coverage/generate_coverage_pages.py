#!/usr/bin/env python3
"""
Medicare Coverage Lookup (MCL) HTML Generator for GougeStop.com
Generates 21 static HTML files from CPT test data.
"""

import os
import json
from datetime import datetime

# ============================================================================
# TEST DATA
# ============================================================================

TESTS = [
    {
        "cpt": "80053",
        "name": "Comprehensive Metabolic Panel (CMP)",
        "medicare": 14.35,
        "lab_min": 45,
        "lab_max": 237,
        "markup_min": 214,
        "markup_max": 1552,
        "description": "A comprehensive metabolic panel (CMP) measures 14 chemical compounds in your blood, including electrolytes, kidney function, liver function, and glucose levels. This test is commonly ordered during routine physicals, when monitoring chronic conditions, or as part of a comprehensive health assessment.",
        "coverage": "Yes, Medicare Part B covers CMP when ordered by your treating physician and deemed medically necessary.",
        "denials": [
            "Test ordered without medical necessity or clear clinical indication",
            "Ordered too frequently (e.g., more than once per year without change in condition)",
            "Duplicate test—another lab already performed the same test recently",
            "Ordered for screening purposes only in asymptomatic patients",
            "Ordered by a non-treating physician without established patient relationship"
        ],
        "faqs": [
            {
                "q": "Why is my lab charging $150 when Medicare only pays $14?",
                "a": "Labs charge different rates based on their overhead, location, and payer mix. Medicare rates are set by CMS; private insurance and self-pay patients often pay much more. The GougeStop app helps you compare prices before testing."
            },
            {
                "q": "Is a CMP the same as a BMP?",
                "a": "No. A BMP (Basic Metabolic Panel) includes 8 measurements, while a CMP includes 14. A CMP is more comprehensive and costs more."
            },
            {
                "q": "Can Medicare deny my CMP?",
                "a": "Rarely, if it's clearly medically necessary. But some labs may bill it incorrectly or your doctor may order it without sufficient documentation—check your Explanation of Benefits."
            }
        ],
        "related": ["80048", "80076", "82947"]
    },
    {
        "cpt": "85025",
        "name": "Complete Blood Count with Differential (CBC)",
        "medicare": 7.77,
        "lab_min": 30,
        "lab_max": 124,
        "markup_min": 286,
        "markup_max": 1496,
        "description": "A CBC with differential counts different types of white blood cells, red blood cells, and platelets. It's one of the most common lab tests, used to detect infections, anemia, clotting disorders, and many other conditions. Doctors order it during routine check-ups and when evaluating symptoms.",
        "coverage": "Yes, Medicare Part B covers CBC with differential when medically necessary and ordered by a treating physician.",
        "denials": [
            "Ordered for screening only without clinical indication",
            "Duplicate test within short timeframe (less than 30 days)",
            "Ordered by provider not in established patient relationship",
            "No documentation of medical necessity in patient record",
            "Ordered as part of routine screening in completely asymptomatic patient"
        ],
        "faqs": [
            {
                "q": "How often can I get a CBC without Medicare denying it?",
                "a": "There's no strict limit, but Medicare expects your doctor to document medical necessity. Routine annual physicals are typically covered; multiple CBCs per month without clinical reason may be denied."
            },
            {
                "q": "What's the difference between CBC and CBC with differential?",
                "a": "A regular CBC counts total white cells, red cells, and platelets. With differential, it breaks down white cell types (neutrophils, lymphocytes, etc.), giving more detail."
            },
            {
                "q": "Why do labs charge $100+ when the Medicare rate is $7.77?",
                "a": "Lab overhead (staff, equipment, facilities) is significant. Uninsured and commercial insurance patients subsidize the system; they pay retail rates that cover all costs."
            }
        ],
        "related": ["85027", "80053", "83036"]
    },
    {
        "cpt": "80061",
        "name": "Lipid Panel",
        "medicare": 13.39,
        "lab_min": 50,
        "lab_max": 177,
        "markup_min": 273,
        "markup_max": 1222,
        "description": "A lipid panel measures cholesterol (total, LDL, HDL) and triglycerides. It's essential for assessing cardiovascular risk and monitoring treatment with statins or other cholesterol-lowering medications. Doctors typically order this annually or more frequently if results are abnormal.",
        "coverage": "Yes, Medicare Part B covers lipid panels when ordered by a treating physician, particularly for patients with cardiovascular disease, diabetes, or as part of preventive screening.",
        "denials": [
            "Ordered too frequently (more than once per year without clinical change)",
            "No history of cardiovascular disease or risk factors documented",
            "Patient already had lipid panel done recently at another facility",
            "Ordered for screening only in very low-risk patient without justification",
            "Missing ICD-10 code indicating medical necessity"
        ],
        "faqs": [
            {
                "q": "How often should I have a lipid panel?",
                "a": "Medicare typically covers annual lipid panels. If you're on statin therapy or have high cholesterol, your doctor may order more frequently (every 3-6 months) to monitor treatment effectiveness."
            },
            {
                "q": "What's included in a lipid panel?",
                "a": "Total cholesterol, LDL (bad), HDL (good), and triglycerides. Some labs also include VLDL and ratios."
            },
            {
                "q": "Why is the markup so high on lipid panels?",
                "a": "Lab costs are relatively fixed per test. Lipid panels require chemistry analyzers and reagents. Medicare's reimbursement doesn't cover full lab overhead for self-pay patients."
            }
        ],
        "related": ["82947", "84480", "84443"]
    },
    {
        "cpt": "83036",
        "name": "Hemoglobin A1c (HbA1c)",
        "medicare": 11.78,
        "lab_min": 40,
        "lab_max": 130,
        "markup_min": 240,
        "markup_max": 1003,
        "description": "HbA1c measures average blood glucose over the past 2-3 months. It's the gold standard for diagnosing and monitoring diabetes. Doctors order this regularly for diabetic patients and to diagnose prediabetes or diabetes.",
        "coverage": "Yes, Medicare Part B covers HbA1c. For diagnosis, it's typically covered once per year if results are normal; for monitoring diabetes, it's often covered 2-4 times per year depending on treatment.",
        "denials": [
            "Ordered more frequently than clinically appropriate (e.g., monthly without medication changes)",
            "No diagnosis of diabetes or prediabetes on record",
            "Duplicate test—same test done at another lab within 30 days",
            "Patient with well-controlled diabetes getting tested too frequently",
            "No medical record documentation of clinical indication"
        ],
        "faqs": [
            {
                "q": "How often should I have HbA1c tested?",
                "a": "If you have diabetes, every 3-6 months is typical if your treatment is changing, or annually if stable. If you're prediabetic, once per year is common."
            },
            {
                "q": "Can I use HbA1c instead of a fasting glucose?",
                "a": "For diagnosis and monitoring, yes—HbA1c is often preferred because it doesn't require fasting. For acute blood sugar checks, fasting glucose or point-of-care testing is needed."
            },
            {
                "q": "Why is there such variation in lab charges ($40–$130)?",
                "a": "Urban labs and hospital systems often charge more. Independent labs may charge less. Geography and facility type heavily influence pricing."
            }
        ],
        "related": ["82947", "80053", "80048"]
    },
    {
        "cpt": "80048",
        "name": "Basic Metabolic Panel (BMP)",
        "medicare": 9.64,
        "lab_min": 35,
        "lab_max": 148,
        "markup_min": 263,
        "markup_max": 1435,
        "description": "A BMP measures 8 key chemicals: electrolytes (sodium, potassium, chloride, CO2), kidney function (BUN, creatinine), glucose, and sometimes calcium. It's ordered to monitor kidney and liver health, especially in patients on medications or with chronic conditions.",
        "coverage": "Yes, Medicare Part B covers BMP when ordered by a treating physician and medically necessary.",
        "denials": [
            "Ordered without clear clinical indication",
            "Duplicate test—recent BMP or CMP already in medical record",
            "Ordered too frequently (e.g., monthly without medication changes)",
            "No documented chronic condition or medication justification",
            "Screening test in asymptomatic, low-risk patient"
        ],
        "faqs": [
            {
                "q": "What's the difference between BMP and CMP?",
                "a": "BMP has 8 measurements (basic electrolytes and kidney function). CMP has 14 (includes liver function tests and more). Both are covered; your doctor chooses based on clinical need."
            },
            {
                "q": "If I'm on blood pressure medication, how often should I get a BMP?",
                "a": "Initial BMP is often done before starting medication, then annually or as clinically indicated. If your medication changes, your doctor may order another BMP to check kidney function."
            },
            {
                "q": "Why is lab charging $120 when Medicare pays $9.64?",
                "a": "Lab overhead costs are fixed. Medicare rates don't reflect the full operational cost of the lab; they're a negotiated minimum."
            }
        ],
        "related": ["80053", "80076", "84443"]
    },
    {
        "cpt": "84443",
        "name": "Thyroid Stimulating Hormone (TSH)",
        "medicare": 16.80,
        "lab_min": 60,
        "lab_max": 220,
        "markup_min": 257,
        "markup_max": 1210,
        "description": "TSH is the primary screening test for thyroid function. Elevated or low TSH can indicate hyperthyroidism or hypothyroidism. Doctors order this when evaluating fatigue, weight changes, temperature sensitivity, or to monitor thyroid medication (levothyroxine).",
        "coverage": "Yes, Medicare Part B covers TSH screening and monitoring. Initial screening is typically covered; ongoing monitoring is covered for patients on thyroid medication.",
        "denials": [
            "Ordered without symptoms or history of thyroid disease",
            "Tested too frequently (e.g., monthly) without medication changes",
            "Patient on stable thyroid replacement with recent TSH test",
            "Screening in asymptomatic patient without risk factors",
            "Duplicate test within short timeframe"
        ],
        "faqs": [
            {
                "q": "How often should I get TSH tested if I'm on levothyroxine?",
                "a": "After starting or changing dose, recheck in 6-8 weeks. Once stable, annual testing is typical. If symptoms persist, your doctor may test more frequently."
            },
            {
                "q": "Does Medicare cover Free T4 if my TSH is abnormal?",
                "a": "Yes, if clinically indicated. Often both TSH and Free T4 are ordered together to fully evaluate thyroid function."
            },
            {
                "q": "Why such a big gap between Medicare ($16.80) and lab charges ($60–$220)?",
                "a": "TSH requires specialized equipment and reagents. Hospital labs and major chains often charge premium rates; independent labs may be cheaper."
            }
        ],
        "related": ["84480", "82607", "80076"]
    },
    {
        "cpt": "81003",
        "name": "Urinalysis, Automated",
        "medicare": 2.92,
        "lab_min": 15,
        "lab_max": 67,
        "markup_min": 414,
        "markup_max": 2195,
        "description": "An automated urinalysis checks for glucose, protein, nitrites, leukocyte esterase, and other markers in urine. It's used to screen for urinary tract infections, kidney disease, and diabetes. It's one of the cheapest lab tests but often has the highest markup.",
        "coverage": "Yes, Medicare Part B covers urinalysis when medically necessary—routine screening during annual physicals, or when evaluating UTI symptoms, kidney disease, or diabetes.",
        "denials": [
            "Screening test in asymptomatic patient without clinical indication",
            "Routine urinalysis at annual physical may require specific diagnosis codes",
            "Duplicate test—recent urinalysis on file",
            "Ordered without documentation of clinical reason",
            "Patient with no history of kidney disease or UTI getting tested without symptoms"
        ],
        "faqs": [
            {
                "q": "Why is urinalysis the most expensive markup on my bill?",
                "a": "Because the base cost is so low ($2.92 Medicare rate) but lab charges are fixed ($15–$67 per test). The markup percentage is huge, but absolute cost is still low."
            },
            {
                "q": "What's the difference between automated and microscopic urinalysis?",
                "a": "Automated urinalysis runs samples through a machine for basic screening. Microscopic adds manual examination of cells. Microscopic costs more but provides more detail."
            },
            {
                "q": "How often should I get urinalysis?",
                "a": "Annual screening during physical is standard. If you have symptoms or a UTI history, your doctor may order it more frequently."
            }
        ],
        "related": ["82947", "80048", "83036"]
    },
    {
        "cpt": "82306",
        "name": "Vitamin D, 25-Hydroxy",
        "medicare": 29.04,
        "lab_min": 65,
        "lab_max": 298,
        "markup_min": 124,
        "markup_max": 926,
        "description": "This test measures 25-hydroxyvitamin D, the form that indicates your vitamin D status. Low vitamin D is linked to bone health, immune function, and mood. Doctors order this to screen for deficiency, especially in older adults, those with limited sun exposure, or those with bone or autoimmune conditions.",
        "coverage": "Yes, Medicare Part B covers vitamin D testing for patients with symptoms of deficiency, bone disease, or malabsorption. Routine screening may have limitations.",
        "denials": [
            "Screening in asymptomatic patient without bone disease or deficiency symptoms",
            "Tested too frequently (routine annual screening may not be covered)",
            "No diagnosis code documenting reason for test",
            "Patient taking vitamin D supplements and asymptomatic",
            "Duplicate test within 6-12 months without symptom change"
        ],
        "faqs": [
            {
                "q": "When should I get vitamin D tested?",
                "a": "If you have osteoporosis, bone pain, limited sun exposure, or GI conditions affecting absorption, testing is reasonable. Otherwise, routine screening may not be covered."
            },
            {
                "q": "Is vitamin D testing covered by Medicare?",
                "a": "Yes, if medically necessary. Routine screening in healthy, asymptomatic individuals may not be covered. Check with your doctor about medical justification."
            },
            {
                "q": "Why is vitamin D one of the cheaper tests?",
                "a": "It's a more specialized test, so the Medicare rate is higher ($29). Labs still mark it up 2-10x, but absolute cost is lower than many basic panels."
            }
        ],
        "related": ["80076", "84443", "82728"]
    },
    {
        "cpt": "84403",
        "name": "Testosterone, Total",
        "medicare": 25.10,
        "lab_min": 89,
        "lab_max": 350,
        "markup_min": 255,
        "markup_max": 1294,
        "description": "This test measures total testosterone in blood. It's ordered for men with fatigue, low libido, or erectile dysfunction; for women with irregular periods or ovarian concerns; and to monitor hormone replacement therapy. Testosterone levels vary by time of day and sex.",
        "coverage": "Yes, Medicare Part B covers testosterone testing when ordered by a physician for documented symptoms or hormone-related concerns.",
        "denials": [
            "Ordered without clinical symptoms or documented indication",
            "Screening in asymptomatic patient",
            "Testing to monitor testosterone replacement in healthy individual without medical record",
            "Duplicate test without symptom change or therapy adjustment",
            "Ordered for bodybuilding or athletic performance assessment"
        ],
        "faqs": [
            {
                "q": "What time of day should I get testosterone tested?",
                "a": "Early morning (before 10am) is best, since testosterone levels peak in the morning and decline throughout the day. Your doctor should specify this."
            },
            {
                "q": "Is testosterone testing covered by Medicare?",
                "a": "Yes, if you have documented symptoms (fatigue, low libido, muscle loss) and a treating physician. Routine screening in healthy men is less likely to be covered."
            },
            {
                "q": "Why is the lab charge range so wide ($89–$350)?",
                "a": "Urban teaching hospitals and specialized clinics charge more. Independent labs and rural facilities often charge less. Location and facility type matter."
            }
        ],
        "related": ["84480", "82728", "80076"]
    },
    {
        "cpt": "80076",
        "name": "Hepatic Function Panel",
        "medicare": 10.41,
        "lab_min": 40,
        "lab_max": 170,
        "markup_min": 284,
        "markup_max": 1534,
        "description": "A hepatic (liver) function panel measures liver enzymes and bilirubin to assess liver health. It's ordered to check for liver disease, monitor medications that affect the liver, or evaluate jaundice and abdominal pain. It includes AST, ALT, ALP, bilirubin, and albumin.",
        "coverage": "Yes, Medicare Part B covers hepatic function panels when medically necessary—to monitor chronic liver disease, check medication side effects, or evaluate acute symptoms.",
        "denials": [
            "Screening in asymptomatic patient without liver disease risk",
            "Tested too frequently without medication changes or symptom worsening",
            "No documented medical indication in patient record",
            "Duplicate test within short timeframe",
            "Routine monitoring without clear clinical justification"
        ],
        "faqs": [
            {
                "q": "What medications require liver function monitoring?",
                "a": "Many—including statins, acetaminophen, NSAIDs, antibiotics, and anticonvulsants. Your doctor should order baseline and periodic testing if you take these regularly."
            },
            {
                "q": "How often should I have liver function tested?",
                "a": "Baseline testing before starting hepatotoxic medication, then every 6-12 months if on long-term therapy. More frequent testing if dose changes."
            },
            {
                "q": "Why is there such high variation in lab charges?",
                "a": "Hospital labs typically charge more than independent labs. Many tests are bundled differently, leading to wide price variation."
            }
        ],
        "related": ["80053", "80048", "82607"]
    },
    {
        "cpt": "82947",
        "name": "Glucose, Blood",
        "medicare": 4.52,
        "lab_min": 20,
        "lab_max": 75,
        "markup_min": 343,
        "markup_max": 1560,
        "description": "Blood glucose (blood sugar) measures glucose concentration. It's one of the most basic tests, used to screen for and monitor diabetes. A fasting glucose is most accurate; random glucose can also be tested.",
        "coverage": "Yes, Medicare Part B covers blood glucose testing. Screening in asymptomatic patients is often covered as part of routine physicals; monitoring is covered for diabetic patients.",
        "denials": [
            "Ordered too frequently (e.g., daily at lab for non-diabetic patient)",
            "No clear indication for testing",
            "Home glucose monitoring should be used instead for diabetic patients",
            "Screening in very low-risk asymptomatic patient without justification",
            "Duplicate test same day"
        ],
        "faqs": [
            {
                "q": "Should I fast before a glucose test?",
                "a": "If your doctor ordered a fasting glucose, yes—8-12 hours without food. Random glucose doesn't require fasting. Ask your lab which type was ordered."
            },
            {
                "q": "How often should I get glucose tested?",
                "a": "Annual screening is typical. If prediabetic or diabetic, your doctor may order fasting glucose 1-2 times per year, plus HbA1c every 3-6 months."
            },
            {
                "q": "Why is the markup so extreme (up to 1,560%)?",
                "a": "The Medicare rate is very low ($4.52), but lab overhead is fixed. For self-pay patients, labs charge more, leading to huge percentage markups despite low absolute cost."
            }
        ],
        "related": ["83036", "80048", "80053"]
    },
    {
        "cpt": "85027",
        "name": "CBC without Differential",
        "medicare": 6.47,
        "lab_min": 25,
        "lab_max": 100,
        "markup_min": 286,
        "markup_max": 1446,
        "description": "A CBC without differential counts red blood cells, white blood cells (total), and platelets but doesn't break down white cell types. It's a simpler, cheaper version of the CBC with differential. It's used for basic screening and to detect anemia or infection.",
        "coverage": "Yes, Medicare Part B covers CBC without differential when medically necessary.",
        "denials": [
            "Ordered without clinical indication",
            "Screening in completely asymptomatic patient",
            "Duplicate test within short timeframe",
            "More detailed CBC with differential already done",
            "Routine screening without documented medical necessity"
        ],
        "faqs": [
            {
                "q": "Why would my doctor order CBC without differential instead of with?",
                "a": "For basic screening or cost control. The differential costs more but adds detail. For simple anemia or infection screening, basic CBC may suffice."
            },
            {
                "q": "Is the quality of a CBC without differential lower?",
                "a": "No—it's just less detailed. Red cells, white cells, and platelets are still accurately counted. The differential (breakdown of white cell types) is just omitted."
            },
            {
                "q": "What if my CBC is abnormal?",
                "a": "Your doctor may order CBC with differential or additional tests to get more information about what's causing the abnormality."
            }
        ],
        "related": ["85025", "80053", "83036"]
    },
    {
        "cpt": "84153",
        "name": "PSA (Prostate Specific Antigen)",
        "medicare": 18.73,
        "lab_min": 65,
        "lab_max": 240,
        "markup_min": 247,
        "markup_max": 1181,
        "description": "PSA measures a protein produced by the prostate. Elevated PSA can indicate prostate cancer, benign prostate hyperplasia (BPH), or prostatitis. It's commonly used for cancer screening in men over 50, though its utility is debated. Medicare covers it for men with symptoms or diagnosed prostate disease.",
        "coverage": "Yes, Medicare Part B covers PSA for men with prostate symptoms or diagnosed prostate disease. Routine screening may be covered under certain circumstances but is not universally covered.",
        "denials": [
            "Routine screening in asymptomatic men without prostate disease history",
            "Screening without shared decision-making or documented medical necessity",
            "Tested too frequently without clinical change",
            "No diagnosis code indicating prostate disease or symptoms",
            "Age-based screening alone without clear indication"
        ],
        "faqs": [
            {
                "q": "Should I get PSA screening?",
                "a": "That's debated. Organizations differ on recommendations. Talk to your doctor about risks/benefits, especially if you have family history of prostate cancer."
            },
            {
                "q": "Does Medicare always cover PSA tests?",
                "a": "For men with prostate symptoms or diagnosed disease, yes. For asymptomatic men as pure screening, it may not be covered—check your policy."
            },
            {
                "q": "What if my PSA is elevated?",
                "a": "Elevated PSA doesn't always mean cancer. Your doctor may repeat the test, do a digital rectal exam, or refer to a urologist for further evaluation."
            }
        ],
        "related": ["84403", "80076", "80053"]
    },
    {
        "cpt": "82728",
        "name": "Ferritin",
        "medicare": 16.39,
        "lab_min": 55,
        "lab_max": 210,
        "markup_min": 236,
        "markup_max": 1181,
        "description": "Ferritin measures iron storage in your body. High ferritin can indicate iron overload (hemochromatosis) or inflammation; low ferritin suggests iron deficiency anemia. It's ordered when investigating anemia, fatigue, or suspected iron disorders.",
        "coverage": "Yes, Medicare Part B covers ferritin testing when ordered to evaluate anemia, iron overload, or symptoms of iron deficiency.",
        "denials": [
            "Screening in asymptomatic patient without anemia symptoms",
            "Tested too frequently without clinical indication",
            "No diagnosis code documenting reason (anemia, fatigue, iron overload)",
            "Duplicate test within short timeframe",
            "Routine supplementation monitoring without medical necessity"
        ],
        "faqs": [
            {
                "q": "When is ferritin testing necessary?",
                "a": "If you have symptoms of anemia (fatigue, weakness), are diagnosed with anemia, or have a family history of hemochromatosis."
            },
            {
                "q": "Can ferritin be high even if I don't have iron overload?",
                "a": "Yes—ferritin is an inflammatory marker. Infections, liver disease, cancer, and autoimmune conditions can raise ferritin independent of iron status."
            },
            {
                "q": "Is iron supplementation recommended if ferritin is low?",
                "a": "Only if iron deficiency anemia is confirmed. Taking iron supplements without anemia can cause problems. Your doctor will advise."
            }
        ],
        "related": ["85025", "80053", "82607"]
    },
    {
        "cpt": "82607",
        "name": "Vitamin B12 (Cyanocobalamin)",
        "medicare": 14.49,
        "lab_min": 50,
        "lab_max": 195,
        "markup_min": 245,
        "markup_max": 1246,
        "description": "Vitamin B12 is essential for nerve function and red blood cell formation. Low B12 causes pernicious anemia and neurological symptoms. It's ordered for patients with anemia, fatigue, neuropathy, or those on metformin or with GI absorption issues.",
        "coverage": "Yes, Medicare Part B covers B12 testing when ordered to evaluate anemia, neurological symptoms, or diagnosis of pernicious anemia.",
        "denials": [
            "Screening in asymptomatic patient without risk factors",
            "Routine supplementation monitoring without documented deficiency",
            "Tested too frequently without symptom change",
            "No diagnosis code indicating reason for test",
            "Duplicate test within short timeframe"
        ],
        "faqs": [
            {
                "q": "Who should get B12 testing?",
                "a": "Patients with fatigue, neuropathy, anemia, those over 65, those on metformin, and those with GI conditions affecting absorption (Crohn's, celiac)."
            },
            {
                "q": "Can B12 be low even if I eat meat?",
                "a": "Yes. B12 requires intrinsic factor (made in the stomach) to be absorbed. Without it, dietary B12 isn't absorbed—this is pernicious anemia."
            },
            {
                "q": "How often should B12 be tested?",
                "a": "If diagnosed with deficiency, baseline testing; if on supplementation, periodic monitoring per your doctor's schedule (often annual or less)."
            }
        ],
        "related": ["82728", "85025", "80076"]
    },
    {
        "cpt": "84480",
        "name": "T3, Total (Triiodothyronine)",
        "medicare": 11.27,
        "lab_min": 45,
        "lab_max": 165,
        "markup_min": 299,
        "markup_max": 1364,
        "description": "T3 is a thyroid hormone. Total T3 measures both bound and free T3. It's ordered to further evaluate thyroid function when TSH is abnormal or to diagnose thyroid disease. T3 is less commonly ordered than TSH but important in certain cases.",
        "coverage": "Yes, Medicare Part B covers T3 testing when ordered by a physician to evaluate abnormal TSH or suspected thyroid disease.",
        "denials": [
            "Ordered without abnormal TSH or thyroid symptoms",
            "Routine screening in asymptomatic patients",
            "Tested too frequently without medication changes",
            "TSH already normal—T3 testing may not be necessary",
            "No clinical indication documented"
        ],
        "faqs": [
            {
                "q": "What's the difference between T3 and T4?",
                "a": "Both are thyroid hormones. T4 is less active; T3 is more biologically active. Both are measured to fully evaluate thyroid function."
            },
            {
                "q": "When would my doctor order T3?",
                "a": "Usually only if TSH is abnormal or symptoms persist despite normal TSH. T3 helps confirm hyperthyroidism or clarify confusing test results."
            },
            {
                "q": "Is total T3 the same as Free T3?",
                "a": "No. Total T3 includes T3 bound to proteins; Free T3 is the biologically active form. Free T3 is more accurate but costs more."
            }
        ],
        "related": ["84443", "82607", "80076"]
    },
    {
        "cpt": "82550",
        "name": "CK / CPK (Creatine Kinase)",
        "medicare": 8.34,
        "lab_min": 30,
        "lab_max": 110,
        "markup_min": 260,
        "markup_max": 1219,
        "description": "Creatine kinase (CK or CPK) is an enzyme found in muscle and heart. Elevated CK indicates muscle damage, heart attack, myositis, or statin side effects. It's ordered when evaluating chest pain, muscle weakness, or to monitor statin therapy.",
        "coverage": "Yes, Medicare Part B covers CK testing when ordered to evaluate chest pain, muscle symptoms, or to monitor medications that can affect muscles.",
        "denials": [
            "Routine screening in asymptomatic patients",
            "Tested too frequently without medication change or symptom worsening",
            "No diagnosis code documenting reason (chest pain, muscle weakness)",
            "Duplicate test within short timeframe",
            "Routine statin monitoring without documented muscle symptoms"
        ],
        "faqs": [
            {
                "q": "Why would my doctor test CK if I'm on a statin?",
                "a": "Statins can cause muscle pain and damage (myopathy). If you have muscle symptoms, baseline and periodic CK testing helps monitor for statin-related injury."
            },
            {
                "q": "What CK level is concerning?",
                "a": "Normal is roughly 30-200 U/L (varies by lab). Markedly elevated (>1,000) suggests significant muscle damage. Your doctor interprets results in context."
            },
            {
                "q": "Is CK always elevated with a heart attack?",
                "a": "Usually, but troponin is more specific for heart attacks. CK can be elevated by strenuous exercise, muscle injury, or muscle diseases."
            }
        ],
        "related": ["80053", "84403", "84443"]
    },
    {
        "cpt": "86140",
        "name": "C-Reactive Protein (CRP)",
        "medicare": 5.09,
        "lab_min": 25,
        "lab_max": 95,
        "markup_min": 391,
        "markup_max": 1766,
        "description": "CRP is an inflammatory marker. Elevated CRP indicates inflammation from infection, autoimmune disease, or cardiovascular disease. High-sensitivity CRP (hs-CRP) is used to assess cardiovascular risk. It's ordered when evaluating fever, joint pain, or assessing inflammation.",
        "coverage": "Yes, Medicare Part B covers CRP testing when ordered to evaluate inflammation or cardiovascular risk in appropriate clinical contexts.",
        "denials": [
            "Routine cardiovascular screening without symptoms or risk factors",
            "Tested too frequently without clinical indication",
            "No diagnosis code documenting reason (fever, inflammation, cardiovascular assessment)",
            "Duplicate test within short timeframe",
            "Pure screening without medical justification"
        ],
        "faqs": [
            {
                "q": "What does elevated CRP mean?",
                "a": "Inflammation from some cause—infection, autoimmune disease, heart disease, or even stress/poor sleep. It's non-specific; your doctor must interpret with other findings."
            },
            {
                "q": "Is CRP useful for cardiovascular risk?",
                "a": "High-sensitivity CRP (hs-CRP) can help assess CV risk, but it's not a screening test for everyone. Your doctor uses it in context of other risk factors."
            },
            {
                "q": "Can CRP be normal even if I'm sick?",
                "a": "Yes. Early infections or certain conditions may not elevate CRP significantly. Your doctor interprets all results together."
            }
        ],
        "related": ["80076", "80053", "82947"]
    },
    {
        "cpt": "83735",
        "name": "Magnesium",
        "medicare": 6.31,
        "lab_min": 25,
        "lab_max": 85,
        "markup_min": 296,
        "markup_max": 1247,
        "description": "Magnesium is a mineral essential for muscle and nerve function. Low magnesium causes muscle cramps, weakness, and irregular heart rhythm. High levels are rare but can occur with kidney disease. It's tested to evaluate muscle symptoms or electrolyte imbalance.",
        "coverage": "Yes, Medicare Part B covers magnesium testing when ordered to evaluate electrolyte imbalance, muscle symptoms, or kidney disease.",
        "denials": [
            "Routine screening in asymptomatic patients",
            "Tested too frequently without symptom change",
            "No diagnosis code documenting clinical reason",
            "Supplement monitoring without medical necessity",
            "Duplicate test within short timeframe"
        ],
        "faqs": [
            {
                "q": "What are symptoms of low magnesium?",
                "a": "Muscle cramps, weakness, fatigue, irregular heart rhythm, and personality changes. But many causes of these symptoms exist—magnesium testing clarifies."
            },
            {
                "q": "Should I take magnesium supplements?",
                "a": "Only if magnesium deficiency is confirmed by blood test. Excess supplementation can cause diarrhea and interact with medications."
            },
            {
                "q": "Is magnesium testing usually covered by Medicare?",
                "a": "Yes, if ordered for a specific reason (muscle symptoms, electrolyte imbalance, kidney disease). Routine screening is less likely to be covered."
            }
        ],
        "related": ["80048", "80053", "84443"]
    },
    {
        "cpt": "82746",
        "name": "Folate (Folic Acid)",
        "medicare": 14.49,
        "lab_min": 45,
        "lab_max": 170,
        "markup_min": 211,
        "markup_max": 1073,
        "description": "Folate (folic acid) is a B vitamin essential for red blood cell production and DNA synthesis. Low folate causes anemia and neurological problems. It's ordered to evaluate anemia, neuropathy, or in patients with poor diet or GI absorption issues.",
        "coverage": "Yes, Medicare Part B covers folate testing when ordered to evaluate anemia, neurological symptoms, or confirmed folate deficiency.",
        "denials": [
            "Routine screening in asymptomatic patients without risk factors",
            "Supplement monitoring without documented deficiency",
            "Tested too frequently without symptom change",
            "No diagnosis code indicating reason for test",
            "Duplicate test within short timeframe"
        ],
        "faqs": [
            {
                "q": "Who is at risk for folate deficiency?",
                "a": "People with poor diet (inadequate vegetables/grains), alcoholism, GI diseases (Crohn's, celiac), and those on certain medications (methotrexate, sulfasalazine)."
            },
            {
                "q": "Should I take folic acid supplements?",
                "a": "Only if deficiency is documented or you're planning pregnancy (folic acid prevents neural tube defects). Otherwise, a normal diet usually provides enough."
            },
            {
                "q": "Is folate testing always covered?",
                "a": "When medically necessary (anemia workup, documented deficiency, high-risk patient). Routine screening is less likely to be covered."
            }
        ],
        "related": ["82607", "85025", "80053"]
    }
]

# ============================================================================
# CSS (inline for all pages)
# ============================================================================

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #212529; background: #f8f9fa; -webkit-font-smoothing: antialiased; line-height: 1.6; }
.site-header { background: #1B3A5C; color: #fff; padding: 20px 24px; text-align: center; position: sticky; top: 0; z-index: 100; }
.back-link { position: absolute; left: 20px; top: 50%; transform: translateY(-50%); color: rgba(255,255,255,0.8); text-decoration: none; font-size: 14px; }
.back-link:hover { color: #fff; }
.logo { font-size: 32px; font-weight: 800; letter-spacing: -0.5px; }
.logo a { text-decoration: none; }
.logo-gouge { color: #fff; }
.logo-stop { color: #FF6B6B; }
.header-tagline { font-size: 14px; opacity: 0.85; margin-top: 2px; }
.site-nav { background: #152e4a; display: flex; justify-content: center; gap: 32px; padding: 10px 20px; flex-wrap: wrap; }
.site-nav a { color: rgba(255,255,255,0.85); text-decoration: none; font-size: 15px; font-weight: 500; transition: color 0.2s; }
.site-nav a:hover { color: #FF6B6B; }
.site-nav .nav-cta { color: #FF6B6B; }
.content { max-width: 680px; margin: 0 auto; padding: 0 20px 40px; }
.content.wide { max-width: 900px; }
.hero { text-align: center; padding: 48px 0 32px; }
.hero h1 { font-size: 28px; color: #1B3A5C; line-height: 1.3; margin-bottom: 16px; font-weight: 800; }
.hero .subtitle { font-size: 16px; color: #6c757d; font-style: italic; }
.story { background: #fff; border-radius: 14px; padding: 32px 28px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin: 24px 0; }
.story p { font-size: 17px; color: #495057; line-height: 1.8; margin-bottom: 20px; }
.story p:last-child { margin-bottom: 0; }
.pull-quote { background: linear-gradient(135deg, #1B3A5C, #2C5F8A); color: #fff; border-radius: 14px; padding: 32px 28px; margin: 32px 0; text-align: center; }
.pull-quote p { font-size: 20px; font-weight: 600; line-height: 1.5; margin: 0; }
.data-note { background: #e7f3ff; border-left: 4px solid #1B3A5C; border-radius: 8px; padding: 20px; margin: 24px 0; font-size: 14px; color: #495057; line-height: 1.7; }
.data-note strong { color: #1B3A5C; }
.cta-section { text-align: center; padding: 32px 0 24px; }
.cta-section h2 { font-size: 24px; color: #1B3A5C; margin-bottom: 20px; }
.cta-button { display: inline-block; background: #FF6B6B; color: #fff; font-size: 20px; font-weight: 700; padding: 18px 48px; border-radius: 14px; text-decoration: none; transition: background 0.2s, transform 0.1s; box-shadow: 0 4px 12px rgba(255, 107, 107, 0.35); }
.cta-button:hover { background: #e55a5a; transform: translateY(-1px); }
.cta-sub { font-size: 14px; color: #6c757d; margin-top: 12px; }
.site-footer { background: #1B3A5C; color: rgba(255,255,255,0.7); text-align: center; padding: 24px 20px; font-size: 13px; }
.site-footer a { color: rgba(255,255,255,0.9); text-decoration: none; }
.search-box { background: #fff; border-radius: 14px; padding: 24px; margin: 24px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.search-box input { width: 100%; padding: 12px 16px; font-size: 16px; border: 2px solid #ddd; border-radius: 8px; font-family: inherit; }
.search-box input:focus { outline: none; border-color: #1B3A5C; }
.test-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 24px 0; }
.test-card { background: #fff; border-radius: 14px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); transition: box-shadow 0.2s, transform 0.2s; text-decoration: none; color: inherit; }
.test-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.12); transform: translateY(-2px); }
.test-card h3 { font-size: 18px; font-weight: 700; color: #1B3A5C; margin-bottom: 12px; }
.test-card .cpt-code { font-size: 13px; color: #6c757d; font-weight: 500; margin-bottom: 12px; }
.test-card .rate-line { font-size: 15px; margin-bottom: 8px; }
.test-card .rate-line strong { color: #1B3A5C; }
.test-card .lab-line { font-size: 15px; margin-bottom: 8px; }
.test-card .markup-line { font-size: 14px; color: #6c757d; margin-bottom: 12px; }
.test-card .learn-more { display: inline-block; margin-top: 8px; color: #FF6B6B; font-weight: 600; font-size: 14px; }
.breadcrumb { font-size: 13px; color: #6c757d; margin-bottom: 24px; padding-top: 12px; }
.breadcrumb a { color: #1B3A5C; text-decoration: none; }
.breadcrumb a:hover { text-decoration: underline; }
.data-table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 14px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin: 24px 0; }
.data-table td { padding: 16px; border-bottom: 1px solid #e9ecef; }
.data-table td:first-child { font-weight: 600; color: #1B3A5C; width: 50%; }
.data-table td:last-child { text-align: right; color: #FF6B6B; font-weight: 600; }
.data-table tr:last-child td { border-bottom: none; }
.section { margin: 32px 0; }
.section h2 { font-size: 22px; color: #1B3A5C; margin-bottom: 16px; font-weight: 700; }
.section h3 { font-size: 18px; color: #1B3A5C; margin: 20px 0 12px; font-weight: 600; }
.section p { font-size: 16px; color: #495057; line-height: 1.8; margin-bottom: 12px; }
.section ul { margin: 16px 0 16px 24px; }
.section li { font-size: 16px; color: #495057; line-height: 1.8; margin-bottom: 8px; }
.faq-item { background: #fff; border-radius: 14px; padding: 24px; margin: 16px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.faq-item strong { color: #1B3A5C; font-size: 16px; display: block; margin-bottom: 8px; }
.faq-item p { color: #495057; font-size: 15px; line-height: 1.8; }
.related-tests { background: #f0f4f8; border-radius: 14px; padding: 24px; margin: 24px 0; }
.related-tests h3 { font-size: 18px; color: #1B3A5C; margin-bottom: 16px; font-weight: 700; }
.related-tests ul { margin: 0; padding: 0; list-style: none; }
.related-tests li { margin-bottom: 12px; }
.related-tests a { color: #1B3A5C; text-decoration: none; font-weight: 500; }
.related-tests a:hover { text-decoration: underline; }
@media (max-width: 768px) { .test-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 480px) { .hero h1 { font-size: 24px; } .story { padding: 24px 20px; } .story p { font-size: 16px; } .pull-quote p { font-size: 18px; } .cta-button { font-size: 18px; padding: 16px 36px; } .test-grid { grid-template-columns: 1fr; } .site-nav { gap: 16px; } }
"""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def escape_html(text):
    """Escape HTML special characters."""
    return (text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;"))

def format_money(value):
    """Format value as currency."""
    return f"${value:.2f}"

def generate_landing_page(tests):
    """Generate the Medicare Coverage Lookup landing page."""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medicare Coverage Lookup - GougeStop</title>
    <meta name="description" content="Search Medicare rates and lab charges for 20 common lab tests. See what Medicare pays vs. what labs actually charge.">
    <meta property="og:title" content="Medicare Coverage Lookup - GougeStop">
    <meta property="og:description" content="Search Medicare rates and lab charges for 20 common lab tests. See what Medicare pays vs. what labs actually charge.">
    <meta property="og:url" content="https://www.gougestop.com/coverage/">
    <meta property="og:type" content="website">
    <style>
{CSS}
    </style>
</head>
<body>
    <header class="site-header">
        <a href="/" class="back-link">← Home</a>
        <div class="logo"><a href="/"><span class="logo-gouge">Gouge</span><span class="logo-stop">Stop</span></a></div>
        <p class="header-tagline">Know what Medicare pays. Stop overpaying.</p>
    </header>

    <nav class="site-nav">
        <a href="/blog">Blog</a>
        <a href="/our-story">Our Story</a>
        <a href="/coverage">Coverage Lookup</a>
        <a href="/install">Install on Phone</a>
        <a href="/app" class="nav-cta">Open GougeStop</a>
    </nav>

    <div class="content wide">
        <div class="hero">
            <h1>Medicare Coverage Lookup</h1>
            <p class="subtitle">See what Medicare pays for common lab tests — and what labs actually charge.</p>
        </div>

        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Search by test name or CPT code (e.g., &quot;CMP&quot; or &quot;80053&quot;)...">
        </div>

        <div class="data-note">
            <strong>Data Note:</strong> Medicare rates shown are from the 2023 CMS Clinical Lab Fee Schedule (CLFS). Lab charge ranges reflect 2023 national pricing data. As we build out our database from GougeStop usage (no patient information is collected), we'll enhance this tool with real-world pricing data.
        </div>

        <div class="test-grid" id="testGrid">
"""

    for test in tests:
        html += f"""            <a href="/coverage/cpt-{test['cpt']}.html" class="test-card">
                <h3>{escape_html(test['name'])}</h3>
                <div class="cpt-code">CPT {test['cpt']}</div>
                <div class="rate-line"><strong>Medicare:</strong> {format_money(test['medicare'])}</div>
                <div class="lab-line"><strong>Lab charge range:</strong> {format_money(test['lab_min'])}–{format_money(test['lab_max'])}</div>
                <div class="markup-line">Markup: {test['markup_min']}%–{test['markup_max']}%</div>
                <div class="learn-more">Learn More →</div>
            </a>
"""

    html += """        </div>

        <div class="cta-section">
            <h2>Have a Lab Bill? Compare It Now</h2>
            <a href="/app" class="cta-button">Open GougeStop</a>
        </div>
    </div>

    <footer class="site-footer">
        <p><a href="/">Home</a> | <a href="/blog">Blog</a> | <a href="/our-story">Our Story</a> | <a href="/coverage">Coverage Lookup</a> | <a href="/install">Install on Phone</a> | <a href="/app">Open GougeStop</a></p>
        <p>© 2026 GougeStop. All rights reserved. For informational purposes only. Not medical or financial advice.</p>
    </footer>

    <script>
        const searchInput = document.getElementById('searchInput');
        const testGrid = document.getElementById('testGrid');
        const cards = testGrid.querySelectorAll('.test-card');

        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase().trim();

            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (query === '' || text.includes(query)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    </script>
</body>
</html>
"""
    return html

def find_related_tests(cpt, all_tests, count=3):
    """Find related tests for a given CPT code."""
    # Simple categorization based on test type
    categories = {
        "metabolic": ["80053", "80048", "80076", "82947"],
        "blood": ["85025", "85027", "82728", "82607"],
        "hormone": ["84443", "84403", "84480"],
        "vitamin": ["82306", "82607", "82746", "83735"]
    }

    # Categorize current test
    category = None
    for cat, codes in categories.items():
        if cpt in codes:
            category = cat
            break

    # Find related tests in same category (up to 3)
    related = []
    if category:
        for code in categories[category]:
            if code != cpt:
                related.append(code)
                if len(related) >= count:
                    break

    return related[:count]

def generate_cpt_page(test, all_tests):
    """Generate an individual CPT code page."""

    related_codes = find_related_tests(test['cpt'], all_tests)
    related_tests_html = ""
    if related_codes:
        related_tests_html = """        <div class="related-tests">
            <h3>Related Tests</h3>
            <ul>
"""
        for code in related_codes:
            for t in all_tests:
                if t['cpt'] == code:
                    related_tests_html += f"""                <li><a href="/coverage/cpt-{code}.html">{escape_html(t['name'])} (CPT {code})</a></li>
"""
        related_tests_html += """            </ul>
        </div>
"""

    # Build FAQ HTML
    faq_schema = []
    faq_html = ""
    for faq in test['faqs']:
        faq_html += f"""        <div class="faq-item">
            <strong>Q: {escape_html(faq['q'])}</strong>
            <p>A: {escape_html(faq['a'])}</p>
        </div>
"""
        faq_schema.append({
            "type": "Question",
            "name": faq['q'],
            "acceptedAnswer": {
                "type": "Answer",
                "text": faq['a']
            }
        })

    # Build breadcrumb
    breadcrumb = f"""<div class="breadcrumb">
        <a href="/">Home</a> > <a href="/coverage/">Coverage Lookup</a> > {escape_html(test['name'])}
    </div>"""

    # Calculate percentage
    markup_low = test['markup_min']
    markup_high = test['markup_max']

    # Schema markup
    schema_markup = f"""    <script type="application/ld+json">
{{
    "@context": "https://schema.org/",
    "@type": "MedicalWebPage",
    "name": "{escape_html(test['name'])} (CPT {test['cpt']}) — Medicare Rate vs. Lab Charges",
    "url": "https://www.gougestop.com/coverage/cpt-{test['cpt']}.html",
    "description": "Medicare pays {format_money(test['medicare'])} for this test. Labs commonly charge {format_money(test['lab_min'])}–{format_money(test['lab_max'])}. See what you should know about coverage and pricing."
}}
    </script>
    <script type="application/ld+json">
{{
    "@context": "https://schema.org/",
    "@type": "FAQPage",
    "mainEntity": [
"""

    for i, item in enumerate(faq_schema):
        schema_markup += f"""        {{
            "@type": "Question",
            "name": "{escape_html(item['name'])}",
            "acceptedAnswer": {{
                "@type": "Answer",
                "text": "{escape_html(item['acceptedAnswer']['text'])}"
            }}
        }}{'' if i == len(faq_schema) - 1 else ','}
"""

    schema_markup += f"""    ]
}}
    </script>
    <script type="application/ld+json">
{{
    "@context": "https://schema.org/",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://www.gougestop.com"
        }},
        {{
            "@type": "ListItem",
            "position": 2,
            "name": "Coverage Lookup",
            "item": "https://www.gougestop.com/coverage/"
        }},
        {{
            "@type": "ListItem",
            "position": 3,
            "name": "{escape_html(test['name'])}",
            "item": "https://www.gougestop.com/coverage/cpt-{test['cpt']}.html"
        }}
    ]
}}
    </script>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(test['name'])} (CPT {test['cpt']}) — Medicare Rate vs. Lab Charges</title>
    <meta name="description" content="Medicare pays {format_money(test['medicare'])} for {escape_html(test['name'])} (CPT {test['cpt']}). Labs commonly charge {format_money(test['lab_min'])}–{format_money(test['lab_max'])}. Learn about coverage and what to do if overcharged.">
    <meta property="og:title" content="{escape_html(test['name'])} (CPT {test['cpt']}) — Medicare Rate vs. Lab Charges">
    <meta property="og:description" content="Medicare pays {format_money(test['medicare'])} for {escape_html(test['name'])}. Labs commonly charge {format_money(test['lab_min'])}–{format_money(test['lab_max'])}. See pricing breakdown and coverage info.">
    <meta property="og:url" content="https://www.gougestop.com/coverage/cpt-{test['cpt']}.html">
    <meta property="og:type" content="article">
    <style>
{CSS}
    </style>
{schema_markup}</head>
<body>
    <header class="site-header">
        <a href="/" class="back-link">← Home</a>
        <div class="logo"><a href="/"><span class="logo-gouge">Gouge</span><span class="logo-stop">Stop</span></a></div>
        <p class="header-tagline">Know what Medicare pays. Stop overpaying.</p>
    </header>

    <nav class="site-nav">
        <a href="/blog">Blog</a>
        <a href="/our-story">Our Story</a>
        <a href="/coverage">Coverage Lookup</a>
        <a href="/install">Install on Phone</a>
        <a href="/app" class="nav-cta">Open GougeStop</a>
    </nav>

    <div class="content">
        {breadcrumb}

        <div class="hero">
            <h1>{escape_html(test['name'])} (CPT {test['cpt']})</h1>
            <p class="subtitle">Medicare Rate vs. Lab Charges</p>
        </div>

        <div class="pull-quote">
            <p>Medicare pays {format_money(test['medicare'])} for this test. Labs commonly charge {format_money(test['lab_min'])}–{format_money(test['lab_max'])}. That's a {markup_low}%–{markup_high}% markup above what Medicare pays.</p>
        </div>

        <div class="section">
            <h2>What This Test Is</h2>
            <p>{escape_html(test['description'])}</p>
        </div>

        <div class="section">
            <h2>Medicare Rate vs. Lab Charges</h2>
            <table class="data-table">
                <tr>
                    <td>Medicare Allowable Rate</td>
                    <td>{format_money(test['medicare'])}</td>
                </tr>
                <tr>
                    <td>Typical Lab Charge Range</td>
                    <td>{format_money(test['lab_min'])}–{format_money(test['lab_max'])}</td>
                </tr>
                <tr>
                    <td>Average Markup Above Medicare</td>
                    <td>{markup_low}%–{markup_high}%</td>
                </tr>
            </table>
        </div>

        <div class="section">
            <h2>Does Medicare Cover This Test?</h2>
            <p>{escape_html(test['coverage'])}</p>
        </div>

        <div class="section">
            <h2>Common Reasons for Denial</h2>
            <ul>
"""

    for reason in test['denials']:
        html += f"""                <li>{escape_html(reason)}</li>
"""

    html += f"""            </ul>
        </div>

        <div class="section">
            <h2>What To Do If You're Overcharged</h2>
            <p>If you received a lab bill that seems unusually high compared to Medicare rates:</p>
            <ul>
                <li><strong>Check your Explanation of Benefits (EOB)</strong> from Medicare or your insurance to see what should have been paid.</li>
                <li><strong>Request an itemized bill</strong> from the lab showing all charges.</li>
                <li><strong>Compare to GougeStop rates</strong> for your area to see if the charge is reasonable.</li>
                <li><strong>Contact the lab's billing department</strong> to dispute erroneous charges or negotiate a lower rate.</li>
                <li><strong>File an appeal</strong> with Medicare if a claim was incorrectly denied.</li>
            </ul>
            <div class="cta-section" style="margin-top: 20px;">
                <a href="/app" class="cta-button">Compare Your Lab Bill Now</a>
            </div>
        </div>

        <div class="section">
            <h2>Frequently Asked Questions</h2>
{faq_html}        </div>

        {related_tests_html}

        <div class="cta-section">
            <h2>Have a Lab Bill? Compare It Now</h2>
            <a href="/app" class="cta-button">Open GougeStop</a>
        </div>
    </div>

    <footer class="site-footer">
        <p><a href="/">Home</a> | <a href="/blog">Blog</a> | <a href="/our-story">Our Story</a> | <a href="/coverage">Coverage Lookup</a> | <a href="/install">Install on Phone</a> | <a href="/app">Open GougeStop</a></p>
        <p>© 2026 GougeStop. All rights reserved. For informational purposes only. Not medical or financial advice.</p>
    </footer>
</body>
</html>
"""
    return html

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Generate all coverage pages."""
    output_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate landing page
    landing_html = generate_landing_page(TESTS)
    landing_path = os.path.join(output_dir, "index.html")
    with open(landing_path, 'w', encoding='utf-8') as f:
        f.write(landing_html)
    print(f"✓ Generated {landing_path}")

    # Generate individual CPT pages
    for test in TESTS:
        cpt_html = generate_cpt_page(test, TESTS)
        cpt_path = os.path.join(output_dir, f"cpt-{test['cpt']}.html")
        with open(cpt_path, 'w', encoding='utf-8') as f:
            f.write(cpt_html)
        print(f"✓ Generated {cpt_path}")

    print(f"\n✓ All files generated successfully!")
    print(f"  Location: {output_dir}")
    print(f"  Total files: 21 (1 landing + 20 CPT pages)")

if __name__ == "__main__":
    main()
