from base.models import Product, Review, Category
from base.serializers import ProductSerializer, CategorySerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response

from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from base.filters import ProductFilter



@api_view(['GET'])
def getProducts(request):
    try:
        query = request.query_params.get('keyword')
        print('query:',query)
        if query == None:
            query =''
        
        products = Product.objects.filter(
            name__icontains=query).order_by('-createdAt')

        page = request.query_params.get('page')
        paginator = Paginator(products, 3)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)
        print('Page:', page)
        serializer = ProductSerializer(products, many=True)
        return Response({'products': serializer.data, 'page':page, 'pages':paginator.num_pages})
    except:
        message = {"detail" : 'something went wrong'}
        return Response(message,status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def getStoreProducts(request):
    try:
        products = Product.objects.all()   
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except:
        message = {"detail" : 'something went wrong'}
        return Response(message,status.HTTP_400_BAD_REQUEST)

#category filter
class FilterProduct(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


#get top products for carousel
@api_view(['GET'])
def getTopProducts(request):
    try:
        products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
        serializer = ProductSerializer(products, many=True)
        
        return Response(serializer.data)
    except:
        message = {"detail" : 'something went wrong'}
        return Response(message,status.HTTP_400_BAD_REQUEST)


#get single product
@api_view(['GET'])
def getProduct(request, pk):
    try:
        product = Product.objects.get(_id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    except:
        message = {"detail" : 'something went wrong'}
        return Response(message,status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    try:
        user = request.user
        product = Product.objects.get(_id = pk)
        data = request.data
        # rating = data['rating']
        
        #1 - review already exists
        alreadyExists = product.review_set.filter(user=user).exists()
        
        if alreadyExists:
            content = {'detail':'Product already reviewed'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        #2 - No rating or 0
        elif data['rating'] == 0:
            content = {'detail':'Please select a rating here'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        #3 - create review
        else:
            review = Review.objects.create(
                user = user,
                product = product,
                name = user.first_name,
                rating = data['rating'],
                comment = data['comment'], 
            )
            
            reviews = product.review_set.all()
            product.numReviews = len(reviews)
            
            total = 0
            for i in reviews:
                total += i.rating
            product.rating = total / len(reviews)
            product.save()
            
            return Response({'Review Addded'})
    except:
        message = {"detail" : 'something went wrong'}
        return Response(message,status.HTTP_400_BAD_REQUEST)    
    
    
    
    
@api_view(['POST'])
def createProduct(request):
    try:
        data = request.data
        print(data)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            response = {
                'data' : serializer.data
            }
            return Response(response)
        else:
            print(serializer.errors)
            return Response(serializer.errors)
    except:
        message = {"detail" : 'something went wrong'}
        return Response(message,status.HTTP_400_BAD_REQUEST)
    
    
#admin update product
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    try:
        data = request.data
        product = Product.objects.get(_id=pk)
        
        product.name = data['name']
        product.price = data['price']
        product.brand = data['brand']
        product.countInStock = data['countInStock']
        product.category = data['category']
        product.description = data['description']
        
        product.save()
        
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    except Exception as e:
        raise e

#admin delete product
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    try:
        product = Product.objects.get(_id=pk)
        product.delete()
        return Response('Product Deleted')
    except:
        message = {"detail" : 'something went wrong'}
        return Response(message,status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def uploadImage(request):
    try:
        data =request.data
        product_id = data['product_id']
        product=Product.objects.get(_id=product_id)
        
        product.image= request.FILES.get('image')
        product.save()
        
        return Response('Image was uploaded')
    except:
        message = {"detail" : 'something went wrong'}
        return Response(message,status.HTTP_400_BAD_REQUEST)
    
    
#admin get category
@api_view(['GET'])
def getCategory(request):
    try:
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
    except:
        message = {"detail" : 'something went wrong'}
        return Response(message,status.HTTP_400_BAD_REQUEST)
    
    
    
#admin view category details
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getCategoryDetails(request, pk):
    try:
        category = Category.objects.get(id=pk)
        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data)
    except:
        message = {"detail" : 'something went wrong'}
        return Response(message,status.HTTP_400_BAD_REQUEST)
    
    

# admin create category
@api_view(['POST'])
@permission_classes([IsAdminUser])
def createCategory(request):
    try:
        category = Category.objects.create(
            category_name='Sample name',
            description=''
        )
        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data)
    except:
        message = {"detail" : 'something went wrong'}
        return Response(message,status.HTTP_400_BAD_REQUEST)
    
    

#admin delete product
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteCategoryt(request, pk):
    try:
        category = Category.objects.get(id=pk)
        category.delete()
        return Response('Product Deleted')
    except:
        message = {"detail" : 'something went wrong'}
        return Response(message,status.HTTP_400_BAD_REQUEST)



#admin update category
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateCategory(request, pk):
    try:
        data = request.data
        category = Category.objects.get(id=pk)
        category.category_name = data['category_name']
        category.description = data['description']
        
        category.save()
        
        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data)
    except:
        message = {"detail" : 'something went wrong'}
        return Response(message,status.HTTP_400_BAD_REQUEST)