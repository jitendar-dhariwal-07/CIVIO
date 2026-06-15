-- ============================================================================
-- CitizenAI - Seed Data
-- Realistic data for Indian government schemes, departments, and sample records
-- ============================================================================

-- ============================================================================
-- CENTRAL GOVERNMENT SCHEMES (20+)
-- ============================================================================

INSERT INTO schemes (scheme_id, name, full_name, description, short_description, ministry, department, type, benefit_type, benefit_amount, benefit_description, eligibility_summary, application_process, application_url, helpline, launch_date, is_active, tags, priority_score, total_beneficiaries, budget_allocation) VALUES

('pm_kisan', 'PM-KISAN', 'Pradhan Mantri Kisan Samman Nidhi',
 'Under this scheme, all landholding farmer families shall get income support of Rs. 6,000 per year in three equal installments of Rs. 2,000 each, every four months. The fund is directly transferred to the bank accounts of the beneficiaries.',
 'Direct income support of ₹6,000/year for farmer families',
 'Ministry of Agriculture & Farmers Welfare', 'Department of Agriculture & Farmers Welfare', 'central', 'dbt',
 '₹6,000 per year (3 installments of ₹2,000)', 'Direct benefit transfer of ₹2,000 every 4 months to farmer bank accounts.',
 'All landholding farmer families with cultivable land. Excludes institutional landholders, former/present holders of constitutional posts, serving/retired government employees with pension above ₹10,000/month.',
 '1. Visit pmkisan.gov.in or nearest CSC 2. Register with Aadhaar, land records 3. Verify bank details 4. Submit and track application',
 'https://pmkisan.gov.in', '155261', '2019-02-01', TRUE,
 ARRAY['agriculture', 'farmer', 'dbt', 'income_support'], 95, 110000000, '₹75,000 Crore'),

('pm_awas_gramin', 'PMAY-G', 'Pradhan Mantri Awaas Yojana - Gramin',
 'Housing for All by 2022 mission providing financial assistance for construction of pucca houses with basic amenities to eligible rural households. Beneficiaries receive ₹1.20 lakh in plain areas and ₹1.30 lakh in hilly/difficult areas.',
 'Financial assistance for rural housing construction',
 'Ministry of Rural Development', 'Department of Rural Development', 'central', 'dbt',
 '₹1,20,000 (plains) / ₹1,30,000 (hilly areas)', 'Financial assistance for pucca house construction with toilet, LPG connection, electricity, and drinking water.',
 'Houseless or living in kutcha/dilapidated houses as per SECC 2011 data. Priority to SC/ST, freed bonded labourers, minorities, BPL families.',
 '1. Identified from SECC 2011 data 2. Gram Sabha validates list 3. Sanctioned by District/Block 4. Amount disbursed in installments',
 'https://pmayg.nic.in', '1800-11-6446', '2016-11-20', TRUE,
 ARRAY['housing', 'rural', 'construction', 'bpl'], 90, 29500000, '₹48,000 Crore'),

('pm_awas_urban', 'PMAY-U', 'Pradhan Mantri Awaas Yojana - Urban',
 'Credit-linked subsidy and financial assistance for urban housing. Provides interest subsidy on housing loans ranging from 3% to 6.5% for EWS, LIG, and MIG categories for construction or purchase of houses.',
 'Interest subsidy on home loans for urban housing',
 'Ministry of Housing & Urban Affairs', NULL, 'central', 'subsidy',
 '₹2.67 lakh subsidy (EWS/LIG)', 'Interest subsidy of 6.5% for EWS/LIG, 4% for MIG-I, 3% for MIG-II on housing loans.',
 'Annual household income up to ₹18 lakh for MIG-II, ₹12 lakh for MIG-I, ₹6 lakh for LIG, ₹3 lakh for EWS. Family should not own a pucca house.',
 '1. Apply online at pmaymis.gov.in 2. Apply through bank/housing finance company 3. Apply at nearest CSC center',
 'https://pmaymis.gov.in', '1800-11-3377', '2015-06-25', TRUE,
 ARRAY['housing', 'urban', 'subsidy', 'home_loan'], 88, 12000000, '₹79,000 Crore'),

('ayushman_bharat', 'AB-PMJAY', 'Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana',
 'World''s largest health assurance scheme providing free health coverage of ₹5 lakh per family per year for secondary and tertiary care hospitalization. Covers over 1,900 procedures including surgeries, medical and day care treatments.',
 'Free health insurance cover of ₹5 lakh per family per year',
 'Ministry of Health & Family Welfare', 'National Health Authority', 'central', 'insurance',
 '₹5,00,000 per family per year', 'Cashless and paperless hospitalization at any empanelled hospital across India for over 1,900 procedures.',
 'Deprived rural families and identified occupational categories of urban workers as per SECC 2011 data. Also covers families listed under RSBY.',
 '1. Check eligibility on mera.pmjay.gov.in 2. Visit empanelled hospital with Aadhaar/ration card 3. Get e-card generated 4. Avail cashless treatment',
 'https://pmjay.gov.in', '14555', '2018-09-23', TRUE,
 ARRAY['health', 'insurance', 'hospital', 'cashless'], 95, 550000000, '₹7,200 Crore'),

('atal_pension', 'APY', 'Atal Pension Yojana',
 'A pension scheme for unorganized sector workers guaranteeing minimum pension of ₹1,000 to ₹5,000 per month after attaining 60 years of age, depending on contributions. Government co-contributes 50% of total contribution for eligible subscribers.',
 'Guaranteed pension of ₹1,000-₹5,000/month for unorganized workers',
 'Ministry of Finance', 'Department of Financial Services', 'central', 'pension',
 '₹1,000 to ₹5,000 per month (post 60 years)', 'Monthly pension starting from ₹1,000 to ₹5,000 based on contribution amount and age of joining.',
 'Indian citizen aged 18-40 years, having a savings bank account, not a member of any statutory social security scheme, not an income tax payer.',
 '1. Visit nearest bank branch or apply via net banking 2. Fill APY registration form 3. Provide Aadhaar & mobile number 4. Set auto-debit',
 'https://npscra.nsdl.co.in/scheme-details.php', '1800-110-069', '2015-06-09', TRUE,
 ARRAY['pension', 'unorganized_sector', 'savings', 'retirement'], 80, 56000000, '₹1,000 Crore'),

('pm_ujjwala', 'PMUY', 'Pradhan Mantri Ujjwala Yojana',
 'Provides free LPG connections to women of BPL households. Under PMUY 2.0, a deposit-free LPG connection with first refill and stove supplied free of cost. Aims to replace unclean cooking fuels with clean LPG.',
 'Free LPG gas connection and first refill for BPL women',
 'Ministry of Petroleum & Natural Gas', NULL, 'central', 'in_kind',
 'Free LPG connection + first refill + stove', 'Deposit-free LPG connection, free first refill (14.2 kg), and free hot plate/stove.',
 'Adult woman of a poor household not having LPG in her name or in the name of any family member. Must have SECC-2011 data or belong to 7 identified categories.',
 '1. Visit nearest LPG distributor 2. Submit application with Aadhaar and BPL card 3. Connection released at doorstep',
 'https://www.pmuy.gov.in', '1906', '2016-05-01', TRUE,
 ARRAY['lpg', 'cooking', 'women', 'bpl', 'clean_energy'], 85, 103000000, '₹12,800 Crore'),

('sukanya_samriddhi', 'SSY', 'Sukanya Samriddhi Yojana',
 'A small savings scheme for girl child education and marriage expenses. Offers one of the highest interest rates among government savings schemes (currently 8.2% p.a.) with tax benefits under Section 80C. Account can be opened for a girl child below 10 years.',
 'High-interest savings scheme for girl child future',
 'Ministry of Finance', 'Department of Economic Affairs', 'central', 'tax_benefit',
 '8.2% p.a. interest + tax benefits', 'Tax-free interest at 8.2% per annum, minimum deposit ₹250/year, maximum ₹1.5 lakh/year.',
 'Any parent/guardian of a girl child below 10 years of age. Maximum 2 accounts for 2 girl children (exception for twins/triplets).',
 '1. Visit any post office or authorized bank 2. Fill account opening form 3. Birth certificate of girl child 4. Minimum deposit of ₹250',
 'https://www.indiapost.gov.in', '1800-266-6868', '2015-01-22', TRUE,
 ARRAY['girl_child', 'savings', 'education', 'marriage', 'tax_benefit'], 82, 32000000, NULL),

('pm_mudra', 'PMMY', 'Pradhan Mantri Mudra Yojana',
 'Provides collateral-free loans up to ₹10 lakh to micro/small enterprises. Three categories: Shishu (up to ₹50,000), Kishore (₹50,000-₹5 lakh), and Tarun (₹5 lakh-₹10 lakh). No processing fee charged.',
 'Collateral-free business loans up to ₹10 lakh',
 'Ministry of Finance', 'Department of Financial Services', 'central', 'loan',
 'Up to ₹10,00,000 (Shishu/Kishore/Tarun)', 'Shishu: up to ₹50,000, Kishore: ₹50,001 to ₹5,00,000, Tarun: ₹5,00,001 to ₹10,00,000.',
 'Any Indian citizen with a business plan for non-farm income generating activity. Includes manufacturing, trading, service sector, and allied agricultural activities.',
 '1. Prepare business plan 2. Visit any bank/NBFC/MFI 3. Fill MUDRA loan application 4. Submit documents and business plan',
 'https://www.mudra.org.in', '1800-11-0001', '2015-04-08', TRUE,
 ARRAY['business', 'loan', 'entrepreneur', 'msme', 'self_employment'], 87, 430000000, '₹3,30,000 Crore'),

