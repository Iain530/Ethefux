from django.contrib.auth.models import User
from django.db import models
from web3 import Web3, IPCProvider
from django.db import models
from ethefux.settings import ENABLE_ETH

web3 = Web3(IPCProvider(testnet=True))

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    wallet = models.ForeignKey("Wallet")
    credit_score = models.IntegerField(default=100)

    def save(self, *args, **kwargs):
        if self.pk is None:
            try:
                wallet = self.wallet
            except Wallet.DoesNotExist:
                if ENABLE_ETH:
                    self.wallet = Wallet.objects.create(address=str(web3.personal.newAccount('password')))
                else:
                    self.wallet = Wallet.objects.create()

            self.wallet.save()

        super(UserProfile, self).save()

# For keeping track of wallets
class Wallet(models.Model):
    address = models.CharField(max_length=42, default="0x255750c6f883f5d470ea7ed4a9a33ca56c890cd8")

# A deployed contract
class Contract(models.Model):
    address = models.CharField(max_length=42)
    parties = models.ManyToManyField("UserProfile")

# A proposed contract between some parties, will be deployed after all parties confirm
class ContractProposal(models.Model):
    partyconfirmations = models.ManyToManyField("DeployConfirmation")
    
# A confirmation by a party for a contract
class DeployConfirmation(models.Model):
    contract = models.ForeignKey("Contract")
    confirmer = models.ForeignKey("UserProfile")
