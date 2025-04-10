from uuid import UUID
from ..core.logging import logger
from ..core.database import get_supabase_client

def create_inventory_item(org_id: UUID, data: dict):
    logger.debug(f"Creating inventory item in database for org_id: {org_id}")
    print(data)
    try:
        supabase = get_supabase_client()
        insert_result = supabase.table("inventory_items") \
            .insert({
                "org_id": str(org_id),
                **data,
            }) \
            .execute()
        logger.debug(f"Successfully created inventory item with ID: {insert_result.data[0].get('id')}")


        name = data["name"]
        fetch_result = supabase.table("inventory_items") \
            .select("*") \
            .eq("org_id", str(org_id)) \
            .eq("name", name) \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()
        logger.debug(f"Successfully created inventory item with ID: {fetch_result.data[0].get('id')}")
        return fetch_result.data[0]
    except Exception as e:
        logger.error(f"Failed to create inventory item: {str(e)}")
        raise

def get_inventory_items_by_org(org_id: UUID):
    logger.debug(f"Fetching inventory items for org_id: {org_id}")
    try:
        supabase = get_supabase_client()
        result = supabase.table("inventory_items").select("*").eq("org_id", str(org_id)).execute()
        logger.debug(f"Retrieved {len(result.data)} inventory items")
        return result.data
    except Exception as e:
        logger.error(f"Failed to fetch inventory items for org {org_id}: {str(e)}")
        raise

def update_inventory_item(item_id: UUID, updates: dict):
    logger.debug(f"Updating inventory item with ID: {item_id}")
    logger.debug(f"Update data: {updates}")
    try:
        supabase = get_supabase_client()
        result = supabase.table("inventory_items").update(updates).eq("id", str(item_id))
        logger.debug(f"Successfully updated inventory item {result}")

        # return the updated item
        updated_item = supabase.table("inventory_items").select("*").eq("id", str(item_id)).single().execute()
        logger.debug(f"Successfully updated inventory item {item_id}")
        return updated_item.data
    except Exception as e:
        logger.error(f"Failed to update inventory item {item_id}: {str(e)}")
        raise

def delete_inventory_item(item_id: UUID):
    logger.debug(f"Deleting inventory item with ID: {item_id}")
    try:
        supabase = get_supabase_client()
        supabase.table("inventory_items").delete().eq("id", str(item_id)).execute()
        logger.debug(f"Successfully deleted inventory item {item_id}")
    except Exception as e:
        logger.error(f"Failed to delete inventory item {item_id}: {str(e)}")
        raise

def get_inventory_item_by_id(item_id: UUID):
    logger.debug(f"Fetching inventory item with ID: {item_id}")
    try:
        supabase = get_supabase_client()
        result = supabase.table("inventory_items").select("*").eq("id", str(item_id)).single().execute()
        if result.data:
            logger.debug(f"Found inventory item {item_id}")
        else:
            logger.debug(f"Inventory item {item_id} not found")
        return result.data
    except Exception as e:
        logger.error(f"Error fetching inventory item {item_id}: {str(e)}")
        raise
