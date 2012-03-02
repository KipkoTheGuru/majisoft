
def checkCredentials(request):
    if request.user.get_group_permissions()==set([u'meter.add_meterreading']):
        return True

def checkDirector(request):
    if request.user.get_group_permissions()==set([u'consumer.change_application']):
        return True

def checkReceptionist(request):
    if request.user.get_group_permissions()==set([u'consumer.add_application', u'consumer.change_consumer', u'consumer.delete_consumer', u'consumer.add_consumer']):
        return True