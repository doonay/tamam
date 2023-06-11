from rest_framework import serializers

class XboxGameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_id = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)
    platforms = serializers.ListField(child=serializers.CharField(max_length=255))
    base_price = serializers.IntegerField()
    discounted_price = serializers.IntegerField()
    discount = serializers.IntegerField()
    img = serializers.CharField()
    last_modified = serializers.DateTimeField()
