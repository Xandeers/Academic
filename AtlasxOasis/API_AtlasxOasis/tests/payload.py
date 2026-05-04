general_customer_payload = {
    "firstname": "jean",
    "lastname": "pierre",
    "username": "polnareff",
    "email": "test_customer@email.com",
    "description": "test description",
    "auth_type": "password",  # REQUIS PAR TON SCHÉMA
    "token": "valid-token-123" # REQUIS PAR TON SCHÉMA
}

general_organizer_payload = {
    "username": "test_organizer",
    "email": "test_organizer@email.com",
    "siret": "string",
    "description": "organizer test",
    "auth_type": "password",
    "token": "valid-token-321"
}

general_event_payload = {
    "name": "Test Event",
    "start_date": "2026-01-01T10:00:00",
    "end_date": "2026-01-01T12:00:00",
    "created_date": "2026-01-01T09:00:00",
    "event_status": "published",
    "max_capacity": 100,
    "description": "Test description",
    "metadata": {}
}

general_category_payload = {
    "label" : "testCategory"
}

general_location_payload = {
  "max_capacity": 0,
  "name": "string",
  "address": "string",
  "city": "string",
  "postal_code": "string",
  "longitude": 0,
  "latitude": 0,
  "accessibility": True,
  "nearby_transport": "string"
}

general_media_payload = {
  "label": "test_media",
  "description": "media pour les test",
  "format_media": "jpeg",
  "url": "test_url",
  "usage_media": "test",
  "upload_date": "2026-04-28T14:13:49.055Z",
  "sharing_status": "private",
}

general_ticket_type_payload = {}

general_promotion_payload = {
  "id_promotion_type": 1,
  "start_date": "2026-04-28T14:43:36.766Z",
  "end_date": "2026-04-28T14:43:36.766Z",
  "status_promotion": "string",
  "type_promotion": "string",
  "description": "string"
}