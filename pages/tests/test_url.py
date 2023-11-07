from django.test import  SimpleTestCase

class TestUrls(SimpleTestCase):
  def test_list_url_is_resolved(self):
    assert 1 == 2
    # url = reverse('index')
    # self.assertEquals(resolve(url).func, index)