('standup_india', 'SUI', 'Stand Up India',
 'Facilitates bank loans between ₹10 lakh and ₹1 crore to at least one SC/ST and one woman borrower per bank branch for setting up a greenfield enterprise in manufacturing, services, trading, or agri-allied activities.',
 'Bank loans ₹10L-₹1Cr for SC/ST and women entrepreneurs',
 'Ministry of Finance', 'Department of Financial Services', 'central', 'loan',
 '₹10 lakh to ₹1 crore', 'Composite loan covering term loan and working capital. Repayable in 7 years with 18-month moratorium.',
 'SC/ST and/or woman entrepreneur aged 18+, for greenfield enterprise. Borrower should not be in default to any bank.',
 '1. Apply on standupmitra.in portal 2. Contact nearest bank branch 3. Submit project report 4. Bank processing and sanction',
 'https://www.standupmitra.in', '1800-180-1111', '2016-04-05', TRUE,
 ARRAY['sc_st', 'women', 'entrepreneur', 'business_loan', 'greenfield'], 78, 1800000, NULL),

('pm_svamitva', 'SVAMITVA', 'Survey of Villages Abadi and Mapping with Improvised Technology in Village Areas',
 'Provides property cards (Record of Rights) to rural household owners using drone survey technology. Helps in monetization of rural residential assets for taking loans, reducing property disputes, and enabling better village-level planning.',
 'Property cards for rural households via drone surveys',
 'Ministry of Panchayati Raj', NULL, 'central', 'free_service',
 'Free Property Card (Record of Rights)', 'Drone-based mapping and free distribution of property cards with legal validity.',
 'Owners of residential properties in rural areas (Abadi areas). Villages are covered in phased manner based on state participation.',
 '1. Village selected for drone survey 2. Survey conducted 3. Data processed and verified 4. Property cards distributed through Gram Panchayat',
 'https://svamitva.nic.in', '1800-11-5665', '2020-04-24', TRUE,
 ARRAY['property', 'rural', 'land_rights', 'drone_survey'], 70, 15000000, '₹566 Crore'),

('pm_fasal_bima', 'PMFBY', 'Pradhan Mantri Fasal Bima Yojana',
 'Comprehensive crop insurance scheme providing financial support to farmers suffering crop loss/damage from natural calamities, pests, and diseases. Premium rate: 2% for Kharif, 1.5% for Rabi, and 5% for commercial/horticulture crops.',
 'Affordable crop insurance for all farmers',
 'Ministry of Agriculture & Farmers Welfare', 'Department of Agriculture & Farmers Welfare', 'central', 'insurance',
 'Full sum insured minus farmer premium', 'Low premium rates: 2% Kharif, 1.5% Rabi, 5% commercial. Remaining premium paid by government.',
 'All farmers including sharecroppers and tenant farmers growing notified crops. Voluntary for loanee and non-loanee farmers.',
 '1. Visit bank/CSC/insurance company 2. Apply with land records and sowing certificate 3. Pay nominal premium 4. Claim processed on crop loss assessment',
 'https://pmfby.gov.in', '1800-200-7710', '2016-02-18', TRUE,
 ARRAY['crop_insurance', 'agriculture', 'farmer', 'natural_disaster'], 84, 57000000, '₹15,500 Crore'),

('deen_dayal_upadhyaya', 'DDUGJY', 'Deen Dayal Upadhyaya Gram Jyoti Yojana',
 'Aims to provide 24x7 power supply to all rural households. Covers separation of agricultural and domestic feeders, strengthening of sub-transmission and distribution infrastructure, and rural electrification.',
 '24x7 rural electrification and power supply',
 'Ministry of Power', NULL, 'central', 'free_service',
 'Free electricity connection + infrastructure', 'Free electricity connections to BPL households and strengthening of rural power infrastructure.',
 'All rural areas not yet electrified or having inadequate power supply. Priority to villages with tribal populations, Naxal-affected areas, and border areas.',
 '1. Identified by state DISCOM 2. Infrastructure work undertaken 3. Free connection provided 4. Regular supply ensured',
 'https://www.ddugjy.gov.in', '1800-11-5765', '2015-07-25', TRUE,
 ARRAY['electricity', 'rural', 'power_supply', 'infrastructure'], 75, 28000000, '₹43,033 Crore'),

('pm_jan_dhan', 'PMJDY', 'Pradhan Mantri Jan Dhan Yojana',
 'Financial inclusion program providing universal access to banking facilities with zero balance BSBD accounts, RuPay debit card, and insurance cover. Overdraft facility up to ₹10,000 available to eligible account holders.',
 'Zero-balance bank account with RuPay card and insurance',
 'Ministry of Finance', 'Department of Financial Services', 'central', 'free_service',
 'Zero-balance account + ₹2L accident insurance + ₹30K life cover',
 'Free BSBD bank account, free RuPay card, ₹2 lakh accidental insurance, ₹30,000 life insurance, overdraft up to ₹10,000.',
 'Any Indian citizen aged 10+ who does not have a bank account. Minor aged 10+ can open account with guardian.',
 '1. Visit any bank branch 2. Fill account opening form 3. Aadhaar/Voter ID as KYC 4. Receive RuPay debit card',
 'https://pmjdy.gov.in', '1800-11-0001', '2014-08-28', TRUE,
 ARRAY['banking', 'financial_inclusion', 'insurance', 'debit_card'], 85, 520000000, NULL),

('pm_matru_vandana', 'PMMVY', 'Pradhan Mantri Matru Vandana Yojana',
 'Maternity benefit of ₹11,000 in three installments for first live birth and ₹6,000 for second if it is a girl child. Provides partial compensation for wage loss during pregnancy and childbirth, promotes safe delivery and nutrition.',
 'Maternity benefit of ₹11,000 for pregnant women',
 'Ministry of Women & Child Development', NULL, 'central', 'dbt',
 '₹11,000 (first child) / ₹6,000 (second girl child)', 'First installment of ₹3,000 on pregnancy registration, ₹3,000 after 6 months, ₹5,000 at child birth registration.',
 'All pregnant and lactating women for first live birth. For second child, benefit available only if the child is a girl.',
 '1. Register at nearest Anganwadi Centre or health facility 2. Submit MCP card and Aadhaar 3. Bank details verified 4. Amount credited in installments',
 'https://wcd.nic.in/schemes/pradhan-mantri-matru-vandana-yojana', '011-23381611', '2017-01-01', TRUE,
 ARRAY['maternity', 'women', 'pregnancy', 'nutrition', 'dbt'], 83, 35000000, '₹2,500 Crore'),

('pm_vishwakarma', 'PMV', 'PM Vishwakarma',
 'Holistic scheme for traditional artisans and craftspeople working with hands and tools. Provides recognition, skill training, toolkit incentive of ₹15,000, credit support up to ₹3 lakh at 5% interest, and digital marketing support.',
 'Skill training, toolkit, and credit for traditional artisans',
 'Ministry of Micro, Small and Medium Enterprises', NULL, 'central', 'loan',
 '₹15,000 toolkit + up to ₹3 lakh loan at 5%', 'PM Vishwakarma Certificate, 5-7 day skill training, ₹500/day stipend, ₹15,000 toolkit, ₹1-3 lakh credit at 5%, digital marketing support.',
 'Artisan or craftsperson aged 18+ working in any of the 18 identified trades (carpenter, blacksmith, goldsmith, potter, sculptor, etc.) with hands and tools. Should be unorganized sector worker.',
 '1. Register on pmvishwakarma.gov.in 2. Verify at CSC with biometrics 3. Attend skill training 4. Receive toolkit grant 5. Apply for credit',
 'https://pmvishwakarma.gov.in', '1800-599-0044', '2023-09-17', TRUE,
 ARRAY['artisan', 'craftsperson', 'skill_training', 'toolkit', 'traditional'], 79, 3000000, '₹13,000 Crore'),

