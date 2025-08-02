from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator, URLValidator, RegexValidator


class Media(models.Model):
    class MediType(models.TextChoices):
        IMAGE = 'image', _('Image')
        FILE = 'file', _('File')
        MUSIC = 'music', _('Music')
        VIDEO = 'video', _('Video')

    file = models.FileField(_("File"), upload_to='files/',
                            validators=[FileExtensionValidator(
                                allowed_extensions=
                                ['jpg', 'jpeg', 'png', 'gif', 'mp3', 'mp4', 'flac', 'doc', 'pdf'])])  # Fixed here
    type = models.CharField(_("Type"), max_length=60, choices=MediType.choices)

    def __str__(self):
        return f"{str(self.id)} - {self.file.name.split('/')[-1]}"  # Fixed here

    def clean(self):
        if self.type == self.MediType.IMAGE:
            if not self.file.name.endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError(_('Invalid image format. Only JPEG, PNG, and GIF images are allowed.'))
        elif self.type == self.MediType.FILE:
            if not self.file.name.endswith(('.pdf', '.doc')):
                raise ValidationError(_('Invalid file format. Only PDF and DOC files are allowed.'))
        elif self.type == self.MediType.MUSIC:
            if not self.file.name.endswith(('.mp3', '.flac')):
                raise ValidationError(_('Invalid music format. Only MP3 and FLAC files are allowed.'))
        elif self.type == self.MediType.VIDEO:
            if not self.file.name.endswith(('.mp4')):
                raise ValidationError(_('Invalid video format. Only MP4 files are allowed.'))
        else:
            raise ValidationError(_('File type not supported.'))

class Settings(models.Model):
    home_image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    home_title = models.CharField(_("Home title"), max_length=120)
    home_subtitle = models.TextField(_("Home subtitle"), max_length=1500)
    def __str__(self):
        return self.home_title

class Country(models.Model):
    name = models.CharField(_("Country name"), max_length=120)
    code = models.CharField(_("Country code"), max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

class Region(models.Model):
    name = models.CharField(_("Region name"), max_length=120)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, related_name='regions', null=True)  # Fixed here

    def __str__(self):
        return self.name

class OurInstagramStory(models.Model):
    image = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='our_instagram_story')
    link = models.URLField(
        _("Link"),
        validators=[
            RegexValidator(
                regex=r'^https?://(www\.)?instagram\.com/.*$',
                message=_('Please enter a valid Instagram URL.')
            )
        ]
    )
    def __str__(self):
        return f"ID:{self.id}|LINK: {self.link}"

class CustomerFeedback(models.Model):
    description = models.TextField(_("Description"))
    rank = models.IntegerField(_("Rank"))
    customer_name = models.CharField(_("Customer name"), max_length=120)
    customer_position = models.CharField(_("Customer position"), max_length=120)
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, related_name='customer_feedback', null=True, blank=True)

    def __str__(self):
        return self.customer_name