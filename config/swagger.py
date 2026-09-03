from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


schema_view = SpectacularAPIView.as_view()


swagger_view = SpectacularSwaggerView.as_view(
    url_name="schema"
)


redoc_view = SpectacularRedocView.as_view(
    url_name="schema"
)