('pm_suraksha_bima', 'PMSBY', 'Pradhan Mantri Suraksha Bima Yojana',
 'Accidental death and disability insurance scheme at just ₹20 per year. Provides ₹2 lakh for accidental death/permanent total disability and ₹1 lakh for permanent partial disability. Auto-debited from bank account.',
 'Accident insurance of ₹2 lakh at ₹20/year premium',
 'Ministry of Finance', 'Department of Financial Services', 'central', 'insurance',
 '₹2 lakh (death/disability) at ₹20/year', 'Accidental death: ₹2 lakh, Total permanent disability: ₹2 lakh, Partial permanent disability: ₹1 lakh.',
 'Savings bank account holder aged 18-70 years with Aadhaar linked to bank account. Auto-debit consent required.',
 '1. Visit bank or apply through net banking/mobile banking 2. Give auto-debit consent 3. Aadhaar seeded to bank account 4. ₹20 auto-debited annually',
 'https://financialservices.gov.in/insurance-divisions/Government-Sponsored-Socially-Oriented-Insurance-Schemes/Pradhan-Mantri-Suraksha-Bima-Yojana(PMSBY)', '1800-180-1111', '2015-05-09', TRUE,
 ARRAY['insurance', 'accident', 'death', 'disability', 'low_premium'], 82, 350000000, NULL),

('pm_jeevan_jyoti', 'PMJJBY', 'Pradhan Mantri Jeevan Jyoti Bima Yojana',
 'Life insurance scheme providing ₹2 lakh life cover at just ₹436 per year. Renewable on yearly basis. Premium auto-debited from bank account. Available to all savings bank account holders aged 18-50.',
 'Life insurance of ₹2 lakh at ₹436/year premium',
 'Ministry of Finance', 'Department of Financial Services', 'central', 'insurance',
 '₹2 lakh at ₹436/year premium', 'Death cover of ₹2 lakh for any reason, premium of ₹436 per year auto-debited from bank account.',
 'Savings bank account holder aged 18-50 years with Aadhaar linked to bank account.',
 '1. Apply through bank, net banking, or mobile banking 2. Give auto-debit consent 3. ₹436 debited annually on June 1st',
 'https://financialservices.gov.in/insurance-divisions/Government-Sponsored-Socially-Oriented-Insurance-Schemes/Pradhan-Mantri-Jeevan-Jyoti-Bima-Yojana(PMJJBY)', '1800-180-1111', '2015-05-09', TRUE,
 ARRAY['life_insurance', 'death_cover', 'low_premium'], 80, 160000000, NULL),

('nps_traders', 'NPS-T', 'National Pension Scheme for Traders and Self-Employed',
 'Voluntary pension scheme for small traders, shopkeepers, and self-employed persons. Provides monthly pension of ₹3,000 after attaining 60 years. Monthly contribution ranges from ₹55 to ₹200 depending on age of joining.',
 'Monthly pension of ₹3,000 for traders after age 60',
 'Ministry of Labour & Employment', NULL, 'central', 'pension',
 '₹3,000 per month after 60 years', 'Monthly pension of ₹3,000 from age 60, equal government contribution, family pension on death.',
 'Self-employed shopkeeper/trader/self-employed person aged 18-40 with annual turnover below ₹1.5 crore. Should not be EPFO/ESIC/PMSBY member.',
 '1. Visit nearest CSC or apply online 2. Aadhaar and bank details 3. Monthly contribution set up 4. Pension from age 60',
 'https://maandhan.in', '1800-267-6888', '2019-07-22', TRUE,
 ARRAY['pension', 'trader', 'shopkeeper', 'self_employed'], 72, 5000000, NULL),

('agnipath', 'AGNIPATH', 'Agnipath Scheme',
 'Short-term recruitment scheme for Indian Armed Forces. Agniveers serve for 4 years with attractive pay package starting at ₹30,000/month. After 4 years, 25% retained permanently and 75% receive Seva Nidhi package of approximately ₹11.71 lakh.',
 'Short-term military service with Seva Nidhi package',
 'Ministry of Defence', NULL, 'central', 'dbt',
 '₹30,000/month + ₹11.71 lakh Seva Nidhi', 'Monthly pay starting ₹30,000, contributes 30% to Seva Nidhi corpus matched by government, tax-free lump sum after 4 years.',
 'Indian citizen aged 17.5-23 years, meeting physical and educational criteria as per entry level (10th pass/12th pass/graduate depending on branch).',
 '1. Apply through joinindianarmy.nic.in / joinindiannavy.gov.in / airmenselection.cdac.in 2. Written exam 3. Physical fitness test 4. Medical exam 5. Merit-based selection',
 'https://www.mod.gov.in', '011-23011449', '2022-06-14', TRUE,
 ARRAY['defence', 'military', 'youth', 'armed_forces'], 65, 400000, NULL),

('saubhagya', 'SAUBHAGYA', 'Pradhan Mantri Sahaj Bijli Har Ghar Yojana',
 'Free electricity connection to all remaining un-electrified households in rural and urban areas. Provides free LED bulbs, wiring, and energy meter. Solar standalone systems for remote areas without grid connectivity.',
 'Free electricity connection to every household',
 'Ministry of Power', 'Rural Electrification Corporation', 'central', 'free_service',
 'Free electricity connection + LED bulbs + wiring', 'Free connection, free prepaid/smart meter, 5 LED lights, 1 DC fan for solar beneficiaries in remote areas.',
 'All un-electrified households in rural and urban areas. BPL households get free connection. APL households pay ₹500 in 10 installments.',
 '1. Contact local DISCOM office 2. Submit application with identity proof 3. Free connection installed within 7-10 days',
 'https://saubhagya.gov.in', '1800-599-0912', '2017-09-25', TRUE,
 ARRAY['electricity', 'free_connection', 'led_bulbs', 'rural', 'urban'], 78, 28000000, '₹16,320 Crore'),

('pm_svanidhi', 'PMSVANidhi', 'PM Street Vendor''s AtmaNirbhar Nidhi',
 'Micro-credit facility for street vendors affected by COVID-19. Working capital loan of ₹10,000 (1st tranche), ₹20,000 (2nd), ₹50,000 (3rd) with interest subsidy of 7%. Digital transaction cashback incentive also provided.',
 'Working capital loans for street vendors',
 'Ministry of Housing & Urban Affairs', NULL, 'central', 'loan',
 '₹10,000-₹50,000 with 7% interest subsidy', 'Micro loans in 3 tranches: ₹10,000 → ₹20,000 → ₹50,000, 7% interest subsidy, digital payment cashback up to ₹1,200/year.',
 'Street vendors with vending certificate/Letter of Recommendation or identified in survey. Vendors operating in urban areas as on or before March 24, 2020.',
 '1. Apply on pmsvanidhi.mohua.gov.in 2. ULB verifies credentials 3. Apply at nearest lending institution 4. Loan sanctioned in 30 days',
 'https://pmsvanidhi.mohua.gov.in', '1800-11-1979', '2020-06-01', TRUE,
 ARRAY['street_vendor', 'micro_credit', 'working_capital', 'self_employed'], 76, 6500000, '₹8,100 Crore');

-- ============================================================================
-- TAMIL NADU STATE SCHEMES (10+)
-- ============================================================================

INSERT INTO schemes (scheme_id, name, full_name, description, short_description, ministry, department, type, state, benefit_type, benefit_amount, benefit_description, eligibility_summary, application_process, application_url, helpline, launch_date, is_active, tags, priority_score) VALUES

('tn_magalir_urimai', 'Magalir Urimai Thogai', 'Kalaignar Magalir Urimai Thogai Thittam',
 'Monthly financial assistance of ₹1,000 directly transferred to women heads of family in Tamil Nadu. Aims to empower women financially and reduce gender-based economic inequality. Covers all eligible women above 21 years who are family heads.',
 'Monthly ₹1,000 for women heads of families in Tamil Nadu',
 NULL, 'Department of Social Welfare', 'state', 'Tamil Nadu', 'dbt',
 '₹1,000 per month', 'Direct bank transfer of ₹1,000 every month to eligible women heads of households.',
 'Woman aged 21+ who is the head of a family in Tamil Nadu. Annual family income should not exceed ₹2,50,000. Should not be a government employee or income tax payer.',
 '1. Apply at nearest Taluk office or online portal 2. Submit Aadhaar, family card, income certificate 3. Verification by village administrative officer 4. Amount credited monthly',
 'https://wcd.tn.gov.in', '1800-425-4747', '2023-09-15', TRUE,
 ARRAY['women', 'dbt', 'financial_empowerment', 'tamil_nadu'], 92),

('tn_breakfast_scheme', 'CM Breakfast Scheme', 'Chief Minister''s Breakfast Scheme',
 'Free nutritious breakfast provided to students of Classes 1-5 in government schools across Tamil Nadu. Includes a balanced meal with egg/banana, served before school hours to improve nutrition, attendance, and learning outcomes.',
 'Free breakfast for government school students (Class 1-5)',
 NULL, 'School Education Department', 'state', 'Tamil Nadu', 'in_kind',
 'Free daily breakfast', 'Nutritious breakfast including rice/wheat-based meal with egg/banana/milk for primary school students daily.',
 'All students enrolled in Classes 1 to 5 in Tamil Nadu government and government-aided schools.',
 'Automatically available to all eligible students. Schools prepare and serve breakfast before first class.',
 'https://tnschools.gov.in', '14417', '2022-09-15', TRUE,
 ARRAY['education', 'nutrition', 'children', 'school', 'tamil_nadu'], 88),

