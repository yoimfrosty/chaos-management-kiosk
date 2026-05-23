from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from functools import wraps


def age_verified_required(view_func):
    """Decorator to ensure user has verified their age before accessing view"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('is_21_plus'):
            # Handle JSON/AJAX requests differently
            if request.headers.get('Content-Type') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'Age verification required',
                    'redirect_url': str(reverse_lazy('kiosk:verify_age'))
                }, status=403)
            
            # Regular requests get redirected
            return redirect(reverse_lazy('kiosk:verify_age'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view
