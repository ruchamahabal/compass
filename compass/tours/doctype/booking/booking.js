// Copyright (c) 2025, rucha@frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("Booking", {
	// refresh(frm) {
	// },
	number_of_travellers(frm) {
		frm.set_value("total_amount", frm.doc.number_of_travellers * frm.doc.price);
	}
});
