from django.contrib.auth.models import Group, Permission
from meetings.models import Meeting, ActionItem


def setup_permissions():
    admin_group, _ = Group.objects.get_or_create(name="admin")
    editor_group, _ = Group.objects.get_or_create(name="editor")
    viewer_group, _ = Group.objects.get_or_create(name="viewer")

    change_meeting = Permission.objects.get(codename="change_meeting")
    view_meeting = Permission.objects.get(codename="view_meeting")
    add_meeting = Permission.objects.get(codename="add_meeting")

    editor_group.permissions.add(add_meeting, change_meeting, view_meeting)
    viewer_group.permissions.add(view_meeting)

    admin_group.permissions.add(
        Permission.objects.get(codename="add_meeting"),
        Permission.objects.get(codename="change_meeting"),
        Permission.objects.get(codename="delete_meeting"),
        Permission.objects.get(codename="view_meeting"),
    )

    return admin_group, editor_group, viewer_group


def setup_action_item_permissions():
    change_actionitem = Permission.objects.get(codename="change_actionitem")
    view_actionitem = Permission.objects.get(codename="view_actionitem")
    add_actionitem = Permission.objects.get(codename="add_actionitem")

    editor_group = Group.objects.get(name="editor")
    editor_group.permissions.add(add_actionitem, change_actionitem, view_actionitem)

    viewer_group = Group.objects.get(name="viewer")
    viewer_group.permissions.add(view_actionitem)
