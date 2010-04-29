from django.db import models

class BannerManager(models.Manager):
  def magic(self):
    weights = []
    for b in super(BannerManager, self).get_query_set():
      weight = 0
      while weight < b.weight:
        weights.append(b.id)
        weight+=1
    import random
    random_selection = random.choice(weights)
    banner = super(BannerManager, self).get(pk=random_selection)
    # banner.impressions+=1
    # banner.save()
    return banner
    
class Banner(models.Model):
  WEIGHT_CHOICES = (
    (0, "00 - Never Show"),
    (1, "01"),
    (2, "02"),
    (3, "03"),
    (4, "04"),
    (5, "05"),
    (6, "06"),
    (7, "07"),
    (8, "08"),
    (9, "09"),
    (10, "10 - Always Show"),
  )
   
  name = models.CharField(max_length=255)
  href = models.URLField(max_length=255)
  height = models.CharField(editable=False, max_length=5, null=True, blank=True)
  width = models.CharField(editable=False, max_length=5, null=True, blank=True)
  banner_image = models.ImageField(upload_to="images/adto", height_field="height", width_field="width", max_length=255, null=True, blank=True)
  swf_file = models.TextField(verbose_name="Flash Embed Code", null=True, blank=True)
  impressions = models.IntegerField(editable=False, default=0)
  clicks = models.IntegerField(editable=False, default=0)
  weight = models.IntegerField(choices=WEIGHT_CHOICES)
  objects = BannerManager()
  
  def __unicode__(self):
    return self.name
    
  def impression(self):
    self.impressions = self.impressions+1
    self.save()
    
  def click(self): 
    self.clicks +=1
    
  def banner_markup(self):
    self.impression()
    if self.banner_image:
      return u'<a href="/affiliate/%s" target="_blank"><img src="/media/%s" /></a>\r\n' % (self.id, self.banner_image)
    else:
      return u'<div class="swf">%s</div>' % (self.swf_file)

  def clean(self):
    if self.banner_image and self.swf_file:
      raise ValidationError('You can\'t have both an image and a flash file')
    else:
      if self.banner_image == "" and self.swf_file == "":
        raise ValidationError('You must add either an image or a flash file')
    super(Banner, self).clean()
    
class Referrer(models.Model):
  href = models.URLField(max_length=255)
  time = models.DateTimeField(auto_now_add=True)
  banner = models.ForeignKey(Banner)
  
  def __unicode__(self):
    return "Click from %s at %s" % (self.href, self.time)
