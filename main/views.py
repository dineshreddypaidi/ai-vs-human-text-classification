from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from . import models , utils
import json

@csrf_exempt
def login(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            return JsonResponse({"message": "is already authenticated"}, status=405)
        
        content_type = request.headers.get('Content-Type')

        if 'application/json' in content_type:
            try:
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)

        elif 'application/x-www-form-urlencoded' in content_type:
            username = request.POST.get('username')
            password = request.POST.get('password')

        else:
            return JsonResponse({"error": "Unsupported content type"}, status=415)

        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user:
            auth_login(request, user)  # Log in the user
            return JsonResponse({"message": "User loggedin successfully"}, safe=False, status=200)
        else:
            return JsonResponse({"error": "Invalid username or password"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def register(request):
    if request.method == "POST":
        content_type = request.headers.get('Content-Type')

        if 'application/json' in content_type:
            try:
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')
                email = data.get('email')
                name = data.get('name')
                phone_number = data.get('phone')
                
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)

        elif 'application/x-www-form-urlencoded' in content_type:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            name = request.POST.get('name')
            phone_number = request.POST.get('phone')
            
        else:
            return JsonResponse({"error": "Unsupported content type"}, status=415)   

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=405)   

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=405)

        if models.UserProfile.objects.filter(phone_number=phone_number).exists():
            JsonResponse({"error": "Phone already exists"}, status=405)
        
        user_obj = {
            'username' : username,
            'password' : password,
            'email' : email,
            'first_name': name,
        }
        
        user_obj = User.objects.create_user(**user_obj)
        user_obj.save()
        
        profile_obj = models.UserProfile(username=user_obj,no_of_enquires=0,phone_number=phone_number)
        profile_obj.save()
        
        return JsonResponse({"message": "User registered successfully"}, safe=False, status=200)
    
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

@csrf_exempt
def logout(request):
    auth_logout(request)
    return JsonResponse({"message": "logout succesful"}, status=200)

@csrf_exempt
def user(request):
    if request.user.is_authenticated:
        user_obj = User.objects.get(username=request.user)
        try:
            profile_obj = models.UserProfile.objects.get(username=user_obj)
        except models.UserProfile.DoesNotExist:
            profile_obj = None 
            
        user_data = {
            "username": user_obj.username,
            "email": user_obj.email,
            "name" : user_obj.first_name,
            "last login" : user_obj.last_login
        }
        if profile_obj:
            profile_data = {
                "phone number" : profile_obj.phone_number,
                "enquires" : profile_obj.no_of_enquires
                }
        else:
            profile_data = {}
            
        data = {**user_data, **profile_data}    
        return JsonResponse({"data" : data},status=200)
    else:
        return JsonResponse({"message": "is not autenticated"}, status=401)
    
@csrf_exempt
def index(request):
    return JsonResponse({"result": "hello"}, status=200, safe=False)

@csrf_exempt
def predict(request):
    if request.user.is_authenticated:
        user = models.UserProfile.objects.get(username=request.user)
        if request.method == "POST":
            data = json.loads(request.body)
            text = data.get('text')
            predicted_result = utils.predict_text(text)
            
            history = models.History(
                user = user,
                text = text,
                result = predicted_result,
                model_used = "BERT"
            )
            history.save()
            user.no_of_enquires +=1 
            user.save()
            
            return JsonResponse({"result": predicted_result }, status=200, safe=False)
        else:
            return JsonResponse({"error": "Invalid request method"}, status=405)
    else:
            return JsonResponse({"message": "is not autenticated"}, status=401)
    
@csrf_exempt
def history(request):
    if request.user.is_authenticated:
        try:
            user = models.UserProfile.objects.get(username=request.user)
        except models.UserProfile.DoesNotExist:
            return JsonResponse({"message": "userprofile not found"}, status=401)
    else:
        return JsonResponse({"message": "is not autenticated"}, status=401)
    
    historydata = models.History.objects.filter(user=user).all()
    history = [{"user" : hist.user.username.username,
                "text" : hist.text,
                "result" : hist.result,
                }
               for hist in historydata
            ]
    return JsonResponse({"history" : history }, status=200, safe=False)