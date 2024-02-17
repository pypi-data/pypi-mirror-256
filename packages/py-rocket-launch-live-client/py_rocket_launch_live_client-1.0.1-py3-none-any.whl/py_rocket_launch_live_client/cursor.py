
from requests import Response
import requests
from urllib.parse import parse_qsl
from typing import List, Any


class RocketLaunchliveCursor:
    BASE_URL = 'https://fdo.rocketlaunch.live/json/'
    def __init__(self, subject:str, headers: dict | None = None, params: dict | None = None, page_size: int = 25, limit: int | None = None):
        if params is None:
            params = {}
        if page_size is not None:
            if page_size not in range(1, 26):
                raise ValueError('Page_size must be between 1 and 25')
            params['limit'] = page_size
        self.subject = subject
        response = requests.get(f'{self.BASE_URL}{self.subject}/',headers=headers,params=params)
        if response.request.url is None:
            raise ValueError('Response from request without a url')
        self.offset: int | None = None
        self.position: int | None = None
        self.isOk = response.status_code == 200
        self.currentResponse = response
        self.responseData = response.json()
        self.results: List[Any] | None = self.responseData['result']

        self.currentPage = 1
        self.lastPage = self.responseData['last_page']
        urlParts = str(self.currentResponse.request.url).split('?')
        url = urlParts[0]
        urlParts.pop(0)
        urlParams = '?'.join(urlParts)
        self.params: dict[str, Any] = dict(parse_qsl(urlParams))
        self.headers = self.currentResponse.request.headers
        self.page_size = page_size
        self.url = f'{self.BASE_URL}{self.subject}/'
        self.limit = limit
  
    def __iter__(self):
        return self

    def __next__(self):
        self.position = self.position + 1 if self.position is not None else 0
        self.offset = self.offset + 1 if self.offset is not None else 0
        if self.offset == self.page_size:
            self.GetNextPage()
            self.offset = 0
        if self.limit is not None:
            if self.position >= self.limit:
                raise StopIteration
        if self.results is not None:
            if len(self.results) > self.offset:
                return self.results[self.offset]
        raise StopIteration

    def Rewind(self):
        self.GoToPage(1)
        self.position = None

    def HasNextPage(self):
        return self.currentPage < self.lastPage

    def HasPrevPage(self):
        return self.currentPage > 1

    def GoToPage(self, pageNum: int):
        self.currentPage = pageNum
        self.params['page'] = self.currentPage
        if self.limit is not None:
            limit = self.limit - ((self.currentPage - 1) * self.page_size)
            if limit < 25:
                self.params['limit'] = limit
        self.currentResponse = requests.get(
            self.url, self.params, headers=self.headers)
        self.isOk = self.currentResponse.status_code == 200
        self.responseData = self.currentResponse.json()
        self.results = self.responseData['result']
        self.offset = None

    def GetNextPage(self):
        if not self.HasNextPage():
            raise ValueError('attempting to get next page from last page')
        self.GoToPage(self.currentPage + 1)

    def GetPrevPage(self):
        if not self.HasPrevPage():
            raise ValueError('attempting to get prev page from first page')
        self.GoToPage(self.currentPage - 1)
        self.currentPage -= 1
        if self.limit is not None:
            limit = self.limit - (self.currentPage * self.page_size)
            if limit < 25:
                self.params['limit'] = limit
            else:
                if 'limit' in self.params:
                    del self.params['limit']
        else:
            if 'limit' in self.params:
                del self.params['limit']
        self.params['page'] = self.currentPage
        self.currentResponse = requests.get(
            self.url, self.params, headers=self.headers)
