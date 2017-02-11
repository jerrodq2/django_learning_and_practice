


# Helper functions I use repeatedly

def check_id(request):
    if not 'id' in request.session:
        return redirect(reverse('br:index'))

def check_method(request):
    if request.method != 'Post':
        return redirect(reverse('br:index'))
def flash_messages(request, errors):
    for error in errors:
        messages.info(request, error)
