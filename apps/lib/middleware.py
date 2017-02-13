# from django.http import HttpResponsePermanentRedirect
# from django.conf import settings
#
# class RedirectCorrectHostname(object):
#     """
#     redirects to correct hostname if requested hostname and settings.CORRECT_HOST does not match
#     (at heroku domain redirects to custom domain)
#     """
#     def process_request(self, request):
#         if not getattr(settings, 'CORRECT_HOST', None):
#             return None
#         if request.get_host() == settings.CORRECT_HOST:
#             return None
#
#         return HttpResponsePermanentRedirect(
#             '{scheme}://{host}{path}'.format(scheme=request.scheme,
#                                              host=settings.CORRECT_HOST,
#                                              path=request.get_full_path()))