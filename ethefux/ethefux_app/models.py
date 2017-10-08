from django.contrib.auth.models import User
from django.db import models
from web3 import Web3, HTTPProvider
from django.db import models
from ethefux.settings import ENABLE_ETH
from django.db.models.signals import post_save

web3 = Web3(HTTPProvider('http://localhost:8545'))

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    name = models.CharField(max_length=100)
    identification = models.ImageField(blank=True, null=True)
    home_address = models.CharField(max_length=300)
    wallet = models.ForeignKey("Wallet")
    credit_score = models.IntegerField(default=100)
    verified = models.BooleanField(default=False)

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
    lender = models.ForeignKey("UserProfile", related_name="%(class)s_lender")
    borrower = models.ForeignKey("UserProfile", related_name="%(class)s_borrower")
    amount = models.DecimalField(decimal_places=4, max_digits=100)
    duration = models.IntegerField()
    interest_rate = models.DecimalField(decimal_places=5, max_digits=20)
    address = models.CharField(max_length=42)

# A proposed contract between some parties, will be deployed after all parties confirm
class ContractProposal(models.Model):
   lender = models.ForeignKey("UserProfile", related_name="%(class)s_lender")
   borrower = models.ForeignKey("UserProfile", related_name="%(class)s_borrower")
   amount = models.DecimalField(decimal_places=4,max_digits=100)

   # Duration in months
   duration = models.IntegerField()
   interest_rate = models.DecimalField(decimal_places=5,max_digits=20)
   
# A confirmation by a party for a contract
class DeployConfirmation(models.Model):
    contract = models.ForeignKey("ContractProposal")
    confirmer = models.ForeignKey("UserProfile")
    confirmed = models.BooleanField(default=False)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
