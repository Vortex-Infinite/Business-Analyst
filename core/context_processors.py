def user_context(request):
    """Context processor to make user data available globally in templates"""
    if request.user.is_authenticated:
        # Get display name from first_name + last_name or username
        display_name = f"{request.user.first_name} {request.user.last_name}".strip()
        if not display_name:
            display_name = request.user.username
        
        # Get job title from UserProfile if exists, otherwise default
        job_title = "Business Analyst"
        if hasattr(request.user, 'profile') and request.user.profile:
            job_title = request.user.profile.get_role_display()
        
        return {
            'current_user_name': display_name,
            'current_user_title': job_title,
            'current_user_email': request.user.email,
        }
    return {
        'current_user_name': 'Guest User',
        'current_user_title': 'Business Analyst',
        'current_user_email': '',
    }
