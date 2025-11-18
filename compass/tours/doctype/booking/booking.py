# Copyright (c) 2025, rucha@frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
from frappe.model.document import Document


class Booking(Document):
	def validate(self):
		self.validate_availability()
		self.set_total_amount()

	def validate_availability(self):
		max_group_size = frappe.db.get_value(
			"Tour Package", self.tour_package, "max_group_size"
		)
		bookings = frappe.qb.get_query(
			"Booking",
			fields=[{"SUM": "number_of_travellers", "as": "number_of_travellers"}],
			filters={"tour_package": self.tour_package, "docstatus": ("!=", 2)}
		).run(pluck=True)[0] or 0

		if bookings >= max_group_size:
			frappe.throw(
				_("Cannot book {0}. Maximum group size of {1} has been reached.").format(
					self.tour_package, max_group_size
				),
				title=_("Booking Unavailable"),
			)

	def set_total_amount(self):
		self.total_amount = flt(self.price * self.number_of_travellers)
