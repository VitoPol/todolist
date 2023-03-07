from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from goals.models import GoalCategory
from goals.serializers import GoalCreateSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCreateSerializer
