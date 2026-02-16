# from django.shortcuts import redirect
# from django.urls import reverse

# class RoleBasedAccessMiddleware:

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):

#         if request.user.is_authenticated:

#             # Skip admin panel
#             if request.path.startswith('/admin'):
#                 return self.get_response(request)

#             try:
#                 role = request.user.user_role.role
#             except:
#                 role = 'VIEWER'

#             # Protect Add/Edit/Delete URLs
#             restricted_paths = ['/add/', '/edit/', '/delete/']

#             if role == 'VIEWER':
#                 for path in restricted_paths:
#                     if request.path.startswith(path):
#                         return redirect('event_list')

#             if role == 'MANAGER':
#                 if request.path.startswith('/delete/'):
#                     return redirect('event_list')

#         return self.get_response(request)
