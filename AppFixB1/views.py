from AppFixB1.models import App
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from AppFixB1.forms import AppForm, ReportForm
from AppFixB1.models import App, Report


def check_app_owner(request,app):
    if app.owner != request.user:
        raise Http404



def index(request):
    return render(request, 'index.html')


@login_required(login_url='users:login')
def apps(request):
    # """Wyświetlenie wszystkich tematów."""

    apps = App.objects.filter(owner=request.user).order_by('date_added')


    # apps = App.objects.order_by('date_added')
    context = {'apps': apps}
    return render(request, 'apps.html', context)

@login_required
def app(request, app_id):
    app = App.objects.get(id=app_id)

    check_app_owner(request,app)

    reports = app.report_set.order_by('-date_created')
    context = {'app': app, 'reports': reports}
    return render(request, 'app.html', context)

@login_required
def new_app(request):
    if request.method != 'POST':
        # Nie przekazano żadnych danych, należy utworzyć pusty formularz.
        form = AppForm()
    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = AppForm(data=request.POST)
    if form.is_valid():
        app = form.save(commit=False)
        app.owner = request.user

        app.save()
        return redirect('apps')
        # Wyświetlenie pustego formularza.
    context = {'form': form}
    return render(request, 'new_app.html', context)
@login_required
def new_report(request, app_id):
    app = get_object_or_404(App, id=app_id)

    check_app_owner(request,app)
    if request.method != 'POST':
        # Nie przekazano żadnych danych, należy utworzyć pusty formularz.
        form = ReportForm()
    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = ReportForm(data=request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            app.owner = request.user
            report.app = app
            report.id = app.id  # Przypisz poprawny identyfikator reportId_id
            report.save()
            return redirect('apps')

    context = {'form': form, 'app_id': app_id}
    return render(request, 'new_report.html', context)

@login_required
def edit_report(request, report_id):
    #"""Edycja istniejącego wpisu."""
    report = Report.objects.get(id=report_id)
    app = report.app

    check_app_owner(request,app)

    if request.method != 'POST':
        # Żądanie początkowe, wypełnienie formularza aktualną treścią wpisu.
        form = ReportForm(instance=report)
    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = ReportForm(instance=report, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('app', app.id)

    context = {'report': report, 'app': app, 'form': form}
    return render(request, 'edit_report.html', context)