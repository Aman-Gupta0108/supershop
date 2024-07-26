from django import template
register = template.Library()


@register.filter(name='paymantMode')
def paymantMode(Request, num):
    if (num == 0):
        return 'COD'
         
    else:
        return 'NetBanking'


@register.filter(name='paymantStatus')
def paymantStatus(Request, num):
    if (num == 0):
        return 'Pending'
         
    else:
        return 'Done'


   


@register.filter(name='orderStatus')
def orderStatus(Request, num):
    if (num == 0):
        return 'Order is Plased'
    elif(num == 1):
        return 'Order is packed'  
    elif(num == 2):
        return 'Ready to Dispatch'
    elif(num == 3):
        return 'Dispatched'
    elif(num == 4):
        return 'Out of Delivery' 
    elif(num == 5):
        return 'Delivered' 
    else:
        return 'out of range'
    


@register.filter(name='paymantCondition')
def paymantCondition(mode, status):
    if (mode == 1 and status == 0):
        return True
         
    else:
        return False