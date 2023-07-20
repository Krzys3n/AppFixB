from AppFixB1.models import App, User, UserCompany, Company
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from AppFixB1.forms import AppForm, ReportForm, CompanyForm
from AppFixB1.models import App, Report


def check_app_owner(request,app):
    if app.owner != request.user:
        raise Http404



def index(request):
    return render(request, 'index.html')


@login_required(login_url='users:login')
def apps(request):
    # """Wyświetlenie wszystkich tematów."""

    apps = App.objects.order_by('date_added')
    user = request.user


    # apps = App.objects.order_by('date_added')
    context = {'apps': apps, 'user': user}
    return render(request, 'apps.html', context)

@login_required
def app(request, app_id):
    app = App.objects.get(id=app_id)



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

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.app = app
            report.save()
            return redirect('app', app_id = app_id)
    else:
        form = ReportForm()

    context = {'form': form, 'app_id': app_id}
    return render(request, 'new_report.html', context)

@login_required
def edit_report(request, report_id):
    #"""Edycja istniejącego wpisu."""
    report = Report.objects.get(id=report_id)
    app = report.app



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

def view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)


    user_company = UserCompany.objects.filter(user=user).first()

    if not user_company:
        user_company = 'No Company'

    report_count = Report.objects.filter(user=user).count()
    context = {'user': user, 'user_company': user_company, 'report_count': report_count}
    return render(request, 'view_profile.html', context)

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':

        discord_profile = request.POST.get('discord_profile')
        github_profile = request.POST.get('github_profile')
        linkedin_profile = request.POST.get('linkedin_profile')
        twitter_profile = request.POST.get('twitter_profile')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')


        user.discord_profile = discord_profile
        user.github_profile = github_profile
        user.linkedin_profile = linkedin_profile
        user.twitter_profile = twitter_profile
        user.phone_number = phone_number
        user.email = email
        user.save()

        return redirect('view_profile', user.id)
    else:
        initial_data = {

            'discord_profile': user.discord_profile,
            'github_profile': user.github_profile,
            'linkedin_profile': user.linkedin_profile,
            'twitter_profile': user.twitter_profile,
            'phone_number': user.phone_number,
            'email': user.email
        }
        return render(request, 'edit_profile.html', {'initial_data': initial_data})

@login_required
def company(request):
    user = request.user
    user_company = UserCompany.objects.filter(user=user).first()




    context = {}
    if user_company:
        # The user is part of a company or has created a company
        company = user_company.company
        context['company'] = company
    return render(request, 'company.html', context)


class CompanyUser:
    pass


@login_required
def new_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            # Create a new company instance but do not save it yet.
            new_company = form.save(commit=False)
            # Set the owner of the company to the currently logged-in user.
            new_company.owner = request.user
            # Save the new company to the database.
            new_company.save()

            UserCompany.objects.create(user=request.user, id_company=new_company, role_company='Boss')
            # Redirect to a success page or any other desired URL.
            return redirect('company')
    else:
        # If the request method is GET, create an empty form to display to the user.
        form = CompanyForm()

    context = {'form': form}
    return render(request, 'new_company.html', context)


@login_required
def company_members(request):
    # Assuming you want to get the company members for the currently logged-in user
    user = request.user

    # Fetch the CompanyUser object associated with the current user
    company_user = UserCompany.objects.get(user=user)

    # Fetch all users associated with the same company as the current user
    company_users = UserCompany.objects.filter(company=company_user.company)

    context = {'companyUsers': company_users}
    return render(request, 'company_members.html', context)
