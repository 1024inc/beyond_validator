listing_ids_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "array",
    "items": {"type": "string", "minLength": 1},
    "uniqueItems": True,
}

listings_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "accountId": {"type": "string", "minLength": 1},
        "createdAt": {"type": "string", "format": "date-time", "minLength": 1},
        "updatedAt": {"type": "string", "format": "date-time", "minLength": 1},
        "title": {"type": "string", "minLength": 1},
        "bedrooms": {"type": "number"},
        "bathrooms": {"type": "number"},
        "minNights": {"type": "number"},
        # Needed to be able to handle empty strings
        "imageUrl": {"type": "string", "oneOf": [{"format": "uri"}, {"maxLength": 0}]},
        "images": {
            "type": "array",
            "items": {"type": "string", "format": "uri"},
        },
        "description": {"type": "string"},
        "isListed": {"type": "boolean"},
        "currency": {"type": "string", "minLength": 1},
        "checkinDays": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "sunday",
                    "monday",
                    "tuesday",
                    "wednesday",
                    "thursday",
                    "friday",
                    "saturday",
                ],
                "uniqueItems": True,
            },
        },
        "checkoutDays": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "sunday",
                    "monday",
                    "tuesday",
                    "wednesday",
                    "thursday",
                    "friday",
                    "saturday",
                ],
                "uniqueItems": True,
            },
        },
        "roomType": {"type": "string"},
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string", "minLength": 1},
                "city": {"type": "string", "minLength": 1},
                "state": {"type": "string"},
                "country": {"type": "string", "minLength": 1},
                "zipCode": {"type": "string", "minLength": 1},
                "latitude": {"type": "string", "minLength": 1},
                "longitude": {"type": "string", "minLength": 1},
            },
            "required": [
                "street",
                "city",
                "state",
                "country",
                "zipCode",
                "latitude",
                "longitude",
            ],
        },
    },
    "required": [
        "id",
        "accountId",
        "createdAt",
        "updatedAt",
        "title",
        "bedrooms",
        "bathrooms",
        "minNights",
        "description",
        "isListed",
        "currency",
        "checkinDays",
        "checkoutDays",
        "roomType",
        "address",
    ],
}

calendar_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "date": {"type": "string", "format": "date", "minLength": 1},
            "dailyPrice": {"type": "number"},
            "availability": {
                "type": "string",
                "enum": ["booked", "blocked", "available"],
                "minLength": 1,
            },
            "minNights": {"type": "integer"},
            "checkinDays": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [
                        "sunday",
                        "monday",
                        "tuesday",
                        "wednesday",
                        "thursday",
                        "friday",
                        "saturday",
                    ],
                    "uniqueItems": True,
                },
            },
            "checkoutDays": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [
                        "sunday",
                        "monday",
                        "tuesday",
                        "wednesday",
                        "thursday",
                        "friday",
                        "saturday",
                    ],
                    "uniqueItems": True,
                },
            },
        },
        "required": [
            "date",
            "dailyPrice",
            "availability",
            "minNights",
            "checkinDays",
            "checkoutDays",
        ],
    },
}
