import os
import httpx
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("Fakturownia")

# API Configuration
API_TOKEN = os.getenv("FAKTUROWNIA_API_TOKEN")
DOMAIN = os.getenv("FAKTUROWNIA_DOMAIN")

if not API_TOKEN or not DOMAIN:
    print("Warning: FAKTUROWNIA_API_TOKEN or FAKTUROWNIA_DOMAIN not set.")

BASE_URL = f"https://{DOMAIN}.fakturownia.pl"


async def make_request(
    method: str,
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
):
    """Helper to make authenticated requests to Fakturownia API."""
    actual_params: Dict[str, Any] = params.copy() if params else {}
    actual_params["api_token"] = API_TOKEN

    url = f"{BASE_URL}{endpoint}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        if method.upper() == "GET":
            response = await client.get(url, params=actual_params)
        elif method.upper() == "POST":
            response = await client.post(url, json=json, params=actual_params)
        elif method.upper() == "PUT":
            response = await client.put(url, json=json, params=actual_params)
        elif method.upper() == "PATCH":
            response = await client.patch(url, json=json, params=actual_params)
        elif method.upper() == "DELETE":
            response = await client.delete(url, params=actual_params)
        else:
            raise ValueError(f"Unsupported method: {method}")

        if response.is_error:
            error_data = response.text
            try:
                error_json = response.json()
                if "message" in error_json:
                    error_data = error_json["message"]
            except:
                pass
            return {
                "status": "error",
                "code": response.status_code,
                "details": error_data,
            }

        if response.status_code == 204:
            return {"status": "success", "message": "No content"}
        return response.json()


# --- Invoice Tools ---


@mcp.tool()
async def list_invoices(
    period: Optional[str] = None, page: int = 1, per_page: int = 50
) -> Dict[str, Any]:
    """
    Lists invoices from Fakturownia.
    :param period: Filters invoices by a specific time period (e.g., 'this_month', 'last_month', 'this_year').
    :param page: The page number for pagination.
    :param per_page: The number of items per page.
    """
    params: Dict[str, Any] = {"page": page, "per_page": per_page}
    if period:
        params["period"] = period

    return await make_request("GET", "/invoices.json", params=params)


@mcp.tool()
async def get_invoice(invoice_id: int) -> Dict[str, Any]:
    """
    Retrieves complete invoice details including line items.
    :param invoice_id: The ID of the invoice to retrieve.
    """
    return await make_request("GET", f"/invoices/{invoice_id}.json")


