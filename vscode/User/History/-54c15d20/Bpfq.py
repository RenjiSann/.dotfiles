from datetime import datetime, timedelta
from urllib.parse import urlencode, urlparse, urlsplit

from django.conf import settings
from django.utils.encoding import filepath_to_uri
from storages.backends.s3boto3 import S3Boto3Storage, S3ManifestStaticStorage
from storages.utils import clean_name

import logging

logger = logging.getLogger(__name__)

class GCCBaseStorage(S3Boto3Storage):
    def url(self, name, parameters=None, expire=None, http_method=None):

        # Preserve the trailing slash after normalizing the path.
        name = self._normalize_name(clean_name(name))
        params = parameters.copy() if parameters else {}
        if expire is None:
            expire = self.querystring_expire

        if not self.querystring_auth:
            url_start = self.endpoint_url
            if self.custom_domain:
                url_start = f"{self.url_protocol}//{self.custom_domain}"
            url = "{}/{}/{}{}".format(
                url_start,
                self.bucket.name,
                filepath_to_uri(name),
                "?{}".format(urlencode(params)) if params else "",
            )

            return url

        params["Bucket"] = self.bucket.name
        params["Key"] = name
        url = self.bucket.meta.client.generate_presigned_url(
            "get_object",
            Params=params,
            ExpiresIn=expire,
            HttpMethod=http_method,
        )
        if self.custom_domain:
            parsed = urlsplit(url)
            url = "{}//{}{}?{}".format(
                self.url_protocol, self.custom_domain, parsed[2], parsed[3]
            )
            return url
        return url


class GCCMediaStorage(GCCBaseStorage):
    bucket_name = settings.DJANGO_S3_MEDIA_BUCKET
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    default_acl = "private"


class GCCStaticStorage(GCCBaseStorage):
    bucket_name = settings.DJANGO_S3_STATIC_BUCKET
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    default_acl = "public-read"
    querystring_auth = False
