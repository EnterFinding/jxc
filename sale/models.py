#coding:utf8
from django.db import models
from django.db.models import Q, F
from django.contrib.auth.models import User

# Create your models here.

class TemplateCategory(models.Model):
    code = models.CharField(max_length=6)
    title = models.CharField(max_length=12)
    parent = models.ForeignKey('self', verbose_name='归属', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'templatecategory'
        verbose_name = verbose_name_plural = '板块'


class Mod(models.Model):
    mod_name = models.CharField(verbose_name='规格', max_length=64)
    mod_gram = models.CharField(verbose_name='单位', max_length=4)

    def __str__(self):
        return self.mod_name

    class Meta:
        db_table = 'mod'
        verbose_name = verbose_name_plural = '规格'

class Category(models.Model):
    category_name = models.CharField(verbose_name='类名', max_length=24)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'category'
        verbose_name = verbose_name_plural = '分类'

class Commdity(models.Model):
    commdity_code = models.CharField(verbose_name='商品编号', max_length=8)
    commdity_name = models.CharField(verbose_name='商品名称', max_length=64)
    commdity_mod = models.ForeignKey(Mod, verbose_name='规格型号', on_delete=models.CASCADE)
    commdity_category = models.ForeignKey(Category, verbose_name='商品分类', on_delete=models.CASCADE)
    commdity_price = models.DecimalField(verbose_name='单价', max_digits=8, decimal_places=2)

    def __str__(self):
        return self.commdity_name

    class Meta:
        db_table = 'commdity'
        verbose_name = verbose_name_plural = '商品'

class Patch(models.Model):
    patch_commdity = models.ForeignKey(Commdity, verbose_name='商品', on_delete=models.CASCADE)
    patch_code = models.CharField(verbose_name='批号', max_length=16)
    patch_product = models.DateField(verbose_name='生产日期')
    patch_validity = models.DateField(verbose_name='有效日期')

    def __str__(self):
        return self.patch_code

    class Meta:
        db_table = 'patch'
        verbose_name = verbose_name_plural = '批号'

class Position(models.Model):
    position_code = models.CharField(verbose_name='编号', max_length=6)
    position_name = models.CharField(verbose_name='店名', max_length=64)
    position_phone = models.CharField(verbose_name='电话', max_length=20, null=True, blank=True)
    position_manager = models.CharField(verbose_name='店长', max_length=16, null=True, blank=True)

    def __str__(self):
        return self.position_name

    class Meta:
        db_table = 'position'
        verbose_name = verbose_name_plural = '门店'

class Transfer(models.Model):
    status = (
        ('000101', '入库'),
        ('100001', '销售'),
        ('011001', '调入'),
        ('011002', '调出')
    )
    transfer_code = models.ForeignKey(Commdity, verbose_name='商品', on_delete=models.CASCADE)
    transfer_patch = models.ForeignKey(Patch, verbose_name='批号', on_delete=models.CASCADE)
    transfer_number = models.PositiveSmallIntegerField(verbose_name='数量', default=1)
    transfer_off = models.DecimalField(verbose_name='折扣', max_digits=3, decimal_places=2, default=1, null=True, blank=True)
    transfer_status = models.CharField(verbose_name='分类', max_length=6, choices=status, default='1000')
    transfer_position = models.ForeignKey(Position, verbose_name='门店', on_delete=models.CASCADE, default=None, null=True, blank=True)
    
    
    created = models.DateTimeField(verbose_name='操作时间', auto_now_add=True)

    def __str__(self):
        return self.transfer_code.commdity_name

    class Meta:
        db_table = 'transfer'
        verbose_name = verbose_name_plural = '进销'


class Stock(models.Model):
    stock_code = models.ForeignKey(Commdity, verbose_name='商品', on_delete=models.CASCADE)
    stock_patch = models.ForeignKey(Patch, verbose_name='批号', on_delete=models.CASCADE)
    stock_number = models.SmallIntegerField(verbose_name='数量', default=0)

    def __str__(self):
        return self.stock_code.commdity_name

    class Meta:
        db_table = 'stock'
        verbose_name = verbose_name_plural = '库存'

class Subhead(models.Model):
    subhead_user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    subhead_affair = models.CharField(verbose_name='事务', max_length=128)
    max_date = models.DateField(verbose_name='日期上限')

    created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    def __str__(self):
        return self.subhead_affair[:48]

    class Meta:
        db_table = 'subhead'
        verbose_name = verbose_name_plural = '事务交接'

class Activity(models.Model):
    activity_name = models.CharField(verbose_name='活动', max_length=48)
    activity_content = models.TextField(verbose_name='活动内容')
    start_date = models.DateTimeField(verbose_name='开始时间')
    end_date = models.DateTimeField(verbose_name='结束时间')

    def __str__(self):
        return self.activity_name

    class Meta:
        db_table = 'activity'
        verbose_name = verbose_name_plural = '活动列表'