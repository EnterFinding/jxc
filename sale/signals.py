from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.db.models import F

from sale.models import Stock, Transfer

@receiver(post_save, sender=Transfer)
def TransferInToStockSignal(sender, instance, created, **kwargs):
	if not created:
		pass
	detail = {
		'stock_code': instance.transfer_code,
		'stock_patch': instance.transfer_patch
	}
	status = instance.transfer_status
	commdity = Stock.objects.get_or_create(**detail)
	if status in ['100001', '011002']:
		commdity[0].stock_number = F('stock_number') - instance.transfer_number
	if status in ['000101', '011001']:
		commdity[0].stock_number = F('stock_number') + instance.transfer_number
	commdity[0].save()

@receiver(pre_delete, sender=Transfer)
def TransferInToStockSignal(sender, instance, **kwargs):
	detail = {
		'stock_code': instance.transfer_code,
		'stock_patch': instance.transfer_patch
	}
	status = instance.transfer_status
	commdity = Stock.objects.get_or_create(**detail)
	if status in ['100001', '011002']:
		commdity[0].stock_number = F('stock_number') + instance.transfer_number
	if status in ['000101', '011001']:
		commdity[0].stock_number = F('stock_number') - instance.transfer_number
	commdity[0].save()
