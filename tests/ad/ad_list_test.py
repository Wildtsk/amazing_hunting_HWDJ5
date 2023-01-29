import pytest

from tests.factories import AdFactory
from ad.serializers import AdlistSerializer


@pytest.mark.django_db
def test_ads_list(client, access_token):
    ad_list = AdFactory.create_batch(4)

    response = client.get("/ad/", HTTP_AUTHORIZATION="Bearer " + access_token)
    assert response.status_code == 200
    assert response.data == {"count": 4,
                             "next": None,
                             "previous": None,
                             "results": AdlistSerializer(ad_list, many=True).data}
