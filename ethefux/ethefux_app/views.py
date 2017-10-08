from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from web3 import Web3, HTTPProvider
from ethefux_app.models import ContractProposal,DeployConfirmation,Contract
from ethefux_app.forms import LoanForm
import random


web3 = Web3(HTTPProvider('http://localhost:8545'))

def index(request):
    context_dict = {}
    return render(request, 'index.html', context_dict)


def about(request):
    return render(request, 'about.html')

def account(request):
    return render(request, 'account.html')

@login_required
def dashboard(request):
    context_dict = {}
    profile = request.user.user_profile
    context_dict["credit_score"] = 100

    prop_lend = list(ContractProposal.objects.filter(lender=request.user.user_profile))
    for x in prop_lend: x.party = x.borrower

    prop_borrow = list(ContractProposal.objects.filter(borrower=request.user.user_profile))
    for x in prop_borrow: x.party = x.borrower

    context_dict["proposed_contracts"] = {"lend":prop_lend, "borrow":prop_borrow}

    loan_data =  list(Contract.objects.filter(borrower=request.user.user_profile))
    loans = None

    if len(loan_data) > 0: 
        loans = {
            "red":[],
            "green":[]
        }
        for loan in loan_data:
            loan.due = (loan.amount * loan.interest_rate)/ loan.duration

            if random.randint(0,1)==0:
                loans.red.append(loan)
            else:
                loans.green.append(loan)
        

    lends =  list(Contract.objects.filter(lender=request.user.user_profile))

    context_dict["current_loans"] = loans
    context_dict["current_lends"] = lends

    context_dict["total_contracts"] = len(loan_data) + len(lends)
    return render(request, 'dashboard.html', context_dict)

# Propose a contract to a debtor
@login_required
def propose_contract(request):
    context_dict = {}
    loanForm = LoanForm()

    if request.method == "POST":
        loanForm = LoanForm(request.POST)

        if loanForm.is_valid():
            data = loanForm.cleaned_data
            party = User.objects.get(username = data["party"])

            if(party):      
                loanProposal = ContractProposal.objects.create(lender=request.user.user_profile, borrower=party.user_profile,amount=data["amount"], 
                                                               duration=data["duration"], interest_rate=data["interest_rate"])
                loanProposal.save()

                #Ask other party for confirmation
                DeployConfirmation.objects.create(contract=loanProposal, confirmer=party.user_profile)
                return HttpResponseRedirect(reverse("ethefux_app:dashboard"))

    context_dict["form"] = loanForm
    return render(request, "ethefux_app/propose_contract.html", context_dict)


# Request a loan from a loaner
@login_required
def request_contract(request):
    context_dict = {}
    loanForm = LoanForm()

    if request.method == "POST":
        loanForm = LoanForm(request.POST)

        if loanForm.is_valid():
            data = loanForm.cleaned_data
            party = User.objects.get(username = data["party"])

            if(party):      
                loanProposal = ContractProposal.objects.create(lender=party.user_profile, borrower=party.user_profile,amount=data["amount"], 
                                                               duration=data["duration"], interest_rate=data["interest_rate"])
                loanProposal.save()

                #Ask other party for confirmation
                DeployConfirmation.objects.create(contract=loanProposal, confirmer=party.user_profile)
                return HttpResponseRedirect(reverse("ethefux_app:dashboard"))
    context_dict["form"] = loanForm
    return render(request, "ethefux_app/request_contract.html", context_dict)

# Show a potential contract to a user and allow them to accept/decline it
@login_required
def accept_contract(request):
    context_dict = {}
    if request.method == "POST":
        contractid = request.POST.get("contract_id")
        proposal = ContractProposal.objects.get(id=contractid)
        
        if(proposal is not None):
            # Check if user is part of the contract
            present = False

            parties = DeployConfirmations.objects.filter(contract=proposal)

            for party in parties:
                if party.confirmer == request.user.user_profile:
                    present = True
                    break

            if(present==True):
                
                # Check if user has accepted or declined
                accepted = request.POST.get("accepted")
                
                if(accepted is not None):
                    if accepted == True:
                        # Try to deploy the contract
                        return deploy_contract(request)
                else:
                    # Decline the proposed contract and notify other parties
                    proposal.delete()
                    return False

    return False


# Deploy
@login_required
def deploy_contract(request):
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
            contract = web3.eth.Contract(abi)
            contract.deploy({'from': proposal.lender.wallet.address}, [proposal.lender.wallet.address, proposal.borrower.wallet.address,
                                                                       proposal.amount, proposal.duration, proposal.interest_rate])

            Contract.objects.create(lender=proposal.lender, borrower=proposal.borrower, amount=proposal.amount, 
                                    duration=proposal.duration, interest_rate=proposal.interest_rate, address=contract.address)
            return True
    return False

