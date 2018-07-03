from django.contrib import admin

from sale.models import *

class StockAdmin(admin.ModelAdmin):
	list_display = 'stock_code', 'stock_patch', 'stock_number'

class CommdityAdmin(admin.ModelAdmin):
	list_display = 'commdity_code', 'commdity_name', 'commdity_mod', 'commdity_category', 'commdity_price'

class TransferAdmin(admin.ModelAdmin):
	list_display = 'transfer_code', 'transfer_patch', 'transfer_number', 'transfer_off', 'transfer_position'

	list_filter = 'transfer_position',
	search_fields = 'transfer_code', 'transfer_patch','transfer_position'
class CategoryAdmin(admin.ModelAdmin):
	list_display = 'category_name',

class ModAdmin(admin.ModelAdmin):
	list_display = 'mod_name', 'mod_gram'

class PositionAdmin(admin.ModelAdmin):
	list_display = 'position_name', 'position_phone', 'position_manager'

class TemplateCategoryAdmin(admin.ModelAdmin):
	list_display = 'title',

class PatchAdmin(admin.ModelAdmin):
	list_display = 'patch_commdity', 'patch_code', 'patch_product', 'patch_validity'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Mod, ModAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Commdity, CommdityAdmin)
admin.site.register(Transfer, TransferAdmin)
admin.site.register(TemplateCategory, TemplateCategoryAdmin)
admin.site.register(Patch, PatchAdmin)