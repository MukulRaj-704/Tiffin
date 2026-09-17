import csv
import io
import re
import secrets
from calendar import monthrange
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from django.contrib.auth import get_user_model
from django.db import transaction

from customers.models import Customer
from subscriptions.models import Subscription

User = get_user_model()


def normalize_phone(value):
    if not value or not str(value).strip():
        raise ValueError("Missing phone number")
    digits = re.sub(r"\D", "", str(value))
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]
    if len(digits) != 10:
        raise ValueError("Invalid phone number")
    return digits


def parse_start_date(value):
    if not value or not value.strip():
        raise ValueError("Missing start date")
    for date_format in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(value.strip(), date_format).date()
        except ValueError:
            continue
    raise ValueError("Invalid start date")


def month_end(start_date):
    return start_date.replace(day=monthrange(start_date.year, start_date.month)[1])


def existing_customer_phones():
    phones = {}
    for customer in Customer.objects.all():
        try:
            phones[normalize_phone(customer.phone)] = customer
        except ValueError:
            continue
    return phones


def import_customers(upload):
    try:
        decoded = upload.read().decode("utf-8-sig")
    except UnicodeDecodeError:
        return {"imported": 0, "deduped": 0, "rejected": 1, "errors": [{"row": 1, "reason": "CSV must be UTF-8"}]}

    reader = csv.DictReader(io.StringIO(decoded))
    required_headers = {"name", "phone", "start_date", "monthly_price"}
    if not required_headers.issubset(set(reader.fieldnames or [])):
        return {"imported": 0, "deduped": 0, "rejected": 1, "errors": [{"row": 1, "reason": "Missing required CSV headers"}]}

    report = {"imported": 0, "deduped": 0, "rejected": 0, "errors": []}
    known_phones = existing_customer_phones()

    for row_number, row in enumerate(reader, start=2):
        try:
            name = (row.get("name") or "").strip()
            if not name:
                raise ValueError("Missing customer name")
            phone = normalize_phone(row.get("phone"))
            if phone in known_phones:
                report["deduped"] += 1
                continue
            start_date = parse_start_date(row.get("start_date"))
            try:
                monthly_price = Decimal((row.get("monthly_price") or "").strip())
            except (InvalidOperation, AttributeError):
                raise ValueError("Invalid monthly price")
            if monthly_price <= 0:
                raise ValueError("Invalid monthly price")

            with transaction.atomic():
                username = f"customer_{phone}"
                if User.objects.filter(username=username).exists():
                    username = f"{username}_{secrets.token_hex(3)}"
                user = User.objects.create_user(
                    username=username,
                    password=secrets.token_urlsafe(18),
                    phone=phone,
                    role="CUSTOMER",
                )
                customer = Customer.objects.create(
                    user=user,
                    name=name,
                    phone=phone,
                    email=(row.get("email") or "").strip() or None,
                    address=(row.get("address") or "").strip() or None,
                )
                subscription = Subscription.objects.create(
                    customer=customer,
                    monthly_price=monthly_price,
                    start_date=start_date,
                    end_date=month_end(start_date),
                )
                subscription.generate_delivery_records()
            known_phones[phone] = customer
            report["imported"] += 1
        except Exception as exc:
            report["rejected"] += 1
            report["errors"].append({"row": row_number, "reason": str(exc)})

    return report