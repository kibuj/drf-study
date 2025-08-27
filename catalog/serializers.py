from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Resort, Tag

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_password(self, data):
        validate_password(data)
        return data

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data.get('email',''))
        user.set_password(validated_data['password']) #перетворює в хеш, User(...), не канає, бо Django приймає тільки хеш паролів
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

    def create(self, validated_data):
        if Tag.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError('Tag with name {} already exists'.format(validated_data['name']))

        user = self.context['request'].user
        return Tag.objects.create(user=user, name = validated_data['name'])

class ResortSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Resort
        fields = ('id','name','description','location','rating','tags','created_at','updated_at')
        read_only_fields = ('id','created_at','updated_at')

    def create(self, validated_data):
        tags = validated_data.pop('tags',[])
        user = self.context['request'].user
        resort =  Resort.objects.create(user=user, **validated_data)
        if tags:
            resort.tags.set(tags)
        return resort

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags',[])
        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()
        if tags:
            instance.tags.set(tags)
        return instance

