from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models
from authentication import models as userModel
from datetime import datetime
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from config import API_BASE,SERVER_BASE
import requests
import threading
TOGGLE_USE_API = True

def generate_qr_code(web_url):
    # call api to get qr code
    return

def send_notification(reader,post):
    # Handle Lambda/SES call or API
    return

def get_shortened_url(web_url):
    # Handle shortned url API call
    url = "https://ulvis.net/api.php?url="+web_url
    print(f"API call to : {url}")
    res = requests.get(url)
    return str(res.content)[2:][:-1]

def get_all_posts():
    url = API_BASE+'/posts'
    print(f"API call to : {url}")
    res = requests.get(url)
    return res.json()["posts"]

def get_author_posts(email):
    url = API_BASE+'/author/posts/'+email
    print(f"API call to : {url}")
    res = requests.get(url)
    return res.json()["posts"]

def get_tag_posts(tag):
    url = API_BASE+'/tag/posts/'+tag
    print(f"API call to : {url}")
    res = requests.get(url)
    return res.json()["posts"]

def get_content(id):
    url = API_BASE+f'/post/{id}'
    print(f"API call to : {url}")
    res = requests.get(url)
    return res.json()["post"]

def get_author_name(email):
    url = API_BASE+'/author/'+email
    print(f"API call to : {url}")
    res = requests.get(url)
    return res.json()["author"]

def get_translation(data, lang):
    url = "https://v8aeftpa0i.execute-api.us-west-2.amazonaws.com/default/x2213868Translate"
    print(f"API call to : {url}")
    res = requests.post(url,json={
    "text" : data,
    "to" : lang,
    "from" : "en"
})
    return res.json()["translatedText"]

class api_thread(threading.Thread):
    def __init__(self, func, args):
        super().__init__()
        self.arg = args
        self.result = None
        self.func = func

    def run(self):
        self.result = self.func(self.arg)

def construct_post_preview(args):
    i = args[0]
    postsObjects = args[1]
    colors = args[2]
    url = None
    try:
        url = postsObjects[i]["image"]
    except Exception as e:
        print("No image for", postsObjects[i].title)
    content = ""
    try:
        content = get_content(postsObjects[i]["id"])["content"][:500]
        content += "..."
    except Exception as e:
        print("No content")
    return {
            "id": postsObjects[i]["id"],
            "color": colors[i % len(colors)],
            "image": url,
            "title": postsObjects[i]["title"],
            "subheading": postsObjects[i]["subheading"],
            "content": content,
            "tag": postsObjects[i]["tag"],
        }

def construct_post_edit_grid(args):
    i = args[0]
    postsObjects = args[1]
    colors = args[2]
    url = None
    try:
        url = postsObjects[i]["image"]
    except Exception as e:
        print("No image for", postsObjects[i].title)
    return {
            "id": postsObjects[i]["id"],
            "color": colors[i % len(colors)],
            "image": url,
            "title": postsObjects[i]["title"],
            "subheading": postsObjects[i]["subheading"],
            "tag": postsObjects[i]["tag"],
        }


@require_http_methods(["GET", "POST"])
@login_required(login_url="/auth/")
def posts(request):
    if TOGGLE_USE_API:
        try:
            user = userModel.user.objects.get(email=request.user)
            colors = ["blue", "red", "orange", "green", "yellow", "brown", "grey"]
            postsObjects = get_all_posts()
            threads = []
            for i in range(len(postsObjects)):
                thread = api_thread(construct_post_preview,(i,postsObjects,colors))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
            post = [thread.result for thread in threads]
            return render(
                request, "post_list.html", context={"user_name": user.name, "posts": post}
            )
        except Exception as e:
            print("error:", e)
            return redirect("/auth/")
    else:
        try:
            user = userModel.user.objects.get(email=request.user)
            colors = ["blue", "red", "orange", "green", "yellow", "brown", "grey"]
            postsObjects = models.post.objects.all().order_by("-updated")
            post = list()

            for i in range(len(postsObjects)):
                url = None
                try:
                    url = postsObjects[i].image.url
                except Exception as e:
                    print("No image for", postsObjects[i].title)
                content = ""
                try:
                    content = postsObjects[i].content[:500]
                    content += "..."
                except Exception as e:
                    print("No content")
                post.append(
                    {
                        "id": postsObjects[i].id,
                        "color": colors[i % len(colors)],
                        "image": url,
                        "title": postsObjects[i].title,
                        "subheading": postsObjects[i].subheading,
                        "content": content,
                        "tag": postsObjects[i].tag,
                    }
                )
            return render(
                request, "post_list.html", context={"user_name": user.name, "posts": post}
            )
        except Exception as e:
            print("error:", e)
            return redirect("/auth/")

@require_http_methods(["GET", "POST"])
@login_required(login_url="/auth/")
def myPosts(request):
    if TOGGLE_USE_API:
        user = userModel.user.objects.get(email=request.user)
        colors = ["blue", "red", "orange", "green", "yellow", "brown", "grey"]
        postsObjects = get_author_posts(user.email)
        threads = []
        for i in range(len(postsObjects)):
            thread = api_thread(construct_post_preview,(i,postsObjects,colors))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        post = [thread.result for thread in threads]
        return render(
            request, "myposts.html", context={"user_name": user.name, "posts": post}
        )
    else:
        user = userModel.user.objects.get(email=request.user)
        colors = ["blue", "red", "orange", "green", "yellow", "brown", "grey"]
        postsObjects = models.post.objects.filter(user__email=request.user).order_by(
            "-updated"
        )
        post = list()
        for i in range(len(postsObjects)):
            url = None
            try:
                url = postsObjects[i].image.url
            except Exception as e:
                print("No image for", postsObjects[i].title)
            post.append(
                {
                    "id": postsObjects[i].id,
                    "color": colors[i % len(colors)],
                    "image": url,
                    "title": postsObjects[i].title,
                    "subheading": postsObjects[i].subheading,
                    "tag": postsObjects[i].tag,
                }
            )
        return render(
            request, "myposts.html", context={"user_name": user.name, "posts": post}
        )

