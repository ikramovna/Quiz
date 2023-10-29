from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from rest_framework import serializers

from mirahmad.models import Category, UserAnswer, User
from mirahmad.utils import *
from root.settings import EMAIL_HOST_USER

error_messages = Messages()


# Api Serializers
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['answer']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question']


class CategorySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField('get_questions')

    def get_questions(self, obj):
        questions = Question.objects.filter(category=obj)
        result = []
        for question in questions:
            d = {}
            d['id'] = question.id
            d['question'] = question.question
            choices = Choice.objects.filter(question=question)
            choices_data = [{"id": choice.id, "answer": choice.answer} for choice in choices]
            d['answer'] = choices_data
            result.append(d)
        return result

    class Meta:
        model = Category
        fields = ['questions']


class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description']


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        exclude = ['created_at', 'updated_at', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        if validated_data['end'] is False:
            if check_is_update(validated_data) is False:
                return super().create(validated_data)
            else:
                user_answer = UserAnswer.objects.filter(
                    category_id=validated_data['category'],
                    user=validated_data['user'],
                    question_id=validated_data['question']
                ).first()
                if user_answer:
                    return super().update(user_answer, validated_data)
                else:
                    raise serializers.ValidationError("UserAnswer not found for update")
        elif validated_data['end'] is True:
            UserAnswer.objects.create(question=validated_data['question'],
                                      answer=validated_data['answer'],
                                      user=validated_data['user'],
                                      category=validated_data['category'],
                                      end=True)
            user_answers = UserAnswer.objects.filter(category_id=validated_data['category'])

            return list_user_answers(user_answers)


# Auth Serializers
class UserRegisterSerializer(serializers.ModelSerializer):
    # full_name = serializers.CharField(max_length=125, write_only=True)
    # email = serializers.EmailField(write_only=True)
    # username = serializers.CharField(max_length=125, write_only=True)
    # password = serializers.CharField(max_length=125, write_only=True)

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "username",
            "password",
        ]

    def create(self, validated_data):
        activate_code = random.randint(100000, 999999)
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['is_active'] = False
        user = super().create(validated_data)
        setKey(
            key=validated_data['email'],
            value={
                "user": user,
                "activate_code": activate_code,
            },
            timeout=300,
        )
        print(getKey(validated_data['email']))
        send_mail(
            subject="Subject here",
            message=f"Your activation code: {activate_code}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[validated_data['email']],
            fail_silently=False,
        )

        return user


class CheckActivationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activate_code = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        data = getKey(key=attrs['email'])
        print(data)
        if data and data['activate_code'] == attrs['activate_code']:
            return attrs
        raise serializers.ValidationError(
            {"error": "Error activate code or email"}
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    activation_code = serializers.IntegerField(write_only=True)
    email = serializers.EmailField(write_only=True)
    new_password = serializers.CharField(max_length=150, write_only=True)
    confirm_password = serializers.CharField(max_length=150, write_only=True)  # Add this field

    def validate(self, attrs):
        user = User.objects.filter(email=attrs.get('email')).first()
        if not user:
            raise serializers.ValidationError({"email": "Email not found"})

        if user.check_activation_code(
                attrs.get('activation_code')):  # Add a method to check the activation code on the User model
            validate_password(attrs.get('new_password'), user)
            return attrs
        else:
            raise serializers.ValidationError({"activation_code": "Invalid activation code"})


class SendEmailResetSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"email": error_messages.EMAIL_NOT_FOUND})
        user = User.objects.get(email=attrs.get('email'))
        self.context['user'] = user
        ActivationEmail(self.context.get('request'), self.context).send([user.email])
        return attrs
