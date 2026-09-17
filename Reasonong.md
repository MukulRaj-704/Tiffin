# Project Reasoning

## Why this design?

The main thing I focused on was keeping **subscription, delivery and billing separate**.

A customer can have an active subscription but may be paused on a particular day. Also, having a subscription does not always mean the tiffin was actually delivered. So I used the delivery record as the main source for billing.

```text
Subscription → Delivery → Billing
```

Billing is based on `SERVED` deliveries instead of simply subtracting pause days from the monthly price.

---

## Pause / Resume

Pause is stored as a date range.

For example:

```text
14 Sep - 18 Sep → PAUSED
```

If the customer comes back on 16 Sep, I don't delete the whole pause. I treat it as:

```text
14-15 Sep → PAUSED
16 Sep onwards → ACTIVE
```

This handles early resume without losing the original data.

---

## Subscription Transfer

For a mid-cycle transfer, I don't simply change the customer on the subscription.

Example:

```text
1-15 Sep  → Customer A
16-30 Sep → Customer B
```

I store these ownership periods separately using `SubscriptionCustomer`.

This is important because old deliveries should still belong to Customer A. Only future deliveries move to Customer B.

Billing is also split based on the actual served deliveries of each customer.

---

## Notifications

Every morning, `/clock` checks:

* subscription is active
* today is a weekday
* customer is not paused
* delivery is due today

Then it creates a notification in the outbox.

I also made notification creation idempotent, so calling `/clock` twice does not create duplicate notifications for the same delivery.

---

## CSV Import

For messy customer data, I don't directly insert the CSV into the database.

The flow is:

```text
CSV → Normalize → Validate → Deduplicate → Save
```

Phone numbers are normalized so values like:

```text
9876543210
+91 98765 43210
98765-43210
```

can be treated as the same number.

Different date formats are also converted to one format before saving.

The import returns:

```text
imported
deduped
rejected
```

so it is clear what happened to every row.

---

## How I Handle Edge Cases

Whenever I find an edge case, I first ask:

1. What should happen from a business point of view?
2. Will existing/historical data be affected?
3. Is this a duplicate or retry case?
4. Does the database need a constraint?
5. Do I need a transaction?
6. Can I write a test for it?

The main idea is to **solve the underlying problem in the data model instead of adding random conditions in the code.**
