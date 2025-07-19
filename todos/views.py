from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render

from .models import TodoItem
from .serializers import TodoItemSerializer
from .utils import translate_text

LANGUAGE_CHOICES = [
    {"code": "es", "name": "Spanish"},
    {"code": "fr", "name": "French"},
    {"code": "de", "name": "German"},
    {"code": "ru", "name": "Russian"},
    {"code": "zh", "name": "Chinese"},
    {"code": "ar", "name": "Arabic"},
    {"code": "ja", "name": "Japanese"},
    {"code": "pt", "name": "Portuguese"},
    {"code": "it", "name": "Italian"},
    {"code": "ko", "name": "Korean"},
    {"code": "hi", "name": "Hindi"},
]

def index(request):
    return render(request, 'todos/index.html', {'languages': LANGUAGE_CHOICES})


class TodoItemViewSet(viewsets.ModelViewSet):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer

    def perform_create(self, serializer):
        language = self.request.data.get('language', 'en')
        instance = serializer.save(language=language)
        if language != 'en':
            translated = translate_text(instance.title, language)
            instance.translated_title = translated
        else:
            instance.translated_title = ''
        instance.save()


    def perform_update(self, serializer):
        # Get the original instance before it's updated
        original_instance = self.get_object()
        original_language = original_instance.language

        # Get new language from request
        new_language = self.request.data.get('language', original_language)
        print("Requested new language:", new_language)
        print("Original instance language:", original_language)

        # Save updated fields (but language isn't yet changed on DB until .save() is called)
        instance = serializer.save()

        if new_language != original_language:
            print("Language has changed — updating translation.")
            if new_language != 'en':
                translated = translate_text(instance.title, new_language)
                instance.translated_title = translated
                print("New translation:", translated)
            else:
                instance.translated_title = ''
                print("Cleared translation for English.")

            instance.language = new_language
            print("Saving updated instance.")
            instance.save()
        else:
            print("Language did not change — no update performed.")


