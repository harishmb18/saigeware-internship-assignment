from flask import Flask, jsonify, render_template, request, redirect, url_for
from google.cloud import firestore
import os

app = Flask(__name__)

# Point to the service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "serviceAccountKey.json"

# Initialize Firestore client
db = firestore.Client()
customers_ref = db.collection("customers")


@app.route("/ping")
def ping():
    return jsonify({"message": "Flask is running!"})


@app.route("/test-firestore")
def test_firestore():
    sample_customer = {
        "name": "Test User",
        "email": "testuser@example.com",
        "phone": "9999999999"
    }
    customers_ref.add(sample_customer)

    docs = customers_ref.stream()
    customers = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        customers.append(data)

    return jsonify({
        "message": "Firestore is working!",
        "total_customers": len(customers),
        "customers": customers
    })


@app.route("/")
def home():
    # Redirect to customers page
    return redirect(url_for("list_customers"))


@app.route("/customers")
def list_customers():
    """
    Show all customers in an HTML table.
    Optional: filter by name or email using ?q= search query.
    """
    search_query = request.args.get("q", "").strip().lower()

    docs = customers_ref.stream()
    customers = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id

        name = str(data.get("name", "")).lower()
        email = str(data.get("email", "")).lower()

        # If there's a search query, filter by name OR email
        if search_query:
            if (search_query not in name) and (search_query not in email):
                continue  # skip this customer

        customers.append(type("Customer", (), data))

    return render_template(
        "customers_list.html",
        title="Customers",
        customers=customers,
        search_query=search_query
    )


@app.route("/customers/add", methods=["GET", "POST"])
def add_customer():
    """
    Show a form (GET) and handle form submit (POST) to add a new customer.
    """
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")

        if name and email and phone:
            customers_ref.add({
                "name": name,
                "email": email,
                "phone": phone
            })

        return redirect(url_for("list_customers"))

    # GET request → show empty form
    return render_template(
        "customer_form.html",
        title="Add Customer",
        heading="Add New Customer",
        customer=None
    )


@app.route("/customers/edit/<customer_id>", methods=["GET", "POST"])
def edit_customer(customer_id):
    """
    Edit an existing customer.
    - GET: show form with existing data
    - POST: update Firestore and redirect
    """
    doc_ref = customers_ref.document(customer_id)
    doc = doc_ref.get()

    if not doc.exists:
        # If somehow the doc was deleted or ID is wrong
        return redirect(url_for("list_customers"))

    customer_data = doc.to_dict()
    customer_data["id"] = doc.id
    customer_obj = type("Customer", (), customer_data)

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")

        if name and email and phone:
            doc_ref.update({
                "name": name,
                "email": email,
                "phone": phone
            })

        return redirect(url_for("list_customers"))

    # GET → pre-fill form with current values
    return render_template(
        "customer_form.html",
        title="Edit Customer",
        heading="Edit Customer",
        customer=customer_obj
    )


@app.route("/customers/delete/<customer_id>")
def delete_customer(customer_id):
    """
    Delete a customer by ID and redirect back to list.
    """
    doc_ref = customers_ref.document(customer_id)
    doc_ref.delete()
    return redirect(url_for("list_customers"))


if __name__ == "__main__":
    app.run(debug=True)
