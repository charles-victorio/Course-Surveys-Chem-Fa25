
[LAMP master mix](https://www.neb.com/en-us/products/m1800-warmstart-colorimetric-lamp-2x-master-mix-dna-rna) - colorimetric - $250
E coli nucleic acid sample
- K-12 cells for full pipeline and lysis validation in real matrix - Microkwik Vial
	- [live harmless cells](https://www.carolina.com/bacteria/escherichia-coli-living-k-12-strain-plate/155067.pr?l_155067&bvstate=pg%3A2%2Fct%3Ar) - $15
- Dangerous strain purified DNA for primer specificity and analytical sensitivity
	- [gBlock tube](https://www.idtdna.com/pages/products/genes-and-gene-fragments/double-stranded-dna-fragments/gblocks-gene-fragments) - $50
	- [pure DNA](https://www.atcc.org/products/43895D-5) - $400
- Together these are considered sufficient for a publishable, credible assay validation
- dangerous cells only needed to be official 
[molecular biology grade water](https://www.ibisci.com/products/molecular-biology-grade-water?variant=31245652656239) - $25
heater - eg [this sous vide heater](https://www.homedepot.com/p/Tayama-Black-Sous-Vide-Immersion-Cooker-ELE-01/300524078?source=shoppingads&locale=en-US&fp=ggl#see-more-details) - $50
container for sous vide heater
- check what volume works for the heater's minimum water depth, we only need 1-2L volume (higher is fine)

primers - ~$80 \* 2
- below are the primers to detect stx2a.  later, we may want to also detect uidA, stx1, or other strains of stx2
- primers for stx2a (from [this paper](https://journals.asm.org/doi/full/10.1128/aem.00880-25))
	- F3: CGCTTCAGGCAGATACAGAG = 20 bases
	- B3: CCCCCTGATGATGGCAATT = 19 bases
	- FIP: TTCGCCCCCAGTTCAGAGTGAGTCAGGCACTGTCTGAAACT = 42 bases
	- BIP: TGCTTCCGGAGTATCGGGGAGCAGTCCCCAGTATCGCTGA = 41 bases
	- LF: GCGTCATCGTATACACAGGAGC = 22 bases (plain sequence, no tags)
	- LB: GATGGTGTCAGAGTGGGGAGAA = 22 bases (plain sequence, no tags)
- buy [custom dna oligos](https://www.idtdna.com/pages/products/custom-dna-rna/dna-oligos/custom-dna-oligos)

Liquid Handling Consumables
- pipettes - $36 \* 2
	- P20 and P200
	- [4E's USA](https://www.4es-usa.com/products/precipette-single-channel-pipette)
- pipette filter tips
	- how many tips we'll need: estimating ~100 LAMP reactions / this project * ~5-10 tips / reaction = 500-1000 tips, for each of P20 and P200
	- must be compatible with pipette
	- [4E's USA](https://www.4es-usa.com/products/racked-filtered-pipettes-tips-for-2ul-1250ul-pipettes?variant=41164094341213) - guaranteed compatible
	- [Kashi Scientific](https://www.amazon.com/gp/aw/d/B09XYTPW28/) - maybe compatible (look online + order once to test), cheaper at higher volume
- microtubes - buy 500 1.5mL Eppendorf tubes, eg [amazon](https://www.amazon.com/Microcentrifuge-Sterilized-Plastic-Storage-Without/dp/B09FJFB6PM?crid=1UTJ3MYILTU3C&dib=eyJ2IjoiMSJ9.25BbtWQQzXQtns3cP_x49l18TcQF1RTcVfI3kBx_cDahUXq8oqCONfl4u8US2deR_3S-rYDlA2f-rkANsh1hgKlhjwQNec-CMMMeZIlUcO2rdZsE2FMQ31U3bW6CkZBNqnUWVSwwJsjtwNlsLwbCv7LYfQqY4nSKFcPl90Bhgmlcxwgkx1e7LdBDfbn8aZL_F4od7wj0UdDSruWj3qNzyIEK3oCLFS5Tw-0SuxnVugU.syRJhy6mheXrIEegPMFIRGo_BihYkAX_UbUZM5Bnkzk&dib_tag=se&keywords=1.5%2Bml%2Btubes&qid=1754093864&sprefix=1.5%2Bml%2Btubes%2Caps%2C165&sr=8-4&th=1&linkCode=sl1&tag=diybiotech-20&linkId=e912fd94576677716965757ff42cc1fa&language=en_US&ref_=as_li_ss_tl)
- pcr tubes or strips - buy 500, 0.2 mL thin-wall
- 3d printed tube racks

Lab consumables
- [x] nitrile gloves
- lab coats (I have 1)
- parafilm - sealing & covering
- markers and masking tape for labeling
- ice bucket + ice
- distilled water gallon jugs (for washing, not for reaction)
- alcohol wipes
- paper towels

Growing K-12 cells
- premade agar plates
- LB broth - for growing liquid cultures of K-12 before lysis. buy powder, make it and autoclave it
- plastic inoculation loops - transfer bacteria from culture to plates or broth
- pressure cooker
	- DIY autoclave to sterilize LB broth and dispose K-12
	- >= 6 qts, 15 PSI, 121 C, steams
	- or instant pot
- bleach
- 70% isopropyl alcohol, or 99% and dilute it

tools
- mini vortex mixer
- UV lamp - 254 nm, ozone free, >= 30W, timer
- Liquid waste container
	- small bottle that can handle bleach like https://www.amazon.com/United-Scientific-33309-Polypropylene-Capacity/dp/B00ES3PX6G
	- 500mL, fill 50mL with bleach. When done/full, wait 30 mins, add tap water if needed to dilute the bleach to 10%, pour bottle down the drain, rinse with tap water a few times. 
- 2 cleaning spray bottles
- shelf

Larger purchases
- 4 degrees C fridge or mini fridge
- manual defrost chest freezer that can reach -20 degrees C, eg [Home Depot](https://www.homedepot.com/p/COWSAR-Garage-Ready-20-67-in-1-8-cu-ft-Manual-Defrost-Chest-Freezer-with-Temperature-Alarm-Chest-Freezer-in-White-WSBG-D68100-WH/331875653?source=shoppingads&locale=en-US&fp=ggl)

Too expensive but only needed occasionally, either borrow or go without
- "**Spectrophotometer or OD measurement** — to measure bacterial culture density (OD600) so you know how many cells you're adding to your lysis experiments. A cheap visible light spectrophotometer that reads at 600 nm is sufficient, around $200-400. Alternatively some university core facilities will do this for you."
-  - ? microvolume spectrophotometer "to measure DNA cancentration when you recieve your ATCC genomic DNA and resuspend your gBlock. NanoDrop or equivalent"

maybe later
- DIY stainless steel test tube holder for autoclaving
- DIY fume hood (lots of videos online)
- DIY lyophilization (lots of videos online)



make info/wiki abt
- what genes we want to detect
- what different sample sources tell us (pure dna vs gblock vs k-12 cells)
- what primers will work
- diff types of detection methods (or at least the ones we are interested in)
- packaging methods of the live cells?

questions
- can we get any supplies from them
- do we have to talk with EHS?
- what are LA / municipality rules for bio/hazard waste disposal

# How to handle waste
Solid waste (pipette tips, tubes, gloves)
- put it into a bag, put the bag into an autoclave, put the bag into a regular garbage bag, throw it into the regular garbage
- we aren't using any sharps
- don't open tubes which have already undergone LAMP unless necessary. If necessary, do it far away from the pre-LAMP work area
Liquid waste (LAMP reaction stuff)
- ? put into liquid waste container with bleach, leave it in for 30 mins, pour down drain

---
also make photolithography shopping list
& notes/learn how to do it obv
