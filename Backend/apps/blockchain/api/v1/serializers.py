from rest_framework import serializers


class DeviceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    ip_address = serializers.CharField(max_length=255)
    mac_address = serializers.CharField(max_length=255)
    running_device = serializers.CharField(required=False, allow_blank=True, max_length=1024)
    os_cpe = serializers.CharField(required=False, allow_blank=True, max_length=1024)
    os_details = serializers.CharField(required=False, allow_blank=True, max_length=1024)
    os_guesses = serializers.CharField(required=False, allow_blank=True, max_length=1024)
