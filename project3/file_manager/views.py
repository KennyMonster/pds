from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from sendfile import sendfile, os
from forms import ManifestForm, MediaFileForm
from models import Manifest, MediaFile


def manifest_upload(request):
    """
    Form for uploading manifest files
    """
    form = ManifestForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        manifest = form.save()
        return HttpResponseRedirect(reverse('file-upload', args=(manifest.id,)))

    return render(request, 'file_manager/manifest_upload.html', {
        'form': form,
    })


def media_file_upload(request, manifest_id):
    """
    Form for uploading individual media files associated with a manifest
    """
    manifest = get_object_or_404(Manifest, id=manifest_id)

    manifest_files = MediaFile.objects.filter(manifest=manifest)
    total_files_count = manifest_files.count()
    files_needing_upload = manifest_files.filter(file='')
    files_needing_upload_count = files_needing_upload.count()

    file_to_upload = files_needing_upload.first()

    # If no files left to upload, mark the manifest complete and move on
    if files_needing_upload_count < 1:
        Manifest.objects.filter(id=manifest.id).update(all_media_present=True)
        return HttpResponseRedirect(reverse('manifest-view', args=(manifest.id,)))

    form = MediaFileForm(request.POST or None, request.FILES or None, instance=file_to_upload)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('file-upload', args=(manifest.id,)))  # Refresh view

    return render(request, 'file_manager/file_upload.html', {
        'form': form,
        'upload_number': total_files_count - files_needing_upload_count + 1,  # Which place in order of upload e.g. 2 of 3
        'total_files_count': manifest_files.count(),
        'file_to_upload': file_to_upload,
    })


def manifest_view(request, manifest_id):
    """
    Detail view of the contents of the manifest
    """
    manifest = get_object_or_404(Manifest, id=manifest_id)

    # If files left to upload, redirect back to file upload screen
    manifest_files = MediaFile.objects.filter(manifest=manifest).filter(file='')
    if manifest_files.count() > 0:
        return HttpResponseRedirect(reverse('file-upload', args=(manifest.id,)))

    return render(request, 'file_manager/manifest_view.html', {
        'manifest': manifest,
    })


def media_file_download(request, media_file_id):
    """
    Use x-sendfile to get the client facing web server to send down
    the requested file, so the Django app server doesn't have to

    Probably also useful to use the correct filename as well
    """
    media_file = get_object_or_404(MediaFile, id=media_file_id)
    full_path = os.path.join(settings.MEDIA_ROOT, str(media_file.file))
    return sendfile(request, full_path, attachment=True, attachment_filename=media_file.filename)