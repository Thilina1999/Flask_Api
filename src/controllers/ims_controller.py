from flask import request, jsonify
import uuid
from datetime import datetime
from ... import db
from ..models.ims_model import InventoryHistory
from flask import request, jsonify

def list_all_history_controller():
    inventoryHistories = InventoryHistory.query.all()
    response = []
    for inventoryHistory in inventoryHistories: response.append(inventoryHistory.to_dict())
    return jsonify(response)

def create_inventory_history():
    """Endpoint to create a new InventoryHistory record."""
    
    # Parse JSON data from request
    request_data = request.get_json()

    # Extract values from the JSON payload
    assy_part_number = request_data.get('assy_part_number')
    subassy_product_number = request_data.get('subassy_product_number')
    manufacturer = request_data.get('manufacturer')
    shipping_classification = request_data.get('shipping_classification')
    airtightness_inspection = request_data.get('airtightness_inspection')
    scu = request_data.get('scu')
    water_vapor_test = request_data.get('water_vapor_test')
    characteristic_inspection = request_data.get('characteristic_inspection')
    char_inspection_fractional_items = request_data.get('char_inspection_fractional_items')
    accessor = request_data.get('accessor')
    fa = request_data.get('fa')
    fa_fractional_items = request_data.get('fa_fractional_items')
    visual_inspection = request_data.get('visual_inspection')

    # Validate required fields
    required_fields = [
        'assy_part_number', 'subassy_product_number', 'manufacturer', 'shipping_classification',
        'airtightness_inspection', 'scu', 'water_vapor_test', 'characteristic_inspection',
        'char_inspection_fractional_items', 'accessor', 'fa', 'fa_fractional_items', 'visual_inspection'
    ]
    
    missing_fields = [field for field in required_fields if request_data.get(field) is None]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Create new InventoryHistory record
    new_inventory_history = InventoryHistory(
        assy_part_number=assy_part_number,
        subassy_product_number=subassy_product_number,
        manufacturer=manufacturer,
        shipping_classification=shipping_classification,
        airtightness_inspection=airtightness_inspection,
        scu=scu,
        water_vapor_test=water_vapor_test,
        characteristic_inspection=characteristic_inspection,
        char_inspection_fractional_items=char_inspection_fractional_items,
        accessor=accessor,
        fa=fa,
        fa_fractional_items=fa_fractional_items,
        visual_inspection=visual_inspection,
        update_date_time=datetime.now()  # Set current timestamp
    )

    # Add and commit to database
    db.session.add(new_inventory_history)
    db.session.commit()

    # Return response
    return jsonify(new_inventory_history.to_dict()), 201  # 201 Created