
def get_item_by_id(items_list, item_id):
    return next((item for item in items_list if item["id"] == item_id), None)


def get_item_index_by_id(items_list, item_id):
    return next((i for i, item in enumerate(items_list) if item["id"] == item_id), None)
