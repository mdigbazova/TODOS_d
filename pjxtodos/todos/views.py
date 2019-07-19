from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework import permissions, renderers
import django_filters.rest_framework
from rest_framework import filters

from . models import Profile, Todo
from . serializers import UserSerializer, UserCreateSerializer, ProfileSerializer, TodoSerializer, TodoCreateSerializer
from . permissions import IsOwnerOrReadOnly
from . method_serializer_view import MethodSerializerView

from . filters import TodoFilter

# Create your views here.


class TodosList(MethodSerializerView, generics.ListCreateAPIView):
    queryset = Todo.objects.all()#RetrieveUpdateDestroyAPIView supports CRUD-like functionality
    serializer_class = TodoSerializer

    method_serializer_classes = {
        ('GET',): TodoSerializer,
        ('POST'): TodoCreateSerializer
    }

    # only authenticated users to be able to create, update, and delete code snippets.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class TodosDetail(MethodSerializerView, generics.RetrieveUpdateDestroyAPIView): #
    queryset = Todo.objects.all() # to create a read-only endpoint that lists
    #all available todoinstances
    serializer_class = TodoCreateSerializer

    method_serializer_classes = {
        ('GET'): TodoSerializer,
        ('PUT', 'PATCH'): TodoCreateSerializer,
    }

    # only authenticated users to be able to create, update, and delete todos.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    """
    To automatically associate the logged-in user with created todo - by overriding 
    .perform_create() method on the todo view - that let's modify how an instance is saved.
    """
    # def perform_create(self, serializer):
    #     import pdb; pdb.set_trace ()
    #     serializer.save(owner=self.request.user)
    # def create(self, validated_data): #
    #     #import pdb; pdb.set_trace()
    #     validated_data['owner'] = self.context['request'].user
    #     return super(TodoSerializer, self).create(validated_data)



"""
To add two new read-only views for a list of all users and a detail view of individual users.
I use the generic class-based RetrieveAPIView for the read-only detail view.
"""



#------------------------


class RegisterUser(MethodSerializerView, generics.ListCreateAPIView):
    permissions_classes = [permissions.AllowAny, ]

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    method_serializer_classes = {
        ('POST'): UserCreateSerializer
    }

#------------------------

class UserList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

"""
To add two new read-only views for a list of all users and a detail view of individual users.
I use the generic class-based RetrieveAPIView for the read-only detail view.
"""


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

"""
Highlighted Todos Endpoint -  there’s no existing generic view that will work 
so is needed to create my own .get() method.
"""
class TodoDetail(generics.GenericAPIView):#TodoHighlight
    queryset = Todo.objects.all ()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        Todo = self.get_object ()
        return Response(Todo.code) #title


#--------------------------

class FilterView(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('title', 'description', 'language')
    ordering_fields = ('title', 'description')


#--------------------------



"""
To have a single entry point to the API - Root API Endpoint
"""
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'todos': reverse('todos-list', request=request, format=format),
        'search': reverse('searcher', request=request, format=format),
    })
