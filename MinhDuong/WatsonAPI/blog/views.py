from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, \
    EntityMention, EntitiesResult

from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
import json
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import LanguageTranslatorV3 as LanguageTranslator
from watson_developer_cloud import NaturalLanguageUnderstandingV1


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    tone_analyzer = ToneAnalyzerV3(
        username='', #get your own API key and password from IBM Watson
        password='',
        version='2016-05-19')

    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2018-07-30',
        username='', #get your own API key and password from IBM Watson
        password='')

    language_translator = LanguageTranslator(
        version='2018-07-22',
        iam_api_key='' #get your API key from IBM Watson
    )

    # print(json.dumps(translation, indent=2, ensure_ascii=False))

    for post in posts:
        posting = post.text
        posting = post.text
        toneObj = json.dumps(tone_analyzer.tone(tone_input=posting,
                                                content_type="text/plain"), indent=2)
        post.toneObj2 = json.loads(toneObj)
        post.angerScore = post.toneObj2['document_tone']['tone_categories'][0]['tones'][0]['score']
        post.disgustScore = post.toneObj2['document_tone']['tone_categories'][0]['tones'][1]['score']
        post.fearScore = post.toneObj2['document_tone']['tone_categories'][0]['tones'][2]['score']
        post.joyScore = post.toneObj2['document_tone']['tone_categories'][0]['tones'][3]['score']
        post.sadScore = post.toneObj2['document_tone']['tone_categories'][0]['tones'][4]['score']

        translation = language_translator.translate(
            text=post.text,
            source='en',
            target='es')

        translationFrench = language_translator.translate(
            text=post.text,
            source='en',
            target='fr')
        obj = json.dumps(translation, indent=2, ensure_ascii=False)
        obj2 = json.dumps(translationFrench, indent=2, ensure_ascii=False)
        post.obj = json.loads(obj)
        post.obj2 = json.loads(obj2)

        post.translationFrench = post.obj2['translations'][0]['translation']
        post.translation = post.obj['translations'][0]['translation']
        post.wordCount = post.obj2['word_count']
        post.characterCount = post.obj2['character_count']

        response = natural_language_understanding.analyze(
            text=posting,
            features=Features(
                entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
                keywords=KeywordsOptions(
                    emotion=True,
                    sentiment=True,
                    limit=2)))

        obj3 = (json.dumps(response, indent=2))
        post.obj3 = json.loads(obj3)
        post.entities = post.obj3['entities']
        post.name = None
        """if ('disambiguation' in post.entities[0]):
                post.name = post.entities[0]['disambiguation']['name']
                post.link = post.entities[0]['disambiguation']['dbpedia_resource']
        else:
            post.name = post.entities[1]['disambiguation']['name']
            post.link = post.entities[1]['disambiguation']['dbpedia_resource']"""
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    tone_analyzer = ToneAnalyzerV3(
        username='', #get your own API key and password from IBM Watson
        password='',
        version='2016-05-19 ')

    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='', #get your own API key and password from IBM Watson
        username='',
        password='T22WEcXkH1J3')

    language_translator = LanguageTranslator(
        version='', #get your own API key and password from IBM Watson
        iam_api_key='GQKCZYnTvRuyF7ETgKfqCrHfmDqi1b7JDsghX76zyYKO'
    )
    posting = post.text
    toneObj = json.dumps(tone_analyzer.tone(tone_input=posting,
                                            content_type="text/plain"), indent=2)
    post.toneObj2 = json.loads(toneObj)
    post.angerScore = post.toneObj2['document_tone']['tone_categories'][0]['tones'][0]['score']
    post.disgustScore = post.toneObj2['document_tone']['tone_categories'][0]['tones'][1]['score']
    post.fearScore = post.toneObj2['document_tone']['tone_categories'][0]['tones'][2]['score']
    post.joyScore = post.toneObj2['document_tone']['tone_categories'][0]['tones'][3]['score']
    post.sadScore = post.toneObj2['document_tone']['tone_categories'][0]['tones'][4]['score']

    translation = language_translator.translate(
        text=posting,
        source='en',
        target='es')

    translationFrench = language_translator.translate(
        text=posting,
        source='en',
        target='fr')
    obj = json.dumps(translation, indent=2, ensure_ascii=False)
    obj2 = json.dumps(translationFrench, indent=2, ensure_ascii=False)
    post.obj = json.loads(obj)
    post.obj2 = json.loads(obj2)

    post.translationFrench = post.obj2['translations'][0]['translation']
    post.translation = post.obj['translations'][0]['translation']
    post.wordCount = post.obj2['word_count']
    post.characterCount = post.obj2['character_count']

    response = natural_language_understanding.analyze(
        text=posting,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(
                emotion=True,
                sentiment=True,
                limit=2)))

    obj3 = (json.dumps(response, indent=2))
    post.obj3 = json.loads(obj3)
    post.entities = post.obj3['entities']
    post.length = len(post.entities)
    post.name = "IBM Watson cannot detect the country's name"
    if 'disambiguation' in post.entities[0]:
        post.disambiguation = post.entities[0]['disambiguation']
        if 'name' in post.disambiguation:
            post.name = post.disambiguation['name']
            post.link = post.disambiguation['dbpedia_resource']
    else:
        if 'disambiguation' in post.entities[1]:
            post.disambiguation = post.entities[1]['disambiguation']
            if 'name' in post.disambiguation:
                post.name = post.disambiguation['name']
                post.link = post.disambiguation['dbpedia_resource']
    # Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
