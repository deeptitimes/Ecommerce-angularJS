from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets, mixins, status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


from Products import models as product_models
from Products import serializers as product_serializers
from CartSystem.common import cart_system as cart_helper
from CartSystem import serializers as cart_serializers
from CartSystem import models as cart_models


class Wishlist(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = cart_models.WishList.objects.all()
    serializer_class = cart_serializers.WishlistSerializer
    permission_classes = [IsAuthenticated, ]

    def list(self, request):
        wishlist = cart_helper.get_wishlist_by_user(request)
        return Response({"status": True, "data": wishlist}, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            product = product_models.Product.objects.get(
                id=request.data['productId'])
        except (Exception, product_models.Product.DoesNotExist) as e:
            return Response({"data": {"message": "Product does not exists."}}, status=status.HTTP_404_NOT_FOUND)
        if not cart_helper.check_whislist(request, product):
            wishlist = cart_models.WishList.objects.create(
                user=request.user, product=product)
            return Response({"data": {"message": "Product added to wishlist"}}, status=status.HTTP_200_OK)
        else:
            return Response({"data": {"message": "Product is already added to wishlist."}}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def destroy(self, request, pk):
        if cart_helper.delete_from_wishlist(request, pk):
            return Response({"data": {"message": "Successfully removed from wishlist"}}, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "data": {"message": "Could not delete product from wishlist."}}, status=status.HTTP_400_BAD_REQUEST)


class WishlistToCart(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = cart_models.WishList.objects.none()
    serializer_class = cart_serializers.WishlistProduct
    permission_classes = [IsAuthenticated, ]

    def create(self, request):
        if not request.data["quantity"] or not request.data["wishlistId"]:
            return Response({"status": False, "data": {"msg": "Data is missing. Please try again."}}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wishlist = cart_models.WishList.objects.get(
                id=request.data["wishlistId"])
            new_cart = cart_models.AddToCart.objects.get_or_create(
                user=request.user, product=wishlist.product, quantity=request.data["quantity"])
            if new_cart:
                if not wishlist.delete():
                    new_cart.delete()
                    return Response({"status": False, "data": {"msg": "Something went wrong. Please try again."}}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({"status": False, "data": {"msg": "Something went wrong. Please try again."}}, status=status.HTTP_409_CONFLICT)
            return Response({"status": True, "data": {"msg": "Successfully added to cart."}}, status=status.HTTP_200_OK)
        except (Exception, cart_models.WishList.DoesNotExist):
            return Response({"status": False, "data": {"msg": "Data not found."}}, status=status.HTTP_404_NOT_FOUND)


class AddToCart(viewsets.ModelViewSet):
    queryset = cart_models.AddToCart.objects.none()
    serializer_class = cart_serializers.AddToCartSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request):
        try:
            try:
                quantity = request.data['quantity']
                productId = request.data['productId']
            except Exception:
                return Response({"data": {"msg": "Data is missing. Please try again."}}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = product_models.Product.objects.get(
                    id=productId)
            except (product_models.Product.DoesNotExist, Exception) as e:
                return Response({"data": {"message": "Product not found."}}, status=status.HTTP_404_NOT_FOUND)
            if not cart_helper.check_cart(request, product):
                cart = cart_models.AddToCart.objects.create(
                    user=request.user, product=product, quantity=quantity)
                return Response({"data": {"message": "Product added to cart."}}, status=status.HTTP_201_CREATED)
            else:
                return Response({"data": {"message": "Product available in cart."}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception:
            return Response({"data": {"message": "Something went wrong. Please try again."}}, status=status.HTTP_409_CONFLICT)

    def list(self, request):
        cart = cart_helper.get_user_cart(request)
        return Response({"data": {"cartItem": cart[0], "grandTotal": cart[1]}}, status=status.HTTP_200_OK)

    def update(self, request, pk):
        try:
            cart = cart_models.AddToCart.objects.get(pk=pk)
            cart.quantity = request.data['quantity']
            cart.save()
            updated_cart = cart_helper.get_user_cart(request)
            data = {
                "totalPrice": cart.product.price * cart.quantity,
                "grandTotal": updated_cart[1],
                "msg": "Cart Updated."
            }
            return Response({"data": data}, status=status.HTTP_200_OK)
        except (cart_models.AddToCart.DoesNotExist, Exception) as e:
            print(e)
            return Response({"data": {"message": "Cart not found. Please try again."}}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        try:
            cart_models.AddToCart.objects.get(pk=pk).delete()
            updated_cart = cart_helper.get_user_cart(request)
            data = {
                "grandTotal": updated_cart[1],
                "msg": "Item deleted from the cart."
            }
            return Response({"data": data}, status=status.HTTP_200_OK)
        except (Exception, cart_models.AddToCart.DoesNotExist):
            return Response({"data": {"message": "Cart not found."}}, status=status.HTTP_404_NOT_FOUND)
