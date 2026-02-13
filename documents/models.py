from django.db import models
from django.utils import timezone


class DiminishedValueReport(models.Model):

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("waiting", "Waiting for Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("deleted", "Deleted"),
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    created_date = models.DateField(editable=False, db_index=True)
    created_year = models.PositiveIntegerField(editable=False, db_index=True)
    created_month = models.PositiveIntegerField(editable=False, db_index=True)

    report_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        db_index=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        db_index=True
    )

    is_deleted = models.BooleanField(default=False, db_index=True)

    pdf_file = models.FileField(
        upload_to="dv_reports/",
        null=True,
        blank=True
    )

    client = models.CharField(max_length=255, blank=True, db_index=True)
    client_email = models.EmailField(blank=True)
    client_phone = models.CharField(max_length=50, blank=True)

    insurance = models.CharField(max_length=255, blank=True, db_index=True)
    claim_number = models.CharField(max_length=255, blank=True, db_index=True)

    loss_date = models.DateField(null=True, blank=True, db_index=True)
    report_date = models.DateField(null=True, blank=True, db_index=True)

    appraiser = models.CharField(max_length=255, blank=True)

    vehicle_year = models.CharField(max_length=10, blank=True, db_index=True)
    vehicle_make = models.CharField(max_length=100, blank=True, db_index=True)
    vehicle_model = models.CharField(max_length=100, blank=True, db_index=True)
    vehicle_trim = models.CharField(max_length=100, blank=True)

    vin = models.CharField(max_length=50, blank=True, db_index=True)
    mileage = models.IntegerField(null=True, blank=True)

    state = models.CharField(max_length=50, blank=True, db_index=True)
    color_trim = models.CharField(max_length=100, blank=True)

    condition = models.CharField(max_length=50, blank=True, db_index=True)
    loss_type = models.CharField(max_length=50, blank=True, db_index=True)

    repair_facility = models.CharField(max_length=255, blank=True)
    repair_total = models.FloatField(default=0)

    preloss_value = models.FloatField(default=0)
    base_loss_pct = models.FloatField(default=0)

    damage_modifier = models.FloatField(default=0)
    mileage_modifier = models.FloatField(default=0)
    other_modifier = models.FloatField(default=0)

    damage_description = models.TextField(blank=True)

    base_dv = models.FloatField(default=0, db_index=True)
    adjusted_dv = models.FloatField(default=0, db_index=True)


    def save(self, *args, **kwargs):

        now = timezone.now()

        if not self.created_date:
            self.created_date = now.date()

        if not self.created_year:
            self.created_year = now.year

        if not self.created_month:
            self.created_month = now.month

        if not self.report_number:
            last_id = DiminishedValueReport.objects.count() + 1
            self.report_number = f"DV-{now.year}-{last_id:06d}"

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.report_number} | {self.client} | {self.status}"
