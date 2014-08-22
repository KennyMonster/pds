from django.test import TestCase
from manifest_parser import ManifestParser, ParseError
from models import MediaFile, Manifest


valid_manifest_file = 'file_manager/test_data/valid.xml'
test_upload_manifest = 'file_manager/test_data/test_upload_manifest.xml'
test_upload_1 = 'file_manager/test_data/test_upload_1.txt'


class ManifestParserTestCase(TestCase):
    def setUp(self):
        self.valid_xml_file = open(valid_manifest_file, 'r')
        self.invalid_xml_file = open('file_manager/test_data/missing_attr.xml', 'r')

    def test_parse_valid_and_save(self):
        mp = ManifestParser(self.valid_xml_file)
        mp.parse()

        self.assertEqual(len(mp.media_file_objs), 2)

        mp.save()

        self.assertEqual(MediaFile.objects.count(), 2)

        manifest = Manifest.objects.get(id=1)
        self.assertEqual(manifest.filename, valid_manifest_file)
        self.assertEqual(manifest.media_files.count(), 2)

    def test_parse_invalid(self):
        with self.assertRaises(ParseError):
            ManifestParser(self.invalid_xml_file).parse()


class MediaFileUploadTestCase(TestCase):
    def setUp(self):
        mp = ManifestParser(open(test_upload_manifest, 'r'))
        mp.parse()
        self.manifest = mp.save()

        self.upload_url = '/upload/%d' % self.manifest.id

    def test_valid_file_upload(self):
        with open(test_upload_1, 'r') as media_file:
            response = self.client.post(self.upload_url, {
                'file': media_file,
            })
        self.assertRedirects(response, self.upload_url)

    def test_wrong_file_upload(self):
        # Try uploading the manifest as a media file for kicks
        with open(test_upload_manifest, 'r') as media_file:
            response = self.client.post(self.upload_url, {
                'file': media_file,
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'The MD5 checksum of the uploaded file does not match the manifest' in response.content
        )