('tn_marriage_assistance', 'Marriage Assistance', 'Tamil Nadu Marriage Assistance Scheme',
 'Financial assistance of ₹50,000 along with 8 grams of gold for marriage of women from economically weaker sections. Special enhanced assistance for inter-caste marriages. Applicable for first two marriages in the family.',
 'Marriage assistance of ₹50,000 + 8g gold for women',
 NULL, 'Department of Social Welfare', 'state', 'Tamil Nadu', 'dbt',
 '₹50,000 + 8 grams gold', '₹50,000 cash and 8 grams of 22-carat gold coin for marriage of girls from poor families. Enhanced for inter-caste marriages.',
 'Bride from Tamil Nadu, annual family income below ₹72,000. Must have passed at least Class 10. Applicable for SC/ST, MBC, BC, and denotified communities.',
 '1. Apply at nearest District Social Welfare office 2. Submit certificates (education, income, community, birth) 3. Apply at least 40 days before marriage 4. Amount disbursed before marriage',
 'https://wcd.tn.gov.in', '044-25670900', '1989-01-01', TRUE,
 ARRAY['marriage', 'women', 'gold', 'financial_assistance', 'tamil_nadu'], 85),

('tn_free_laptop', 'Free Laptop', 'Tamil Nadu Free Laptop Scheme',
 'Free laptop distribution to students joining Class 11 and undergraduate courses in government and government-aided institutions. Aims to bridge the digital divide and enhance digital literacy among students.',
 'Free laptops for government school/college students',
 NULL, 'Department of Information Technology', 'state', 'Tamil Nadu', 'in_kind',
 'Free laptop computer', 'One laptop per eligible student joining higher secondary or undergraduate education in government institutions.',
 'Students joining Class 11 or first year of college in Tamil Nadu government and government-aided institutions.',
 '1. Enroll in eligible institution 2. Institution submits student list 3. Laptops distributed at institution',
 'https://tn.gov.in', '1800-425-6753', '2011-09-01', TRUE,
 ARRAY['education', 'laptop', 'digital', 'students', 'tamil_nadu'], 80),

('tn_uzhavar_sandhai', 'Uzhavar Sandhai', 'Uzhavar Sandhai (Farmer''s Market)',
 'Direct farmer-to-consumer market eliminating middlemen. Farmers sell fresh vegetables and fruits directly at government-managed markets. Provides free stall, weighing scale, and basic facilities. Ensures fair price for farmers and affordable prices for consumers.',
 'Direct farmer-to-consumer markets with free stalls',
 NULL, 'Department of Agricultural Marketing', 'state', 'Tamil Nadu', 'free_service',
 'Free market stall and facilities', 'Free stall, weighing scale, packaging material, and basic amenities at Uzhavar Sandhai premises.',
 'Registered farmers in Tamil Nadu growing fruits, vegetables, and flowers. Must register with the local Uzhavar Sandhai manager.',
 '1. Contact local Uzhavar Sandhai manager 2. Register with farmer ID and land records 3. Get allotted stall schedule 4. Sell produce directly to consumers',
 'https://agrimarketing.tn.gov.in', '044-28524894', '1999-01-01', TRUE,
 ARRAY['agriculture', 'farmer_market', 'vegetables', 'direct_sale', 'tamil_nadu'], 72),

('tn_amma_unavagam', 'Amma Unavagam', 'Amma Unavagam (Amma Canteen)',
 'Subsidized canteens providing meals at nominal prices across Tamil Nadu. Idli at ₹1, variety rice/sambar rice at ₹5, curd rice at ₹3. Over 400 canteens operational in Chennai and other cities.',
 'Subsidized meals at ₹1-₹5 in government canteens',
 NULL, 'Greater Chennai Corporation', 'state', 'Tamil Nadu', 'in_kind',
 'Meals at ₹1-₹5', 'Idli (1 piece): ₹1, Chapati: ₹3, Sambar rice/variety rice: ₹5, Curd rice: ₹3. Clean, hygienic, and unlimited quantity.',
 'Open to all. No eligibility criteria required. Walk-in service at any Amma Unavagam outlet.',
 'Simply walk in to any Amma Unavagam outlet. No application or registration required.',
 'https://chennaicorporation.gov.in', '044-25619206', '2013-02-01', TRUE,
 ARRAY['food', 'subsidized_meal', 'canteen', 'affordable', 'tamil_nadu'], 75),

('tn_free_bus_women', 'Free Bus for Women', 'Tamil Nadu Free Bus Travel for Women',
 'Free travel for women in ordinary government buses operated by TNSTC across Tamil Nadu. Women can travel in any ordinary (non-AC, non-deluxe) government bus without ticket. Aims to enhance women''s mobility and economic participation.',
 'Free bus travel for women in government buses',
 NULL, 'Transport Department', 'state', 'Tamil Nadu', 'free_service',
 'Free bus travel in ordinary buses', 'Unlimited free travel in all ordinary TNSTC and metropolitan transport buses for women of all ages.',
 'All women passengers in Tamil Nadu. No income or age restriction. Valid only in ordinary government buses (not AC/deluxe/premium services).',
 'No application needed. Women can board any ordinary government bus and travel for free.',
 'https://tnstc.in', '044-25361888', '2021-01-01', TRUE,
 ARRAY['women', 'transport', 'free_bus', 'mobility', 'tamil_nadu'], 90),

('tn_pudhumai_penn', 'Pudhumai Penn', 'Moovalur Ramamirtham Ammaiyar Pudhumai Penn Scheme',
 'Monthly assistance of ₹1,000 to girl students who have studied Classes 6-12 in Tamil Nadu government schools and are pursuing higher education (degree/diploma/ITI). Aims to promote higher education among government school girls.',
 'Monthly ₹1,000 for government school girls in higher education',
 NULL, 'Department of Higher Education', 'state', 'Tamil Nadu', 'dbt',
 '₹1,000 per month during higher education', '₹1,000 per month deposited directly to girl students pursuing undergraduate/diploma/ITI after schooling in government institutions.',
 'Girl students who studied Classes 6-12 in Tamil Nadu government schools and enrolled in recognized degree, diploma, or ITI courses. No income criterion.',
 '1. Apply online through higher education portal 2. Submit government school study certificates 3. College/institution verification 4. Monthly credit to bank account',
 'https://pudhugai.tn.gov.in', '044-25672300', '2022-09-05', TRUE,
 ARRAY['women', 'education', 'higher_education', 'scholarship', 'tamil_nadu'], 86),

('tn_kalaignar_insurance', 'Kalaignar Insurance', 'Kalaignar Magalir Urimai Thogai Kappeedu Thittam',
 'Life and health insurance scheme for families below poverty line in Tamil Nadu. Covers hospitalization up to ₹5 lakh for specified surgeries and treatments. Combined with state health protection scheme.',
 'Health insurance coverage for BPL families in Tamil Nadu',
 NULL, 'Health & Family Welfare Department', 'state', 'Tamil Nadu', 'insurance',
 'Up to ₹5,00,000 per family per year', 'Cashless treatment at empanelled hospitals for over 1,000 procedures. Combined coverage under Chief Minister''s Comprehensive Health Insurance Scheme.',
 'Families with annual income below ₹72,000. Priority to BPL ration card holders. Must be Tamil Nadu resident with family card.',
 '1. Visit any empanelled hospital with ration card and Aadhaar 2. Get enrolled at hospital 3. Avail cashless treatment as needed',
 'https://cmchistn.com', '104', '2009-01-01', TRUE,
 ARRAY['health', 'insurance', 'bpl', 'hospital', 'tamil_nadu'], 87),

('tn_naan_mudhalvan', 'Naan Mudhalvan', 'Naan Mudhalvan (I am the First) Skill Development',
 'Comprehensive skill development and career guidance platform for Tamil Nadu youth. Provides industry-relevant training, soft skills development, internship opportunities, and placement support for college and polytechnic students.',
 'Free skill training and placement support for TN students',
 NULL, 'Department of Higher Education', 'state', 'Tamil Nadu', 'free_service',
 'Free skill training + internship + placement', 'Industry-relevant courses, soft skill training, mock interviews, resume building, company-linked internships, and placement drives.',
 'Students enrolled in any recognized college, university, or polytechnic in Tamil Nadu.',
 '1. Register on naanmudhalvan.tn.gov.in 2. Choose skill courses 3. Complete training modules 4. Participate in placement drives',
 'https://naanmudhalvan.tn.gov.in', '044-25361888', '2022-04-05', TRUE,
 ARRAY['skill_development', 'youth', 'placement', 'training', 'tamil_nadu'], 83),

('tn_amma_two_wheeler', 'Amma Two Wheeler', 'Amma Two Wheeler Scheme for Working Women',
 'Subsidy of 50% (up to ₹25,000) on purchase of two-wheelers for working women in Tamil Nadu. Aims to improve women''s commuting convenience and economic independence.',
 '50% subsidy on two-wheeler purchase for working women',
 NULL, 'Department of Social Welfare', 'state', 'Tamil Nadu', 'subsidy',
 '50% subsidy up to ₹25,000', '50% of the two-wheeler cost or ₹25,000 (whichever is less) provided as subsidy. Balance to be paid by beneficiary.',
 'Working women in Tamil Nadu aged 18+ with annual income below ₹2,50,000. Must have valid driving license. Preference to women from rural areas.',
 '1. Apply at District Social Welfare office 2. Submit income certificate, driving license, Aadhaar 3. Get approval 4. Purchase vehicle and claim subsidy',
 'https://wcd.tn.gov.in', '044-25670900', '2018-01-01', TRUE,
 ARRAY['women', 'two_wheeler', 'subsidy', 'commute', 'tamil_nadu'], 74);

