from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Card, CardItem

from apps.product.models import Product
from apps.product.serializers import ProductSerializer

class getItemsView(APIView):
    def get(self, request, format=None):
        user=self.request.user
        try:
            card=Card.objects.get(user=user)
            card_items=CardItem.objects.order_by('product').filter(card=card)
            result =[]

            if CardItem.objects.filter(card=card).exists():
                for cart_item in card_items:
                    item={}
                    item['id']=cart_item.id
                    item['count']=cart_item.count
                    product=Product.objects.get(id=cart_item.product.id)
                    product=ProductSerializer(product)

                    item['product']=product.data

                    result.append(item)
            return Response({'cart': result}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Something went wrong when retrieving cart items'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddItemView(APIView):
    def post(self, request,format=None):
        user=self.request.user
        data=self.request.data

        try:
            product_id=int(data['product_id'])
        except:
            return Response({'error':'Product ID must be an integer'},status=status.HTTP_404_NOT_FOUND)

        count=1

        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response({'error':'This product does not exist'},status=status.HTTP_404_NOT_FOUND)
            product= Product.objects.filter(id=product_id)
            cart=Card.objects.get(user=user)

            if CardItem.objects.filter(card=cart,product=product).exists():
                return Response({'error': 'Item is already in cart'}, status=status.HTTP_409_CONFLICT)
            
            if int(product.quantity)>0:
                CardItem.objects.create(product=product,cart=cart,count=count)
                if CardItem.objects.filter(cart=cart,product=product).exists():
                    total_items=int(cart.total_items) +1
                    Card.objects.filter(user=user).update(total_items=total_items)

                    cart_items=CardItem.objects.order_by('product').filter(cart=cart)

                    result=[]
    
                    for cart_item in cart_items:
                        item={}
                        item['id']=cart_item.id
                        item['count']=cart_item.count
                        product=Product.objects.get(id=cart_item.product.id)
                        product=ProductSerializer(product)
                        item['product']=product.data
                        result.append(item)
                    return Response({'cart':result},status=status.HTTP_201_CREATED)
                else:
                    return Response({'error':'Not enough of this item in stock'},status=status.HTTP_200_OK)
        except:
            return Response({'error':'Something went wrong when adding item to cart'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetTotalView(APIView):
    def get(self, request,format=None):
        user=self.request.user

        try:
            cart=Card.objects.get(user=user)
            cart_items=CardItem.objects.filter(cart=cart)
            
            total_cost=0.0
            total_compare_cost=0.0

            if cart_items.exists():
                for cart_item in cart_items:
                    total_cost += (float(cart_item.product.price)*float(cart_item.count))
                    total_compare_cost+=(float(cart_item.product.compare_price)*float(cart_item.count))
                
                total_cost=round(total_cost,2)
                total_compare_cost=round(total_compare_cost,2)
            return Response({'total_cost':total_cost,'total_compare_cost':total_compare_cost},status=status.HTTP_200_OK)
        except:
            return Response({'error':'Something went wrong when retrieving total costs'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetItemTotalView(APIView):
    def get(self, request,format=None):
        user=self.request.user

        try:
            cart=Card.objects.get(user=user)
            total_items=cart.total_items
            return Response({'total_items':total_items},status=status.HTTP_200_OK)
        except:
            return Response({'error':'Something went wrong getting total number of items'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateItemView(APIView):
    def put(self, request,format=None):
        user=self.request.user
        data=self.request.data

        try:
            product_id=int(data['product_id'])
        except:
            return Response({'error':'Product ID must be an integer'},status=status.HTTP_404_NOT_FOUND)
        
        try:
            count=int(data['count'])
        except:
            return Response({'error':'Count value must be an integer'},status=status.HTTP_404_NOT_FOUND)
        
        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response({'error':'This product does not exist'},status=status.HTTP_404_NOT_FOUND)
            product=Product.objects.get(id=product_id)
            cart=Card.objects.get(user=user)

            if not CardItem.objects.filter(cart=cart,product=product).exists():
                return Response({'error':'This product is not in your cart'},status=status.HTTP_404_NOT_FOUND)
            
            quantity=product.quantity

            if count <= quantity:
                CardItem.objects.filter(product=product,cart=cart).update(count=count)
                
                cart_items=CardItem.objects.order_by('product').filter(cart=cart)
                result=[]

                for cart_item in cart_items:
                    item={}

                    item['id']=cart_item.id
                    item['count']=cart_item.count
                    product= Product.objects.get(id=cart_item.product.id)
                    product=ProductSerializer(product)

                    item['product']=product.data
                    result.append(item)
                return Response({'cart':result},status=status.HTTP_200_OK)
            else:
                return Response({'error':'Not enough of this item in stock'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            return Response({'error':'Something went wrong when updating cart item'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveItemView(APIView):
    def delete(self, request, format=None):
        user=self.request.user
        data=self.request.data

        try:
            product_id=int(data['product_id'])
        except:
            return Response({'error': 'Product ID must be an integer'},status=status.HTTP_404_NOT_FOUND)
        
        try:
            if not Product.objects.filter(id=product_id).exists():
                return Response({'error':'This product does not exist'},status=status.HTTP_404_NOT_FOUND)
            product=Product.objects.get(id=product_id)
            cart=Card.objects.get(user=user)
            
            if not CardItem.objects.filter(cart=cart,product=product).exists():
                return Response({'error': 'This product is not in your cart'},status=status.HTTP_404_NOT_FOUND)
            
            CardItem.objects.filter(cart=cart,product=product).delete()

            if not CardItem.objects.filter(cart=cart,product=product).exists():
                total_items=int(cart.total_items) -1
                Card.objects.filter(user=user).update(total_items=total_items)
            
            cart_items=CardItem.objects.order_by('product').filter(cart=cart)

            result=[]

            if CardItem.objects.filter(cart=cart).exists():
                for cart_item in cart_items:
                    item={}
                    item['id']=cart_item.id
                    item['count']=cart_item.count
                    product=Product.objects.get(id=cart_item.product.id)
                    product=ProductSerializer(product)
                    item['product']=product.data
                    result.append(item)
            
            return Response({'cart':result},status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Something went wrong when removing item'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmptyCartView(APIView):
    def delete(self, request,format=None):
        user=self.request.user
        try:
            cart=Card.objects.get(user=user)

            if not CardItem.objects.filter(cart=cart).exists():
                return Response({'success':'card Is already empty'},status=status.HTTP_200_OK)
            CardItem.objects.filter(cart=cart).delete()
            Card.objects.filter(user=user).update(total_items=0)
            return Response({'success':'Card emptied successfully'},status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Something went wrong emptying card'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SynchCartView(APIView):
    def put(self, request,format=None):
        user=self.request.user
        data=self.request.data

        try:
            cart_items=data['cart_items']
            
            for cart_item in cart_items:
                cart=Card.objects.get(user=user)

                try:
                    product_id=int(cart_item['product_id'])
                except:
                    return Response({'error':'Product ID must be an integer'},status=status.HTTP_404_NOT_FOUND)

                if not Product.objects.filter(id=product_id).exists():
                    return Response({'error': 'Product with this ID does not exist'},status=status.HTTP_404_NOT_FOUND)
                product=Product.objects.get(id=product_id)
                quantity=product.quantity

                if CardItem.objects.filter(cart=cart,product=product).exists():
                    item=CardItem.objects.get(cart=cart,product=product)
                    count=item.count

                    try:
                        cart_item_count=int(cart_item['count'])
                    except:
                        cart_item_count=1
                    
                    if (cart_item_count + int(count) <= int(quantity)):
                        updated_count=cart_item_count+int(count)
                        CardItem.objects.filter(product=product,cart=cart,count=cart_item_count).update(count=updated_count)

                else:
                    try:
                        cart_item_count = int(cart_item['count'])
                    except:
                        cart_item_count = 1
                    if cart_item_count <= quantity:
                        CardItem.objects.create(cart=cart,product=product,count=cart_item_count)
                        total_items=int(cart.total_items)+1
                        Card.objects.filter(user=user).update(total_items=total_items)
                        if CardItem.objects.filter(cart=cart,product=product).exists():
                            total_items=int(cart.total_items)+1
                            Card.objects.filter(user=user).update(total_items=total_items)

                return Response({'success': 'Cart Synchronized'},status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'Something went wrong when synching cart'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




























