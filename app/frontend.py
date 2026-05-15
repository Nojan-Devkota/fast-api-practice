import streamlit as st
import requests

# ─── Configuration ───────────────────────────────────────────────────────────
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="ShopDash — Product Manager",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Clean Minimal CSS ──────────────────────────────────────────────────────
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    /* Clean white background */
    .stApp {
        background-color: #f8f9fb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e8eaed;
    }

    /* Hide default streamlit stuff */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)


# ─── Helper Functions ─────────────────────────────────────────────────────────
def fetch_all_products():
    """Fetch all products from the FastAPI backend."""
    try:
        response = requests.get(f"{API_URL}/allproducts", timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to the backend. Make sure FastAPI is running on port 8000!")
        return []


def format_currency(amount, currency="INR"):
    """Format price with currency symbol."""
    symbols = {"INR": "₹", "USD": "$", "EUR": "€", "NPR": "Rs."}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.0f}"


def render_stars(rating):
    """Render star rating as emoji string."""
    full = int(rating)
    half = rating - full >= 0.5
    return "⭐" * full + ("✨" if half else "") + f"  {rating}/5"


def render_product_card(product):
    """Render a product card using native Streamlit components."""
    name = product.get("name", "Unknown")
    brand = product.get("brand", "Unknown")
    price = product.get("price", 0)
    currency = product.get("currency", "INR")
    discount = product.get("discount_percent", 0)
    stock = product.get("stock", 0)
    rating = product.get("rating", 0)
    category = product.get("category", "")
    tags = product.get("tags", [])
    seller = product.get("seller", {})
    sku = product.get("sku", "N/A")

    selling_price = price * (1 - discount / 100) if discount > 0 else price

    with st.container(border=True):
        # Brand + Category header
        header_text = f"**{brand.upper()}**"
        if discount > 0:
            header_text += f"  ·  🔥 {discount:.0f}% OFF"
        st.caption(header_text)

        # Product Name
        st.subheader(name)

        # Rating
        st.caption(render_stars(rating))

        # Price
        if discount > 0:
            st.markdown(
                f"### {format_currency(selling_price, currency)}\n"
                f"~~{format_currency(price, currency)}~~"
            )
        else:
            st.markdown(f"### {format_currency(price, currency)}")

        # Tags row
        tag_cols = st.columns(min(len(tags) + 2, 5))
        with tag_cols[0]:
            st.caption(f"📁 {category}")
        with tag_cols[1]:
            if stock > 50:
                st.caption(f"📦 {stock} in stock")
            elif stock > 0:
                st.caption(f"⚡ {stock} left")
            else:
                st.caption("❌ Out of stock")
        for i, tag in enumerate(tags[:3]):
            if i + 2 < len(tag_cols):
                with tag_cols[i + 2]:
                    st.caption(f"🏷️ {tag}")

        # Seller info
        st.divider()
        st.caption(
            f"🏪 {seller.get('name', 'N/A')}  ·  "
            f"📧 {seller.get('email', 'N/A')}  ·  "
            f"🆔 {sku}"
        )


