from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import List
from ...crud import inventory
from ...schemas.inventory import InventoryItemCreate, InventoryItemResponse, InventoryItemUpdate
from ...core.auth import get_current_user
from ...core.logging import logger

router = APIRouter(prefix="/inventory", tags=["inventory"])

def validate_org_access(user, org_id: UUID):
    # TODO: Implement proper validation against user's organization
    # This is a simplified check assuming the user profile has an org_id field
    if user.get("org_id") != str(org_id):
        logger.warning(f"User {user.get('id')} attempted to access unauthorized org {org_id}")
        raise HTTPException(status_code=403, detail="Not authorized to access this organization's data")
    return True

@router.post("/", response_model=InventoryItemResponse)
def create_inventory_item(item: InventoryItemCreate, current_user=Depends(get_current_user)):
    org_id = current_user.org_id
    logger.info(f"Creating inventory item '{item.name}' in org {org_id} by user {current_user.id}")
    validate_org_access(current_user, org_id)
    result = inventory.create_inventory_item(org_id, item.dict(exclude={"org_id"}))
    logger.info(f"Inventory item created with ID: {result.get('id')}")
    return result

@router.get("/", response_model=List[InventoryItemResponse])
def get_inventory_items(current_user=Depends(get_current_user)):
    org_id = current_user.org_id
    logger.info(f"Fetching inventory items for org {org_id} by user {current_user.get('id')}")
    validate_org_access(current_user, org_id)
    items = inventory.get_inventory_items_by_org(org_id)
    logger.info(f"Retrieved {len(items)} inventory items for org {org_id}")
    return items

@router.put("/{item_id}", response_model=InventoryItemResponse)
def update_inventory_item(item_id: UUID, item: InventoryItemUpdate, current_user=Depends(get_current_user)):
    logger.info(f"Full update of inventory item {item_id} by user {current_user.id}")
    # Get the item first to check organization
    item_data = inventory.get_inventory_item_by_id(item_id)
    if not item_data:
        logger.warning(f"Item {item_id} not found for update")
        raise HTTPException(status_code=404, detail="Item not found")
    
    validate_org_access(current_user, UUID(item_data.get("org_id")))
    result = inventory.update_inventory_item(item_id, item.dict(exclude_unset=True))
    logger.info(f"Inventory item {item_id} successfully updated")
    return result

@router.patch("/{item_id}", response_model=InventoryItemResponse)
def update_item(item_id: UUID, update: InventoryItemUpdate, current_user=Depends(get_current_user)):
    logger.info(f"Partial update of inventory item {item_id} by user {current_user.get('id')}")
    # Get the item first to check organization
    item_data = inventory.get_inventory_item_by_id(item_id)
    if not item_data:
        logger.warning(f"Item {item_id} not found for patch update")
        raise HTTPException(status_code=404, detail="Item not found")
    
    validate_org_access(current_user, UUID(item_data.get("org_id")))
    result = inventory.update_inventory_item(item_id, update.dict(exclude_unset=True))
    logger.info(f"Inventory item {item_id} successfully patched")
    return result

@router.delete("/{item_id}")
def delete_item(item_id: UUID, current_user=Depends(get_current_user)):
    logger.info(f"Deleting inventory item {item_id} by user {current_user.get('id')}")
    # Get the item first to check organization
    item_data = inventory.get_inventory_item_by_id(item_id)
    if not item_data:
        logger.warning(f"Item {item_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Item not found")
    
    validate_org_access(current_user, UUID(item_data.get("org_id")))
    inventory.delete_inventory_item(item_id)
    logger.info(f"Inventory item {item_id} successfully deleted")
    return {"success": True}