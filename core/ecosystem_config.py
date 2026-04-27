# core/ecosystem_config.py

# AQUA-CYCLE ROLES SYSTEM
AQUA_ROLES = {
    # 🧬 1. PRE-PRODUCTION
    "broodstock": {"name": "Genetics & Broodstock", "icon": "🧬", "category": "Pre-Production"},
    "hatchery": {"name": "Hatchery", "icon": "🏢", "category": "Production"},
    
    # 🌱 2. INPUT SUPPLY
    "feed_supplier": {"name": "Feed Supplier", "icon": "🍽️", "category": "Supply"},
    "equipment": {"name": "Equipment & Medicine", "icon": "⚙️", "category": "Supply"},
    
    # 🧠 3. FARMING / GROWTH
    "farmer": {"name": "Farmer", "icon": "👨‍🌾", "category": "Production"},
    "lab_tech": {"name": "Lab Technician", "icon": "🧪", "category": "Support"},
    "consultant": {"name": "Aqua Consultant / IoT", "icon": "👨‍🔬", "category": "Support"},
    
    # 🚜 4. HARVEST STAGE
    "harvest_contractor": {"name": "Harvest Contractor", "icon": "🚜", "category": "Harvest"},
    "cold_storage": {"name": "Cold Storage", "icon": "❄️", "category": "Storage"},
    
    # 🚚 5. LOGISTICS
    "transport": {"name": "Cold Chain Transport", "icon": "🚛", "category": "Logistics"},
    
    # 🏭 6. PROCESSING
    "processing_plant": {"name": "Processing Plant", "icon": "🏭", "category": "Processing"},
    "certifier": {"name": "Quality Certification", "icon": "🧾", "category": "Regulation"},
    
    # 🌍 7. MARKET / SELLING
    "buyer": {"name": "Wholesale Buyer", "icon": "🤝", "category": "Market"},
    "exporter": {"name": "Exporter", "icon": "🚢", "category": "Market"},
    "retailer": {"name": "Retailer / HoReCa", "icon": "🛍️", "category": "Market"},
    
    # 🏦 8. FINANCIAL & SUPPORT
    "bank": {"name": "Bank & Insurance", "icon": "🏦", "category": "Financial"},
    
    # ⚖️ 9. REGULATION & TRUST
    "regulator": {"name": "Regulatory Authority", "icon": "📜", "category": "Regulation"},
    
    # ⚡ SYSTEM
    "admin": {"name": "System Admin", "icon": "⚡", "category": "System"}
}

# AQUA-CYCLE CONNECTIVITY GRAPH (Who connects with whom)
AQUACYCLE_CONNECTIONS = {
    "broodstock": ["hatchery", "regulator"],
    "hatchery": ["broodstock", "farmer", "lab_tech", "transport", "regulator"],
    "feed_supplier": ["farmer", "transport"],
    "equipment": ["farmer", "hatchery", "processing_plant"],
    "farmer": ["hatchery", "feed_supplier", "equipment", "lab_tech", "consultant", "harvest_contractor", "transport", "buyer", "bank", "regulator"],
    "lab_tech": ["hatchery", "farmer", "processing_plant", "certifier"],
    "consultant": ["farmer", "bank"],
    "harvest_contractor": ["farmer", "transport", "processing_plant", "cold_storage"],
    "cold_storage": ["harvest_contractor", "transport", "processing_plant", "exporter"],
    "transport": ["hatchery", "feed_supplier", "farmer", "harvest_contractor", "cold_storage", "processing_plant", "buyer", "exporter", "retailer"],
    "processing_plant": ["transport", "cold_storage", "certifier", "buyer", "exporter"],
    "certifier": ["lab_tech", "processing_plant", "exporter", "regulator"],
    "buyer": ["farmer", "processing_plant", "transport", "retailer", "bank"],
    "exporter": ["processing_plant", "cold_storage", "transport", "certifier", "bank", "regulator"],
    "retailer": ["buyer", "transport", "regulator"],
    "bank": ["farmer", "buyer", "exporter", "regulator"],
    "regulator": ["broodstock", "hatchery", "farmer", "certifier", "exporter", "retailer", "bank", "admin"],
    "admin": list(AQUA_ROLES.keys())
}

