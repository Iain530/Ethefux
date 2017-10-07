from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ethefux_app.forms import LoanForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

def index(request):
    context_dict = {}
    return render(request, 'index.html', context_dict)


def about(request):
    return render(request, 'about.html')


# Propose a contract to a debtor
@login_required
def proposeContract(request):
    context_dict = {}
    loanForm = LoanForm()

    if request.method == "POST":
        loanForm = LoanForm(request.POST)

        if loanForm.is_valid():

            party = User.objects.get(username = loanForm.party)

            if(party):      
                loanProposal = ContractProposal.objects.create(loaner=request.user.userprofile, amount=loanForm.amount, 
                                                               duration=loanForm.duration, interest_rate=loanForm.interest_rate)
                loanProposal.save()

                #Ask other party for confirmation
                DeployConfirmation.objects.create(contract=loanProposal, confirmer=party.userprofile)

    context_dict["form"] = loanForm
    return render(request, "ethefux_app/propose_contract.html", context_dict)


# Request a loan from a loaner
@login_required
def requestContract(request):
    context_dict = {}
    loanForm = LoanForm()

    if request.method == "POST":
        loanForm = LoanForm(request.POST)

        if loanForm.is_valid():

            party = User.objects.get(username = loanForm.party)

            if(party):      
                loanProposal = ContractProposal.objects.create(loaner=party.userprofile, amount=loanForm.amount, 
                                                               duration=loanForm.duration, interest_rate=loanForm.interest_rate)
                loanProposal.save()

                #Ask other party for confirmation
                DeployConfirmation.objects.create(contract=loanProposal, confirmer=party.userprofile)

    context_dict["form"] = loanForm
    return render(request, "ethefux_app/request_contract.html", context_dict)

# Show a potential contract to a user and allow them to accept/decline it
@login_required
def acceptContract(request):
    context_dict = {}

    if request.method == "POST":
        contractid = request.POST.get("contract_id")
        proposal = ContractProposal.objects.get(id=contractid)
        
        if(proposal is not None):
            # Check if user is part of the contract
            present = False

            if proposal.loaner != request.user.userprofile:
                parties = DeployConfirmations.objects.filter(contract=proposal)

                for party in parties:
                    if party.confirmer == request.user.userprofile:
                        present = True
                        break
            else:
                present = True

            if(present==True):
                
                # Check if user has accepted or declined
                accepted = request.POST.get("accepted")
                
                if(accepted is not None):
                    if accepted == True:
                        # Try to deploy the contract
                        pass
                else:
                    # Decline the proposed contract and notify other parties
                    pass

    return render(request, "ethefux_app/accept_contract.html", context_dict)
    

# Deploy 
@login_required
def deployContract(request):
    if request.method == "POST":
        contractid = request.POST.get("contract_id")
        proposal = ContractProposal.objects.get(id=contractid)

        if(proposal):
            confirmations = DeployConfirmation.objects.filter(contract=proposal)
            
            for confirmation in confirmations:
                if confirmation.confirmed != True:
                    # Can't deploy contract as parties are not agreed
                    return False

            # Deploy Contract
            return True
    return False


