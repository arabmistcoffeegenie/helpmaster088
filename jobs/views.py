from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CVUploadForm
from .models import CVUpload, JobApplication
from .utils import auto_apply_jobs

@login_required
def upload_cv(request):
    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            cv_upload = form.save(commit=False)
            cv_upload.student = request.user
            cv_upload.save()

            # Call the auto-apply function using the uploaded CV file
            # (Assumes a 'postcode' field is in the form or sent via POST; defaults to 'London')
            applications = auto_apply_jobs(cv_upload.cv, location=request.POST.get('postcode', 'London'))

            # Save each application result to the database
            for app in applications:
                JobApplication.objects.create(
                    student=request.user,
                    job_title=app.get('job_title', 'Untitled'),
                    company=app.get('company', 'Unknown'),
                    status=app.get('status', 'Submitted')
                )

            # Redirect to the auto-applied results page
            # You can pass the applications list via session or context if needed.
            return render(request, 'jobs/job_application_results.html', {'applications': applications})
    else:
        form = CVUploadForm()
    return render(request, 'jobs/job_upload_cv.html', {'form': form})

@login_required
def job_application_results(request):
    """
    Displays the results immediately after a CV upload (auto-applied jobs).
    In our flow, this is rendered right after the upload.
    """
    # This view might be used only as a one-time result display.
    # Here, we assume the results were passed in the context from upload_cv.
    # If you need a persistent version, store the results in the database and use job_list.
    return render(request, 'jobs/job_application_results.html')

@login_required
def job_list(request):
    """
    Displays all job applications (auto-applied or manually submitted) for the logged-in user.
    """
    job_apps = JobApplication.objects.filter(student=request.user)
    return render(request, 'jobs/job_list.html', {'job_apps': job_apps})