-- ============================================================================
-- KARNATAKA STATE SCHEMES (10+)
-- ============================================================================

INSERT INTO schemes (scheme_id, name, full_name, description, short_description, ministry, department, type, state, benefit_type, benefit_amount, benefit_description, eligibility_summary, application_process, application_url, helpline, launch_date, is_active, tags, priority_score) VALUES

('ka_gruha_lakshmi', 'Gruha Lakshmi', 'Gruha Lakshmi Scheme',
 'Monthly financial assistance of ₹2,000 to women heads of households in Karnataka. Transferred directly to Aadhaar-linked bank account. One of the five guarantee schemes of the Karnataka government.',
 'Monthly ₹2,000 for women heads of families in Karnataka',
 NULL, 'Department of Women & Child Development', 'state', 'Karnataka', 'dbt',
 '₹2,000 per month', 'Direct bank transfer of ₹2,000 per month to women who are heads of households in Karnataka.',
 'Woman who is the head of a BPL/APL family in Karnataka. Only one woman per family eligible. Should not be a government employee or income tax payer.',
 '1. Apply online at sevasindhuservices.karnataka.gov.in 2. Submit Aadhaar, ration card, bank details 3. Gram Panchayat/ULB verification 4. Monthly credit starts',
 'https://sevasindhuservices.karnataka.gov.in', '1902', '2023-07-01', TRUE,
 ARRAY['women', 'dbt', 'financial_assistance', 'karnataka'], 92),

('ka_shakti', 'Shakti', 'Shakti Free Bus Travel for Women',
 'Free travel for all women in non-AC government buses operated by KSRTC and BMTC across Karnataka. Women can obtain a Shakti smart card for seamless travel. Over 1.5 crore women have availed this benefit.',
 'Free bus travel for women in Karnataka government buses',
 NULL, 'Transport Department', 'state', 'Karnataka', 'free_service',
 'Free bus travel in non-AC buses', 'Unlimited free travel in all non-premium, non-AC KSRTC and BMTC buses with Shakti smart card.',
 'All women residents of Karnataka. Must obtain Shakti smart card with Aadhaar and photo. Valid in non-AC government buses only.',
 '1. Apply for Shakti smart card online or at KSRTC/BMTC counter 2. Submit photo and Aadhaar 3. Receive smart card 4. Tap and travel free',
 'https://transport.karnataka.gov.in', '1800-425-9355', '2023-06-11', TRUE,
 ARRAY['women', 'transport', 'free_bus', 'smart_card', 'karnataka'], 91),

('ka_anna_bhagya', 'Anna Bhagya', 'Anna Bhagya Scheme',
 'Enhanced food security scheme providing 10 kg of free rice per person per month to BPL families (up from 7 kg under NFSA). Benefits over 4.5 crore people across Karnataka through the public distribution system.',
 '10 kg free rice per person per month for BPL families',
 NULL, 'Department of Food and Civil Supplies', 'state', 'Karnataka', 'in_kind',
 '10 kg free rice per person per month', 'Free rice distribution through ration shops. Additional 3 kg over NFSA entitlement of 7 kg.',
 'BPL ration card holders (Antyodaya and Priority household cards) in Karnataka.',
 '1. Must have BPL/AAY/PHH ration card 2. Visit nearest fair price shop 3. Collect rice using biometric/ration card authentication',
 'https://ahara.kar.nic.in', '1967', '2013-07-10', TRUE,
 ARRAY['food', 'ration', 'rice', 'bpl', 'food_security', 'karnataka'], 89),

('ka_yuva_nidhi', 'Yuva Nidhi', 'Yuva Nidhi Scheme',
 'Monthly unemployment allowance of ₹3,000 for graduate and ₹1,500 for diploma holders in Karnataka while seeking employment. Provided for a maximum period of 2 years from date of completion of education.',
 'Monthly unemployment allowance for graduates and diploma holders',
 NULL, 'Department of Skill Development', 'state', 'Karnataka', 'dbt',
 '₹3,000/month (graduates), ₹1,500/month (diploma)', 'Monthly allowance while job searching, skill training linkage, and placement assistance for up to 2 years.',
 'Karnataka domicile, graduate or diploma holder from government/aided institution, aged below 25, unemployed, not employed in any government/private job, annual family income below ₹6 lakh.',
 '1. Register on Yuva Nidhi portal 2. Submit graduation/diploma certificate 3. Kayaka portal job seeker registration 4. Monthly amount credited after compliance',
 'https://sevasindhuservices.karnataka.gov.in', '1902', '2023-07-01', TRUE,
 ARRAY['youth', 'unemployment', 'graduate', 'allowance', 'karnataka'], 84),

('ka_bhagya_jyothi', 'Bhagya Jyothi', 'Bhagya Jyothi / Kutir Jyothi',
 'Free electricity supply of up to 75 units per month to BPL families in Karnataka. Covers SC/ST households, rural poor, and urban slum dwellers. Monthly electricity bill is zero for consumption within the free limit.',
 'Free 75 units of electricity per month for BPL families',
 NULL, 'Energy Department', 'state', 'Karnataka', 'free_service',
 'Free 75 units electricity per month', 'Zero electricity bill for consumption up to 75 units per month for BPL families.',
 'BPL families in Karnataka with electricity connection. SC/ST households automatically eligible. Must have valid BPL card.',
 '1. Submit BPL/SC/ST certificate to nearest BESCOM/HESCOM/CESCOM/GESCOM office 2. Service connection assessed 3. Free units applied to meter',
 'https://bescom.karnataka.gov.in', '1912', '2005-01-01', TRUE,
 ARRAY['electricity', 'free_power', 'bpl', 'sc_st', 'karnataka'], 80),

('ka_vidyasiri', 'Vidyasiri', 'Vidyasiri Scholarship',
 'Post-matric scholarship for SC/ST/OBC students in Karnataka covering tuition fees, hostel charges, and monthly maintenance allowance. Covers professional and non-professional courses in government and private institutions.',
 'Post-matric scholarship for SC/ST/OBC students',
 NULL, 'Department of Social Welfare', 'state', 'Karnataka', 'scholarship',
 'Full tuition + hostel + ₹1,500/month maintenance', 'Complete tuition fee reimbursement, hostel fee, and monthly maintenance allowance of ₹1,500 for hostellers.',
 'SC/ST/OBC students of Karnataka who have passed Class 10 and enrolled in post-matric courses. Annual family income below ₹2.5 lakh (SC/ST) or ₹1 lakh (OBC).',
 '1. Apply on SSP portal (ssp.karnataka.gov.in) 2. Submit income, caste, marks certificates 3. Institution verification 4. Scholarship credited to bank',
 'https://ssp.karnataka.gov.in', '080-22353930', '2006-01-01', TRUE,
 ARRAY['scholarship', 'sc_st', 'obc', 'education', 'post_matric', 'karnataka'], 83),

('ka_raitha_vidya_nidhi', 'Raitha Vidya Nidhi', 'Raitha Vidya Nidhi',
 'Free education for children of farmers in Karnataka from Class 1 to post-graduation. Government covers all educational expenses including tuition fees, hostel fees, and examination fees for children of registered farmers.',
 'Free education for children of farmers in Karnataka',
 NULL, 'Department of Agriculture', 'state', 'Karnataka', 'scholarship',
 'Full tuition + exam fees + hostel', 'Complete educational expenses covered including tuition, exam fees, uniforms (for school students), and hostel charges.',
 'Children of registered farmers in Karnataka. Both agricultural and horticultural farmer children are eligible. No income ceiling.',
 '1. Parent must be registered on Fruits portal 2. Apply on SSP portal 3. Submit parent farmer registration certificate 4. Institution verification',
 'https://ssp.karnataka.gov.in', '080-22032481', '2023-07-01', TRUE,
 ARRAY['farmer', 'education', 'children', 'scholarship', 'free_education', 'karnataka'], 82),

('ka_griha_aashraya', 'Griha Aashraya', 'Basava Vasati Yojane / Griha Aashraya',
 'Housing scheme providing financial assistance up to ₹1.50 lakh for construction of houses for BPL families in rural Karnataka. Beneficiaries selected through Gram Panchayats based on priority list.',
 'Housing assistance of ₹1.5 lakh for rural BPL families',
 NULL, 'Department of Housing', 'state', 'Karnataka', 'dbt',
 'Up to ₹1,50,000', 'Financial assistance of ₹1.50 lakh in installments for construction of pucca house with toilet.',
 'BPL families in rural Karnataka who do not own a pucca house. Priority to SC/ST, widows, differently-abled, and destitute families.',
 '1. Apply through Gram Panchayat 2. Beneficiary list approved by Gram Sabha 3. Funds released in installments on construction milestones 4. House completion verified',
 'https://housing.karnataka.gov.in', '080-22264612', '2015-01-01', TRUE,
 ARRAY['housing', 'rural', 'bpl', 'construction', 'karnataka'], 81),