@mcp.tool()
async def create_invoice(
    client_id: int,
    kind: str = "vat",
    seller_name: Optional[str] = None,
    buyer_name: Optional[str] = None,
    buyer_tax_no: Optional[str] = None,
    positions: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Creates a new invoice for an existing client.
    :param client_id: The ID of the existing client.
    :param kind: Type of invoice, e.g., 'vat', 'proforma', 'bill'.
    :param seller_name: Optional name of the seller (sometimes required by API).
    :param buyer_name: Optional name of the buyer.
    :param buyer_tax_no: Optional tax ID of the buyer (NIP).
    :param positions: List of invoice line items. Each item should have 'product_id' and 'quantity' OR 'name', 'total_price_gross', 'quantity'.
    """
    invoice_data: Dict[str, Any] = {
        "kind": kind,
        "client_id": client_id,
        "positions": positions or [],
    }
    if seller_name:
        invoice_data["seller_name"] = seller_name
    if buyer_name:
        invoice_data["buyer_name"] = buyer_name
    if buyer_tax_no:
        invoice_data["buyer_tax_no"] = buyer_tax_no

    payload = {"invoice": invoice_data}
    return await make_request("POST", "/invoices.json", json=payload)


# --- Client Tools ---


@mcp.tool()
async def list_clients(
    name: Optional[str] = None, page: int = 1, per_page: int = 50
) -> Dict[str, Any]:
    """
    Retrieves a paginated list of clients.
    :param name: Optional filter by client name.
    :param page: The page number for pagination.
    :param per_page: The number of clients per page.
    """
    params: Dict[str, Any] = {"page": page, "per_page": per_page}
    if name:
        params["name"] = name

    return await make_request("GET", "/clients.json", params=params)


@mcp.tool()
async def get_client(client_id: int) -> Dict[str, Any]:
    """
    Retrieves complete details of a specific client identified by their ID.
    :param client_id: The ID of the client to retrieve.
    """
    return await make_request("GET", f"/clients/{client_id}.json")


@mcp.tool()
async def create_client(
    name: str,
    email: Optional[str] = None,
    tax_no: Optional[str] = None,
    company: bool = True,
) -> Dict[str, Any]:
    """
    Creates a new client in the system.
    :param name: The name of the company or individual.
    :param email: Client's email address.
    :param tax_no: Tax identification number (e.g., NIP).
    :param company: Set to True for a company, False for an individual.
    """
    payload = {
        "client": {"name": name, "email": email, "tax_no": tax_no, "company": company}
    }
    return await make_request("POST", "/clients.json", json=payload)


# --- Product Tools ---


@mcp.tool()
async def list_products(
    page: int = 1, per_page: int = 100, warehouse_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Retrieves a list of all products.
    :param page: The page number for pagination.
    :param per_page: The number of products per page.
    :param warehouse_id: Optional filter by warehouse ID to include stock levels.
    """
    params: Dict[str, Any] = {"page": page, "per_page": per_page}
    if warehouse_id:
        params["warehouse_id"] = warehouse_id
    return await make_request("GET", "/products.json", params=params)


@mcp.tool()
async def get_product(
    product_id: int, warehouse_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Retrieves the complete details of a specific product by its ID.
    :param product_id: The ID of the product to retrieve.
    :param warehouse_id: Optional filter by warehouse ID to include stock levels.
    """
    params: Dict[str, Any] = {}
    if warehouse_id:
        params["warehouse_id"] = warehouse_id
    return await make_request("GET", f"/products/{product_id}.json", params=params)


@mcp.tool()
async def create_product(
    name: str,
    price_gross: float,
    tax: int,
    code: Optional[str] = None,
    description: Optional[str] = None,
    currency: str = "PLN",
    quantity_unit: str = "piece",
) -> Dict[str, Any]:
    """
    Adds a new product to the catalog.
    :param name: The name of the product.
    :param price_gross: The gross price of the product.
    :param tax: The tax percentage (e.g., 23).
    :param code: Optional unique code for the product.
    :param description: Optional detailed description.
    :param currency: Currency (default 'PLN').
    :param quantity_unit: Unit of quantity (default 'piece').
    """
    payload = {
        "product": {
            "name": name,
            "price_gross": price_gross,
            "tax": tax,
            "code": code,
            "description": description,
            "currency": currency,
            "quantity_unit": quantity_unit,
        }
    }
    return await make_request("POST", "/products.json", json=payload)


# --- Payment Tools ---


@mcp.tool()
async def list_payments(
    page: int = 1, include_invoices: bool = False
) -> Dict[str, Any]:
    """
    Retrieves all payments.
    :param page: The page number for pagination.
    :param include_invoices: If true, includes related invoice data.
    """
    params: Dict[str, Any] = {"page": page}
    if include_invoices:
        params["include"] = "invoices"
    return await make_request("GET", "/banking/payments.json", params=params)


@mcp.tool()
async def create_payment(
    name: str,
    price: float,
    invoice_id: Optional[int] = None,
    invoice_ids: Optional[List[int]] = None,
    paid: bool = True,
    kind: str = "api",
) -> Dict[str, Any]:
    """
    Records a payment.
    :param name: Description of the payment.
    :param price: Amount of the payment.
    :param invoice_id: Optional ID of a single invoice to link to.
    :param invoice_ids: Optional list of invoice IDs for bulk payment.
    :param paid: Indicates if marked as paid.
    :param kind: Type of payment (e.g., 'api', 'cash').
    """
    payload = {
        "banking_payment": {
            "name": name,
            "price": price,
            "invoice_id": invoice_id,
            "invoice_ids": invoice_ids,
            "paid": paid,
            "kind": kind,
        }
    }
    return await make_request("POST", "/banking/payments.json", json=payload)


# --- Department Tools ---


@mcp.tool()
async def list_departments() -> Any:
    """Lists all departments (business locations)."""
    return await make_request("GET", "/departments.json")


@mcp.tool()
async def get_department(department_id: int) -> Dict[str, Any]:
    """Retrieves details of a specific department."""
    return await make_request("GET", f"/departments/{department_id}.json")


if __name__ == "__main__":
    mcp.run()
