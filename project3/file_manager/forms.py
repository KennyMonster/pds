import hashlib
import os
from django import forms
from django.conf import settings
from manifest_parser import ManifestParser, ParseError


class ManifestForm(forms.Form):
    """
    Manifest file upload form
    """
    file = forms.FileField(label='Manifest File')

    def __init__(self, *args, **kwargs):
        self._parser = None  # XML parser
        super(ManifestForm, self).__init__(*args, **kwargs)

    def clean_file(self):
        self._parser = ManifestParser(self.cleaned_data['file'])

        try:
            self._parser.parse()
        except ParseError:
            raise forms.ValidationError('Invalid manifest file uploaded')

    def save(self):
        return self._parser.save()


class MediaFileForm(forms.Form):
    """
    Media file upload form

    Looks and acts like a ModelForm, but handles saving the uploaded file
    in a very different way. Also handles all file validation rules.
    """
    file = forms.FileField(label='Media File')

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        del kwargs['instance']

        super(MediaFileForm, self).__init__(*args, **kwargs)

        # Remember the uploaded file MD5 once computed
        self._tmp_file_md5 = None

    def clean_file(self):
        tmp_file = self.cleaned_data['file']

        # Make sure the uploaded files matches the MD5 checksum provided in the Manifest
        m = hashlib.md5()
        for chunk in tmp_file.chunks():
            m.update(chunk)

        self._tmp_file_md5 = m.hexdigest()

        if self.instance.md5_checksum != self._tmp_file_md5:
            raise forms.ValidationError('The MD5 checksum of the uploaded file does not match the manifest')

        # Do the file names match?
        # [questionable if this validation is needed if checksums match]
        if self.instance.filename != tmp_file.name:
            raise forms.ValidationError('The filename of the uploaded file does not match the manifest')

        return tmp_file

    def save(self):
        tmp_file = self.cleaned_data['file']

        dest_path = os.path.join(settings.MEDIA_ROOT, settings.MANIFEST_MEDIA_FILES_DIR, self._tmp_file_md5)

        # Avoid copying if file already exists
        # TODO: Consider moving instead of copying to handle large files
        if not os.path.isfile(dest_path):
            with open(dest_path, 'wb') as dest_file:
                for chunk in tmp_file.chunks():
                    dest_file.write(chunk)

        # Update the model instance
        self.instance.file = os.path.join(settings.MANIFEST_MEDIA_FILES_DIR, self._tmp_file_md5)
        self.instance.save()