('ka_arogya_sanjeevini', 'Arogya Sanjeevini', 'Arogya Sanjeevini Health Insurance',
 'State health insurance scheme providing cashless treatment up to ₹5 lakh per family per year in empanelled hospitals. Covers over 1,900 procedures including surgeries, day care, and medical treatments.',
 'Health insurance of ₹5 lakh per family per year',
 NULL, 'Department of Health & Family Welfare', 'state', 'Karnataka', 'insurance',
 '₹5,00,000 per family per year', 'Cashless hospitalization at 800+ empanelled hospitals across Karnataka covering 1,900+ medical procedures.',
 'All ration card holders in Karnataka (BPL and APL). Family covered includes head, spouse, parents, and up to 3 dependent children.',
 '1. Visit empanelled hospital with Aadhaar and ration card 2. Eligibility verified online 3. Treatment provided cashless 4. Insurance claim settled with hospital',
 'https://arogya.karnataka.gov.in', '104', '2018-01-01', TRUE,
 ARRAY['health', 'insurance', 'cashless', 'hospital', 'karnataka'], 88),

('ka_krishi_bhagya', 'Krishi Bhagya', 'Krishi Bhagya Scheme',
 'Integrated farming scheme providing farm ponds, drip/sprinkler irrigation, poly houses, and shade nets to small and marginal farmers in rain-fed areas of Karnataka. Subsidizes rainwater harvesting and modern irrigation.',
 'Farm ponds and modern irrigation for small farmers',
 NULL, 'Department of Agriculture', 'state', 'Karnataka', 'subsidy',
 '90% subsidy on farm ponds + irrigation systems', '90% subsidy on farm pond construction, drip irrigation, sprinkler systems, poly house, and shade nets for rain-fed farmers.',
 'Small and marginal farmers (land holding up to 5 acres) in rain-fed areas of Karnataka. Priority to SC/ST farmers.',
 '1. Apply at nearest Raitha Samparka Kendra 2. Submit land records and photo 3. Technical survey of land 4. Work order issued 5. Subsidy released after completion',
 'https://raitamitra.kar.nic.in', '080-22212818', '2014-01-01', TRUE,
 ARRAY['agriculture', 'irrigation', 'farm_pond', 'rain_fed', 'subsidy', 'karnataka'], 77),

('ka_mathru_purna', 'Mathru Purna', 'Mathru Purna Scheme',
 'One full meal per day for pregnant and lactating women at Anganwadi centres in Karnataka. Includes nutritious food with rice, dal, vegetables, egg, and milk to address maternal malnutrition and improve child health outcomes.',
 'One free meal daily for pregnant women at Anganwadi centres',
 NULL, 'Department of Women & Child Development', 'state', 'Karnataka', 'in_kind',
 'One full meal per day', 'Nutritious meal including rice, dal, vegetables, egg, fruit, and milk served daily at Anganwadi centres.',
 'All pregnant women and lactating mothers registered at Anganwadi centres in Karnataka. No income restriction.',
 '1. Register at nearest Anganwadi centre 2. Show MCP card and Aadhaar 3. Visit centre daily for meal 4. Also receive take-home ration',
 'https://dwcd.karnataka.gov.in', '1098', '2017-01-01', TRUE,
 ARRAY['women', 'nutrition', 'pregnancy', 'anganwadi', 'food', 'karnataka'], 79);

-- ============================================================================
-- DEPARTMENTS (Tamil Nadu & Karnataka)
-- ============================================================================

INSERT INTO departments (name, short_name, state, category, head_designation, email, phone, website, grievance_portal, sla_hours) VALUES

-- Tamil Nadu Departments
('Tamil Nadu Highways Department', 'TNHD', 'Tamil Nadu', 'roads', 'Chief Engineer (Highways)', 'ce.highways@tn.gov.in', '044-25671898', 'https://tnhighways.gov.in', 'https://www.tnpgrs.tn.gov.in', 72),
('Tamil Nadu Water Supply and Drainage Board', 'TWAD', 'Tamil Nadu', 'water_supply', 'Managing Director', 'twad@tn.gov.in', '044-24343344', 'https://twadboard.tn.gov.in', 'https://www.tnpgrs.tn.gov.in', 48),
('Greater Chennai Corporation - Storm Water Drain', 'GCC-SWD', 'Tamil Nadu', 'drainage', 'Commissioner (GCC)', 'commr.gcc@tn.gov.in', '044-25619206', 'https://chennaicorporation.gov.in', 'https://www.tnpgrs.tn.gov.in', 48),
('Tamil Nadu Generation and Distribution Corporation', 'TANGEDCO', 'Tamil Nadu', 'electricity', 'Chairman & Managing Director', 'cmd@tangedco.gov.in', '044-28520700', 'https://tangedco.gov.in', 'https://www.tnpgrs.tn.gov.in', 24),
('Tamil Nadu Pollution Control Board', 'TNPCB', 'Tamil Nadu', 'environment', 'Chairman', 'tnpcb@tn.gov.in', '044-22200552', 'https://tnpcb.gov.in', 'https://www.tnpgrs.tn.gov.in', 72),
('Greater Chennai Corporation - Solid Waste', 'GCC-SWM', 'Tamil Nadu', 'garbage', 'Commissioner (GCC)', 'swm.gcc@tn.gov.in', '044-25619206', 'https://chennaicorporation.gov.in', 'https://www.tnpgrs.tn.gov.in', 24),
('Tamil Nadu State Transport Corporation', 'TNSTC', 'Tamil Nadu', 'public_transport', 'Managing Director', 'md@tnstc.in', '044-25361888', 'https://tnstc.in', 'https://www.tnpgrs.tn.gov.in', 48),
('Directorate of Public Health', 'DPH-TN', 'Tamil Nadu', 'healthcare', 'Director of Public Health', 'dph@tn.gov.in', '044-28592062', 'https://dph.tn.gov.in', 'https://www.tnpgrs.tn.gov.in', 48),
('Tamil Nadu Civil Supplies Corporation', 'TNCSC', 'Tamil Nadu', 'ration_shop', 'Managing Director', 'md@tncsc.tn.gov.in', '044-28583311', 'https://tncsc.tn.gov.in', 'https://www.tnpgrs.tn.gov.in', 72),
('Corporation of Chennai - Street Lights', 'GCC-SL', 'Tamil Nadu', 'streetlights', 'Commissioner (GCC)', 'lights.gcc@tn.gov.in', '1913', 'https://chennaicorporation.gov.in', 'https://www.tnpgrs.tn.gov.in', 48),
('Directorate of School Education', 'DSE-TN', 'Tamil Nadu', 'education', 'Director', 'dse@tn.gov.in', '044-28278039', 'https://tnschools.gov.in', 'https://www.tnpgrs.tn.gov.in', 72),
('Tamil Nadu Slum Clearance Board', 'TNSCB', 'Tamil Nadu', 'housing', 'Managing Director', 'md@tnscb.gov.in', '044-28524894', 'https://tnscb.org', 'https://www.tnpgrs.tn.gov.in', 72),
('Revenue and Disaster Management Department', 'REV-TN', 'Tamil Nadu', 'land_revenue', 'Commissioner of Revenue Administration', 'cra@tn.gov.in', '044-28590828', 'https://tnrd.gov.in', 'https://www.tnpgrs.tn.gov.in', 72),
('Tamil Nadu Police - Citizen Portal', 'TNP', 'Tamil Nadu', 'police', 'Director General of Police', 'dgp@tnpolice.gov.in', '044-28447777', 'https://eservices.tnpolice.gov.in', 'https://www.tnpgrs.tn.gov.in', 24),
('Directorate of Vigilance and Anti-Corruption', 'DVAC-TN', 'Tamil Nadu', 'corruption', 'Director', 'dvac@tn.gov.in', '044-24353138', 'https://dvac.tn.gov.in', 'https://www.tnpgrs.tn.gov.in', 72),

