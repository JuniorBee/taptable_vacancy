class Place(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=250),
        address=models.CharField(max_length=300),
        oh_weekday=models.CharField(max_length=200, null=True, blank=True,
                                    verbose_name=_("Weekday operating hours weekdays")),
        oh_weekend=models.CharField(max_length=200, null=True, blank=True,
                                    verbose_name=_("Weekend operating hours weekdays")),
        under_construction_text=models.CharField(max_length=200, null=True, blank=True),
        description=models.TextField(verbose_name=_("Description")),
    )

    min_price = models.PositiveIntegerField(verbose_name=_("Minimum price"))
    max_price = models.PositiveIntegerField(verbose_name=_("Maximum price"))
    order_number = models.IntegerField(verbose_name=_("Ordering Number"), unique=True, null=True, blank=True)
    phone = models.CharField(max_length=30)
    category = models.ForeignKey('Category')
    recommended = models.BooleanField(default=0)
    notification_time_start = models.TimeField(auto_now_add=False, default='10:00')
    notification_time_end = models.TimeField(auto_now_add=False, default='20:00')
    director_number = models.CharField(max_length=30, blank=True, null=True)
    manager_number = models.CharField(max_length=30, blank=True, null=True)
    website = models.CharField(max_length=100)
    map_latitude = models.CharField(max_length=100)
    map_longitude = models.CharField(max_length=100)
    image = ImageField(upload_to='images', default='')  # sizes=((640, 640),)
    logo = ImageField(upload_to='images', null=True, blank=True)  # sizes=((205, 145),)
    selected = models.BooleanField(default=False, verbose_name=_("Selected"))
    service = models.ManyToManyField(Service, verbose_name=_("Services"), related_name='place_services')
    cuisine = models.ManyToManyField(Cuisine, verbose_name=_("Cuisines"), related_name='place_cusines')
    tags = models.ManyToManyField(Tag, verbose_name=_("Cuisines"), related_name='place_tags')
    is_reservable = models.BooleanField(default=1)
    percentage = models.DecimalField(decimal_places=1, max_digits=3, default=0)
    monday_start = models.TimeField(auto_now_add=False, blank=True, null=True)
    monday_end = models.TimeField(auto_now_add=False, blank=True, null=True)
    tuesday_start = models.TimeField(auto_now_add=False, blank=True, null=True)
    tuesday_end = models.TimeField(auto_now_add=False, blank=True, null=True)
    thursday_start = models.TimeField(auto_now_add=False, blank=True, null=True)
    thursday_end = models.TimeField(auto_now_add=False, blank=True, null=True)
    wednesday_start = models.TimeField(auto_now_add=False, blank=True, null=True)
    wednesday_end = models.TimeField(auto_now_add=False, blank=True, null=True)
    friday_start = models.TimeField(auto_now_add=False, blank=True, null=True)
    friday_end = models.TimeField(auto_now_add=False, blank=True, null=True)
    saturday_start = models.TimeField(auto_now_add=False, blank=True, null=True)
    saturday_end = models.TimeField(auto_now_add=False, blank=True, null=True)
    sunday_start = models.TimeField(auto_now_add=False, blank=True, null=True)
    sunday_end = models.TimeField(auto_now_add=False, blank=True, null=True)
    oh_weekday_time = models.CharField(max_length=200, null=True, blank=True,
                                       verbose_name=_("Weekday operating hours time"))
    oh_weekend_time = models.CharField(max_length=200, null=True, blank=True,
                                       verbose_name=_("Weekend operating hours time"))
    status = models.BooleanField(default=True)
