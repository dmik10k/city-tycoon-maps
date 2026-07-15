# Company artwork (CDN)

This directory is published through jsDelivr. Keep one **WebP** image per company
here, named exactly `<companyId>.webp`.

These render on the company card when a player opens a building slot.

## How it works

- The game advertises every canonical catalogue id through `/api/game/categories`.
- Run `npm test` from this repository before publishing so missing or invalid files
  are caught before the game requests them.
- Push the changed file to `main`; jsDelivr serves it from this repository.

## Format

- Format: **.webp** (lowercase `.webp` extension).
- Rendered at width 100% × **80px tall**, `object-fit: cover` → use ~**2:1** art,
  e.g. **320×160** (or 640×320 @2x). Larger is fine; it is cropped to fit.

## Required filenames (193 companies)


### aerospace

- `aerospace_components.webp`  — Aerospace Components
- `aircraft_maintenance.webp`  — Aircraft Maintenance
- `aircraft_manufacturer.webp`  — Aircraft Manufacturer
- `avionics_firm.webp`  — Avionics Firm
- `defence_contractor.webp`  — Defence Contractor
- `defence_systems.webp`  — Defence Systems
- `drone_company.webp`  — Drone Company
- `flight_training_centre.webp`  — Flight Training Centre
- `galactic_industries.webp`  — Galactic Industries
- `helicopter_company.webp`  — Helicopter Company
- `interplanetary_corp.webp`  — Interplanetary Corp
- `satellite_services.webp`  — Satellite Services
- `space_launch_services.webp`  — Space Launch Services
- `space_station_operations.webp`  — Space Station Operations

### agriculture

- `agro_industrial_complex.webp`  — Agro-Industrial Complex
- `coffee_roastery.webp`  — Coffee Roastery
- `creamery.webp`  — Creamery
- `crop_farm.webp`  — Crop Farm
- `dairy_farm.webp`  — Dairy Farm
- `fish_processing.webp`  — Fish Processing Plant
- `grain_mill.webp`  — Grain Mill
- `greenhouse_complex.webp`  — Greenhouse Complex
- `livestock_farm.webp`  — Livestock Farm
- `market_garden.webp`  — Market Garden
- `orchard.webp`  — Orchard
- `plantation.webp`  — Plantation
- `poultry_farm.webp`  — Poultry Farm
- `timber_yard.webp`  — Timber Yard
- `vineyard.webp`  — Vineyard
- `winery.webp`  — Winery

### civic

- `city_hall.webp`  — City Hall
- `courthouse.webp`  — Courthouse
- `dmv.webp`  — DMV
- `embassy.webp`  — Embassy
- `fire_station.webp`  — Fire Station
- `library.webp`  — Library
- `metro_authority.webp`  — Metro Authority
- `museum.webp`  — Museum
- `police_station.webp`  — Police Station
- `post_office.webp`  — Post Office
- `tax_office.webp`  — Tax Office
- `town_hall.webp`  — Town Hall

### commercial

- `bakery.webp`  — Bakery
- `bank_branch.webp`  — Bank Branch
- `barber_shop.webp`  — Barber Shop
- `book_store.webp`  — Book Store
- `butcher.webp`  — Butcher
- `cafe.webp`  — Café
- `clothing_boutique.webp`  — Clothing Boutique
- `deli.webp`  — Deli
- `department_store.webp`  — Department Store
- `flower_shop.webp`  — Flower Shop
- `furniture_store.webp`  — Furniture Store
- `hardware_store.webp`  — Hardware Store
- `insurance_company.webp`  — Insurance Company
- `jeweler.webp`  — Jeweler
- `kebab_house.webp`  — Kebab House
- `luxury_showroom.webp`  — Luxury Showroom
- `pet_shop.webp`  — Pet Shop
- `pharmacy.webp`  — Pharmacy
- `pizza_parlour.webp`  — Pizza Parlour
- `restaurant.webp`  — Restaurant
- `supermarket.webp`  — Supermarket
- `sushi_place.webp`  — Sushi Place
- `tailor.webp`  — Tailor
- `tech_store.webp`  — Tech Store
- `wine_bar.webp`  — Wine Bar

### education

- `art_college.webp`  — Art College
- `business_school.webp`  — Business School
- `coding_bootcamp.webp`  — Coding Bootcamp
- `driving_school.webp`  — Driving School
- `engineering_college.webp`  — Engineering College
- `language_school.webp`  — Language School
- `medical_school.webp`  — Medical School
- `music_academy.webp`  — Music Academy
- `primary_school.webp`  — Primary School
- `research_institute.webp`  — Research Institute
- `secondary_school.webp`  — Secondary School
- `trade_school.webp`  — Trade School
- `tutoring_centre.webp`  — Tutoring Centre
- `university.webp`  — University

### entertainment

- `arcade.webp`  — Arcade
- `art_gallery.webp`  — Art Gallery
- `bowling_alley.webp`  — Bowling Alley
- `casino.webp`  — Casino
- `cinema.webp`  — Cinema
- `comedy_club.webp`  — Comedy Club
- `concert_arena.webp`  — Concert Arena
- `escape_room_complex.webp`  — Escape Room Complex
- `jazz_club.webp`  — Jazz Club
- `night_club.webp`  — Night Club
- `rooftop_bar.webp`  — Rooftop Bar
- `sports_bar.webp`  — Sports Bar
- `theatre.webp`  — Theatre
- `vr_centre.webp`  — VR Centre

