# gui/finance_pages.py
import streamlit as st
import pandas as pd

def show_finance_page(manager):
    """Renders the UI for all financial operations."""
    st.header("Finance & Payments")

    # --- Section 1: Record a Payment ---
    st.subheader("Record New Payment")
    with st.form("payment_form"):
        # Create a selectbox to choose a student (e.g., from a list of names).
        student_list = {s.name: s.id for s in manager.students}
        selected_student_name = st.selectbox("Select Student", student_list.keys())
        
        # Create a number_input for amount and a text_input for method.
        amount = st.number_input("Payment Amount", min_value=0.01)
        method = st.text_input("Payment Method (e.g., Credit Card, Cash)")
        
        submitted = st.form_submit_button("Record Payment")
        if submitted:
            student_id = student_list[selected_student_name]
            # Call manager.record_payment() and show a success message.
            manager.record_payment(student_id, amount, method)
            st.success(f"Payment of {amount} for {selected_student_name} recorded.")

    # --- Section 2: View Payment History ---
    st.subheader("View Student Payment History")
    # Create a selectbox to choose a student.
    history_student_name = st.selectbox("Select Student to View History", student_list.keys())
    if history_student_name:
        history_student_id = student_list[history_student_name]
        # Call manager.get_payment_history().
        history = manager.get_payment_history(history_student_id)
        if history:
            # Convert the list of dictionaries to a pandas DataFrame and display it.
            df = pd.DataFrame(history)
            st.dataframe(df)
        else:
            st.info("This student has no payment history.")
    
    st.divider()
    st.subheader("Payments Summary (All Students)")


    only_with_payments = st.checkbox("Only show students with at least one payment", value=True)

    rows = []
    for s in manager.students:
        sid = getattr(s, "user_id", getattr(s, "id", None))
        if sid is None:
            continue

        history = manager.get_payment_history(sid) or []
        count = len(history)
        total = sum((h.get("amount") or 0) for h in history)
        last_ts = max([h.get("timestamp", "") for h in history], default="")

        if (not only_with_payments) or count > 0:
            rows.append({
                "student_id": sid,
                "name": getattr(s, "name", ""),
                "payments": count,
                "total_amount": round(total, 2),
                "last_payment": last_ts,
            })

    if rows:
        df = pd.DataFrame(rows).sort_values(
            ["payments", "total_amount"], ascending=[False, False], ignore_index=True
        )
        st.dataframe(df, use_container_width=True)

        