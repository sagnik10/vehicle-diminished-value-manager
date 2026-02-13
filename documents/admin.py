from django.contrib import admin
from django.utils.html import format_html
from .models import DiminishedValueReport


@admin.register(DiminishedValueReport)
class DiminishedValueReportAdmin(admin.ModelAdmin):

    list_display = (
        "report_number",
        "client",
        "claim_number",
        "status",
        "created_at",
        "vehicle_make",
        "vehicle_model",
        "adjusted_dv",
        "approve_action",
        "reject_action",
        "delete_action",
        "pdf_download",
    )

    list_filter = (
        "status",
        "created_at",
        "vehicle_make",
        "state",
        "loss_type",
    )

    search_fields = (
        "report_number",
        "claim_number",
        "client",
        "vin",
    )

    readonly_fields = (
        "report_number",
        "created_at",
        "pdf_file",
        "base_dv",
        "adjusted_dv",
    )

    ordering = ("-created_at",)

    list_per_page = 50


    fieldsets = (

        ("Report Status", {
            "fields": (
                "status",
                "is_deleted",
            )
        }),

        ("Report Info", {
            "fields": (
                "report_number",
                "created_at",
                "pdf_file",
            )
        }),

        ("Client Information", {
            "fields": (
                "client",
                "client_email",
                "client_phone",
                "insurance",
                "claim_number",
                "loss_date",
                "report_date",
                "appraiser",
            )
        }),

        ("Vehicle Information", {
            "fields": (
                "vehicle_year",
                "vehicle_make",
                "vehicle_model",
                "vehicle_trim",
                "vin",
                "mileage",
                "state",
                "color_trim",
                "condition",
                "loss_type",
            )
        }),

        ("Valuation Inputs", {
            "fields": (
                "preloss_value",
                "base_loss_pct",
                "damage_modifier",
                "mileage_modifier",
                "other_modifier",
            )
        }),

        ("Damage Summary", {
            "fields": (
                "repair_facility",
                "repair_total",
                "damage_description",
            )
        }),

        ("Calculated Values", {
            "fields": (
                "base_dv",
                "adjusted_dv",
            )
        }),

    )


    actions = [
        "mark_waiting",
        "mark_approved",
        "mark_rejected",
        "mark_deleted",
    ]


    def mark_waiting(self, request, queryset):
        queryset.update(status="waiting", is_deleted=False)


    def mark_approved(self, request, queryset):
        queryset.update(status="approved")


    def mark_rejected(self, request, queryset):
        queryset.update(status="rejected")


    def mark_deleted(self, request, queryset):
        queryset.update(status="deleted", is_deleted=True)


    def approve_action(self, obj):
        if obj.status != "approved":
            return format_html(
                '<a href="/admin/documents/diminishedvaluereport/{}/change/">Approve</a>',
                obj.id
            )
        return "Approved"


    def reject_action(self, obj):
        if obj.status != "rejected":
            return format_html(
                '<a href="/admin/documents/diminishedvaluereport/{}/change/">Reject</a>',
                obj.id
            )
        return "Rejected"


    def delete_action(self, obj):
        if not obj.is_deleted:
            return format_html(
                '<a href="/admin/documents/diminishedvaluereport/{}/change/">Delete</a>',
                obj.id
            )
        return "Deleted"


    def pdf_download(self, obj):

        if obj.pdf_file:
            return format_html(
                '<a href="{}" target="_blank">Download PDF</a>',
                obj.pdf_file.url
            )

        return "No PDF"