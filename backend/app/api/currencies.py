from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(prefix="/api/currencies", tags=["currencies"])

CURRENCY_META = {
    "BRL": {"symbol": "R$", "name": "Real Brasileiro"},
    "USD": {"symbol": "$", "name": "US Dollar"},
    "EUR": {"symbol": "€", "name": "Euro"},
    "GBP": {"symbol": "£", "name": "British Pound"},
    "JPY": {"symbol": "¥", "name": "Japanese Yen"},
    "CAD": {"symbol": "C$", "name": "Canadian Dollar"},
    "AUD": {"symbol": "A$", "name": "Australian Dollar"},
    "CHF": {"symbol": "Fr", "name": "Swiss Franc"},
    "CNY": {"symbol": "¥", "name": "Chinese Yuan"},
    "ARS": {"symbol": "$", "name": "Peso Argentino"},
    "MXN": {"symbol": "$", "name": "Peso Mexicano"},
    "CLP": {"symbol": "$", "name": "Peso Chileno"},
    "COP": {"symbol": "$", "name": "Peso Colombiano"},
    "PEN": {"symbol": "S/", "name": "Sol Peruano"},
    "UYU": {"symbol": "$U", "name": "Peso Uruguayo"},
}


@router.get("")
async def list_currencies():
    """Return the list of supported currencies configured for this instance."""
    settings = get_settings()
    codes = [c.strip() for c in settings.supported_currencies.split(",") if c.strip()]

    currencies = []
    for code in codes:
        meta = CURRENCY_META.get(code, {})
        currencies.append({
            "code": code,
            "symbol": meta.get("symbol", code),
            "name": meta.get("name", code),
        })

    return currencies