-- Karnataka Departments
('Karnataka Public Works Department', 'KPWD', 'Karnataka', 'roads', 'Chief Engineer', 'ce.pwd@karnataka.gov.in', '080-22263484', 'https://kpwd.karnataka.gov.in', 'https://janaspandana.karnataka.gov.in', 72),
('Karnataka Urban Water Supply & Drainage Board', 'KUWSDB', 'Karnataka', 'water_supply', 'Managing Director', 'md.kuwsdb@karnataka.gov.in', '080-22266861', 'https://kuwsdb.karnataka.gov.in', 'https://janaspandana.karnataka.gov.in', 48),
('BBMP Stormwater Drain Department', 'BBMP-SWD', 'Karnataka', 'drainage', 'Chief Engineer (SWD)', 'swd.bbmp@karnataka.gov.in', '080-22975803', 'https://bbmp.gov.in', 'https://janaspandana.karnataka.gov.in', 48),
('Bangalore Electricity Supply Company', 'BESCOM', 'Karnataka', 'electricity', 'Managing Director', 'md@bescom.co.in', '1912', 'https://bescom.karnataka.gov.in', 'https://janaspandana.karnataka.gov.in', 24),
('Karnataka State Pollution Control Board', 'KSPCB', 'Karnataka', 'environment', 'Chairman', 'kspcb@karnataka.gov.in', '080-22952259', 'https://kspcb.karnataka.gov.in', 'https://janaspandana.karnataka.gov.in', 72),
('BBMP Solid Waste Management', 'BBMP-SWM', 'Karnataka', 'garbage', 'Commissioner (BBMP)', 'swm.bbmp@karnataka.gov.in', '080-22975803', 'https://bbmp.gov.in', 'https://janaspandana.karnataka.gov.in', 24),
('Bangalore Metropolitan Transport Corporation', 'BMTC', 'Karnataka', 'public_transport', 'Managing Director', 'md@bmtcinfo.com', '080-22952522', 'https://mybmtc.karnataka.gov.in', 'https://janaspandana.karnataka.gov.in', 48),
('Directorate of Health & Family Welfare Services', 'DHFWS-KA', 'Karnataka', 'healthcare', 'Director', 'dhfws@karnataka.gov.in', '080-22864500', 'https://karunadu.karnataka.gov.in/hfw', 'https://janaspandana.karnataka.gov.in', 48),
('Department of Food and Civil Supplies', 'DFCS-KA', 'Karnataka', 'ration_shop', 'Commissioner', 'fcs@karnataka.gov.in', '1967', 'https://ahara.kar.nic.in', 'https://janaspandana.karnataka.gov.in', 72),
('BBMP Electrical Division', 'BBMP-ELEC', 'Karnataka', 'streetlights', 'Chief Engineer (Electrical)', 'elec.bbmp@karnataka.gov.in', '080-22975803', 'https://bbmp.gov.in', 'https://janaspandana.karnataka.gov.in', 48),
('Department of Public Instruction', 'DPI-KA', 'Karnataka', 'education', 'Commissioner', 'dpi@karnataka.gov.in', '080-22260901', 'https://schooleducation.kar.nic.in', 'https://janaspandana.karnataka.gov.in', 72),
('Karnataka Housing Board', 'KHB', 'Karnataka', 'housing', 'Commissioner', 'khb@karnataka.gov.in', '080-22266034', 'https://karnatakahousing.com', 'https://janaspandana.karnataka.gov.in', 72),
('Department of Revenue', 'REV-KA', 'Karnataka', 'land_revenue', 'Principal Secretary (Revenue)', 'revenue@karnataka.gov.in', '080-22353938', 'https://revenue.karnataka.gov.in', 'https://janaspandana.karnataka.gov.in', 72),
('Karnataka Police - Citizen Services', 'KAP', 'Karnataka', 'police', 'Director General & Inspector General of Police', 'dgp@ksp.gov.in', '080-22942777', 'https://ksp.karnataka.gov.in', 'https://janaspandana.karnataka.gov.in', 24),
('Lokayukta Karnataka', 'LOK-KA', 'Karnataka', 'corruption', 'Lokayukta', 'lokayukta@karnataka.gov.in', '080-22261531', 'https://lokayukta.karnataka.gov.in', 'https://janaspandana.karnataka.gov.in', 72);

-- ============================================================================
-- SAMPLE USERS
-- ============================================================================

INSERT INTO users (name, phone, email, age, gender, state, district, preferred_language, occupation, income_range, annual_income, education, family_status, family_size, category, is_bpl, documents_available, role) VALUES
('Rajesh Kumar', '+919876543210', 'rajesh.kumar@email.com', 45, 'male', 'Tamil Nadu', 'Chennai', 'ta', 'auto_driver', '1l_2.5l', 180000, 'class_10', 'married', 5, 'obc', TRUE, ARRAY['aadhaar', 'voter_id', 'ration_card', 'driving_license'], 'citizen'),
('Priya Lakshmi', '+919876543211', 'priya.l@email.com', 32, 'female', 'Tamil Nadu', 'Coimbatore', 'ta', 'homemaker', 'below_1l', 80000, 'class_12', 'married', 4, 'sc', TRUE, ARRAY['aadhaar', 'voter_id', 'ration_card'], 'citizen'),
('Mohammed Irfan', '+919876543212', 'irfan.m@email.com', 28, 'male', 'Karnataka', 'Bengaluru Urban', 'en', 'software_engineer', '5l_10l', 800000, 'graduate', 'single', 1, 'general', FALSE, ARRAY['aadhaar', 'pan', 'voter_id', 'passport'], 'citizen'),
('Kavitha Devi', '+919876543213', NULL, 55, 'female', 'Tamil Nadu', 'Madurai', 'ta', 'agricultural_laborer', 'below_1l', 60000, 'class_5', 'widow', 3, 'sc', TRUE, ARRAY['aadhaar', 'ration_card'], 'citizen'),
('Suresh Gowda', '+919876543214', 'suresh.g@email.com', 38, 'male', 'Karnataka', 'Mysuru', 'kn', 'farmer', '1l_2.5l', 200000, 'class_10', 'married', 6, 'obc', FALSE, ARRAY['aadhaar', 'voter_id', 'ration_card', 'land_records'], 'citizen'),
('Lakshmi Narayanan', '+919876543215', 'lakshmi.n@email.com', 62, 'female', 'Tamil Nadu', 'Thanjavur', 'ta', 'retired', '1l_2.5l', 150000, 'graduate', 'married', 2, 'general', FALSE, ARRAY['aadhaar', 'voter_id', 'pan', 'pension_card'], 'citizen'),
('Deepa Krishnan', '+919876543216', 'deepa.k@email.com', 24, 'female', 'Karnataka', 'Bengaluru Urban', 'en', 'student', 'below_1l', 0, 'post_graduate', 'single', 1, 'st', FALSE, ARRAY['aadhaar', 'voter_id', 'student_id'], 'citizen'),
('Venkatesh Murthy', '+919876543217', 'venkatesh.m@email.com', 42, 'male', 'Karnataka', 'Dharwad', 'kn', 'shopkeeper', '2.5l_5l', 350000, 'class_12', 'married', 4, 'general', FALSE, ARRAY['aadhaar', 'voter_id', 'pan', 'gst_certificate'], 'citizen'),
('Admin TN', '+919999999901', 'admin.tn@citizenai.gov.in', 40, 'male', 'Tamil Nadu', 'Chennai', 'en', 'government', '5l_10l', 700000, 'post_graduate', 'married', 4, 'general', FALSE, ARRAY['aadhaar', 'pan', 'voter_id'], 'admin'),
('Admin KA', '+919999999902', 'admin.ka@citizenai.gov.in', 38, 'female', 'Karnataka', 'Bengaluru Urban', 'en', 'government', '5l_10l', 700000, 'post_graduate', 'married', 3, 'general', FALSE, ARRAY['aadhaar', 'pan', 'voter_id'], 'admin');

-- ============================================================================
-- SAMPLE COMPLAINTS
-- ============================================================================

-- NOTE: complaint_number is auto-generated by trigger
INSERT INTO complaints (user_id, category, subcategory, subject, description, original_language, state, district, locality, pincode, latitude, longitude, status, priority, ai_priority_score, upvote_count)
SELECT
    u.id,
    'roads'::complaint_category,
    'pothole',
    'Large pothole on Anna Salai near Teynampet causing accidents',
    'There is a dangerous pothole approximately 3 feet wide and 1 foot deep on Anna Salai near the Teynampet junction. Multiple two-wheelers have skidded here in the past week. During rains, the pothole fills with water and becomes invisible. Urgent repair needed before a fatal accident occurs.',
    'en'::supported_language,
    'Tamil Nadu',
    'Chennai',
    'Teynampet, Anna Salai',
    '600018',
    13.0418,
    80.2467,
    'in_progress'::complaint_status,
    'high'::complaint_priority,
    82.5,
    15
FROM users u WHERE u.name = 'Rajesh Kumar';

INSERT INTO complaints (user_id, category, subcategory, subject, description, original_language, state, district, locality, pincode, latitude, longitude, status, priority, ai_priority_score, upvote_count)
SELECT
    u.id,
    'water_supply'::complaint_category,
    'no_water',
    'No water supply for 5 days in Vadapalani area',
    'Our entire street in Vadapalani has not received metro water supply for the past 5 days. Over 50 families are affected. We are forced to buy water from private tankers at ₹1,500 per load. The local corporation office has not responded to our calls. Children and elderly are suffering the most.',
    'ta'::supported_language,
    'Tamil Nadu',
    'Chennai',
    'Vadapalani',
    '600026',
    13.0524,
    80.2121,
    'escalated'::complaint_status,
    'critical'::complaint_priority,
    95.0,
    42
FROM users u WHERE u.name = 'Priya Lakshmi';

