from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from . models import Profile, Todo


# relationships between entities -> to use hyperlinks
class TodoSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField( view_name='todos:todo-detail', read_only=True, format='html')

    class Meta:
        model = Todo
        fields = ('url', 'id', 'title', 'end_date', 'description', 'state', 'language', 'code', 'owner')



class TodoCreateSerializer(serializers.ModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')
    """
    The source argument used here controls which attribute is used to populate a field and can 
    point to any attribute on the serialized instance.
    """

    url = serializers.HyperlinkedRelatedField(view_name='todos:todo-detail', read_only=True, format='html')
    created_date = serializers.DateField(read_only=True)
    id = serializers.CharField(read_only=True)
    owner = serializers.IntegerField(read_only=True, source='owner.user_id')
    state = serializers.CharField(read_only=True)


    class Meta:
        model = Todo
        fields = ('url', 'id', 'title', 'created_date', 'end_date', 'description', 'state', 'language', 'code', 'owner') #

    """
    To automatically associate the logged-in user with created todo - by overriding 
    .perform_create() method on the todo view - that let's modify how an instance is saved.
    """
    def create(self, validated_data): #return ExampleModel.objects.create(**validated_data)
        #import pdb; pdb.set_trace()
        validated_data['owner'] = self.context['request'].user
        return super(TodoCreateSerializer, self).create(validated_data)


    def save(self, *args, **kwargs):
        return super(TodoCreateSerializer, self).save(*args, **kwargs)  #




class UserSerializer(serializers.ModelSerializer):
    todos = serializers.HyperlinkedRelatedField(many=True, view_name='todos-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'todos')


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

#----------------------


class OwnerSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
            default=serializers.CurrentUserDefault(),
            required=False,
            allow_null=True
        )

    def validate_owner(self, value):
        return self.context['request'].user

#---------------------


class ProfileSerializer(serializers.ModelSerializer):
    #comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('phone_number', 'profession', 'user')

#----------------------