AQUA_ROLE_ACTIONS = {
    "hatchery": [
        {"id": "register_hatchery", "name": "Register Hatchery", "icon": "🏢", "desc": "Setup new hatchery facility"},
        {"id": "create_seed_batches", "name": "Create Seed Batches", "icon": "🧬", "desc": "Initialize PL/Fingerling batches"},
        {"id": "upload_health_cert", "name": "Health Certificates", "icon": "📜", "desc": "Upload seed health verification"},
        {"id": "list_for_sale", "name": "List Seed For Sale", "icon": "💰", "desc": "Push stock to the marketplace"},
        {"id": "accept_orders", "name": "Accept Farmer Orders", "icon": "🛒", "desc": "Process incoming seed requests"},
        {"id": "track_deliveries", "name": "Track Deliveries", "icon": "🚛", "desc": "Monitor outbound shipments"}
    ],
    "farmer": [
        {"id": "register_farm_ponds", "name": "Register Ponds", "icon": "🚜", "desc": "Setup farm and pond units"},
        {"id": "buy_seed", "name": "Buy Seed", "icon": "🛒", "desc": "Order PL/Fingerlings from hatcheries"},
        {"id": "record_stocking", "name": "Pond Stocking", "icon": "🐟", "desc": "Log initial stocking density"},
        {"id": "track_feed_usage", "name": "Feed Usage", "icon": "🍽️", "desc": "Log daily feed consumption"},
        {"id": "water_test", "name": "Water Quality", "icon": "🧪", "desc": "Record pH, DO, Salinity readings"},
        {"id": "report_disease", "name": "Report Disease", "icon": "🚑", "desc": "Alert experts about livestock issues"},
        {"id": "schedule_harvest", "name": "Schedule Harvest", "icon": "⚖️", "desc": "Coordinate with harvest teams"},
        {"id": "list_harvest_sale", "name": "List for Sale", "icon": "💰", "desc": "Push stock to the trade matrix"}
    ],
    "feed_supplier": [
        {"id": "list_feed_products", "name": "List Feed Products", "icon": "📦", "desc": "Market your feed inventory to farmers"},
        {"id": "update_stock", "name": "Update Stock", "icon": "🔄", "desc": "Synchronize available feed inventory"},
        {"id": "receive_orders", "name": "Receive Farmer Orders", "icon": "✅", "desc": "Approve and manage feed purchase orders"},
        {"id": "track_deliveries", "name": "Track Deliveries", "icon": "🚛", "desc": "Monitor active distribution routes"}
    ],
    "lab_tech": [
        {"id": "receive_samples", "name": "Receive Samples", "icon": "🧪", "desc": "Log incoming water/seed samples"},
        {"id": "record_results", "name": "Record Test Results", "icon": "📝", "desc": "Input lab analysis parameters"},
        {"id": "upload_reports", "name": "Upload Reports", "icon": "📤", "desc": "Publish official digital lab reports"},
        {"id": "send_alerts", "name": "Send Alerts", "icon": "🔔", "desc": "Notify farmers of critical water issues"}
    ],
    "harvest_contractor": [
        {"id": "receive_harvest_requests", "name": "Harvest Requests", "icon": "🚜", "desc": "Manage farmer booking for harvest"},
        {"id": "schedule_teams", "name": "Schedule Teams", "icon": "📅", "desc": "Assign labor and equipment to farms"},
        {"id": "confirm_completion", "name": "Confirm Harvest", "icon": "✅", "desc": "Verify completion of harvest tasks"},
        {"id": "record_quantity", "name": "Record Quantity", "icon": "⚖️", "desc": "Log final harvested weight and counts"}
    ],
    "transport": [
        {"id": "accept_transport", "name": "Transport Requests", "icon": "🚚", "desc": "Review and accept shipment jobs"},
        {"id": "track_shipment", "name": "Track Shipment", "icon": "📍", "desc": "Real-time updates for active cargo"},
        {"id": "update_delivery_status", "name": "Update Status", "icon": "🔄", "desc": "Mark shipments as picked-up or delivered"}
    ],
    "processing_plant": [
        {"id": "receive_harvest", "name": "Receive Harvest", "icon": "🚜", "desc": "Log arrival of raw materials at plant"},
        {"id": "record_batch", "name": "Record Processing", "icon": "🏭", "desc": "Start processing and batch creation"},
        {"id": "grade_seafood", "name": "Grade Seafood", "icon": "📏", "desc": "Assign quality and size grades"},
        {"id": "manage_packaging", "name": "Packaging", "icon": "📦", "desc": "Verify final packaging and labeling"},
        {"id": "send_to_buyers", "name": "Ship to Buyers", "icon": "🚢", "desc": "Initiate export or local sales logistics"}
    ],
    "buyer": [
        {"id": "view_harvest_lots", "name": "Browse Harvest", "icon": "🦐", "desc": "View available fish and shrimp lots"},
        {"id": "place_orders", "name": "Purchase Order", "icon": "💰", "desc": "Buy stock directly from farms/plants"},
        {"id": "track_deliveries", "name": "Track Deliveries", "icon": "🚛", "desc": "Monitor arrival of purchased lots"},
        {"id": "make_payments", "name": "Payments", "icon": "💳", "desc": "Process digital payments for goods"}
    ],
    "exporter": [
        {"id": "view_bulk_availability", "name": "Bulk Availability", "icon": "🚢", "desc": "Discover large-scale export lots"},
        {"id": "purchase_stock", "name": "International Purchase", "icon": "🌎", "desc": "Execute bulk purchase agreements"},
        {"id": "upload_docs", "name": "Export Docs", "icon": "📂", "desc": "Manage customs and shipping paperwork"},
        {"id": "track_shipments", "name": "Track Global Shipments", "icon": "📍", "desc": "Monitor international logistics status"}
    ],
    "admin": [
        {"id": "manage_users", "name": "Manage Users", "icon": "👥", "desc": "Control account access and roles"},
        {"id": "approve_regs", "name": "Approve Regs", "icon": "✅", "desc": "Validate new ecosystem participants"},
        {"id": "monitor_transactions", "name": "Monitor Ledger", "icon": "📊", "desc": "Audit all financial and trade data"},
        {"id": "handle_disputes", "name": "Support/Disputes", "icon": "⚖️", "desc": "Resolve ecosystem participant conflicts"},
        {"id": "view_analytics", "name": "Global Analytics", "icon": "📈", "desc": "Access high-level system intelligence"}
    ],
    "broodstock": [
        {"id": "register_genetics", "name": "Register Genetics", "icon": "🧬", "desc": "Log SPF/SPR breeding lines"},
        {"id": "supply_hatcheries", "name": "Supply Hatcheries", "icon": "🚛", "desc": "Send certified broodstock to hatcheries"}
    ],
    "equipment": [
        {"id": "list_products", "name": "List Products", "icon": "⚙️", "desc": "Market aerators, pumps & medicine"},
        {"id": "manage_orders", "name": "Manage Orders", "icon": "📦", "desc": "Fulfill farmer equipment orders"}
    ],
    "consultant": [
        {"id": "view_farmer_data", "name": "View Farm Data", "icon": "📊", "desc": "Analyze IoT and Lab data for farmers"},
        {"id": "provide_advisory", "name": "Provide Advisory", "icon": "👨‍🔬", "desc": "Send actionable recommendations to farms"}
    ],
    "cold_storage": [
        {"id": "log_inventory", "name": "Log Inventory", "icon": "❄️", "desc": "Record incoming harvested batches"},
        {"id": "monitor_temp", "name": "Monitor Temp", "icon": "🌡️", "desc": "Track real-time temperature logs"}
    ],
    "certifier": [
        {"id": "inspect_batches", "name": "Inspect Batches", "icon": "🔍", "desc": "Conduct food safety & quality checks"},
        {"id": "issue_certificates", "name": "Issue Certificates", "icon": "🧾", "desc": "Generate export-ready quality certs"}
    ],
    "retailer": [
        {"id": "browse_market", "name": "Browse Market", "icon": "🛒", "desc": "Find certified local/wholesale stock"},
        {"id": "place_orders", "name": "Place Orders", "icon": "🛍️", "desc": "Procure seafood for HoReCa or retail"}
    ],
    "bank": [
        {"id": "review_loans", "name": "Review Loans", "icon": "💸", "desc": "Analyze AI-driven loan eligibility for farms"},
        {"id": "issue_insurance", "name": "Issue Insurance", "icon": "🛡️", "desc": "Approve crop insurance based on health data"}
    ],
    "regulator": [
        {"id": "audit_system", "name": "Audit System", "icon": "📜", "desc": "Check ecosystem compliance & sustainability"},
        {"id": "trace_batch", "name": "Traceability", "icon": "🔍", "desc": "Trace any batch from seed to plate"}
    ]
}

# Legacy Role Mapping (for backward compatibility)
ROLE_MAP = {
    "hatchery": "hatchery",
    "business": "feed_supplier",
    "expert": "lab_tech"
}
