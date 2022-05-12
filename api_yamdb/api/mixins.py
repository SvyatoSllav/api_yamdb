from rest_framework import viewsets, mixins


class CreateListDestroyModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Вьюсет, который может создавать, возвращать и удалять список объектов.
    """
    pass
