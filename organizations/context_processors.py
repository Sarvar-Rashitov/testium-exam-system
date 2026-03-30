def organization_settings(request):
    """Add organization settings to all templates"""
    if request.user.is_authenticated and hasattr(request.user, 'settings'):
        return {
            'org_settings': request.user.settings
        }
    return {}