### extraction

- `coal_mine.webp`  — Coal Mine
- `copper_mine.webp`  — Copper Mine
- `diamond_mine.webp`  — Diamond Mine
- `fishing_harbour.webp`  — Fishing Harbour
- `gold_mine.webp`  — Gold Mine
- `iron_ore_mine.webp`  — Iron Ore Mine
- `logging_camp.webp`  — Logging Camp
- `mine.webp`  — Mine
- `natural_gas_field.webp`  — Natural Gas Field
- `offshore_platform.webp`  — Offshore Platform
- `oil_well.webp`  — Oil Well
- `peat_bog.webp`  — Peat Bog
- `quarry.webp`  — Quarry
- `salt_mine.webp`  — Salt Mine
- `sand_pit.webp`  — Sand Pit
- `semiconductor_fab.webp`  — Semiconductor Fab

### healthcare

- `dental_clinic.webp`  — Dental Clinic
- `diagnostic_imaging_centre.webp`  — Diagnostic Imaging Centre
- `fertility_clinic.webp`  — Fertility Clinic
- `gp_surgery.webp`  — GP Surgery
- `medical_laboratory.webp`  — Medical Laboratory
- `mental_health_clinic.webp`  — Mental Health Clinic
- `optometry_clinic.webp`  — Optometry Clinic
- `pharmacy_clinic.webp`  — Pharmacy Clinic
- `physiotherapy_centre.webp`  — Physiotherapy Centre
- `private_hospital.webp`  — Private Hospital
- `rehabilitation_hospital.webp`  — Rehabilitation Hospital
- `research_hospital.webp`  — Research Hospital
- `specialist_clinic.webp`  — Specialist Clinic
- `urgent_care_centre.webp`  — Urgent Care Centre

### hotel

- `boutique_hotel.webp`  — Boutique Hotel
- `business_inn.webp`  — Business Inn
- `conference_centre_hotel.webp`  — Conference Centre Hotel
- `grand_hotel.webp`  — Grand Hotel
- `harbour_view.webp`  — Harbour View
- `metro_lodge.webp`  — Metro Lodge
- `plaza_inn.webp`  — Plaza Inn
- `resort_spa.webp`  — Resort & Spa
- `royal_suites.webp`  — Royal Suites
- `the_imperial.webp`  — The Imperial

### industrial

- `automobile_factory.webp`  — Automobile Factory
- `electronics_factory.webp`  — Electronics Factory
- `food_processing_plant.webp`  — Food Processing Plant
- `logistics_hub.webp`  — Logistics Hub
- `meat_processing.webp`  — Meat Processing Plant
- `oil_refinery.webp`  — Oil Refinery
- `power_plant.webp`  — Power Plant
- `print_shop.webp`  — Print Shop
- `recycling_centre.webp`  — Recycling Centre
- `sawmill.webp`  — Sawmill
- `shipyard.webp`  — Shipyard
- `smelter.webp`  — Smelter
- `steel_mill.webp`  — Steel Mill
- `storage_depot.webp`  — Storage Depot
- `textile_mill.webp`  — Textile Mill
- `warehouse.webp`  — Warehouse

### office

- `accounting_firm.webp`  — Accounting Firm
- `architecture_studio.webp`  — Architecture Studio
- `consulting_firm.webp`  — Consulting Firm
- `corporate_headquarters.webp`  — Corporate Headquarters
- `coworking_space.webp`  — Coworking Space
- `insurance_hq.webp`  — Insurance HQ
- `investment_bank.webp`  — Investment Bank
- `law_firm.webp`  — Law Firm
- `marketing_agency.webp`  — Marketing Agency
- `media_company.webp`  — Media Company
- `pr_firm.webp`  — PR Firm
- `recruitment_agency.webp`  — Recruitment Agency
- `trading_floor.webp`  — Trading Floor
- `venture_capital.webp`  — Venture Capital Firm

### technology

- `ai_company.webp`  — AI Company
- `biotech_firm.webp`  — Biotech Firm
- `cloud_services.webp`  — Cloud Services
- `cybersecurity_firm.webp`  — Cybersecurity Firm
- `data_centre.webp`  — Data Centre
- `fintech_startup.webp`  — Fintech Startup
- `game_studio.webp`  — Game Studio
- `it_support_firm.webp`  — IT Support Firm
- `mobile_app_studio.webp`  — Mobile App Studio
- `robotics_company.webp`  — Robotics Company
- `software_company.webp`  — Software Company
- `space_tech_company.webp`  — Space Tech Company
- `tech_giant.webp`  — Tech Giant
- `web_agency.webp`  — Web Agency

### transport

- `airline_operations.webp`  — Airline Operations
- `bicycle_courier.webp`  — Bicycle Courier
- `bus_depot.webp`  — Bus Depot
- `cold_chain_logistics.webp`  — Cold Chain Logistics
- `courier_service.webp`  — Courier Service
- `freight_company.webp`  — Freight Company
- `fuel_distribution.webp`  — Fuel Distribution
- `international_airport.webp`  — International Airport
- `logistics_corporation.webp`  — Logistics Corporation
- `port_authority.webp`  — Port Authority
- `rail_freight_depot.webp`  — Rail Freight Depot
- `removal_company.webp`  — Removal Company
- `shipping_company.webp`  — Shipping Company
- `taxi_company.webp`  — Taxi Company