INSERT INTO complaints (user_id, category, subcategory, subject, description, original_language, state, district, locality, pincode, latitude, longitude, status, priority, ai_priority_score, upvote_count)
SELECT
    u.id,
    'garbage'::complaint_category,
    'irregular_collection',
    'Garbage not collected for 10 days in Koramangala 4th Block',
    'The BBMP garbage collection truck has not visited our area in Koramangala 4th Block for over 10 days. Garbage is piling up on the streets and at collection points. The stench is unbearable and there are stray dogs scattering waste everywhere. Mosquito breeding has increased. Multiple calls to BBMP helpline 080-22975803 have gone unanswered.',
    'en'::supported_language,
    'Karnataka',
    'Bengaluru Urban',
    'Koramangala 4th Block',
    '560034',
    12.9352,
    77.6245,
    'submitted'::complaint_status,
    'high'::complaint_priority,
    78.0,
    28
FROM users u WHERE u.name = 'Mohammed Irfan';

INSERT INTO complaints (user_id, category, subcategory, subject, description, original_language, state, district, locality, pincode, latitude, longitude, status, priority, ai_priority_score, upvote_count)
SELECT
    u.id,
    'streetlights'::complaint_category,
    'not_working',
    'Street lights not working on Kamaraj Road for 2 months',
    'All 8 street lights on Kamaraj Road between Periyar Bus Stand and Meenakshi Temple have been non-functional for over 2 months. The area becomes completely dark after 6 PM making it dangerous for women and children. Two chain-snatching incidents were reported last week. Despite complaints to the corporation, no action has been taken.',
    'ta'::supported_language,
    'Tamil Nadu',
    'Madurai',
    'Kamaraj Road, Near Periyar Bus Stand',
    '625001',
    9.9195,
    78.1194,
    'acknowledged'::complaint_status,
    'high'::complaint_priority,
    85.0,
    19
FROM users u WHERE u.name = 'Kavitha Devi';

INSERT INTO complaints (user_id, category, subcategory, subject, description, original_language, state, district, locality, pincode, latitude, longitude, status, priority, ai_priority_score, upvote_count)
SELECT
    u.id,
    'drainage'::complaint_category,
    'blocked_drain',
    'Blocked drainage causing waterlogging in Vijayanagar, Mysuru',
    'The main drainage on 3rd Cross, Vijayanagar, Mysuru has been blocked for the past 3 weeks. Sewage water is overflowing onto the road and entering nearby houses. The situation worsens during rain. Children in the area have developed skin infections. The smell has made it impossible to keep windows open. We need immediate desilting of the drain.',
    'kn'::supported_language,
    'Karnataka',
    'Mysuru',
    'Vijayanagar 3rd Cross',
    '570017',
    12.3051,
    76.6551,
    'in_progress'::complaint_status,
    'critical'::complaint_priority,
    91.0,
    35
FROM users u WHERE u.name = 'Suresh Gowda';

INSERT INTO complaints (user_id, category, subcategory, subject, description, original_language, state, district, locality, pincode, latitude, longitude, status, priority, ai_priority_score, upvote_count)
SELECT
    u.id,
    'ration_shop'::complaint_category,
    'short_supply',
    'Ration shop giving less rice than entitled quantity',
    'The fair price shop number 234 at South Masi Street, Thanjavur is consistently giving only 3 kg rice per person instead of the entitled 5 kg. The shopkeeper claims supply shortage but we suspect diversion. This has been happening for the last 3 months. Many elderly people in our area depend on ration rice as their primary food source.',
    'ta'::supported_language,
    'Tamil Nadu',
    'Thanjavur',
    'South Masi Street',
    '613001',
    10.7905,
    79.1378,
    'submitted'::complaint_status,
    'medium'::complaint_priority,
    65.0,
    8
FROM users u WHERE u.name = 'Lakshmi Narayanan';

INSERT INTO complaints (user_id, category, subcategory, subject, description, original_language, state, district, locality, pincode, latitude, longitude, status, priority, ai_priority_score, upvote_count)
SELECT
    u.id,
    'public_transport'::complaint_category,
    'overcrowding',
    'BMTC Bus Route 500D severely overcrowded during peak hours',
    'The BMTC bus route 500D from Majestic to Electronic City is dangerously overcrowded during morning (8-10 AM) and evening (6-8 PM) hours. Passengers are hanging from doors and footboards. Women and elderly struggle to board. The frequency should be increased from 20 minutes to at least every 10 minutes during peak hours.',
    'en'::supported_language,
    'Karnataka',
    'Bengaluru Urban',
    'Majestic Bus Station',
    '560009',
    12.9770,
    77.5726,
    'acknowledged'::complaint_status,
    'medium'::complaint_priority,
    58.0,
    22
FROM users u WHERE u.name = 'Deepa Krishnan';

INSERT INTO complaints (user_id, category, subcategory, subject, description, original_language, state, district, locality, pincode, latitude, longitude, status, priority, ai_priority_score, upvote_count)
SELECT
    u.id,
    'electricity'::complaint_category,
    'frequent_outages',
    'Daily 4-5 hour power cuts in Dharwad industrial area',
    'Our shop and the entire Jubilee Circle commercial area in Dharwad is experiencing daily power cuts of 4-5 hours, usually between 10 AM to 3 PM. This is peak business hours and causing huge financial losses. My refrigeration unit for the shop has been damaged twice due to voltage fluctuations. The transformer in our area needs replacement as it is overloaded.',
    'kn'::supported_language,
    'Karnataka',
    'Dharwad',
    'Jubilee Circle Commercial Area',
    '580001',
    15.4589,
    75.0078,
    'in_progress'::complaint_status,
    'high'::complaint_priority,
    76.0,
    14
FROM users u WHERE u.name = 'Venkatesh Murthy';

-- ============================================================================
-- SAMPLE COMPLAINT UPDATES
-- ============================================================================

INSERT INTO complaint_updates (complaint_id, old_status, new_status, comment, is_public)
SELECT c.id, 'submitted', 'acknowledged', 'Your complaint has been received and forwarded to the Highways Department. A site inspection is scheduled within 48 hours.', TRUE
FROM complaints c WHERE c.subject LIKE '%pothole on Anna Salai%';

INSERT INTO complaint_updates (complaint_id, old_status, new_status, comment, is_public)
SELECT c.id, 'acknowledged', 'in_progress', 'Site inspection completed. Work order issued to contractor for pothole repair. Expected completion within 5 working days.', TRUE
FROM complaints c WHERE c.subject LIKE '%pothole on Anna Salai%';

INSERT INTO complaint_updates (complaint_id, old_status, new_status, comment, is_public)
SELECT c.id, 'submitted', 'acknowledged', 'Complaint registered with Metro Water. Emergency tanker service being arranged.', TRUE
FROM complaints c WHERE c.subject LIKE '%No water supply for 5 days%';

INSERT INTO complaint_updates (complaint_id, old_status, new_status, comment, is_public)
SELECT c.id, 'acknowledged', 'escalated', 'Issue escalated to Superintending Engineer, Metro Water. Pipeline repair crew dispatched. Water supply expected to resume within 24 hours.', TRUE
FROM complaints c WHERE c.subject LIKE '%No water supply for 5 days%';

-- ============================================================================
-- SAMPLE HOTSPOTS
-- ============================================================================

INSERT INTO hotspots (category, state, district, locality, center_latitude, center_longitude, radius_meters, complaint_count, severity_score, first_reported_at, last_reported_at, is_active, metadata) VALUES
('roads', 'Tamil Nadu', 'Chennai', 'T. Nagar - Anna Salai Corridor', 13.0418, 80.2467, 800, 47, 78.5, '2026-01-15 10:00:00+05:30', '2026-06-14 16:30:00+05:30', TRUE, '{"avg_resolution_days": 12, "recurring": true, "affected_population": 25000}'),
('water_supply', 'Tamil Nadu', 'Chennai', 'Vadapalani - Ashok Nagar Belt', 13.0524, 80.2121, 1200, 83, 92.0, '2026-03-01 08:00:00+05:30', '2026-06-15 09:00:00+05:30', TRUE, '{"avg_resolution_days": 5, "recurring": true, "affected_population": 50000}'),
('garbage', 'Karnataka', 'Bengaluru Urban', 'Koramangala - HSR Layout', 12.9352, 77.6245, 1500, 62, 71.0, '2026-02-10 07:00:00+05:30', '2026-06-13 11:00:00+05:30', TRUE, '{"avg_resolution_days": 8, "recurring": true, "affected_population": 35000}'),
('drainage', 'Karnataka', 'Mysuru', 'Vijayanagar - Jayalakshmipuram', 12.3051, 76.6551, 600, 29, 85.0, '2026-04-01 09:00:00+05:30', '2026-06-12 14:00:00+05:30', TRUE, '{"avg_resolution_days": 15, "recurring": true, "affected_population": 15000}'),
('streetlights', 'Tamil Nadu', 'Madurai', 'Kamaraj Road - South Gate Area', 9.9195, 78.1194, 500, 18, 67.0, '2026-04-20 18:00:00+05:30', '2026-06-10 20:00:00+05:30', TRUE, '{"avg_resolution_days": 20, "recurring": false, "affected_population": 8000}');
