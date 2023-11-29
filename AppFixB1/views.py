import os

from django.utils import timezone

from AppFixB1.models import App, User, UserCompany, Company, Invitation, RoleCompany, AppCompany
from django.contrib.auth.decorators import login_required
from django.http import Http404, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from AppFixB1.forms import AppForm, ReportForm, CompanyForm
from AppFixB1.models import App, Report


def check_app_owner(request, app):
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
            return redirect('app', app_id=app_id)
    else:
        form = ReportForm()

    context = {'form': form, 'app_id': app_id}
    return render(request, 'new_report.html', context)


@login_required
def edit_report(request, report_id):
    # """Edycja istniejącego wpisu."""
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
    print(user)
    user_company = UserCompany.objects.filter(user=user).first()

    context = {}
    if user_company:
        # The user is part of a company or has created a company
        company = user_company.company
        context['company'] = company
    return render(request, 'company.html', context)


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


def company_invitations(request):
    user = request.user
    user_company = UserCompany.objects.filter(user=user).first()

    context = {}
    if user_company:
        # The user is part of a company or has created a company
        company = user_company.company
        context['company'] = company
    else:
        invitations = Invitation.objects.all()
        context['invitations'] = invitations
    if request.method == "POST":
        invitation_id = request.POST.get("invitation_id")
        try:
            invitation = Invitation.objects.get(pk=invitation_id)

            if "accept_invite" in request.POST:
                invitation.is_accepted = True
                user_company, created = UserCompany.objects.get_or_create(user=user,
                                                                          defaults={'company': invitation.company,
                                                                                    'role_company': RoleCompany.TESTER.value})

                if created:
                    print(user_company.user.login)  # Example to access the login field of the related User object
                    print(user_company.company.name)  # Example to access the name field of the related Company object
                return redirect('company')
            elif "decline_invite" in request.POST:
                invitation.is_accepted = False

            invitation.save()
        except Invitation.DoesNotExist:
            pass  # Handle the case when the invitation is not found
    return render(request, 'company_invitations.html', context)


def leave_company(request):
    # Assuming you have a user_company relationship for the logged-in user
    user_company = request.user.usercompany

    if user_company:
        # If the user is part of a company, remove them from the company
        user_company.delete()

    return redirect(
        'company')  # Replace 'company_home' with the URL name of the page where you want to redirect after leaving the company



def company_invite_user(request):
    if request.method == 'POST':
        # Get the username entered in the form
        us = request.user
        username = request.POST.get('AppFix_profile')
        print(username)
        try:
            # Check if the user exists in the database
            user = User.objects.get(login=username)
            print(user.login)
            # Check if the user is already part of a company
            # if user.usercompany:
            #     return render(request, 'user_already_in_company.html', {'user': user})

            # Assuming you have a company for the current user (you can customize this logic)
            company = Company.objects.get(owner=request.user.id)

            # Create an invitation for the user
            invitation = Invitation.objects.create(sender=request.user, recipient=user, company = company)
            invitation.save()

            return render(request, 'company.html')

        except User.DoesNotExist:
            return render(request, 'company_members.html')

    return render(request, 'company_invite_user.html')


def company_apps(request):
    # """Wyświetlenie wszystkich tematów."""
    user = request.user
    apps = AppCompany.objects.filter(company=user.usercompany.company).order_by('app__date_added')

    # apps = App.objects.order_by('date_added')
    context = {'apps': apps, 'user': user}
    return render(request, 'company_apps.html', context)


def company_new_app(request):
    # """Wyświetlenie wszystkich tematów."""
    user = request.user
    apps = App.objects.filter(owner = user ).order_by('date_added')

    # apps = App.objects.order_by('date_added')
    context = {'apps': apps, 'user': user}
    return render(request, 'company_new_app.html', context)


def company_add_app(request,app_id):

    return redirect('company_apps')

def doc(request):
    return render(request, 'doc.html')
def download(request):
    return render(request, 'download.html')


def download_file(request):
    file_path = os.path.join(os.path.dirname(__file__), 'static/Projekt.pdf')
    response = FileResponse(open(file_path, 'rb'))

    # Set the Content-Disposition header to force download
    response['Content-Disposition'] = 'attachment; filename="Projekt.pdf"'

    return response

@login_required
def reportPy(request):
    return None