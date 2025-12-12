# Copyright (c) 2025, rucha@frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, cint, get_link_to_form
from frappe.model.document import Document


class Booking(Document):
	def validate(self):
		self.validate_availability()
		self.set_total_amount()

	def validate_availability(self):
		max_group_size = frappe.db.get_value(
			"Tour Package", self.tour_package, "max_group_size"
		)
		if not max_group_size:
			return

		bookings = frappe.qb.get_query(
			"Booking",
			fields=[{"SUM": "number_of_travellers", "as": "number_of_travellers"}],
			filters={"tour_package": self.tour_package, "docstatus": ("!=", 2), "name": ("!=", self.name)}
		).run(pluck=True)[0] or 0

		if (bookings + self.number_of_travellers) > max_group_size:
			available_slots = max_group_size - bookings
			message = _("Cannot book the Tour Package {0}. Only {1} slot(s) available.").format(
				frappe.bold(self.tour_package), frappe.bold(cint(available_slots))
			)
			message += "<br>" + _("You can update the {0} here: {1}").format(frappe.bold(_("Max Group Size")), get_link_to_form("Tour Package", self.tour_package))
			frappe.throw(message, title=_("Booking Unavailable"))

	def set_total_amount(self):
		self.total_amount = flt(self.price * self.number_of_travellers)
