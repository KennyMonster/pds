from django.conf import settings
from django.db import models


class Manifest(models.Model):
    """
    A listing of media files to be uploaded and accounted for
    """
    filename = models.CharField(max_length=255, help_text='Name of original manifest file')
    created = models.DateTimeField(auto_now_add=True, help_text='Time of manifest upload')
    all_media_present = models.BooleanField(default=False, help_text='Have all associated files been uploaded')

    def __unicode__(self):
        return 'Manifest: %s' % self.filename


class MediaFile(models.Model):
    """
    A media file associated with a Manifest
    """
    manifest = models.ForeignKey(Manifest, related_name='media_files')

    title = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    release_date = models.DateField()
    content_type = models.CharField(max_length=255)
    language = models.CharField(max_length=8)
    barcode = models.CharField(max_length=255)  # Could possibly be an int?
    md5_checksum = models.CharField(max_length=32)
    filename = models.CharField(max_length=255, help_text='Filename given in manifest')

    file = models.FileField(upload_to=settings.MANIFEST_MEDIA_FILES_DIR)

    def __unicode__(self):
        return 'MediaFile: %s' % self.title