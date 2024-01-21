HEADER_SCHEMA = {
    "properties": {
        "LogoImg": {"type": "string"},
        "UsedGuid": {"type": "string"},
        "UserName": {"type": "string"}
    }
}

PRODUCTS_SCHEMA = {
    "properties": {
        "Id": {"type": "number"},
        "Name": {"type": "string"},
        "Description": {"type": "string"},
        "Quantity": {"type": "number"},
        "Unit": {"type": "string"},
        "Currency": {"type": "string"},
        "Price": {"type": "number"},
        "DiscountedPrice": {"type": "number"},
        "Images": {
            "FileName": {"type": "string"},
            "FileExtension": {"type": "string"},
            "Image": {"type": "string"},
        }
    }
}

DELETED_SCHEMA = {
    "properties": {
        "Name": {"type": "string"},
        "Description": {"type": "string"}
    }
}

BASKEDSUMMARY_SCHEMA = {
    "properties": {
        "TotalProducts": {"type": "number"},
        "Discount": {"type": "number"},
        "Total": {"type": "number"}
    }
}