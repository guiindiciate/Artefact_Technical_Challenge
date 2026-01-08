"""
External tools for the assistant.
"""
import requests
from langchain_core.tools import tool
from observability.context import mark_tool_used

# Calculator
@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression using a restricted local eval.

    Args:
        expression (str): Expression like "2+2", "10*5", "100/4".

    Returns:
        str: Computed result or an error message.
    """
    mark_tool_used("calculator")
    print("[TOOL] Using local CALCULATOR")
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Calculation error: {str(e)}"


# FX Converter (Frankfurter)
@tool
def fx_convert(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convert fiat currency using Frankfurter public API.

    Args:
        amount (float): Amount to convert.
        from_currency (str): Source currency code (e.g. "USD").
        to_currency (str): Target currency code (e.g. "BRL").

    Returns:
        str: Formatted conversion string or an error message.
    """
    mark_tool_used("fx")
    print("[TOOL] Using FX CONVERTER (Frankfurter API)")

    base = (from_currency or "").upper().strip()
    target = (to_currency or "").upper().strip()
    if amount <= 0:
        return "Amount must be greater than 0."
    if len(base) != 3 or len(target) != 3:
        return "Currency codes must be 3 letters (e.g., USD, BRL)."

    try:
        url = "https://api.frankfurter.app/latest"
        params = {"amount": amount, "from": base, "to": target}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        value = data.get("rates", {}).get(target)
        if value is None:
            return f"Could not convert from {base} to {target}."
        return f"{amount:.2f} {base} = {float(value):.2f} {target}"
    except requests.RequestException as e:
        return f"FX API request failed: {str(e)}"


# Crypto Converter (CoinGecko)
COIN_ID_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "ADA": "cardano",
    "DOGE": "dogecoin",
    "MATIC": "polygon",
}

def _coin_id(coin: str) -> str:
    c = (coin or "").strip()
    if not c:
        return ""
    return COIN_ID_MAP.get(c.upper(), c.lower())

@tool
def crypto_convert(coin: str, vs_currency: str, amount: float = 1.0) -> str:
    """
    Fetch crypto price and convert an amount into a target currency (CoinGecko).

    Args:
        coin (str): Symbol or CoinGecko id (e.g., "BTC" or "bitcoin").
        vs_currency (str): Currency code (e.g., "usd", "brl").
        amount (float): Amount of the crypto asset. Defaults to 1.0.

    Returns:
        str: Formatted conversion string or an error message.
    """
    mark_tool_used("crypto")
    print("[TOOL] Using CRYPTO CONVERTER (CoinGecko)")

    coin_id = _coin_id(coin)
    vs = (vs_currency or "").strip().lower()
    if not coin_id:
        return "Missing 'coin' (e.g., BTC, ETH)."
    if not vs or len(vs) < 3:
        return "Invalid 'vs_currency' (e.g., usd, brl)."
    if amount <= 0:
        return "Amount must be greater than 0."

    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": coin_id, "vs_currencies": vs}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        price = data.get(coin_id, {}).get(vs)
        if price is None:
            return f"Could not fetch price for '{coin}' in '{vs.upper()}'."

        converted = float(price) * float(amount)
        display = coin.strip().upper()
        return f"{amount:.6g} {display} ≈ {converted:.2f} {vs.upper()}"
    except requests.RequestException as e:
        return f"CoinGecko request failed: {str(e)}"
