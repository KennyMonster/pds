from datetime import datetime
from xml.etree import ElementTree
from django.db import transaction
from models import MediaFile, Manifest


class ParseError(Exception):
    """
    An invalid Manifest file error
    """
    pass


class ManifestParser(object):
    """
    Helper responsible for parsing the Manifest XML and creating
    subsequent model objects as defined by the manifest
    """
    def __init__(self, manifest_file):
        """
        Expects a file object of the manifest
        """
        self.manifest_file = manifest_file

        self.media_file_objs = []  # MediaFile model objs extracted from XML

    def parse(self):
        """
        Extracts media file data into model objects for later saving
        """
        try:
            tree = ElementTree.fromstring(self.manifest_file.read())
        except ElementTree.ParseError:
            raise ParseError('Error parsing XML')

        for media_file in tree.findall('file'):
            try:
                mfo = MediaFile()
                mfo.title = media_file.find('title').text
                mfo.version = media_file.find('version').text
                mfo.release_date = datetime.strptime(media_file.find('releasedate').text, '%m/%d/%Y').date()
                mfo.content_type = media_file.find('contenttype').text
                mfo.language = media_file.find('language').text
                mfo.barcode = media_file.find('barcode').text
                mfo.md5_checksum = media_file.find('md5').text
                mfo.filename = media_file.find('filename').text

                self.media_file_objs.append(mfo)
            except AttributeError:
                raise ParseError('Missing required XML attribute')

    @transaction.atomic
    def save(self):
        """
        Save Manifest and MediaFile objects to DB in a single transaction
        """
        manifest = Manifest.objects.create(filename=self.manifest_file.name)

        for media_file in self.media_file_objs:
            media_file.manifest = manifest

        MediaFile.objects.bulk_create(self.media_file_objs)

        return manifest