from django.contrib.auth.models import Group,Permission

def create_group_permission(sender, **kwargs):
    try:
        reader,created = Group.objects.get_or_create(name='Readers')
        authors,created = Group.objects.get_or_create(name='Authors')
        editors,created = Group.objects.get_or_create(name='Editors')

        reader_permissions= [Permission.objects.get(codename='view_detail')]

        authors_permissions= [Permission.objects.get(codename="add_detail"),Permission.objects.get(codename="change_detail"),Permission.objects.get(codename="delete_detail")]

        can_publish,created = Permission.objects.get_or_create(codename="can_publish", content_type_id=7,name="can Publish detail")

        editors_permissions= [can_publish,Permission.objects.get(codename="add_detail"),Permission.objects.get(codename="change_detail"),Permission.objects.get(codename="delete_detail")]

        reader.permissions.set(reader_permissions)
        editors.permissions.set(editors_permissions)
        authors.permissions.set(authors_permissions)
        print("signals is sucessfull")
    except Exception as e:
        print(f"An error occured {e}")