@require_http_methods(["GET", "POST"])
@login_required(login_url="/auth/")
def postDetails(request, id, lang):
    if TOGGLE_USE_API:
        postObject = get_content(id)
        print(postObject)
        author = postObject["author"]
        reader = userModel.user.objects.get(email=request.user)
        suggetionObjects = get_author_posts(author)
        subscribed = not models.subscriber.objects.filter(reader__email=reader.email,author__email=author)
        suggestions = list()
        for suggestion in suggetionObjects:
            url = None
            try:
                url = suggestion["image"]
            except Exception as e:
                print("No image for", suggestion.title)
            suggestions.append(
                {
                    "image": url,
                    "title": suggestion["title"],
                    "subheading": suggestion["subheading"],
                    "id": suggestion["id"],
                }
            )
        translated = (lang!="English")
        data = {
            "id" : postObject["id"],
            "image": postObject["image"],
            "title": get_translation(postObject["title"],lang) if translated else postObject["title"],
            "subheading": get_translation(postObject["subheading"],lang) if translated else postObject["subheading"],
            "author": get_translation(get_author_name(author)["name"],lang) if translated else get_author_name(author)["name"],
            "suggestions": suggestions,
            "content": get_translation(postObject["content"],lang) if translated else postObject["content"],
            "isSubscribed" : subscribed,
            "share_link" : get_shortened_url(SERVER_BASE+f"/post/{postObject["id"]}/{lang}"),
            "lang" : lang
        }
        return render(request, "details.html", context=data)
    else:
        postObject = models.post.objects.get(id=id)
        author = postObject.user
        reader = userModel.user.objects.get(email=request.user)
        suggetionObjects = models.post.objects.filter(user__email=postObject.user.email)
        subscribed = not models.subscriber.objects.filter(reader__email=reader.email,author__email=author.email)
        suggestions = list()
        for suggestion in suggetionObjects:
            url = None
            try:
                url = suggestion.image.url
            except Exception as e:
                print("No image for", suggestion.title)
            suggestions.append(
                {
                    "image": url,
                    "title": suggestion.title,
                    "subheading": suggestion.subheading,
                    "id": suggestion.id,
                }
            )
        data = {
            "id" : postObject.id,
            "image": postObject.image.url,
            "title": postObject.title,
            "subheading": postObject.subheading,
            "author": postObject.user.name,
            "suggestions": suggestions,
            "content": postObject.content,
            "isSubscribed" : subscribed
        }
        return render(request, "details.html", context=data)

@require_http_methods(["GET", "POST"])
@login_required(login_url="/auth/")
def createpost(request, id=None):
    title = ""
    subheading = ""
    content = ""
    tag = ""
    image = None
    updated = None
    user = userModel.user.objects.get(email=request.user)
    post_url = "/post/new/"
    if request.method == "GET":
        if id != None:
            post = models.post.objects.get(id=id)
            if post.user.email != str(request.user):
                return redirect("/post/personal/")
            title = post.title
            subheading = post.subheading
            content = post.content
            tag = post.tag
            post_url = f"/post/edit/{id}/"
        return render(
            request,
            "create.html",
            context={
                "title": title,
                "subheading": subheading,
                "content": content,
                "tag": tag,
                "post_url": post_url,
            },
        )
    elif request.method == "POST":
        if id == None:
            # New post
            try:
                image = request.FILES.get("img")
            except Exception as e:
                print("No image data")
            title = request.POST.get("title")
            subheading = request.POST.get("subheading")
            content = request.POST.get("content")
            tag = request.POST.get("tag").strip().capitalize()
            updated = datetime.now()

            new = models.post(
                title=title,
                subheading=subheading,
                content=content,
                tag=tag,
                image=image,
                updated=updated,
                user=user,
            )
            new.save()
            readers = models.subscriber.objects.filter(author__email=user.email)
            for reader in readers:
                send_notification(reader,new)
        else:
            # Update post
            post = models.post.objects.get(id=id)
            try:
                image = request.FILES.get("img")
                if image != None:
                    post.image = image
            except Exception as e:
                print("No image data")
            title = request.POST.get("title")
            subheading = request.POST.get("subheading")
            content = request.POST.get("content")
            updated = datetime.now()
            tag = request.POST.get("tag")

            post.title = title
            post.subheading = subheading
            post.content = content
            post.tag = tag
            post.updated = updated
            post.save()
        return redirect("/post/personal/")

@require_http_methods(["GET", "POST"])
@login_required(login_url="/auth/")
def deletePost(request, id):
    post = models.post.objects.get(id=id)
    if post.user.email == str(request.user):
        post.delete()
    return redirect("/post/personal/")

@require_http_methods(["GET"])
@login_required(login_url="/auth/")
def subscribe(request,post=None):
    if not post:
        return redirect(f'/post/{post}/English')
    reader = userModel.user.objects.get(email=request.user)
    author = models.post.objects.get(id=post).user
    new  = models.subscriber(reader=reader,author=author)
    new.save()
    return redirect(f'/post/{post}/English')

@csrf_exempt
def serve_image(request):
    req_body = json.loads(request.body.decode('utf-8'))
    post_obj = models.post.objects.get(id=req_body["post"])
    image_url = post_obj.image.url 
    return JsonResponse({"url":image_url},status=200) if image_url else JsonResponse({},status=404)
    