from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,generics
from .models import ToDo
from .serializers import ToDoSerializer

# @csrf_exempt
# def task_list(request):

# 	if request.method == 'GET':
# 		task_obj = ToDo.objects.all()
# 		serializer_obj = ToDoSerializer(task_obj , many= True)
# 		return JsonResponse(serializer_obj.data, safe= False)

# 	elif request.method == 'POST':
# 		data = JSONParser().parse(request)
# 		serializer_obj = ToDoSerializer(data=data,many=True)
# 		if serializer_obj.is_valid():
# 			serializer_obj.save()
# 			return JsonResponse(serializer_obj.data, status=201,safe=False)
# 		return JsonResponse(serializer_obj.errors, status=400,safe=False)

# 	elif request.method == 'PUT':
# 		data = JSONParser().parse(request)

# 		try:
# 			obj = ToDo.objects.all()
# 		except ToDo.DoesNotExist:
# 			return JsonResponse('object not found',status=status.HTTP_404_NOT_FOUND,safe=False)

# 		serializer_obj = ToDoSerializer(obj,data=data,many=True,allow_add_remove=True)
# 		if serializer_obj.is_valid():
# 			serializer_obj.save()
# 			return JsonResponse(serializer_obj.data, status=201)
# 		return JsonResponse(serializer_obj.errors, status=400)

# 	elif request.method == 'DELETE':
# 		data = JSONParser().parse(request)
# 		try:
# 			obj = ToDo.objects.get(id=data['id'])
# 		except ToDo.DoesNotExist:
# 			return JsonResponse('object not found',status=status.HTTP_404_NOT_FOUND,safe=False)
# 		obj.delete()
# 		return JsonResponse('object deleted',status=status.HTTP_204_NO_CONTENT,safe=False)

# Create your views here.

class Task(APIView):

	# queryset = ToDo.objects.all()

	def get_queryset(self):
		return ToDo.objects.all()

	def get(self,request,format=None):
		task_obj = ToDo.objects.all()
		serializer_obj = ToDoSerializer(task_obj , many= True)
		return JsonResponse(serializer_obj.data, safe= False)

	def post(self,request,format=None):
		
		serializer_obj = ToDoSerializer(data=request.data,many=True)
		if serializer_obj.is_valid():
			serializer_obj.save()
			return Response(serializer_obj.data, status=status.HTTP_201_CREATED)
		return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self,request,format=None):
		data = request.data
		response = []

		for i in data:
			try:
				obj = ToDo.objects.get(id=i['id'])
				serializer_obj = ToDoSerializer(obj,data=i)
				if serializer_obj.is_valid():
					serializer_obj.save()
					response.append({i['id']:serializer_obj.data})
				else:
					response.append({i['id']:serializer_obj.errors})
			except ToDo.DoesNotExist:
				response.append({i['id']:'Object Does not exist'})
			except KeyError:
				response.append({0:'ID not found'})

		return JsonResponse(response,status=200,safe=False)

	def delete(self,request,format=None):
		data = request.data
		response = []

		for i in data:
			try:
				obj = ToDo.objects.get(id=i['id'])
				obj.delete()
				response.append({i['id']:'Object Deleted'})
			except ToDo.DoesNotExist:
				response.append({i['id']:'Object Does not exist'})
			except KeyError:
				response.append({0:'ID not present'})

		return JsonResponse(response,status=200,safe=False)

class FilterTask(generics.ListAPIView):
	queryset = ToDo.objects.all()
	serializer_class = ToDoSerializer
	filter_backends = (DjangoFilterBackend,)
	filter_fields = ('state','date')