# ─── Sidebar Navigation ──────────────────────────────────────────────────────
with st.sidebar:
    st.title("🧊 ShopDash")
    st.caption("Product Management Dashboard")
    st.divider()

    page = st.radio(
        "Navigate",
        [
            "📦 Browse Products",
            "🔍 Search",
            "➕ Add Product",
            "✏️ Update Product",
            "🗑️ Delete Product",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("Built with Streamlit + FastAPI")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Browse Products
# ═══════════════════════════════════════════════════════════════════════════════
if page == "📦 Browse Products":
    st.title("📦 All Products")
    st.caption("Browse your entire product catalog")

    products = fetch_all_products()

    if products:
        # ── Metrics Row ──
        m1, m2, m3, m4 = st.columns(4)
        total = len(products)
        avg_price = sum(p.get("price", 0) for p in products) / total
        avg_rating = sum(p.get("rating", 0) for p in products) / total
        total_stock = sum(p.get("stock", 0) for p in products)

        m1.metric("Total Products", total)
        m2.metric("Avg Price", f"₹{avg_price:,.0f}")
        m3.metric("Avg Rating", f"{avg_rating:.1f} ⭐")
        m4.metric("Total Stock", f"{total_stock:,}")

        st.divider()

        # ── Filters ──
        f1, f2 = st.columns(2)
        with f1:
            brands = sorted(set(p.get("brand", "") for p in products))
            selected_brand = st.selectbox("Filter by Brand", ["All"] + brands)
        with f2:
            categories = sorted(set(p.get("category", "") for p in products))
            selected_category = st.selectbox("Filter by Category", ["All"] + categories)

        # Apply filters
        filtered = products
        if selected_brand != "All":
            filtered = [p for p in filtered if p.get("brand") == selected_brand]
        if selected_category != "All":
            filtered = [p for p in filtered if p.get("category") == selected_category]

        st.caption(f"Showing {len(filtered)} product{'s' if len(filtered) != 1 else ''}")

        # ── Product Grid ──
        cols = st.columns(3)
        for i, product in enumerate(filtered):
            with cols[i % 3]:
                render_product_card(product)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Search Products
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Search":
    st.title("🔍 Search Products")
    st.caption("Search by product name with sorting and limits")

    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        search_query = st.text_input(
            "Product Name", placeholder="e.g. Xiaomi, Samsung, Apple..."
        )
    with c2:
        sort_price = st.selectbox("Sort by Price", ["No", "Ascending", "Descending"])
    with c3:
        limit = st.number_input("Limit", min_value=1, max_value=100, value=10)

    if st.button("🔎 Search", use_container_width=True, type="primary"):
        if search_query.strip():
            params = {
                "name": search_query.strip(),
                "sort_by_price": sort_price != "No",
                "order_of_sort": "asc" if sort_price == "Ascending" else "desc",
                "limit": limit,
            }
            try:
                response = requests.get(f"{API_URL}/products", params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    items = data.get("items", [])
                    st.success(f"✅ Found {data.get('total', 0)} product(s)")

                    cols = st.columns(3)
                    for i, product in enumerate(items):
                        with cols[i % 3]:
                            render_product_card(product)

                elif response.status_code == 404:
                    st.warning("🔍 No products found matching your search.")
                else:
                    st.error(
                        f"❌ Error: {response.json().get('detail', 'Unknown error')}"
                    )
            except requests.exceptions.ConnectionError:
                st.error("⚠️ Cannot connect to the backend!")
        else:
            st.warning("Please enter a product name to search.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Add Product
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "➕ Add Product":
    st.title("➕ Add New Product")
    st.caption("Fill in the details below to add a new product to the catalog")

    with st.form("add_product_form"):
        st.subheader("Product Information")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Product Name *", placeholder="e.g. Samsung Galaxy S25")
            brand = st.text_input("Brand *", placeholder="e.g. Samsung")
            category = st.selectbox(
                "Category *", ["mobiles", "laptops", "electronics", "accessories"]
            )
            price = st.number_input("Price (₹) *", min_value=0.01, value=10000.0, step=100.0)
            currency = st.selectbox("Currency", ["INR", "USD", "EUR", "NPR"])
            discount = st.slider("Discount (%)", 0, 100, 0)
            stock = st.number_input("Stock *", min_value=0, value=50, step=1)

        with col2:
            sku = st.text_input("SKU *", placeholder="e.g. SAMS-256GB-001")
            description = st.text_input("Description", placeholder="Product description...")
            rating = st.slider("Rating", 0.0, 5.0, 4.5, 0.1)
            tags_input = st.text_input(
                "Tags (comma separated)", placeholder="5g, camera, gaming"
            )
            seller_name = st.text_input("Seller Name *", placeholder="e.g. Samsung India")
            seller_email = st.text_input(
                "Seller Email *", placeholder="e.g. support@samsungindia.in"
            )
            seller_website = st.text_input(
                "Seller Website", placeholder="https://www.samsungindia.in"
            )

        st.subheader("Dimensions (cm)")
        d1, d2, d3 = st.columns(3)
        with d1:
            length = st.number_input("Length", min_value=0.1, value=15.0, step=0.1)
        with d2:
            width = st.number_input("Width", min_value=0.1, value=7.5, step=0.1)
        with d3:
            height = st.number_input("Height", min_value=0.1, value=0.8, step=0.1)

        submitted = st.form_submit_button(
            "🚀 Create Product", use_container_width=True, type="primary"
        )

        if submitted:
            if not all([name, brand, sku, seller_name, seller_email]):
                st.error("❌ Please fill in all required fields (marked with *)")
            else:
                tags = (
                    [t.strip() for t in tags_input.split(",") if t.strip()]
                    if tags_input
                    else ["general"]
                )

                product_data = {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "sku": sku,
                    "name": name,
                    "description": description or f"Official {brand} product",
                    "category": category,
                    "brand": brand,
                    "price": price,
                    "currency": currency,
                    "discount_percent": discount,
                    "stock": stock,
                    "is_active": stock > 0,
                    "rating": rating,
                    "tags": tags,
                    "image_urls": [
                        f"https://cdn.example.com/{brand.lower()}/front.png"
                    ],
                    "dimensions_cm": {
                        "length": length,
                        "width": width,
                        "height": height,
                    },
                    "seller": {
                        "seller_id": "00000000-0000-0000-0000-000000000000",
                        "name": seller_name,
                        "email": seller_email,
                        "website": seller_website
                        or f"https://www.{brand.lower()}.com",
                    },
                    "created_at": "2024-01-01T00:00:00Z",
                }

                try:
                    response = requests.post(
                        f"{API_URL}/products", json=product_data, timeout=5
                    )
                    if response.status_code == 201:
                        st.success("🎉 Product created successfully!")
                        st.balloons()
                    else:
                        error = response.json().get("detail", response.text)
                        st.error(f"❌ Failed: {error}")
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Cannot connect to the backend!")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Update Product
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "✏️ Update Product":
    st.title("✏️ Update Product")
    st.caption("Select a product and modify its details")

    products = fetch_all_products()

    if products:
        product_options = {
            f"{p['name']} ({p['brand']}) — {p['id'][:8]}...": p for p in products
        }
        selected_label = st.selectbox(
            "Select Product to Update", list(product_options.keys())
        )
        selected_product = product_options[selected_label]

        st.divider()
        st.caption("Edit the fields you want to update — leave others unchanged")

        with st.form("update_product_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input(
                    "Name", value=selected_product.get("name", "")
                )
                new_price = st.number_input(
                    "Price",
                    min_value=0.01,
                    value=float(selected_product.get("price", 0)),
                    step=100.0,
                )
                new_discount = st.slider(
                    "Discount %",
                    0,
                    100,
                    int(selected_product.get("discount_percent", 0)),
                )
            with col2:
                new_stock = st.number_input(
                    "Stock",
                    min_value=0,
                    value=int(selected_product.get("stock", 0)),
                    step=1,
                )
                new_rating = st.slider(
                    "Rating",
                    0.0,
                    5.0,
                    float(selected_product.get("rating", 0)),
                    0.1,
                )
                cat_options = ["mobiles", "laptops", "electronics", "accessories"]
                current_cat = selected_product.get("category", "mobiles")
                new_category = st.selectbox(
                    "Category",
                    cat_options,
                    index=cat_options.index(current_cat)
                    if current_cat in cat_options
                    else 0,
                )

            submitted = st.form_submit_button(
                "💾 Save Changes", use_container_width=True, type="primary"
            )

            if submitted:
                update_data = {}
                if new_name != selected_product.get("name"):
                    update_data["name"] = new_name
                if new_price != selected_product.get("price"):
                    update_data["price"] = new_price
                if new_discount != selected_product.get("discount_percent"):
                    update_data["discount_percent"] = new_discount
                if new_stock != selected_product.get("stock"):
                    update_data["stock"] = new_stock
                if new_rating != selected_product.get("rating"):
                    update_data["rating"] = new_rating
                if new_category != selected_product.get("category"):
                    update_data["category"] = new_category

                if not update_data:
                    st.info("ℹ️ No changes detected.")
                else:
                    try:
                        product_id = selected_product["id"]
                        response = requests.put(
                            f"{API_URL}/products/{product_id}",
                            json=update_data,
                            timeout=5,
                        )
                        if response.status_code == 200:
                            st.success(
                                f"✅ Updated: {', '.join(update_data.keys())}"
                            )
                        else:
                            error = response.json().get("detail", response.text)
                            st.error(f"❌ Failed: {error}")
                    except requests.exceptions.ConnectionError:
                        st.error("⚠️ Cannot connect to the backend!")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Delete Product
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🗑️ Delete Product":
    st.title("🗑️ Delete Product")
    st.caption("Permanently remove a product from the catalog")

    products = fetch_all_products()

    if products:
        product_options = {
            f"{p['name']} ({p['brand']}) — {format_currency(p['price'], p.get('currency', 'INR'))}": p
            for p in products
        }
        selected_label = st.selectbox(
            "Select Product to Delete", list(product_options.keys())
        )
        selected_product = product_options[selected_label]

        st.divider()
        st.subheader("Product to be deleted:")
        render_product_card(selected_product)

        st.divider()
        confirm = st.checkbox(
            "⚠️ I confirm I want to permanently delete this product"
        )

        if st.button(
            "🗑️ Delete Product",
            use_container_width=True,
            type="primary",
            disabled=not confirm,
        ):
            try:
                product_id = selected_product["id"]
                response = requests.delete(
                    f"{API_URL}/products/{product_id}", timeout=5
                )
                if response.status_code == 200:
                    st.success("✅ Product deleted successfully!")
                    st.balloons()
                else:
                    error = response.json().get("detail", response.text)
                    st.error(f"❌ Failed: {error}")
            except requests.exceptions.ConnectionError:
                st.error("⚠️ Cannot connect to the backend!")
